# Edit and invariant prompt template

```text
Change:
[Describe exactly one change. Example: replace only the inactive plaque fill
with muted slate blue.]

Preserve:
- Approved Agentland pixel-art style.
- Original composition and crop.
- Character identity, silhouette, clothing, face or display, and role props.
- Environment zones, perspective, furniture placement, and focal order.
- Deep navy recesses, brass trim, cream highlights, warm amber lamp light, and
  screen-cyan work glows.
- Existing transparent background or chroma-key background, if present.
- No runtime-critical text in the image unless explicitly quoted below.

Text (verbatim): ""

Runtime text policy:
Runtime labels, statuses, chart text, task copy, and user interface (UI) state
strings are rendered by Rust. Do not add or modify text unless the Change
section quotes the exact copy.

Acceptance checks:
Only the requested change is visible; preservation invariants still hold; no
extra objects; no identity drift; no duplicate text; no watermark; no brand
marks; no new layout decisions.

Constraints:
Make one targeted edit. Do not redesign the asset. Do not change camera angle,
panel structure, character pose, palette family, or lighting direction unless
the Change section says so.
```
