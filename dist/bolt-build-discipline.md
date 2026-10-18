---
name: bolt-build-discipline
description: "Use when planning or sequencing an app build, adding a feature, or executing any multi-step implementation in Bolt. Covers build order, prompt scoping, one feature per prompt, establishing the data model and auth before interface work, verifying each step before starting the next, and keeping context focused. Does not apply to single-line edits, isolated styling tweaks, or copy-only changes."
---

# Build Discipline

Work in an order that minimises rework. Every prompt you send re-reads the
project, so a step built on an unverified assumption pays for itself twice:
once when you build it wrong and again when you tear it out. Sequence the work
so each step is still true when the next one starts.

## 1. Plan before building

- For anything larger than a single file, start with an explicit plan: the
  entities, the screens, the actions, and the order you will build them in.
- Write the plan as a short ordered list and keep it visible. Do not begin
  implementation until the plan names every feature the request implies.
- If two parts of the request could share state or a type, decide the shared
  shape now. Retrofitting a shared type later is a full-project refactor.

## 2. Data model and auth before UI

- Model the data first: entities, their fields, their relationships, and their
  persistence. Build a working data layer and prove it before drawing a screen
  against it.
- Build authentication and authorisation before the interfaces that depend on
  them. A UI built against a placeholder user must be rebuilt once real
  sessions, roles, and redirects exist.
- Never stub data that a later step will replace. Stubs become load-bearing and
  cost more to remove than to have built correctly once.

## 3. One feature per prompt

- Scope each prompt to exactly one feature or one bug. A prompt that asks for
  three features produces three half-finished features and an unclear diff.
- Do not bundle "and also fix X" into a feature prompt. Finish and verify the
  feature, then send the fix as its own prompt.
- If a feature cannot fit in one coherent step, split it along its seams (data,
  then logic, then interface), not down the middle of a file.

## 4. Verify each step before starting the next

- After each step, confirm it actually works: run it, exercise the path, read the
  output. A step is not done because the code exists; it is done because it runs.
- Only start the next step on a green result. Building on a broken base
  multiplies the search space for every subsequent bug.
- State what you verified, so a later prompt can rely on it rather than
  re-deriving it.

## 5. Never refactor unrelated code

- Touch only what the current step requires. Do not tidy, rename, or restructure
  code that works and is not part of the feature.
- Unrelated refactors hide the real change, break callers, and make a clean build
  look like a rewrite. If a refactor is genuinely needed, make it its own prompt
  with its own verification.
- Preserve existing public interfaces unless the current feature requires
  changing them. Silent signature changes are the most expensive kind of rework.

## 6. Keep context focused

- Keep the working set small: the files this step touches, plus their immediate
  dependencies. Do not pull the whole project into one prompt.
- Re-state the relevant invariant (the data shape, the auth rule, the active
  feature) at the start of each prompt so it is not re-inferred from scratch.
- Close out a feature before opening the next. Carry no partial feature forward
  as background noise.
