---
name: accessibility-baseline
description: "Use when building or editing any user-facing interface element: components, forms, navigation, buttons, modals, dialogs, and page structure. Covers colour contrast, visible focus states, complete keyboard paths, labelled form inputs, semantic HTML over div soup, meaningful alt text, and honouring prefers-reduced-motion. Does not apply to backend logic, data pipelines, configuration, or non-visual scripts."
---

# Accessibility Baseline

Every interface must clear this floor. Accessibility is part of done, not a
later pass: keyboard paths, contrast, and semantics are structural, and
retrofitting them means rebuilding the component. Meet this baseline as you
build each element.

## Colour contrast

- Body text and icons must reach at least 4.5:1 against their background.
- Large text (18.66px bold, or 24px and above) must reach at least 3:1.
- UI component boundaries, focus rings, and meaningful graphics must reach at
  least 3:1 against adjacent colours.
- Never carry meaning by colour alone. Pair colour with a label, icon, or shape,
  so red/green states read as more than a hue.

## Visible focus states

- Every interactive element must show a clearly visible focus indicator. Never
  set `outline: none` without an equally visible replacement.
- The focus ring must be perceivable against its own background and must not be
  clipped by overflow or rounded corners.
- Use the `:focus-visible` pattern so keyboard users always see focus while
  pointer users are not surprised by it.

## Full keyboard paths

- Every interactive control must be reachable and operable by keyboard alone.
  If it can be clicked, it must be focusable and triggerable from the keyboard.
- Tab order must follow the visual reading order. Do not rely on positive
  `tabindex`; keep the DOM order meaningful instead.
- Provide a visible skip-to-content link as the first focusable element.
- Dialogs and menus must trap focus while open and return focus to the trigger
  on close. Escape must dismiss them.

## Labelled form inputs

- Every input must have a programmatically associated label. Use a `label`
  element tied to the input by `for`/`id`; use `aria-label` only when no visible
  label is possible.
- Mark required fields in an accessible way, not by an asterisk alone.
- Tie errors to their field with `aria-describedby`, set `aria-invalid` on the
  field, and announce the error text. Never signal an error by red border only.
- Group related controls (radios, checkboxes) in a `fieldset` with a `legend`.

## Semantic HTML over div soup

- Reach for the correct element before a generic container: `button`, `a`,
  `nav`, `main`, `header`, `footer`, `ul`/`li`, `form`, `dialog`.
- A click handler on a `div` is not a button. Use `button` for actions and `a`
  with a real `href` for navigation.
- Use one `main` per page and one `h1`; keep heading levels sequential and never
  skip a level for styling.
- Add ARIA only to fill genuine gaps. Native elements already carry the roles,
  states, and keyboard behaviour you need; wrong ARIA is worse than none.

## Alt text

- Give every meaningful image descriptive alt text stating its purpose, not its
  filename or "image of".
- Decorative images take an empty `alt=""` so they are skipped, not announced.
- For icon-only controls, provide an accessible name, and hide the decorative
  icon from the accessibility tree.

## Honour prefers-reduced-motion

- Respect `prefers-reduced-motion: reduce`: remove or drastically shorten
  animations, parallax, and auto-playing motion.
- Never autoplay motion that cannot be paused, stopped, or hidden.
- Keep essential state changes perceivable without motion, so nothing is
  conveyed only through animation.
