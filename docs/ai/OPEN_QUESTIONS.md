# Open Questions

These questions are intentionally unresolved. Do not implement answers without a product or technical decision.

## Product

- Should a later version package Agent Warden as a Windows `.exe`?
- What other coding agents should be supported after Codex?
- Should the overlay support user-selectable display modes, such as compact, detailed, or hidden-until-attention?

## Technical

- Is stdlib Tkinter topmost behavior sufficient for common borderless-windowed games, or is `pywin32` needed?
- Should future Codex event parsing support `needs_attention`, `failed`, and `completed` states through an explicit privacy-reviewed allowlist?
- If local Codex histories grow large, should scanning be limited to recent date folders or cached between polls?
