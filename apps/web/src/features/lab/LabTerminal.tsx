import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchLabCatalog, fetchLabDocument, fetchLabOverview, fetchRuns } from '../../api/client';
import { CommandCenter } from './modules/CommandCenter';
import { ResearchLibrary } from './modules/ResearchLibrary';
import { HypothesisDesk } from './modules/HypothesisDesk';
import { MetricStudio } from './modules/MetricStudio';
import { ExperimentConsole } from './modules/ExperimentConsole';
import { ValidationDesk } from './modules/ValidationDesk';
import { ReplayTerminal } from '../replay/ReplayTerminal';
import type { LabDocumentSummary } from '../../types/lab';

type LabView = 'mission' | 'library' | 'hypotheses' | 'metrics' | 'experiments' | 'validation' | 'replay';

const MODULES: Array<{ id: LabView; label: string; kicker: string }> = [
  { id: 'mission', label: 'Mission Control', kicker: 'System state' },
  { id: 'library', label: 'Research Library', kicker: 'Docs + specs' },
  { id: 'hypotheses', label: 'Hypothesis Desk', kicker: 'Claims + evidence' },
  { id: 'metrics', label: 'Metric Studio', kicker: 'Adapters + runs' },
  { id: 'experiments', label: 'Experiment Console', kicker: 'Tests + artifacts' },
  { id: 'validation', label: 'Validation Desk', kicker: 'Gates + risk' },
  { id: 'replay', label: 'Visual Replay', kicker: 'Chart terminal' },
];

export function LabTerminal() {
  const [view, setView] = useState<LabView>('mission');
  const [activeStage, setActiveStage] = useState('all');
  const [query, setQuery] = useState('');
  const [selectedPath, setSelectedPath] = useState<string | null>(null);

  const overviewQuery = useQuery({ queryKey: ['lab-overview'], queryFn: fetchLabOverview });
  const catalogQuery = useQuery({ queryKey: ['lab-catalog', activeStage, query], queryFn: () => fetchLabCatalog(activeStage, query) });
  const runsQuery = useQuery({ queryKey: ['lab-runs'], queryFn: () => fetchRuns('all') });

  const documents = catalogQuery.data?.documents ?? [];
  const autoSelectedPath = selectedPath ?? catalogQuery.data?.selected_document_path ?? documents[0]?.path ?? null;
  const documentQuery = useQuery({
    queryKey: ['lab-document', autoSelectedPath],
    queryFn: () => fetchLabDocument(autoSelectedPath as string),
    enabled: Boolean(autoSelectedPath),
  });

  const entities = overviewQuery.data?.entities ?? [];
  const hypotheses = useMemo(() => entities.filter((entity) => entity.entity_type === 'hypothesis'), [entities]);
  const metrics = useMemo(() => entities.filter((entity) => entity.entity_type === 'metric'), [entities]);
  const experiments = useMemo(() => entities.filter((entity) => entity.entity_type === 'experiment'), [entities]);
  const validations = useMemo(() => entities.filter((entity) => entity.entity_type === 'validation'), [entities]);

  function openDocument(document: LabDocumentSummary | { primary_path: string }) {
    const path = 'path' in document ? document.path : document.primary_path;
    setSelectedPath(path);
    setView('library');
  }

  return (
    <div className="lab-os">
      <aside className="left-rail">
        <div className="lab-logo">
          <div className="lab-logo-mark">δα</div>
          <div>
            <strong>Decision Alpha</strong>
            <span>Research OS</span>
          </div>
        </div>

        <nav className="module-nav">
          {MODULES.map((module) => (
            <button
              key={module.id}
              className={view === module.id ? 'active' : ''}
              onClick={() => setView(module.id)}
            >
              <span className="nav-kicker">{module.kicker}</span>
              <strong>{module.label}</strong>
            </button>
          ))}
        </nav>

        <div className="system-card">
          <span className="section-kicker">Registry Health</span>
          {(overviewQuery.data?.health ?? []).slice(0, 4).map((item) => (
            <div className="health-row" key={item.id}>
              <i className={`status-dot ${item.status}`} />
              <span>{item.label}</span>
            </div>
          ))}
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <span className="section-kicker">Quant research terminal</span>
            <h1>{MODULES.find((item) => item.id === view)?.label}</h1>
          </div>
          <div className="top-stats">
            <MiniStat label="Entities" value={overviewQuery.data?.stats.entities ?? 0} />
            <MiniStat label="Docs" value={overviewQuery.data?.stats.documents ?? 0} />
            <MiniStat label="Runs" value={overviewQuery.data?.stats.runs ?? 0} />
            <MiniStat label="Metrics" value={overviewQuery.data?.stats.metrics ?? 0} />
          </div>
        </header>

        {view === 'mission' && (
          <CommandCenter
            overview={overviewQuery.data}
            loading={overviewQuery.isLoading}
            onOpenLibrary={() => setView('library')}
            onOpenReplay={() => setView('replay')}
            onOpenMetricStudio={() => setView('metrics')}
          />
        )}

        {view === 'library' && (
          <ResearchLibrary
            stages={overviewQuery.data?.stages ?? []}
            documents={documents}
            activeStage={activeStage}
            query={query}
            selectedPath={autoSelectedPath}
            document={documentQuery.data ?? null}
            loading={catalogQuery.isLoading || documentQuery.isLoading}
            error={documentQuery.error instanceof Error ? documentQuery.error.message : null}
            onStageChange={setActiveStage}
            onQueryChange={setQuery}
            onSelectDocument={(doc) => setSelectedPath(doc.path)}
            onOpenReplay={() => setView('replay')}
          />
        )}

        {view === 'hypotheses' && (
          <HypothesisDesk
            hypotheses={hypotheses}
            documents={documents}
            onOpenDocument={openDocument}
            onOpenReplay={() => setView('replay')}
          />
        )}

        {view === 'metrics' && (
          <MetricStudio
            metrics={metrics}
            runs={runsQuery.data ?? []}
            onOpenDocument={openDocument}
            onOpenReplay={() => setView('replay')}
          />
        )}

        {view === 'experiments' && (
          <ExperimentConsole
            experiments={experiments}
            runs={runsQuery.data ?? []}
            onOpenDocument={openDocument}
            onOpenReplay={() => setView('replay')}
          />
        )}

        {view === 'validation' && (
          <ValidationDesk
            validations={validations}
            runs={runsQuery.data ?? []}
            onOpenDocument={openDocument}
          />
        )}

        {view === 'replay' && <ReplayTerminal />}
      </main>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: number }) {
  return (
    <div className="mini-stat">
      <span>{label}</span>
      <strong>{Number(value ?? 0).toLocaleString()}</strong>
    </div>
  );
}
