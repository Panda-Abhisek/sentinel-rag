import { CheckCircle2, CircleDashed, RotateCcw } from "lucide-react";
import { Empty } from "./RunPanels";

export default function TraceRail({ run, compact = false }) {
  if (!run?.observability) return <section className="panel trace-panel"><div className="section-heading"><div><span className="eyebrow">LIVE EXECUTION</span><h2>Agent trace</h2></div></div><Empty label="The execution trace will appear with your first query." /></section>;
  const { observability: obs } = run;
  return <section className={`panel trace-panel ${compact ? "compact" : ""}`}><div className="section-heading"><div><span className="eyebrow">LIVE EXECUTION</span><h2>Agent trace</h2></div><span className="run-id">{obs.request_id.slice(0, 8)}</span></div><div className="trace-rail">{obs.nodes.map((node, index) => <div className="trace-node" key={`${node.node_name}-${index}`}><div className="trace-line">{node.success ? <CheckCircle2 size={19} /> : <CircleDashed size={19} />}</div><div className="trace-node-content"><div><strong>{humanize(node.node_name)}</strong>{node.retry > 0 && <span className="retry"><RotateCcw size={11} /> Retry {node.retry}</span>}<time>{formatMs(node.duration_ms)}</time></div>{node.decision && <p>{node.decision}{node.reason ? ` · ${node.reason}` : ""}</p>}</div></div>)}</div></section>;
}

export const formatMs = (value = 0) => value >= 1000 ? `${(value / 1000).toFixed(2)}s` : `${Math.round(value)}ms`;
export const humanize = (value = "") => value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
