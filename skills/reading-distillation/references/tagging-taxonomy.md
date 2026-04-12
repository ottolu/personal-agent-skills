# Tagging Taxonomy

Use a small, stable tag vocabulary.

## Always-on base tags

- `reading`
- `wechat-oa` or `web-article`

## Common domain tags

Pick 2-6 as appropriate:

- `agent`
- `agent-os`
- `memory`
- `workflow`
- `tool-use`
- `reasoning`
- `retrieval`
- `search`
- `vision`
- `multimodal`
- `benchmark`
- `paper`
- `research`
- `product`
- `coding`
- `coding-agent`
- `infra`
- `security`
- `startup`

## Common entity tags

Use only when clearly central:

- `openai`
- `anthropic`
- `google`
- `meta`
- `microsoft`
- `oppo`
- `codex`
- `claude`

## Formatting rules

- lowercase only
- kebab-case only
- no spaces
- no Chinese in `tags`
- no hash prefix
- avoid near-duplicates like `tool`, `tools`, `tool-use` in the same note

## Selection heuristic

1. Start with the 2 base tags.
2. Add 2-4 domain tags.
3. Add 0-2 entity tags only if central.
4. Stop once retrieval value starts flattening.

Prefer a compact, reusable taxonomy over expressive but inconsistent tags.
