
import { useState } from "react";
import "./App.css";

const initialFindings = [
  {
    id: 1,
    name: "reqeusts",
    ecosystem: "PyPI",
    version: "2.31.0",
    severity: "Critical",
    status: "Not found",
    reason: "Package does not exist in registry",
  },
  {
    id: 2,
    name: "flask",
    ecosystem: "PyPI",
    version: "3.0.0",
    severity: "Warning",
    status: "Review required",
    reason: "Recently published package",
  },
  {
    id: 3,
    name: "express",
    ecosystem: "npm",
    version: "4.18.2",
    severity: "Safe",
    status: "Verified",
    reason: "Package metadata verified",
  },
  {
    id: 4,
    name: "numpy",
    ecosystem: "PyPI",
    version: "1.26.4",
    severity: "Safe",
    status: "Verified",
    reason: "Package metadata verified",
  },
  {
    id: 5,
    name: "colors",
    ecosystem: "npm",
    version: "1.4.0",
    severity: "Warning",
    status: "Review required",
    reason: "Package requires further review",
  },
];

const navigation = [
  { label: "Overview", icon: "▦" },
  { label: "Scan Results", icon: "⌕" },
  { label: "Scan History", icon: "◷" },
  { label: "Audit Logs", icon: "☷" },
];

function Brand() {
  return (
    <div className="brand">
      <div className="brand-mark">
        <svg viewBox="0 0 48 48" fill="none">
          <path
            d="M24 4L41 10V22C41 33 34 40 24 44C14 40 7 33 7 22V10L24 4Z"
            fill="currentColor"
            opacity=".2"
          />
          <path
            d="M24 4L41 10V22C41 33 34 40 24 44C14 40 7 33 7 22V10L24 4Z"
            stroke="currentColor"
            strokeWidth="2.5"
          />
          <path
            d="M16 24L21.5 29.5L32 19"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>

      <div className="brand-copy">
        <strong>DepShield</strong>
        <span>Dependency Security</span>
      </div>
    </div>
  );
}

function SeverityBadge({ severity }) {
  const icons = {
    Critical: "!",
    Warning: "△",
    Safe: "✓",
  };

  return (
    <span className={`severity-badge ${severity.toLowerCase()}`}>
      <span>{icons[severity]}</span>
      {severity}
    </span>
  );
}

function StatCard({ title, value, description, icon, tone }) {
  return (
    <article className="stat-card">
      <div className="stat-heading">
        <span>{title}</span>
        <div className={`stat-icon ${tone}`}>{icon}</div>
      </div>

      <div className="stat-value">{value}</div>
      <div className="stat-description">{description}</div>
    </article>
  );
}

function FindingsTable({ findings }) {
  return (
    <div className="table-scroll">
      <table className="findings-table">
        <thead>
          <tr>
            <th>PACKAGE</th>
            <th>ECOSYSTEM</th>
            <th>VERSION</th>
            <th>SEVERITY</th>
            <th>VERIFICATION</th>
            <th>DETECTION REASON</th>
          </tr>
        </thead>

        <tbody>
          {findings.map((finding) => (
            <tr key={finding.id}>
              <td>
                <div className="package-cell">
                  <span className="package-symbol">⌘</span>
                  <strong>{finding.name}</strong>
                </div>
              </td>

              <td>
                <span className="ecosystem">{finding.ecosystem}</span>
              </td>

              <td className="version-cell">{finding.version}</td>

              <td>
                <SeverityBadge severity={finding.severity} />
              </td>

              <td>
                <span className="verification">{finding.status}</span>
              </td>

              <td className="reason-cell">{finding.reason}</td>
            </tr>
          ))}

          {findings.length === 0 && (
            <tr>
              <td colSpan={6}>
                <div className="empty-table">
                  <span>⌕</span>
                  <strong>No matching dependencies</strong>
                  <p>Try changing your search or severity filter.</p>
                </div>
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function Overview({ findings, onNavigate }) {
  const critical = findings.filter(
    (item) => item.severity === "Critical"
  ).length;

  const warnings = findings.filter(
    (item) => item.severity === "Warning"
  ).length;

  const safe = findings.filter(
    (item) => item.severity === "Safe"
  ).length;

  const total = findings.length;

  return (
    <>
      <section className="welcome-row">
        <div>
          <div className="eyebrow">SECURITY CENTER</div>
          <h2>Security Overview</h2>
          <p>
            Monitor dependency integrity and identify potential
            package security risks.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => onNavigate("Scan Results")}
        >
          <span>⌕</span>
          View Findings
        </button>
      </section>

      <section className="stats-grid">
        <StatCard
          title="Dependencies Analyzed"
          value={total}
          description="Packages in current sample"
          icon="◈"
          tone="blue"
        />

        <StatCard
          title="Critical Findings"
          value={critical}
          description="Packages not found"
          icon="!"
          tone="red"
        />

        <StatCard
          title="Suspicious Packages"
          value={warnings}
          description="Require further review"
          icon="△"
          tone="amber"
        />

        <StatCard
          title="Verified Dependencies"
          value={safe}
          description="Passed current checks"
          icon="✓"
          tone="green"
        />
      </section>

      <section className="panel findings-panel">
        <div className="panel-heading">
          <div>
            <h3>Latest Security Findings</h3>
            <p>Dependency verification results</p>
          </div>

          <button
            className="secondary-button"
            onClick={() => onNavigate("Scan Results")}
          >
            View all findings <span>→</span>
          </button>
        </div>

        <FindingsTable findings={findings.slice(0, 5)} />
      </section>

      <section className="overview-bottom">
        <div className="panel distribution-panel">
          <div className="panel-heading">
            <div>
              <h3>Risk Distribution</h3>
              <p>Current dependency classification</p>
            </div>
          </div>

          <div className="distribution-total">
            <strong>{total}</strong>
            <span>Total dependencies</span>
          </div>

          <div className="distribution-bar">
            <div
              className="distribution-critical"
              style={{ width: `${total ? (critical / total) * 100 : 0}%` }}
            />
            <div
              className="distribution-warning"
              style={{ width: `${total ? (warnings / total) * 100 : 0}%` }}
            />
            <div
              className="distribution-safe"
              style={{ width: `${total ? (safe / total) * 100 : 0}%` }}
            />
          </div>

          <div className="distribution-legend">
            <div>
              <i className="legend-critical" />
              <span>Critical</span>
              <strong>{critical}</strong>
            </div>

            <div>
              <i className="legend-warning" />
              <span>Warning</span>
              <strong>{warnings}</strong>
            </div>

            <div>
              <i className="legend-safe" />
              <span>Safe</span>
              <strong>{safe}</strong>
            </div>
          </div>
        </div>

        <div className="panel scanner-panel">
          <div className="panel-heading">
            <div>
              <h3>Scanner Health</h3>
              <p>Dependency verification service</p>
            </div>

            <span className="health-indicator">● Ready</span>
          </div>

          <div className="health-content">
            <div className="health-icon">✓</div>
            <div>
              <strong>Verification interface ready</strong>
              <p>
                Sample findings are displayed. Live registry
                verification will be connected through the API.
              </p>
            </div>
          </div>

          <div className="health-footer">
            <span>Application status</span>
            <strong>Operational</strong>
          </div>
        </div>
      </section>
    </>
  );
}

function ScanResults({ findings }) {
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("All");

  const filtered = findings.filter((item) => {
    const matchesSearch =
      item.name.toLowerCase().includes(search.toLowerCase()) ||
      item.ecosystem.toLowerCase().includes(search.toLowerCase());

    const matchesSeverity =
      severity === "All" || item.severity === severity;

    return matchesSearch && matchesSeverity;
  });

  return (
    <section className="panel results-page">
      <div className="panel-heading">
        <div>
          <h3>Dependency Findings</h3>
          <p>Review package verification and risk classifications</p>
        </div>

        <span className="result-count">
          {filtered.length} results
        </span>
      </div>

      <div className="filter-toolbar">
        <div className="search-field">
          <span>⌕</span>
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search package or ecosystem..."
          />
        </div>

        <select
          value={severity}
          onChange={(event) => setSeverity(event.target.value)}
          aria-label="Filter by severity"
        >
          <option value="All">All severities</option>
          <option value="Critical">Critical</option>
          <option value="Warning">Warning</option>
          <option value="Safe">Safe</option>
        </select>
      </div>

      <FindingsTable findings={filtered} />
    </section>
  );
}

function EmptyPage({ title, description, icon }) {
  return (
    <section className="panel empty-page">
      <div className="empty-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      <span className="coming-label">Awaiting backend integration</span>
    </section>
  );
}

export default function App() {
  const [activePage, setActivePage] = useState("Overview");

  const pageTitles = {
    Overview: "Security Overview",
    "Scan Results": "Scan Results",
    "Scan History": "Scan History",
    "Audit Logs": "Audit Logs",
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Brand />

        <div className="sidebar-section-label">WORKSPACE</div>

        <nav className="navigation">
          {navigation.map((item) => (
            <button
              key={item.label}
              className={`navigation-item ${
                activePage === item.label ? "active" : ""
              }`}
              onClick={() => setActivePage(item.label)}
            >
              <span className="navigation-icon">{item.icon}</span>
              <span>{item.label}</span>

              {item.label === "Scan Results" && (
                <span className="navigation-count">5</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-status">
            <span className="status-pulse" />
            <div>
              <strong>Scanner Online</strong>
              <span>Verification service</span>
            </div>
          </div>

          <div className="sidebar-version">DepShield · v1.0</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <span className="breadcrumb">Workspace</span>
            <span className="breadcrumb-separator">/</span>
            <strong>{pageTitles[activePage]}</strong>
          </div>

          <div className="topbar-right">
            <div className="environment-label">
              <span className="environment-dot" />
              Development
            </div>

            <div className="profile">
              <div className="profile-avatar">DS</div>
              <div className="profile-info">
                <strong>Security Workspace</strong>
                <span>Administrator</span>
              </div>
            </div>
          </div>
        </header>

        <div className="page-content">
          {activePage === "Overview" && (
            <Overview
              findings={initialFindings}
              onNavigate={setActivePage}
            />
          )}

          {activePage === "Scan Results" && (
            <ScanResults findings={initialFindings} />
          )}

          {activePage === "Scan History" && (
            <EmptyPage
              title="Scan History"
              description="Historical dependency scans will be displayed here."
              icon="◷"
            />
          )}

          {activePage === "Audit Logs" && (
            <EmptyPage
              title="Security Activity"
              description="Security events and audit records will be displayed here."
              icon="☷"
            />
          )}

          <footer className="app-footer">
            <span>DepShield</span>
            <span>Dependency Security Intelligence</span>
            <span>© 2026</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
