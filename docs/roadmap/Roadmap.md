# Project Roadmap: Workflow Capture Layer & Pattern Mining Layer

This document outlines the roadmap, build strategy, and optional paths for the **Workflow Capture Layer** and **Pattern Mining & Understanding Layer** of the project. It is structured to help future contributors understand possible approaches and make flexible design decisions.

---

# ## 1. Overview
The goal of the system is to:
1. **Capture real browser workflows passively** (always-on recording).
2. **Normalize and structure raw event data**.
3. **Detect repetitive tasks**.
4. **Generalize patterns into automation-ready workflows**.

Each layer includes multiple implementation paths to choose from depending on complexity, performance needs, and future scalability.

---

# # 2. Workflow Capture Layer
The capture layer continuously records browser actions in a structured format. This is the foundation of the entire automation system.

## ### 2.1 Core Responsibilities
- Capture user interactions (clicks, typing, navigation, scrolls, etc.).
- Extract metadata about interacted DOM elements.
- Segment activity into sessions.
- Store the event stream efficiently and safely.
- Maintain low performance overhead.

---

## ### 2.2 Architecture Components
1. **Browser Extension Shell (Manifest v3)**
2. **Content Scripts (per-site injection)**
3. **Event Listener Module**
4. **Selector Extraction Module**
5. **Session & Idle-Time Segmenter**
6. **Local Storage (IndexedDB / Local Storage)**
7. **Prefilter & Noise Reduction Module**
8. **Event Batcher & Exporter**

---

## ### 2.3 Capture Categories
Events to capture may include:
- Clicks & pointer interactions
- Text input (non-sensitive or masked)
- Form submissions
- Page navigation
- Scroll & viewport actions
- Element focus/blur
- File uploads & downloads
- Change events (dropdowns, checkboxes)
- SPA route changes (via pushState, popstate, etc.)

---

# ### 2.4 Selector Extraction Options
Selectors determine how the automation engine will re-identify elements later.

Choose one or combine multiple strategies:

#### **Option A: CSS Selectors (simple)**
- Primary selector type
- Lightweight
- Breaks if DOM structure changes frequently

#### **Option B: XPath (fallback)**
- Works with deep tree structures
- Harder to maintain manually

#### **Option C: Attribute-based selectors**
- `data-*` attributes
- Role/ARIA attributes
- Semantic HTML tags

#### **Option D: Multi-selector Bundles (recommended)**
- Combine CSS + XPath + attributes + innerText + bounding box metadata
- More robust for identifying elements

#### **Option E: AI-generated semantic selectors**
- Use LLM to describe elements in natural language
- Future-proof but not essential for MVP

---

## ### 2.5 Data Storage Options
#### **Option A: IndexedDB (recommended)**
- Efficient for large logs
- Persistent
- Good read/write performance

#### **Option B: `chrome.storage.local` (small-scale)**
- Simpler API
- Lower memory limits

#### **Option C: Local backend (advanced)**
- Push logs to local desktop service
- Good for cross-browser or multi-app capture

#### **Option D: Remote server (optional)**
- Offload processing
- Privacy considerations needed

---

## ### 2.6 Noise Reduction & Prefiltering Options
Implement lightweight client-side filtering to avoid storing useless data.

#### Techniques:
- Combine consecutive similar events
- Ignore insignificant DOM nodes
- Threshold scroll/mouse movement events
- Batch events before writing
- Idle-time segmentation (sessionizing)

---

## ### 2.7 Sessionization Modes
How to segment workflows at the capture stage:

#### **Option A: Time-based segmentation**
- Break session if idle > X seconds

#### **Option B: Navigation-based segmentation**
- New session when page changes or SPA route changes

#### **Option C: Hybrid segmentation (recommended)**
- Combine time + navigation cues

#### **Option D: ML-based segmentation (future)**
- Predict logical boundaries based on event semantics

---

# # 3. Pattern Mining & Understanding Layer
This layer transforms raw event streams into meaningful workflows and identifies patterns.

---

## ### 3.1 Core Responsibilities
- Normalize raw events
- Detect repeated sequences
- Cluster similar tasks
- Generalize workflows into reusable structures
- Identify parameters & variable parts
- Rank tasks by automation value

---

# ### 3.2 Pipeline Stages

## #### 1. Data Normalization
Convert inconsistent event logs into structured sequences.

Options include:
- Rule-based normalization
- Event coalescing
- Semantic labeling via heuristics
- LLM-assisted labeling (advanced)

---

## #### 2. Task Segmentation (Splitting Long Sessions)
Options:

**A. Time-gap segmentation**  
**B. Navigation/URL change-based**  
**C. Content/DOM change-based**  
**D. Hybrid (recommended)**  
**E. ML/LLM-based auto-segmentation (advanced)**

---

## #### 3. Pattern Detection
Several strategies exist, depending on complexity and accuracy.

### **Option A: Exact Matching**
- Hash entire sequences
- Count occurrences
- Simple & fast

### **Option B: Approximate Matching**
- Sequence similarity (Levenshtein, DTW)
- Good for slightly varying workflows

### **Option C: Subsequence Mining**
- Find frequent smaller patterns
- Approaches: PrefixSpan, SPADE

### **Option D: Clustering Approaches**
- Vectorize action sequences
- Use K-means / HDBSCAN
- Identify groups of similar tasks

### **Option E: LLM-based Pattern Identification**
- Convert sequences to text
- Ask model to cluster or summarize
- Powerful for semantic subtleties

---

## #### 4. Task Generalization
Merge multiple similar sequences into a universal template.

### Options:
- Sequence alignment
- Frequency-based optional step detection
- Parameter identification rules
- Template merging
- LLM-based workflow generalization

The output should be a clean workflow representation with:
- Steps
- Parameters
- Branches (optional)
- Loops (optional)

---

## #### 5. Automation Candidate Ranking
Determine which tasks are worth automating.

### Ranking strategies:
- Frequency of repetition
- Total time saved
- Task complexity
- Error-prone/human effort
- Page/website importance

---

# # 4. Deliverables of These Layers
The combined layers should output:

- **Cleaned event logs**
- **Task segments**
- **Detected patterns**
- **Generalized reusable workflows (JSON)**
- **Parameter lists**
- **Automation candidate rankings**

These are then consumed by the **Automation Layer** which will execute or generate scripts.

---

# # 5. Future Enhancements
After MVP:
- Add self-learning models that adapt workflows over time
- Introduce LLM-based reasoning for “next action” prediction
- Enable cross-device workflow capture
- Add vision-based UI understanding
- Introduce self-healing selectors using AI
- Implement recommendation systems based on habits

---

# ## 6. Summary
This roadmap provides options for building both the Workflow Capture Layer and the Pattern Mining Layer. You can start simple (rule-based + exact matching) and progressively adopt more advanced technologies (clustering, LLMs, ML-based segmentation) as the dataset grows.

---

This document is versioned for future updates as the design evolves.