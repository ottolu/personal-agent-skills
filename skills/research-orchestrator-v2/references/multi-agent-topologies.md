# Multi-agent topologies

Use parallelism only when the topic genuinely benefits from role separation.

## Default deep-research topology

1. **Planner**
   - frame the task
   - define success criteria
   - split the work into dimensions

2. **Primary-source scout**
   - collect Tier 1 evidence
   - identify canonical names, dates, repos, docs, papers, or launches
   - build a source map

3. **Domain lane A**
   - usually architecture / capability / benchmarks / implementation

4. **Domain lane B**
   - usually product / market / ecosystem / GTM / pricing / adoption

5. **Skeptic / red-team**
   - search for contradictions, adverse evidence, missing baselines, hype, staleness, and failure cases

6. **Synthesizer**
   - merge findings
   - classify evidence quality
   - surface disagreements
   - produce final judgments and next steps

## Good split patterns

### Technical topic
- architecture
- benchmarks / eval design
- tooling / ecosystem
- practitioner feedback
- red-team

### Product or company topic
- product / capability map
- pricing / packaging / GTM
- adoption / customer evidence
- competitor comparison
- red-team

### Landscape topic
- taxonomy / segmentation
- key players and positioning
- evidence by segment
- strategic implications
- red-team

## When not to parallelize

Avoid subagents when:
- the task is narrow and answerable from a few sources
- the overhead exceeds the value
- the job is mostly summarizing one artifact
- the lanes would all search the same material with no real role distinction

## Failure modes

Avoid:
- multiple agents searching the same thing with different labels
- no primary-source lane
- no contradiction-finding pass
- a final memo that summarizes but does not judge
- mixing facts, inferences, and opinions into one bucket
