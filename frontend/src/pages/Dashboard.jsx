import { BarChart3, Clock3, RotateCcw, ScanSearch, Sigma } from "lucide-react";
import { Empty } from "../components/RunPanels";
import TraceRail, { formatMs } from "../components/TraceRail";

export default function Dashboard({ run }) {
  const obs = run?.observability;
  const metrics = obs && [["Total latency", formatMs(obs.total_latency_ms), Clock3], ["Tokens", obs.token_usage.total_tokens.toLocaleString(), Sigma], ["Retries", obs.retries, RotateCcw], ["Confidence", `${Math.round(obs.final_confidence * 100)}%`, ScanSearch]];
  return <div className="page detail-page"><div className="page-title"><span className="eyebrow">REQUEST TELEMETRY</span><h1>Observability dashboard</h1><p>Request-level performance signals from the latest graph execution.</p></div>{!obs ? <div className="panel"><Empty label="Run a question in Chat to populate request telemetry." /></div> : <><section className="metric-grid">{metrics.map(([label, value, Icon]) => <article className="metric" key={label}><Icon size={18} /><span>{label}</span><strong>{value}</strong></article>)}</section><section className="panel timeline"><div className="section-heading"><div><span className="eyebrow">NODE LATENCY</span><h2>Where time was spent</h2></div><BarChart3 size={20} className="section-icon" /></div>{obs.nodes.map((node) => <div className="bar-row" key={node.node_name}><span>{node.node_name}</span><div><i style={{ width: `${Math.max(6, (node.duration_ms / Math.max(...obs.nodes.map((item) => item.duration_ms))) * 100)}%` }} /></div><b>{formatMs(node.duration_ms)}</b></div>)}</section><TraceRail run={run} /></>}</div>;
}
