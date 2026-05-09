# 🛡️ Agentic A2A: Autonomous Monitoring & Remediation

**Agentic A2A** (Alert-to-Action) is a state-of-the-art, AI-powered system designed to monitor server infrastructure, predict potential failures, and execute autonomous remediation steps. By chaining multiple specialized AI agents, the system transforms raw metrics into actionable insights and verified resolutions without human intervention.

---

## 🚀 Key Features

- **Multi-Agent Orchestration**: A seamless pipeline of specialized agents (Monitoring, Prediction, Remediation, Reporting).
- **Real-Time Dashboards**: High-performance visualization of CPU, RAM, and network metrics.
- **Autonomous Remediation**: Intelligent recovery actions (scaling, service restarts, throttling) driven by Groq (Llama 3.3) and Gemini 1.5.
- **Root Cause Analysis (RCA)**: Automatic generation of professional post-mortem reports for every incident.
- **Hybrid Infrastructure**: Support for both simulated cloud nodes (AWS, GCP, Azure) and real-time local server monitoring.
- **Remediation Proofs**: Every action is verified with "Before vs After" metrics to ensure stability.

---

## 🛠️ Technology Stack

- **Frontend**: React 19, Vite, TailwindCSS 4.0, Recharts, Framer Motion, Lucide Icons.
- **Backend**: Node.js (Express) with ES Modules.
- **AI Engine**: Groq (Llama 3.3 70B), Google Gemini 1.5 Flash.
- **Database**: SQLite (via `better-sqlite3`) for persistent logging and incident tracking.
- **Agents**: Python-based micro-agents for specialized monitoring and remediation tasks.

---

## 🚦 Getting Started

### Prerequisites

- **Node.js**: v18.x or higher
- **Python**: v3.9+ (for backend agents)
- **API Keys**: Access to Groq or Google Gemini

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd abcd
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Install Python dependencies** (optional, for local agent execution):
   ```bash
   pip install psutil
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (or update the existing one):
   ```env
   GROK_API_KEY="your_groq_api_key"
   GEMINI_API_KEY="your_gemini_api_key"
   APP_URL="http://localhost:3000"
   ```

### Running the Project

Launch the full-stack development environment:

```bash
npm run dev
```

The application will be available at: **[http://localhost:3000](http://localhost:3000)**

---

## 🤖 The Agentic Pipeline

1. **Monitoring Agent**: Scans metrics every 3 seconds looking for threshold breaches.
2. **Predictive Agent**: Analyzes historical trends to forecast if a warning will escalate to critical.
3. **Remediation Agent**: Selects and executes the most cost-effective recovery strategy.
4. **Reporting Agent**: Compiles logs and "Proof of Remediation" into a final incident report.

---

## 📂 Project Structure

```text
├── backend_agents/     # Python-based AI agents (Monitor, Predict, Remediate, Report)
├── src/                # React frontend source code
│   ├── components/     # UI Components (Dashboards, Charts, Logs)
│   ├── hooks/          # Custom React hooks for data fetching
│   └── context/        # Global state management
├── server.ts           # Main Node.js/Express server (Vite middleware orchestrator)
├── data.db             # Persistent SQLite database
└── vite.config.ts      # Vite configuration
```

---

## 📜 License

This project is licensed under the MIT License.
