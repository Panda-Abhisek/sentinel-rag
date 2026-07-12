import { useState } from "react";
import { BrainCircuit, Check, ChevronDown, Copy, FileText, RotateCcw, ShieldCheck } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function splitThinkBlocks(response = "") {
  // Preserve the entire response if the model leaves a thinking tag unclosed.
  const normalizedResponse = response.toLowerCase();
  if (normalizedResponse.lastIndexOf("<think>") > normalizedResponse.lastIndexOf("</think>")) {
    return { answer: response.trim(), reasoning: "" };
  }

  const thoughts = [];
  const answer = response.replace(/<think>([\s\S]*?)<\/think>/gi, (_, thought) => {
    const cleanedThought = thought.trim();
    if (cleanedThought) thoughts.push(cleanedThought);
    return "";
  }).trim();

  return { answer: answer || response.trim(), reasoning: thoughts.join("\n\n") };
}

function ReasoningTrace({ reasoning }) {
  const [expanded, setExpanded] = useState(false);
  if (!reasoning) return null;

  return <aside className={`reasoning-trace ${expanded ? "is-expanded" : ""}`}>
    <button className="reasoning-toggle" type="button" onClick={() => setExpanded(!expanded)} aria-expanded={expanded} aria-controls="reasoning-content">
      <span className="reasoning-icon"><BrainCircuit size={16} /></span>
      <span className="reasoning-copy"><b>Reasoning trace</b><small>Diagnostic context · may be incomplete</small></span>
      <ChevronDown size={17} />
    </button>
    <div id="reasoning-content" className="reasoning-content" hidden={!expanded}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{reasoning}</ReactMarkdown>
    </div>
  </aside>;
}

export function AnswerCard({ answer }) {
  const [copied, setCopied] = useState(false);
  const { answer: finalAnswer, reasoning } = splitThinkBlocks(answer);
  async function copyAnswer() { await navigator.clipboard.writeText(finalAnswer); setCopied(true); setTimeout(() => setCopied(false), 1800); }
  return <section className="answer-card panel"><div className="section-heading"><div><span className="eyebrow">GENERATED RESPONSE</span><h2>Answer</h2></div><button className="copy-button" onClick={copyAnswer}>{copied ? <Check size={15} /> : <Copy size={15} />}{copied ? "Copied" : "Copy"}</button></div><ReasoningTrace reasoning={reasoning} /><div className="markdown"><ReactMarkdown remarkPlugins={[remarkGfm]}>{finalAnswer}</ReactMarkdown></div></section>;
}

export function SourcesPanel({ sources = [] }) {
  const [open, setOpen] = useState(null);
  return <section className="panel sources-panel"><div className="section-heading"><div><span className="eyebrow">RETRIEVAL EVIDENCE</span><h2>Sources <em>{sources.length}</em></h2></div></div>{sources.length ? <div className="source-list">{sources.map((source, index) => <article className="source-card" key={`${source.source}-${index}`}><button onClick={() => setOpen(open === index ? null : index)}><div className="source-title"><span className="citation">[{index + 1}]</span><FileText size={16} /><strong>{source.source}</strong><span className="score">{source.score == null ? "ranked" : `${Math.round(source.score * 100)}% match`}</span><ChevronDown className={open === index ? "rotate" : ""} size={17} /></div><span>Page {source.page}</span></button>{open === index && <p>{source.content}</p>}</article>)}</div> : <Empty label="No supporting chunks were returned for this run." />}</section>;
}

export function EvaluationPanel({ evaluation, observability }) {
  const confidence = observability?.final_confidence;
  const score = evaluation?.score ?? evaluation?.answer_score ?? confidence;
  return <section className="panel evaluation-panel"><div className="section-heading"><div><span className="eyebrow">QUALITY GATE</span><h2>Evaluation</h2></div><ShieldCheck size={20} className="section-icon" /></div>{observability ? <div className="evaluation-content"><div className="confidence-meter"><div className="ring" style={{ "--score": `${Math.round((score || 0) * 100)}%` }}><b>{Math.round((score || 0) * 100)}<small>%</small></b></div><span>confidence</span></div><dl><div><dt>Selected attempt</dt><dd>#{observability.selected_attempt + 1}</dd></div><div><dt>Recovery</dt><dd className={observability.retries ? "amber" : "positive"}>{observability.retries ? `${observability.retries} retr${observability.retries === 1 ? "y" : "ies"}` : "No retry"}</dd></div><div><dt>Grounded</dt><dd className="positive">Verified</dd></div></dl></div> : <Empty label="Evaluation appears after your first answer." />}</section>;
}

export function Empty({ label }) { return <div className="empty"><span>—</span><p>{label}</p></div>; }
