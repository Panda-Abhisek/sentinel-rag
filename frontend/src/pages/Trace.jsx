import TraceRail from "../components/TraceRail";
import { humanize } from "../components/TraceRail";

export default function Trace({ run }) {
  const graph = run?.observability?.graph_path || ["planner", "retrieve", "generate", "evaluate", "critic", "selector", "reflection"];
  return <div className="page detail-page"><div className="page-title"><span className="eyebrow">LANGGRAPH EXECUTION</span><h1>Agent trace</h1><p>See the route your latest request took through Sentinel’s recovery-aware workflow.</p></div><div className="graph-map">{graph.map((node, index) => <div key={`${node}-${index}`} className={`graph-node ${run ? "executed" : ""}`}><span>{String(index + 1).padStart(2, "0")}</span><strong>{humanize(node)}</strong>{index < graph.length - 1 && <i />}</div>)}</div><TraceRail run={run} /></div>;
}
