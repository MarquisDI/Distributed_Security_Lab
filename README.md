# Distributed_Security_Lab

> A distributed security monitoring system built in Python — demonstrating real-time data relay, system telemetry, port scanning, and live threat detection across two isolated environments.

![Dashboard Preview](screenshot.png)

---

## What This Is

This project is a two-component security lab that simulates how real enterprise security tools are architected — with a lightweight agent collecting data in one environment and a central server processing and displaying it in another.

It is actively in development. The current phase demonstrates the full data pipeline from agent to server, with a live monitoring dashboard.

**Current Status: Phase 1 — Data Relay & Live Dashboard ✅**

---

## Architecture

```
┌─────────────────────────────┐         ┌──────────────────────────────┐
│         SCOUT               │         │         THE BRAIN            │
│      (VS Code / Local)      │         │         (Replit / Server)    │
│                             │         │                              │
│  • Scans local open ports   │──HTTP──▶│  • Receives JSON payload     │
│  • Collects CPU & memory    │  POST   │  • Analyses for threats      │
│  • Packages data as JSON    │  /60s   │  • Stores heartbeat history  │
│  • Relays every 60 seconds  │         │  • Serves live dashboard     │
└─────────────────────────────┘         └──────────────────────────────┘
```

**Scout** is the field agent. It runs locally in VS Code, continuously monitoring the host machine and relaying what it finds.

**The Brain** is the central server. It lives on Replit, receives Scout's data, runs threat detection logic, stores history, and serves a live web dashboard.

Communication between them happens over a custom HTTP REST API. Scout sends a JSON payload every 60 seconds. The Brain responds with any alerts it has generated.

---

## How The Data Flows

**Step 1 — Scout collects:**
```
open ports: [22, 80, 443]
cpu_percent: 34.2
memory_percent: 61.8
timestamp: 2026-03-01T10:30:00
```

**Step 2 — Scout packages it as JSON and POSTs to The Brain:**
```json
{
  "timestamp": "2026-03-01T10:30:00",
  "cpu_percent": 34.2,
  "memory_percent": 61.8,
  "open_ports": [22, 80, 443]
}
```

**Step 3 — The Brain receives it, runs threat logic, and stores it:**
```
Port 23 open? → ALERT: Telnet detected
CPU > 90%?    → ALERT: High CPU usage
Memory > 90%? → ALERT: High memory usage
```

**Step 4 — The dashboard reflects everything in real time.**

---

## Components

### `scout.py` — The Agent (VS Code)
- Scans a defined list of common ports using Python's `socket` library
- Collects system vitals using `psutil`
- Packages findings as a JSON payload
- POSTs to The Brain every 60 seconds via `requests`
- Handles relay failures gracefully and retries on the next cycle

### `brain.py` — The Server (Replit / Flask)
- Exposes a `/heartbeat` POST endpoint to receive Scout's data
- Runs threat detection on every incoming payload
- Caps stored history at 100 records to manage memory
- Exposes `/heartbeats` and `/latest` GET endpoints for the dashboard
- Serves the live monitoring dashboard at `/`

### `dashboard.html` — The Dashboard
- Displays live CPU and memory gauges with color-coded severity
- Shows a CPU history chart across the last 30 heartbeats
- Port monitor showing open vs suspicious ports
- Real-time alert feed with timestamps
- Full heartbeat history table
- Auto-refreshes every 60 seconds in sync with Scout's relay cycle

---

## Ports Monitored

| Port | Service | Flagged as Suspicious |
|------|---------|----------------------|
| 21   | FTP     | ✅ Yes |
| 22   | SSH     | No |
| 23   | Telnet  | ✅ Yes |
| 80   | HTTP    | No |
| 443  | HTTPS   | No |
| 3306 | MySQL   | ✅ Yes |
| 5432 | PostgreSQL | ✅ Yes |
| 8080 | Alt HTTP | No |
| 8443 | Alt HTTPS | No |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent (Scout) | Python, `socket`, `psutil`, `requests` |
| Server (Brain) | Python, Flask |
| Dashboard | HTML, CSS, JavaScript |
| Data Format | JSON over HTTP REST |
| Deployment | VS Code (local) + Replit (cloud) |

---

## Running It Yourself

**Scout (run locally in VS Code):**
```bash
pip install psutil requests
python scout.py
```

**The Brain (run on Replit or any server):**
```bash
pip install flask
python main.py
```

Then visit your server URL in a browser to see the live dashboard.

---

## Roadmap

- [x] Establish Scout → Brain data relay
- [x] Port scanning and system vitals collection
- [x] Threat detection and alerting logic
- [x] Live monitoring dashboard
- [ ] Connect Scout to live Brain endpoint (Phase 2)
- [ ] Expand vulnerability detection (XSS, SQLi, hardcoded secrets)
- [ ] PDF report generation per scan
- [ ] API key authentication between Scout and Brain
- [ ] Email / webhook alerting on critical findings

---

## What I Learned Building This

- How distributed systems communicate over HTTP APIs
- How JSON is used to structure and transport data between services
- How to build a custom REST API in Flask
- How real security tools separate data collection from analysis
- How to display live data in a browser without a frontend framework

---

*Built as part of an ongoing self-directed cybersecurity and software development portfolio.*
