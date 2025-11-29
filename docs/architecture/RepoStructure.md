# CogniWeave Repository Structure
```
root/
│
├── extension/                      # Workflow Capture Layer (Chrome Extension)
│   ├── src/
│   │   ├── content/                # Content scripts injected into pages
│   │   ├── background/             # Service worker logic
│   │   ├── ui/                     # Popup & extension UI
│   │   └── utils/                  # Shared helpers (selectors, storage)
│   │
│   ├── public/                     # Icons, static assets
│   ├── manifest.json
│   └── README.md
│
├── pattern-mining/                 # Pattern Mining & Understanding Layer
│   ├── src/
│   │   ├── preprocessing/          # Cleaning & normalization
│   │   ├── segmentation/           # Session & task splitting
│   │   ├── mining/                 # Pattern detection algorithms
│   │   ├── generalization/         # Workflow abstraction & parameter extraction
│   │   └── ranking/                # Automation candidate scoring
│   │
│   ├── tests/                      # Unit tests for algorithms
│   └── README.md
│
├── automation/                     # Automation Execution Layer
│   ├── generators/                 # JSON → Playwright/Puppeteer/script generators
│   ├── runners/                    # Execution engines (local, cloud, in-extension)
│   ├── llm/                        # Prompts & logic for selector healing/generalization
│   ├── api/                        # REST API endpoints for execution
│   └── README.md
│
├── models/                         # ML models (optional future)
│   ├── datasets/                   # Anonymized event sequences
│   ├── embeddings/                 # Vector representations
│   ├── training/                   # Training scripts
│   └── README.md
│
├── docs/                           # Full documentation for contributors
│   ├── architecture/               # Diagrams, flowcharts, system design
│   ├── specs/                      # Detailed layer specifications
│   ├── roadmap/                    # MVP → v1 → advanced future plans
│   └── CONTRIBUTING.md
│
├── examples/                       # Example logs, workflows, patterns
│   ├── events/                     # Raw & processed captured events
│   ├── workflows/                  # Generalized automation workflows
│   └── patterns/                   # Detected patterns & clusters
│
├── prototypes/                     # Experimental ideas (LLM, selectors, mining)
│   ├── selector-experiments/
│   ├── pattern-mining-playground/
│   └── llm-tests/
│
├── scripts/                        # Build, lint, deploy, and utility scripts
│
├── .github/                        # GitHub workflows & templates
│   ├── workflows/                  # CI/CD
│   └── ISSUE_TEMPLATE.md
│
├── package.json                    # If using JS/TS across repo
├── LICENSE
└── README.md                       # Main project overview
```

# Notes
- This structure is **modular, scalable, and contributor-friendly**.
- Each core layer is fully separated.
- Future ML, automation, or dashboard additions fit without restructuring.
- Works for solo development now and team collaboration later.