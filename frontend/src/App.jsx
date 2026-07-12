import { useState } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import {
  Activity, BookOpen, Bot, ChevronRight, FileUp, Gauge, GitBranch,
  MessageSquareText, PanelLeftClose, Settings2, Sparkles,
} from "lucide-react";
import Chat from "./pages/Chat";
import Documents from "./pages/Documents";
import Trace from "./pages/Trace";
import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";

const navigation = [
  ["Chat", "/chat", MessageSquareText],
  ["Documents", "/documents", BookOpen],
  ["Agent trace", "/trace", GitBranch],
  ["Dashboard", "/dashboard", Gauge],
  ["Settings", "/settings", Settings2],
];

export default function App() {
  const [latestRun, setLatestRun] = useState(null);
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className={`app-shell ${collapsed ? "sidebar-collapsed" : ""}`}>
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand-mark"><Bot size={20} /></div>
          <div className="brand-copy"><strong>Sentinel</strong><span>STUDIO</span></div>
          <button className="icon-button collapse-button" onClick={() => setCollapsed(!collapsed)} aria-label="Toggle sidebar"><PanelLeftClose size={18} /></button>
        </div>
        <div className="workspace-tag"><span className="signal-dot" /> WORKSPACE / LOCAL</div>
        <nav aria-label="Main navigation">
          {navigation.map(([label, to, Icon]) => <NavLink key={to} to={to} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
            <Icon size={18} /><span>{label}</span>{label === "Agent trace" && latestRun && <i />}
          </NavLink>)}
        </nav>
        <div className="sidebar-footer">
          <div className="system-state"><Activity size={15} /><div><span>System status</span><strong>Ready for query</strong></div></div>
          <p>v1.0.0 · Week 7</p>
        </div>
      </aside>
      <main className="main-frame">
        <header className="topbar"><div className="crumb"><Sparkles size={16} /><span>SentinelRAG</span><ChevronRight size={15} /><b>Execution workspace</b></div><div className="api-status"><span className="signal-dot" /> API connected</div></header>
        <Routes>
          <Route path="/chat" element={<Chat latestRun={latestRun} onRun={setLatestRun} />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/trace" element={<Trace run={latestRun} />} />
          <Route path="/dashboard" element={<Dashboard run={latestRun} />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/chat" replace />} />
        </Routes>
      </main>
    </div>
  );
}
