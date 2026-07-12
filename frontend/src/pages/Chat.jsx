import { useState } from "react";
import { ArrowUp, LoaderCircle, RotateCcw, Sparkles } from "lucide-react";
import { askQuestion } from "../api/chat";
import { AnswerCard, EvaluationPanel, SourcesPanel } from "../components/RunPanels";
import TraceRail from "../components/TraceRail";

const starters = ["How does dependency injection improve a FastAPI application?", "Explain the self-healing workflow.", "What evidence supports the answer?"];

export default function Chat({ latestRun, onRun }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  async function runQuestion(prompt) { if (!prompt || loading) return; setLoading(true); setError(""); try { onRun({ question: prompt, ...(await askQuestion(prompt)) }); } catch (err) { setError(err.message); } finally { setLoading(false); } }
  function submit(event) { event?.preventDefault(); runQuestion(question.trim()); }
  return <div className="page chat-page"><section className="chat-hero"><span className="eyebrow"><Sparkles size={13} /> OBSERVABLE RAG WORKSPACE</span><h1>Ask with evidence.<br /><i>Inspect every decision.</i></h1><p>Sentinel exposes retrieval, evaluation, and the agent path behind every answer.</p></section><form className="query-box" onSubmit={submit}><textarea value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a question about your indexed documents…" rows="2" aria-label="Question" /><div><span>⌘ + Enter to run</span><button className="run-button" disabled={!question.trim() || loading}>{loading ? <LoaderCircle className="spin" size={18} /> : <ArrowUp size={18} />}<b>{loading ? "Running" : "Run query"}</b></button></div></form>{error && <div className="error-panel"><strong>Query could not run.</strong> {error}</div>}{!latestRun && !loading && <section className="starter-section"><span className="eyebrow">TRY A QUESTION</span><div>{starters.map((starter) => <button key={starter} onClick={() => setQuestion(starter)}>{starter}<ArrowUp size={15} /></button>)}</div></section>}{loading && <div className="running-state"><span className="pulse" /><b>Sentinel is tracing your request</b><p>Planner → Retrieval → Generation → Evaluation</p></div>}{latestRun && !loading && <div className="run-grid"><AnswerCard answer={latestRun.answer} /><div className="side-stack"><EvaluationPanel evaluation={latestRun.evaluation} observability={latestRun.observability} /><TraceRail run={latestRun} compact /></div><SourcesPanel sources={latestRun.sources} /><button className="regenerate" onClick={() => { setQuestion(latestRun.question); runQuestion(latestRun.question); }}><RotateCcw size={15} /> Run this question again</button></div>}</div>;
}
