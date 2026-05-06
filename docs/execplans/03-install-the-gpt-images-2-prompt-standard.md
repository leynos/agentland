# Install the GPT Images 2 prompt standard

This ExecPlan (execution plan) is a living document. The sections
`Constraints`, `Tolerances`, `Risks`, `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work
proceeds.

Status: COMPLETE

## Purpose / big picture

Agentland needs one repository-owned prompt standard for development-time Codex
built-in GPT Images 2 work. After this change, a developer can open
`docs/imagegen-workflow.md` or `prompts/templates/README.md` and find the shared
schema, edit schema, generation rules, text rules, transparency policy, and
template catalogue without relying on chat history.

Success is observable when:

- Prompt 03 is checked off in `docs/agentland-prompt-pack.md`.
- `docs/imagegen-workflow.md` documents the standard prompt and edit schemas.
- `prompts/templates/README.md` repeats the shared schema and rules.
- The seven prompt template files exist under `prompts/templates/`.
- `docs/developers-guide.md` section 5 explains how maintainers use the
  standard.
- `make markdownlint` passes.

## Constraints

- Do not generate images while installing prompt standards or templates.
- Use Codex built-in `image_gen` as the default image authoring path in docs.
- Do not document CLI fallback as the default path.
- Do not document a destination-path argument for the built-in tool.
- Do not point templates at missing automation as if it already exists.
- Keep runtime-critical user interface text owned by the Rust renderer.
- Wrap Markdown paragraphs and bullets at 80 columns; wrap code blocks at 120
  columns.

## Tolerances

- Scope: stop and escalate if the work requires production Rust code changes.
- Dependencies: stop and escalate if a new tool or external dependency is
  required.
- Asset generation: stop and escalate if completion appears to require image
  generation.
- Validation: stop and escalate if `make markdownlint` cannot pass after two
  focused repair attempts.

## Risks

- Risk: The chroma-key helper may not exist yet.
  Severity: medium.
  Likelihood: observed.
  Mitigation: document manual chroma-key cleanup as the current workflow and
  mark automation as unavailable or planned.

- Risk: Prompt template rules may drift from the asset manifest schema.
  Severity: medium.
  Likelihood: medium.
  Mitigation: reference `docs/asset-spec.md` for canonical manifest fields such
  as `slice`, `palette`, and `atlas`.

## Progress

- [x] (2026-05-04) Created `docs/imagegen-workflow.md` with the shared
  generation schema, edit schema, built-in `image_gen` rules, text policy,
  transparency policy, manifest requirements, and validation guidance.
- [x] (2026-05-04) Created `prompts/templates/README.md` with the shared schema,
  edit schema, template catalogue, and operational rules.
- [x] (2026-05-04) Added `character-sheet.md`, `animation-sheet.md`,
  `environment-sheet.md`, `prop-cutout.md`, `ui-ornament.md`,
  `edit-invariants.md`, and `transparent-chromakey.md`.
- [x] (2026-05-05) Reflowed documentation and template line lengths to match
  repository Markdown style.
- [x] (2026-05-05) Removed stale references to the missing chroma-key helper and
  documented the manual cleanup workflow.
- [x] (2026-05-06) Marked Prompt 03 complete, added this ExecPlan, and updated
  `docs/developers-guide.md` section 5.

## Surprises & discoveries

- Observation: `tools/remove_chroma_and_validate.py` is referenced by older
  workflow text but does not exist in the repository.
  Evidence: searching `tools/` found no such file.
  Impact: prompt templates now describe manual chroma-key cleanup while
  automation is unavailable.

- Observation: reviewer comments expected section 5 of
  `docs/developers-guide.md` to explain the prompt standard, not only list
  template files.
  Evidence: the failed documentation check named that section explicitly.
  Impact: section 5 now includes the schema, image generation, text, edit, and
  transparency rules maintainers need.

## Decision log

- Decision: Keep GPT Images 2 generation as a development-time Codex workflow,
  not a Rust runtime API.
  Rationale: runtime determinism belongs in Rust, manifests, processed assets,
  and local validation.
  Date/Author: 2026-05-04, Codex.

- Decision: Treat automation for chroma-key removal as unavailable until a real
  script exists under `tools/`.
  Rationale: documentation should not instruct developers to run missing
  commands.
  Date/Author: 2026-05-05, Codex.

- Decision: Use `docs/imagegen-workflow.md` and `prompts/templates/README.md` as
  the primary source for the shared prompt standard.
  Rationale: workflow rules and reusable templates need stable, reviewable
  repository paths.
  Date/Author: 2026-05-06, Codex.

## Outcomes & retrospective

Prompt 03 is complete. The repository now has a documented GPT Images 2 prompt
schema, a separate edit schema, template files for common Agentland asset
requests, manifest expectations for accepted generated images, and an explicit
policy that runtime-critical text belongs in Rust.

The main correction made after review was to stop treating the planned
chroma-key helper as available. The current docs now require manual keying for
transparent sources until automation is implemented.

## Context and orientation

`docs/imagegen-workflow.md` is the detailed workflow for Codex built-in
`image_gen` work. It defines the labelled prompt schema, edit schema, built-in
tool rules, text policy, transparent asset policy, manifest requirements, and
validation checks.

`prompts/templates/README.md` is the template catalogue and quick reference.
The individual templates under `prompts/templates/` are concrete prompt
starting points for characters, animations, environments, props, UI ornaments,
edits, and chroma-key sources.

`docs/asset-spec.md` defines canonical asset buckets, intent classes, manifest
fields, and planned post-processing tools. Templates should refer to this file
for manifest field names.

`docs/developers-guide.md` is the maintainer-facing overview. Its section 5 now
summarises the prompt-template rules that contributors should follow.

## Plan of work

The implementation work is complete. Future changes should keep the standard
coherent by editing the workflow document, template README, concrete templates,
asset specification, and developer guide together when prompt rules or asset
policy changes.

For future automation, add the chroma-key script under `tools/`, document its
command in `docs/imagegen-workflow.md`, update the relevant prompt templates,
and add validation coverage before presenting the script as available.

## Concrete steps

From the repository root:

```bash
make markdownlint
```

Expected result:

```plaintext
Summary: 0 error(s)
```

To inspect the prompt standard manually, open:

```plaintext
docs/imagegen-workflow.md
prompts/templates/README.md
prompts/templates/character-sheet.md
prompts/templates/animation-sheet.md
prompts/templates/environment-sheet.md
prompts/templates/prop-cutout.md
prompts/templates/ui-ornament.md
prompts/templates/edit-invariants.md
prompts/templates/transparent-chromakey.md
```

## Validation and acceptance

Acceptance criteria:

- `docs/agentland-prompt-pack.md` marks Prompt 03 as complete.
- `docs/execplans/03-install-the-gpt-images-2-prompt-standard.md` exists.
- `docs/developers-guide.md` section 5 documents the prompt standard and
  template workflow.
- `make markdownlint` passes with zero errors.
- No image files are generated by this work.

Quality method:

- Run `make markdownlint` from the repository root.
- Search for stale `tools/remove_chroma_and_validate.py` prompt-template
  references before documenting automation as available.

## Idempotence and recovery

The documentation edits are safe to repeat. If a later change reintroduces a
missing helper reference, replace it with the manual workflow until the script
exists and has validation coverage.

If markdown lint fails, inspect the reported file and line, rewrap paragraphs
or bullets at 80 columns, and rerun `make markdownlint`.

## Artifacts and notes

Relevant artifacts:

- `docs/imagegen-workflow.md`
- `prompts/templates/README.md`
- `docs/developers-guide.md`
- `docs/asset-spec.md`
- `prompts/templates/*.md`

The current branch is:

```plaintext
03-install-the-gpt-images-2-prompt-standard
```

## Interfaces and dependencies

This work defines documentation and prompt-template interfaces only. It adds no
Rust APIs, no runtime image-generation integration, and no external dependency.

Revision note: This ExecPlan was created after implementation to satisfy the PR
documentation gate. It records the completed Prompt 03 work, the review-driven
chroma-key correction, and the remaining rule that automation must not be
documented as available until the helper exists under `tools/`.
