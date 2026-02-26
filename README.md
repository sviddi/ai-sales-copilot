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
    %% Custom Enterprise Colors
    classDef actor fill:#f8fafc,stroke:#94a3b8,stroke-width:2px,color:#0f172a,stroke-dasharray: 5 5;
    classDef frontend fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a;
    classDef agent fill:#f0fdf4,stroke:#22c55e,stroke-width:2px,color:#14532d;
    classDef mcp fill:#fff7ed,stroke:#f97316,stroke-width:2px,color:#7c2d12;
    classDef db fill:#f3f4f6,stroke:#4b5563,stroke-width:2px,color:#111827;

    %% 1. Real World
    subgraph Real_World [1. Real World Interaction]
        Manager((👤 Sales Manager)):::actor
        Client((📞 Client)):::actor
    end

    %% 2. Frontend Layer
    subgraph UI_Layer [2. Frontend: Streamlit App]
        UI_Chat[Live Transcript View]:::frontend
        UI_Hints[AI Insights Panel]:::frontend
    end

    %% 3. Cognitive Engine (LangGraph)
    subgraph AI_Core [3. Cognitive Engine: LangGraph]
        LLM[GPT-4o-mini<br>Reasoning Node]:::agent
        Router{Tool Router}:::agent
    end

    %% 4. Integration Layer (MCP)
    subgraph MCP_Layer [4. Integration: FastMCP Server]
        Tool_CRM[⚙️ get_client_profile]:::mcp
        Tool_Inv[⚙️ check_inventory]:::mcp
        Tool_Promo[⚙️ get_dead_stock_promos]:::mcp
    end

    %% 5. Data Layer
    subgraph Data_Layer [5. Enterprise Databases]
        CRM[(CRM DB<br>VIP Tiers)]:::db
        ERP[(ERP DB<br>Stock & Age)]:::db
    end

    %% Data Flow
    Manager -->|Speaks| UI_Chat
    Client -->|Speaks| UI_Chat
    
    UI_Chat -->|Streams Transcript| LLM
    LLM -->|"Generates [🔥 HINT]"| UI_Hints
    UI_Hints -->|Displays Action| Manager

    LLM <-->|ReAct Loop| Router
    Router -->|MCP Protocol| Tool_CRM
    Router -->|MCP Protocol| Tool_Inv
    Router -->|MCP Protocol| Tool_Promo

    Tool_CRM -.->|Read| CRM
    Tool_Inv -.->|Read| ERP
    Tool_Promo -.->|Read| ERP
    Tool_Inv -.->|Read| ERP
    Tool_Promo -.->|Read| ERP
