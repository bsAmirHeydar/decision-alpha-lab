import type { ReactNode } from 'react';
import type { LabDocumentPayload } from '../../types/lab';

export function MarkdownReader({ document, loading }: { document: LabDocumentPayload | null; loading?: boolean }) {
  if (loading) {
    return <div className="doc-reader empty">Loading document…</div>;
  }
  if (!document) {
    return (
      <div className="doc-reader empty">
        <div className="empty-icon">⌁</div>
        <h2>Select a research document</h2>
        <p>Choose an observation, hypothesis, experiment, validation report, core module, or architecture note to inspect it here.</p>
      </div>
    );
  }

  return (
    <article className="doc-reader">
      <header className="doc-reader-header">
        <div>
          <span className="stage-chip">{document.doc.stage_label}</span>
          <h2>{document.doc.title}</h2>
          <p>{document.doc.path}</p>
        </div>
        <div className="doc-status-block">
          <span>Status</span>
          <strong>{document.doc.status ?? 'untracked'}</strong>
        </div>
      </header>

      {document.outline.length > 0 && (
        <div className="doc-outline">
          {document.outline.slice(0, 10).map((item, index) => (
            <span key={`${item.title}-${index}`} style={{ paddingLeft: `${Math.max(0, item.level - 1) * 10}px` }}>{item.title}</span>
          ))}
        </div>
      )}

      <div className="markdown-body">
        {renderMarkdown(document.content)}
      </div>
    </article>
  );
}

function renderMarkdown(content: string) {
  const nodes: ReactNode[] = [];
  const lines = content.split('\n');
  let list: string[] = [];
  let code: string[] = [];
  let inCode = false;

  const flushList = () => {
    if (!list.length) return;
    nodes.push(<ul key={`list-${nodes.length}`}>{list.map((item, index) => <li key={`${item}-${index}`}>{formatInline(item)}</li>)}</ul>);
    list = [];
  };
  const flushCode = () => {
    if (!code.length) return;
    nodes.push(<pre key={`code-${nodes.length}`}><code>{code.join('\n')}</code></pre>);
    code = [];
  };

  lines.forEach((raw, index) => {
    const line = raw.replace(/\r$/, '');
    if (line.trim().startsWith('```')) {
      if (inCode) flushCode(); else flushList();
      inCode = !inCode;
      return;
    }
    if (inCode) {
      code.push(line);
      return;
    }
    if (!line.trim()) {
      flushList();
      return;
    }
    const heading = /^(#{1,4})\s+(.+)$/.exec(line);
    if (heading) {
      flushList();
      const level = heading[1].length;
      const text = heading[2].trim();
      if (level === 1) nodes.push(<h1 key={`h-${index}`}>{text}</h1>);
      else if (level === 2) nodes.push(<h2 key={`h-${index}`}>{text}</h2>);
      else if (level === 3) nodes.push(<h3 key={`h-${index}`}>{text}</h3>);
      else nodes.push(<h4 key={`h-${index}`}>{text}</h4>);
      return;
    }
    if (/^\s*[-*]\s+/.test(line)) {
      list.push(line.replace(/^\s*[-*]\s+/, ''));
      return;
    }
    flushList();
    if (/^\s*---\s*$/.test(line)) {
      nodes.push(<hr key={`hr-${index}`} />);
      return;
    }
    nodes.push(<p key={`p-${index}`}>{formatInline(line)}</p>);
  });
  flushList();
  flushCode();
  return nodes;
}

function formatInline(text: string) {
  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g);
  return parts.map((part, index) => {
    if (part.startsWith('`') && part.endsWith('`')) return <code key={index}>{part.slice(1, -1)}</code>;
    if (part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2, -2)}</strong>;
    return <span key={index}>{part}</span>;
  });
}
