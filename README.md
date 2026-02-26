# 🎧 Enterprise AI Sales Copilot

A real-time AI assistant built for Sales Managers in B2B enterprise environments. This Copilot "listens" to live call transcripts and autonomously provides actionable hints, cross-sell opportunities, and dynamic pricing based on CRM profiles and ERP inventory data.

## 🚀 Key Features

* **Real-time UI (Streamlit):** Split-screen interface simulating live Speech-to-Text transcripts and displaying AI-generated sales hints.
* **Orchestration (LangGraph):** The core reasoning engine that processes conversational context without directly responding to the client, acting strictly as an advisor to the human manager.
* **Isolated Tooling (FastMCP):** External database integrations (CRM, ERP) are completely decoupled into a Model Context Protocol (MCP) server, ensuring secure and scalable enterprise architecture.
* **Dynamic Cross-selling:** Automatically identifies dead stock (>90 days in warehouse) and VIP client tiers to suggest context-aware promotions.

## 🏗 Architecture

*(The diagram below renders automatically in GitHub)*

```mermaid
graph TD
    classDef ui fill:#f3f4f6,stroke:#374151,stroke-width:2px,color:#111827;
    classDef orchestrator fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#0c4a6e;
    classDef mcp fill:#ffedd5,stroke:#ea580c,stroke-width:2px,color:#7c2d12;
    classDef database fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d;

    UI[Streamlit UI<br>Live Transcript & Hints]:::ui
    Agent[LangGraph Copilot<br>Reasoning Engine]:::orchestrator
    MCP[FastMCP Server<br>Enterprise Tools]:::mcp
    DB_CRM[(CRM Database<br>Profiles & Tiers)]:::database
    DB_ERP[(ERP Warehouse<br>Stock & Pricing)]:::database

    UI <-->|Transcript Chunk / HINTs| Agent
    Agent <-->|Secure Tool Calls| MCP
    MCP -.->|get_client_profile| DB_CRM
    MCP -.->|check_inventory<br>get_dead_stock_promos| DB_ERP