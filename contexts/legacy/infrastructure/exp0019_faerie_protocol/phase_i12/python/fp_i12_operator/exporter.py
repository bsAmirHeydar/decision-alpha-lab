from __future__ import annotations
import csv
import io
import json
from .contracts import *
from .canonical import sha256, stable_id, primitive


class AuditExporter:
    def __init__(self, instance_id, config, seen_ids=()):
        self.instance_id = instance_id
        self.config = config
        self.seen = set(seen_ids)

    def records(self, snapshot):
        out = []
        for item in snapshot.items:
            if not self.config.include_suppressed and item.disposition.startswith('SUPPRESSED'):
                continue
            if not self.config.include_blocked and item.disposition == 'BLOCKED':
                continue
            payload = {
                'instance_id': self.instance_id,
                'snapshot_id': snapshot.snapshot_id,
                'semantic_id': item.semantic_id,
                'type': item.kind,
                'event_time': item.event_time,
                'relation': item.relation,
                'direction': item.direction,
                'state': item.state,
                'disposition': item.disposition,
                'session_kind': item.session_kind,
                'symbol': item.symbol,
                'reason_codes': item.reason_codes,
                'source_revision_sequence': snapshot.source_revision_sequence,
            }
            ph = sha256(payload)
            out.append(
                AuditRecord(
                    stable_id('FPAUDIT', payload),
                    self.instance_id,
                    snapshot.snapshot_id,
                    item.semantic_id,
                    item.kind,
                    item.event_time,
                    item.relation,
                    item.direction,
                    item.state,
                    item.disposition,
                    item.session_kind,
                    item.symbol,
                    item.reason_codes,
                    snapshot.source_revision_sequence,
                    ph,
                )
            )
        return tuple(sorted(out, key=lambda x: (x.event_time, x.record_id)))

    def export(self, snapshot, fmt):
        if not self.config.enabled:
            return ExportBatch(
                stable_id('FPEXPORT', {'snapshot': snapshot.snapshot_id, 'format': fmt.value}),
                fmt,
                (),
                0,
                0,
                '',
                sha256(''),
                ExportDisposition.DISABLED,
            )
        recs = self.records(snapshot)
        new = []
        dup = 0
        for r in recs:
            if r.record_id in self.seen:
                dup += 1
            else:
                self.seen.add(r.record_id)
                new.append(r)
        if fmt is ExportFormat.JSONL:
            content = ''.join(
                json.dumps(primitive(r), sort_keys=True, separators=(',', ':')) + '\n'
                for r in new
            )
        else:
            s = io.StringIO()
            fields = (
                'record_id', 'instance_id', 'snapshot_id', 'semantic_id',
                'record_type', 'event_time', 'relation', 'direction', 'state',
                'disposition', 'session_kind', 'symbol', 'reason_codes',
                'source_revision_sequence', 'payload_hash',
            )
            wr = csv.writer(s, lineterminator='\n')
            wr.writerow(fields)
            for r in new:
                wr.writerow([
                    r.record_id, r.instance_id, r.snapshot_id, r.semantic_id,
                    r.record_type, r.event_time, r.relation, r.direction, r.state,
                    r.disposition, r.session_kind, r.symbol,
                    '|'.join(r.reason_codes), r.source_revision_sequence, r.payload_hash,
                ])
            content = s.getvalue()
        payload = {
            'snapshot': snapshot.snapshot_id,
            'format': fmt.value,
            'records': [r.record_id for r in new],
            'duplicate_count': dup,
            'content_hash': sha256(content),
        }
        return ExportBatch(
            stable_id('FPEXPORT', payload),
            fmt,
            tuple(new),
            len(new),
            dup,
            content,
            sha256(content),
            ExportDisposition.APPENDED,
        )
