# Tech Stack

## Frontend (Extension & Dashboard)
*   **Platform**: Chrome Extension (Manifest V3)
*   **Core Languages**: HTML5, CSS3, JavaScript (ES6+)
*   **Architecture**:
    *   **Service Workers**: For background processing and state management (`background.js`).
    *   **Content Scripts**: For DOM event interception and noise reduction (`content.js`).
    *   **IndexedDB**: For local storage of recorded workflows and noise reduction buffering.
*   **Visualization**: `Mermaid.js` (for rendering workflow diagrams in the dashboard).

## Backend (API & Orchestration)
*   **Language**: Python 3.11+
*   **Framework**: **FastAPI** (High-performance Async API).
*   **Package Management**: **uv** (Ultra-fast Python package installer/resolver).
*   **AI/LLM Integration**: 
    *   **Google Gemini** (via `langchain-google-genai`): The core reasoning engine for intent detection and navigation planning.
    *   **LangChain**: For prompt management and model interaction abstraction.
*   **Automation Infrastructure**:
    *   **Browser-use**: The primary high-level driver and Playwright alternative that executes the AI agent's actions.
    *   **Playwright**: The underlying browser control protocol (managed by browser-use).
*   **Communication**: WebSockets (for real-time Human-in-the-Loop interaction).

## Data Interchange
*   **Format**: JSON (API), CSV (Workflow Exports).
*   **Standards**: RESTful API design for client-server communication.
