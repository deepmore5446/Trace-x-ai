import { useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
} from "reactflow";
import "reactflow/dist/style.css";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [wallet, setWallet] = useState("");
  const [loading, setLoading] = useState(false);
  const [investigation, setInvestigation] = useState(null);

  const [graphNodes, setGraphNodes] = useState([]);
  const [graphEdges, setGraphEdges] = useState([]);

  const [error, setError] = useState("");

  // --------------------------------------------------
  // CREATE GRAPH LAYOUT
  // --------------------------------------------------

  const createGraph = (graph) => {
    if (!graph) {
      setGraphNodes([]);
      setGraphEdges([]);
      return;
    }

    const nodes = graph.nodes || [];
    const edges = graph.edges || [];

    const columns = 4;
    const horizontalGap = 260;
    const verticalGap = 150;

    const formattedNodes = nodes.map((node, index) => {
      const column = index % columns;
      const row = Math.floor(index / columns);

      const nodeId = node.id;

      let nodeType = "wallet";

      if (nodeId.startsWith("EXCHANGE")) {
        nodeType = "exchange";
      }

      if (nodeId.startsWith("VICTIM")) {
        nodeType = "victim";
      }

      return {
        id: nodeId,

        position: {
          x: column * horizontalGap,
          y: row * verticalGap,
        },

        data: {
          label: nodeId,
        },

        type: "default",

        className:
          nodeType === "exchange"
            ? "exchange-node"
            : nodeType === "victim"
            ? "victim-node"
            : "wallet-node",
      };
    });

    const formattedEdges = edges.map((edge, index) => ({
      id: `edge-${index}`,

      source: edge.source,
      target: edge.target,

      animated: true,

      label: `${edge.amount} BTC`,

      data: {
        txid: edge.txid,
        amount: edge.amount,
        timestamp: edge.timestamp,
      },

      style: {
        strokeWidth: 2,
      },

      labelStyle: {
        fontSize: 10,
      },
    }));

    setGraphNodes(formattedNodes);
    setGraphEdges(formattedEdges);
  };

  // --------------------------------------------------
  // LOAD GRAPH
  // --------------------------------------------------

  const loadGraph = async () => {
    try {
      const response = await fetch(`${API}/graph`);

      if (!response.ok) {
        throw new Error("Graph API failed");
      }

      const data = await response.json();

      if (data.status === "success") {
        createGraph(data.graph);
      }
    } catch (error) {
      console.error("Graph Error:", error);
    }
  };

  // --------------------------------------------------
  // INVESTIGATION
  // --------------------------------------------------

  const handleInvestigate = async () => {
    if (!wallet.trim()) {
      alert("Please enter a wallet address");
      return;
    }

    setLoading(true);
    setError("");
    setInvestigation(null);

    try {
      const walletAddress = wallet.trim();

      const response = await fetch(
        `${API}/investigation-summary/${encodeURIComponent(
          walletAddress
        )}`
      );

      if (!response.ok) {
        throw new Error("Investigation request failed");
      }

      const data = await response.json();

      if (data.status !== "success") {
        throw new Error("Investigation failed");
      }

      setInvestigation(data.investigation);

      // Load real transaction graph
      await loadGraph();

    } catch (error) {
      console.error("Investigation Error:", error);

      setError(
        "Backend se connection nahi ho raha. Check karo ki FastAPI server running hai."
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // DATA
  // --------------------------------------------------

  const risk = investigation?.risk;

  const ml = investigation?.machine_learning;

  const fundFlow = investigation?.fund_flow;

  const evidence = investigation?.evidence;

  const relatedWallets =
    investigation?.related_wallets || [];

  const tracing = investigation?.tracing;

  const lead =
    investigation?.investigative_lead;

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <h1>TRACE-X</h1>

        <p className="subtitle">
          AI Investigation Platform
        </p>

        <nav>

          <div className="nav-item active">
            Dashboard
          </div>

          <div className="nav-item">
            Investigations
          </div>

          <div className="nav-item">
            Cases
          </div>

          <div className="nav-item">
            Evidence
          </div>

        </nav>

        <div className="sidebar-bottom">

          <div className="nav-item">
            Settings
          </div>

        </div>

      </aside>


      {/* MAIN CONTENT */}

      <main className="main-content">

        {/* HEADER */}

        <header className="topbar">

          <div>

            <h2>
              Investigation Dashboard
            </h2>

            <p>
              Crypto-fraud tracing and evidence analysis
            </p>

          </div>

          <div className="status">

            <span className="status-dot"></span>

            System Online

          </div>

        </header>


        {/* INVESTIGATION SEARCH */}

        <section className="investigation-box">

          <div>

            <h3>
              Start Investigation
            </h3>

            <p>
              Enter a wallet address to analyze
              transaction activity.
            </p>

          </div>

          <div className="search-area">

            <input
              type="text"
              placeholder="Enter wallet address..."
              value={wallet}
              onChange={(e) =>
                setWallet(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  handleInvestigate();
                }

              }}
            />

            <button
              onClick={handleInvestigate}
              disabled={loading}
            >

              {loading
                ? "Investigating..."
                : "Investigate"}

            </button>

          </div>

        </section>


        {/* ERROR */}

        {error && (

          <div className="error-box">

            {error}

          </div>

        )}


        {/* EMPTY STATE */}

        {!investigation &&
          !loading &&
          !error && (

            <section className="empty-state">

              <h3>
                Ready for Investigation
              </h3>

              <p>
                Enter a wallet address above
                to begin crypto-fraud analysis.
              </p>

              <div className="demo-wallet">

                Demo wallet:
                <strong> WALLET_A</strong>

              </div>

            </section>

          )}


        {/* INVESTIGATION RESULTS */}

        {investigation && (

          <>

            {/* WALLET HEADER */}

            <section className="result-header">

              <div>

                <span className="label">
                  INVESTIGATED WALLET
                </span>

                <h3>
                  {investigation.wallet}
                </h3>

              </div>

              <div className="risk-badge">

                Risk:{" "}
                {risk?.level || "UNKNOWN"}

              </div>

            </section>


            {/* STATS */}

            <section className="stats">

              <div className="stat-card">

                <span>
                  Risk Score
                </span>

                <strong>
                  {risk?.score ?? "—"}
                </strong>

              </div>


              <div className="stat-card">

                <span>
                  ML Detection
                </span>

                <strong>
                  {ml?.prediction || "—"}
                </strong>

              </div>


              <div className="stat-card">

                <span>
                  Fund Paths
                </span>

                <strong>
                  {fundFlow?.total_paths ?? "—"}
                </strong>

              </div>


              <div className="stat-card">

                <span>
                  Exchange Flags
                </span>

                <strong>
                  {fundFlow?.exchange_paths ?? "—"}
                </strong>

              </div>

            </section>


            {/* ANALYSIS GRID */}

            <section className="dashboard-grid">


              {/* RISK */}

              <div className="panel">

                <div className="panel-header">

                  <h3>
                    Risk Analysis
                  </h3>

                  <span>
                    {risk?.level || "UNKNOWN"}
                  </span>

                </div>


                <div className="risk-score">

                  {risk?.score ?? 0}

                  <small>
                    /100
                  </small>

                </div>


                <div className="reasons">

                  <h4>
                    Evidence Signals
                  </h4>

                  {risk?.reasons?.length > 0 ? (

                    risk.reasons.map(
                      (reason, index) => (

                        <div
                          className="reason"
                          key={index}
                        >

                          <span>
                            •
                          </span>

                          {reason}

                        </div>

                      )
                    )

                  ) : (

                    <p>
                      No risk signals detected.
                    </p>

                  )}

                </div>

              </div>


              {/* MACHINE LEARNING */}

              <div className="panel">

                <div className="panel-header">

                  <h3>
                    Machine Learning
                  </h3>

                  <span>
                    Isolation Forest
                  </span>

                </div>


                <div className="ml-result">

                  <div>

                    <span>
                      Prediction
                    </span>

                    <strong>
                      {ml?.prediction || "—"}
                    </strong>

                  </div>


                  <div>

                    <span>
                      Anomaly Score
                    </span>

                    <strong>
                      {ml?.anomaly_score ?? "—"}
                    </strong>

                  </div>

                </div>

              </div>


              {/* FUND FLOW */}

              <div className="panel">

                <div className="panel-header">

                  <h3>
                    Fund Flow
                  </h3>

                  <span>
                    {fundFlow?.exchange_paths || 0}
                    {" "}Exchange Flags
                  </span>

                </div>


                <div className="flow-info">

                  <p>

                    Total paths:
                    {" "}
                    <strong>
                      {fundFlow?.total_paths ?? 0}
                    </strong>

                  </p>


                  <p>

                    Exchange paths:
                    {" "}
                    <strong>
                      {fundFlow?.exchange_paths ?? 0}
                    </strong>

                  </p>

                </div>


                {fundFlow
                  ?.exchange_destinations
                  ?.length > 0 && (

                  <div className="exchange-list">

                    <h4>
                      Exchange Destinations
                    </h4>

                    {fundFlow.exchange_destinations.map(
                      (exchange, index) => (

                        <div
                          className="exchange-item"
                          key={index}
                        >

                          {exchange}

                        </div>

                      )
                    )}

                  </div>

                )}

              </div>


              {/* RELATED WALLETS */}

              <div className="panel">

                <div className="panel-header">

                  <h3>
                    Related Wallets
                  </h3>

                  <span>
                    {relatedWallets.length}
                  </span>

                </div>


                {relatedWallets.length > 0 ? (

                  relatedWallets.map(
                    (item, index) => (

                      <div
                        className="wallet-row"
                        key={index}
                      >

                        <span>
                          {item.wallet}
                        </span>

                        <strong>

                          {Math.round(
                            item.similarity * 100
                          )}
                          %

                        </strong>

                      </div>

                    )
                  )

                ) : (

                  <p>
                    No related wallets found.
                  </p>

                )}

              </div>

            </section>


            {/* REAL TRANSACTION GRAPH */}

            <section className="graph-section">

              <div className="section-header">

                <div>

                  <h3>
                    Transaction Network
                  </h3>

                  <p>
                    Real transaction relationships
                    from the investigation dataset
                  </p>

                </div>


                <div className="graph-count">

                  {graphNodes.length} Nodes ·{" "}
                  {graphEdges.length} Transactions

                </div>

              </div>


              <div
                className="real-graph"
                style={{
                  height: "600px",
                  width: "100%",
                  borderRadius: "12px",
                  overflow: "hidden",
                }}
              >

                {graphNodes.length > 0 ? (

                  <ReactFlow
                    nodes={graphNodes}
                    edges={graphEdges}
                    fitView
                    attributionPosition="bottom-left"
                  >

                    <MiniMap />

                    <Controls />

                    <Background />

                  </ReactFlow>

                ) : (

                  <div className="graph-empty">

                    No transaction graph available.

                  </div>

                )}

              </div>

            </section>


            {/* INVESTIGATION TRACE */}

            <section className="panel trace-panel">

              <div className="panel-header">

                <h3>
                  Investigation Trace
                </h3>

                <span>
                  {tracing?.paths?.length || 0}
                  {" "}paths
                </span>

              </div>


              {tracing?.paths?.length > 0 ? (

                <div className="paths">

                  {tracing.paths
                    .slice(0, 10)
                    .map((path, index) => (

                      <div
                        className="path-row"
                        key={index}
                      >

                        {path.map(
                          (
                            walletName,
                            walletIndex
                          ) => (

                            <span
                              key={walletIndex}
                            >

                              {walletName}

                              {walletIndex <
                                path.length - 1
                                ? " → "
                                : ""}

                            </span>

                          )
                        )}

                      </div>

                    ))}

                </div>

              ) : (

                <p>
                  No transaction paths found.
                </p>

              )}

            </section>


            {/* EVIDENCE */}

            <section className="panel">

              <div className="panel-header">

                <h3>
                  Evidence Trail
                </h3>

                <span>
                  {evidence?.total_evidence || 0}
                  {" "}items
                </span>

              </div>


              {evidence?.items?.length > 0 ? (

                evidence.items
                  .slice(0, 10)
                  .map((item, index) => (

                    <div
                      className="evidence-row"
                      key={index}
                    >

                      <strong>
                        {item.type}
                      </strong>

                      <p>
                        {item.description}
                      </p>

                      <small>
                        {item.txid}
                        {" · "}
                        {item.timestamp}
                      </small>

                    </div>

                  ))

              ) : (

                <p>
                  No evidence available.
                </p>

              )}

            </section>


            {/* INVESTIGATIVE LEAD */}

            <section className="lead-box">

              <h3>
                Investigative Lead
              </h3>

              <strong>
                {lead?.status ||
                  "REQUIRES_VERIFICATION"}
              </strong>

              <p>
                {lead?.message ||
                  "This result identifies a potential investigative lead based on transaction and graph evidence. It does not establish the identity of a person."}
              </p>

            </section>

          </>

        )}

      </main>

    </div>
  );
}

export default App;