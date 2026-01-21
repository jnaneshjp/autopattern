# Limitations & Improvements

## Current Limitations

### 1. Contextual Isolation
*   **Issue**: The automation runs in a fresh browser instance (context) for every execution. It does not natively share the user's existing cookies, local storage, or authenticated sessions from the recording phase.
*   **Impact**: Workflows requiring login must include the login steps explicitly, which can be blocked by 2FA (Two-Factor Authentication) or CAPTCHAs.

### 2. LLM Latency & Cost
*   **Issue**: The "Intent Synthesis" phase relies on cloud-based LLMs (Gemini).
*   **Impact**: There is a non-zero latency between submitting a workflow and the start of automation. High-frequency usage may incur API costs.

### 3. Dynamic DOM Complexity
*   **Issue**: While better than coordinate-based clickers, the agent may still struggle with highly dynamic Single Page Applications (SPAs) where element IDs or classes are obfuscated or randomized on every reload, if the semantic description isn't specific enough.

### 4. Non-Standard Browser Interactions
*   **Issue**: The current recorder excels at standard web events (clicks, types) but may have limited fidelity with complex canvas-based apps (like Figma or Maps) or system-level dialogs (file uploads/downloads).

---

## Future Improvements

### 1. Session Persistence & Profile Loading
*   **Goal**: Allow the user to "mount" their browser profile into the automation container.
*   **Benefit**: Bypassing login screens, CAPTCHAs, and maintaining "logged-in" state across multiple automation runs.

### 2. Local Model Support
*   **Goal**: Integrate support for local LLMs (e.g., Llama 3, Mistral) via tools like Ollama.
*   **Benefit**: Improved privacy (data never leaves the machine), reduced latency, and zero AI API costs.

### 3. Parallel Execution Grid
*   **Goal**: Scale the `AutomationRunner` to handle multiple tasks simultaneously.
*   **Benefit**: Enterprise-grade throughput (e.g., "Scrape these 500 URLs" running on 10 parallel browser instances).

### 4. Visual Regression Guardrails
*   **Goal**: Implement visual snapshots during the recording phase.
*   **Benefit**: The agent can compare its current view with the recorded "golden master" to confirm it is on the right page, adding a visual layer of verification to the semantic understanding.

### 5. Smart Selector Learning
*   **Goal**: Use the specific DOM paths captured during recording as "hints" for the agent.
*   **Benefit**: If the semantic description ("Click the blue button") is ambiguous, the agent can fall back to the recorded selector (`#submit-btn-v2`), combining the best of strict recording and flexible AI.
