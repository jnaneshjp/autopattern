# Methodology

AutoPattern operates on a **"Watch, Understand, Replicate"** paradigm. Unlike rigid script-based automation, AutoPattern combines behavioral recording with semantic understanding to create resilient automation workflows.

## 1. Phase One: Observation (Data Capture)
The process begins with the **AutoPattern Task Mining Extension**. This acts as the sensory systems, observing user interactions within the browser.

*   **Event Interception**: The extension monitors low-level DOM events (clicks, inputs, scrolls, navigation) across the user's session.
*   **Signal-to-Noise Processing**: Raw input is noisy. We implement a client-side **Noise Reduction Layer** (see `extension/src/utils/noiseReduction.js`) that filters out:
    *   Insignificant mouse jitters.
    *   Redundant scroll events.
    *   Interactions with non-interactive DOM nodes.
    *   "Ghost" events that don't contribute to the task outcome.
*   **Session Grouping**: Events are temporally grouped into logical sessions, ensuring that a "task" is captured as a coherent unit rather than a disjointed stream of actions.

## 2. Phase Two: Intent Synthesis (The "Brain")
Once the raw behavioral data is captured, it is transmitted to the **AutoPattern Backend**. This is where the core intelligence resides.

*   **Workflow Ingestion**: The backend accepts the structured event log (Workflow CSV/JSON).
*   **Semantic Analysis**: We utilize Large Language Models (Gemini via `llm_client.py`) to analyze the event stream. Instead of simply replaying coordinates, the system "reads" the user's actions to determine the **Intent**.
    *   *Input:* `[Click "Search", input "Red Shoes", Click "Submit"]`
    *   *Output:* "Navigate to the e-commerce platform and search for 'Red Shoes' product listings."
*   **Plan Generation**: The system converts the retrospective recording into a prospective **Action Plan**, decoupling the "what" (the goal) from the "how" (the specific previous clicks).

## 3. Phase Three: Autonomous Execution (The "Hands")
To execute the synthesized intent, AutoPattern orchestrates a robust browser automation environment through the `AutomationRunner`, which manages task lifecycle, configuration (headless modes, logging), and error recovery. We utilize `browser-use`, a powerful alternative to raw Playwright scripting, as the core execution engine that abstracts browser interaction complexities.

The automation layer exposes a comprehensive registry of atomic actions: navigation and search, page interaction (clicks, inputs, scrolls), JavaScript execution, tab management, LLM-powered content extraction, visual analysis via screenshots, form controls, file operations, and task completion signaling. When needed, operators can intervene through WebSocket channels to guide the agent through ambiguous situations.