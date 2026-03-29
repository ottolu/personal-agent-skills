# Output Orientations

Use this file to choose the **output lens** for a Full Deep Research run.
These are not execution modes. Execution remains **Full Deep Research**.
The orientation only changes how the final deliverable is framed, prioritized, and written.

## 1. Exploration-oriented

Use when the goal is to map a space, build a taxonomy, surface open questions, or clarify how a field is structured.

Prioritize:
- segmentation / taxonomy
- key entities and clusters
- major debates or unresolved questions
- where evidence is sparse or fragmented

Typical output shape:
- landscape map
- category definitions
- representative examples by segment
- open questions
- next research directions

## 2. Decision-support-oriented

Use when the user needs to make a choice, allocate resources, compare options, or decide what to prioritize.

Prioritize:
- options and tradeoffs
- evidence behind each option
- risks, constraints, and dependencies
- recommendation with reasoning

Typical output shape:
- decision question
- options compared
- decision criteria
- evidence and tradeoffs
- recommendation
- what could change the recommendation

## 3. Executive-brief-oriented

Use when the audience is a leader or stakeholder who needs a conclusion-first, low-friction synthesis.

Prioritize:
- headline conclusion first
- what matters now
- why this matters strategically
- major risks / uncertainties
- concise action implications

Typical output shape:
- headline takeaway
- 3–5 key findings
- why it matters
- risks / caveats
- recommended next moves

## 4. Technical-due-diligence-oriented

Use when the task is to stress-test technical claims, architecture, benchmarks, implementation realism, or deployment risks.

Prioritize:
- claim-by-claim verification
- benchmark quality and comparability
- architecture details and missing pieces
- implementation constraints
- hidden assumptions and failure modes

Typical output shape:
- claims under review
- primary technical evidence
- benchmark / eval assessment
- implementation realism
- key technical risks
- bottom-line judgment

## Selection heuristic

Choose the orientation that best matches the downstream use:
- if the user wants to understand a space -> **exploration-oriented**
- if the user needs to choose -> **decision-support-oriented**
- if the user needs a leader-ready memo -> **executive-brief-oriented**
- if the user needs technical pressure-testing -> **technical-due-diligence-oriented**

If two orientations both matter, pick one as primary and mention the secondary lens in the planning block.
