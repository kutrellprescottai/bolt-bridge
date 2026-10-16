# Bolt Bridge

Shared hand-off point between the Hermes team on the VPS and **Bolt.new**.

**Why this repo exists:** Bolt has no public API, CLI, or SDK — Hermes cannot drive Bolt's builder. So the team installs its *standards* into Bolt instead, and Bolt builds to spec while burning the Bolt token budget rather than the Hermes budget.

## Layout

| Path | Owner | Purpose |
|---|---|---|
| `skills/` | illustrator | Bolt-format `SKILL.md` files, imported into Bolt's workspace Skills library |
| `design-system/` | illustrator | Tokens, components, patterns — imported as a Bolt design system |
| `briefs/` | alchemist | Paste-ready Bolt build briefs |

## Importing skills into Bolt

This repo must be **PUBLIC** — Bolt's GitHub import accepts public repositories only. Anything committed here is world-readable.

1. In Bolt, open **Settings → Skills library** (workspace level, so every project can use it), or a project's **gear icon → Skills**.
2. Click **Add skill → From GitHub**.
3. **Repository URL:** the public URL of this repo.
4. **Skill folder name:** pick the skill from the dropdown Bolt populates.
5. Click **Create**, then turn the skill on in each project that should use it.

### Rules Bolt enforces

| Field | Constraint |
|---|---|
| `name` | Lowercase letters, numbers, hyphens. Max **64 chars**. No spaces, underscores, XML tags, or reserved words (`anthropic`, `claude`). |
| `description` | Max **1024 chars**, no XML tags. Must open with **"Use when"** and cover trigger, scope, and boundary. |
| File | `.md` / `.mdx`, max **256 KB** (`.zip` max 2 MB, with the skill file itself still ≤256 KB). |

The `description` decides *when* Bolt applies the skill. Too broad → fires everywhere. Too narrow → never fires.

### Two caveats

- **Import is not sync.** Bolt detaches the skill from GitHub the moment it imports. To update, re-import and delete the outdated copy. Keeping the source of truth here is the version-control answer.
- **Cost is near-zero when idle.** Bolt reads only name + description until a prompt matches, then reads the full instructions. Good scoping means you can keep many skills switched on.

Do **not** duplicate Bolt's built-in curated skills — SEO/GEO, Web Design Guidelines, Writing Guidelines already ship with Bolt. This repo is for skill Bolt does *not* have: the owner's brand, voice, and product-specific rules.

## Importing the design system

Bolt accepts a design system from a GitHub repo, npm package, Storybook, website, or files — see **Add your design system**. Point it at `design-system/` so Bolt builds with real components from the first prompt instead of generic styling.

## Confidentiality

Prompts submitted to Bolt become "Bolt Model Development Content" and are used for StackBlitz's model development unless the owner is in the EEA/UK/CH or Forge is enabled. Send **implementation** requirements to Bolt; keep **strategy** on the VPS. Do not commit or paste commercially sensitive reasoning here — express the build requirement without the thinking behind it.
