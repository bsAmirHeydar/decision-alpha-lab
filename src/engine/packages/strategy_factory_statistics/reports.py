from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import csv, json, hashlib
from .models import StatisticalReportManifest, StatisticSummary, ConfidenceInterval, NullComparison, ReportArtifactIndex

class ReportBundleWriter:
    def __init__(self, output_dir: str|Path): self.output_dir=Path(output_dir)
    @staticmethod
    def _sha(path:Path)->str:
        h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()
    def write(self, manifest:StatisticalReportManifest, summaries:list[StatisticSummary],
              intervals:list[ConfidenceInterval], nulls:list[NullComparison]) -> ReportArtifactIndex:
        manifest.validate(); self.output_dir.mkdir(parents=True,exist_ok=True)
        files=[]
        p=self.output_dir/'report_manifest.json'; p.write_text(json.dumps(asdict(manifest),indent=2,sort_keys=True),encoding='utf-8');files.append(p)
        p=self.output_dir/'group_statistics.csv'
        self._csv(p,[asdict(x) for x in summaries]);files.append(p)
        p=self.output_dir/'confidence_intervals.csv';self._csv(p,[asdict(x) for x in intervals]);files.append(p)
        p=self.output_dir/'matched_nulls.csv';self._csv(p,[asdict(x) for x in nulls]);files.append(p)
        p=self.output_dir/'report.md';p.write_text(self._markdown(manifest,summaries,intervals,nulls),encoding='utf-8');files.append(p)
        artifacts=tuple((x.name,self._sha(x),str(x.stat().st_size)) for x in sorted(files,key=lambda q:q.name))
        index=ReportArtifactIndex(manifest.report_id,manifest.manifest_hash,artifacts).with_hash()
        p=self.output_dir/'artifact_index.json';p.write_text(json.dumps(asdict(index),indent=2,sort_keys=True),encoding='utf-8')
        return index
    @staticmethod
    def _csv(path:Path, rows:list[dict])->None:
        if not rows: path.write_text('',encoding='utf-8');return
        keys=list(rows[0]);
        with path.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
    @staticmethod
    def _markdown(m,summaries,intervals,nulls)->str:
        lines=[f"# Statistical Report — {m.report_id}","",f"- Strategy: `{m.strategy_id}`",f"- Source run: `{m.source_run_id}`",f"- Manifest: `{m.manifest_hash}`","","## Group summaries","", "| Group | N | Filled | Mean R | PF | Max DD |", "|---|---:|---:|---:|---:|---:|"]
        for s in summaries: lines.append(f"| {s.group_key} | {s.sample_count} | {s.filled_count} | {s.mean_net_r:.6f} | {s.profit_factor:.6f} | {s.maximum_drawdown_r:.6f} |")
        lines += ["","## Confidence intervals","","| Metric | Group | Estimate | Lower | Upper |", "|---|---|---:|---:|---:|"]
        for x in intervals: lines.append(f"| {x.metric_id} | {x.group_key} | {x.estimate:.6f} | {x.lower:.6f} | {x.upper:.6f} |")
        lines += ["","## Matched null comparisons","","| Null | Group | Matched | Observed | Control | Uplift |", "|---|---|---:|---:|---:|---:|"]
        for x in nulls: lines.append(f"| {x.null_hash} | {x.group_key} | {x.matched_count} | {x.observed_mean_r:.6f} | {x.control_mean_r:.6f} | {x.uplift_r:.6f} |")
        lines += ["","## Interpretation boundary","","This report is statistical evidence. It is not deployment authority. Phase 12 anti-overfit gates and later paper/live gates remain mandatory."]
        return "\n".join(lines) + "\n"
