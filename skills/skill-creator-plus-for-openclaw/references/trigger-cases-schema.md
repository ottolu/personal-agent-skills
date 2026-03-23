# Trigger cases schema

Use this schema with `scripts/improve_skill_description.py`.

```json
{
  "cases": [
    {
      "query": "Turn this recurring research workflow into a reusable skill and package it.",
      "should_trigger": true
    },
    {
      "query": "Summarize this one article for me.",
      "should_trigger": false
    }
  ]
}
```

## Guidance
- Prefer realistic, high-context user phrasing
- Include near-miss negatives, not only obviously irrelevant negatives
- Include enough positive variety to cover adjacent trigger phrasings
