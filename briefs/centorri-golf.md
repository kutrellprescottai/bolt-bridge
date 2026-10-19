# Centorri Golf — Bolt Build Brief

Mission M-007. Paste the prompts below into Bolt.new in order. Send one prompt at
a time and confirm the **Done when** check before sending the next.

---

## Prerequisites — do these before prompt 1

1. Import both skills into your Bolt workspace **Skills library**
   (Settings → Skills library → Add skill → From GitHub).
   Repository URL: `https://github.com/kutrellprescottai/bolt-bridge`
   - `bolt-build-discipline` — turn this ON for the whole project. It governs
     build order, one feature per prompt, and verifying each step.
   - `accessibility-baseline` — turn this ON for the whole project. It governs
     contrast, focus states, keyboard paths, and semantics on every screen.
2. Create a Supabase project (free tier is fine) and have its **Project URL**,
   **anon key**, and **service-role key** ready. Bolt's Supabase integration
   will ask for these.
3. Have an Expo Go app installed on a physical phone or a simulator ready.

If a skill name is misspelled or absent from the dropdown, stop and fix the
import before starting — the build depends on both.

---

## Framing

**Centorri Golf** is a mobile app for golfers who want to play more, and play
with the right people. It is for the everyday club and public-course golfer who
books as a single but would rather not play alone. The one job it does: match a
golfer with nearby players of a similar handicap, then let them join a real
open tee time — a round gets planned and two to four players meet on the first
tee.

It has three surfaces, and nothing else:
- **Match** — swipe through nearby players whose handicap is close to yours.
- **Hitchhike** — browse open tee times posted by other golfers and request to
  join.
- **Play** — your confirmed rounds and the people in them.

## Stack

- **React Native + Expo** (SDK 51 or later) with **Expo Router** — this is a
  **mobile app**, so Expo is set up in prompt 1 and every screen targets iOS
  and Android.
- **TypeScript** throughout.
- **Supabase** for authentication, the Postgres database, file storage (handicap
  screenshots), realtime chat, and Edge Functions (handicap screenshot parsing).
- **Expo Notifications** for push notifications.
- Styling via a small design-token module (`constants/theme.ts`) plus React
  Native `StyleSheet`. No CSS framework — keep the dependency surface small.
- Brand palette: deep navy `#0A1F44`, mid blue `#123C7A`, bright yellow
  `#FFD400`, off-white `#F7F8FA`, ink `#0B1220`. Yellow is an accent and a
  call-to-action colour; never use yellow text on off-white. Street-brand energy
  means confident type and bold yellow CTAs on deep blue; authoritative means
  generous spacing, consistent radii, and no decoration that does not carry
  meaning.

If a design system has been added to the Bolt workspace under `design-system/`,
it overrides this palette. Otherwise use the tokens above.

## Build order

Data model and authentication land **before** any interface work. Handicap
import lands before the matching UI, because matching depends on handicap data
being real. Every prompt below is one feature.

## Risks

- **Handicap import from 18Birdies and similar apps has no official import
  endpoint.** The build must not pretend otherwise. Prompt 4 specifies three
  real paths — manual index entry, paste of a handicap index, and screenshot
  upload parsed server-side — and nothing in the app may claim a direct account
  sync that does not exist. If Bolt invents an OAuth flow against a third-party
  golf app, delete that prompt's output and re-send prompt 4 as written.
- **Location-based discovery drifts.** If prompt 6's nearby query returns the
  wrong city or ignores the radius, the fix is to re-send prompt 6 with the
  radius literal stated, not to patch discovery inside a later prompt.

---

## Prompt 1 — Project scaffold, navigation shell, and theme tokens

```
Plan first, then build. We are starting a mobile app called Centorri Golf.
Before writing code, output a short ordered plan: the entities, the screens,
and the build order you intend to follow. Do not begin implementation until
that plan is written.

Then scaffold it:
- Create a React Native Expo project in TypeScript using Expo Router with a
  bottom tab navigator containing exactly three tabs: Match, Hitchhike, Play.
  Match is the initial route. These names are fixed product terms with these
  exact meanings — do not reinterpret them:
  - Match: swipe through nearby golfers whose handicap is close to yours. A
    mutual like creates a match and opens a chat.
  - Hitchhike: browse open tee times other golfers have posted and request to
    join one. "Hitchhike" means joining someone else's tee time. It is NOT
    transport — there is no ride, carpool, origin, destination, or seats
    anywhere in this product.
  - Play: the confirmed rounds you are in, and the golfers you are playing
    with.
- Add constants/theme.ts exporting the brand tokens as named constants:
  colors (navy #0A1F44, blue #123C7A, yellow #FFD400, offwhite #F7F8FA,
  ink #0B1220, plus muted, border, success, danger), spacing scale
  (xs 4, sm 8, md 16, lg 24, xl 32), radii (sm 8, md 12, lg 20, pill 999),
  and a type scale (display, h1, h2, body, caption).
- Give each of the three tabs a placeholder screen: navy header with the
  screen name in off-white, a short one-line description, and a single yellow
  rounded button. Use the theme tokens, never hard-coded hex values.
- Apply SafeAreaView on every screen and support light mode only for now.
- Follow the accessibility-baseline skill on every tab: semantic elements,
  visible focus, and colour contrast of at least 4.5:1 for body text.
```

**Done when:** `npx expo start` runs with no errors; the app opens on Match; all
three tabs are reachable by tapping and the tab bar shows the correct active
state; no screen shows an error boundary; the placeholder buttons use the yellow
accent from the token file.

---

### Correction 1a — run this if Bolt misread the tab names

Bolt infers product meaning from tab names, and "Hitchhike" is a trap: it will
assume transport. If its plan, icons, or screen copy mention a ride, driver,
passenger, carpool, origin, destination, or seats — or if it gives Play the
tee-time list — run this scoped correction before sending prompt 2.

```
Correction to the scaffold. The tab names are fixed product terms and two of
them were misread, so the placeholder copy and plan are wrong. Do not rebuild
the scaffold — make only these changes.

The meanings, which are not negotiable:
- Match: swipe through nearby golfers whose handicap is close to yours. A
  mutual like creates a match and opens a chat.
- Hitchhike: browse open tee times posted by other golfers and request to join
  one. It means joining someone else's tee time. It has nothing to do with
  transport — no ride, carpool, driver, passenger, origin, destination, or
  seats exists in this product.
- Play: the confirmed rounds you are in, and the golfers you are playing with.

Make exactly these changes:
1. Remove from your plan every ride-related entity or concept (ride offer,
   ride request, origin, destination, seats). Nothing like that exists here.
2. Set the three tab placeholder descriptions to exactly these lines:
   - Match: "Swipe through golfers near you with a similar handicap. A mutual
     like starts a chat."
   - Hitchhike: "Join an open tee time posted by another golfer."
   - Play: "Your confirmed rounds and the golfers you're playing with."
3. Replace the car icon on the Hitchhike tab with a flag icon. Give Play a
   calendar icon. Keep Match as it is.
4. Change nothing else — the theme tokens, SafeAreaView, and accessibility
   work already done all stay.

Then re-run the typecheck and the build and report the result.
```

**Done when:** no screen copy, icon, or entity refers to a ride, driver,
passenger, or seats; the three descriptions match the lines above verbatim;
`tsc --noEmit` and a web export still pass.

---

## Prompt 2 — Data model and migrations

```
Set up the Supabase data layer. Do not build any UI in this prompt.

The schema below is the product. Hitchhike is joining another golfer's open tee
time — it is not transport, so there is no ride, carpool, origin, destination,
or seat anywhere in it. Discard any ride entity from an earlier plan of yours.

Create a migration SQL file that defines these tables with row-level security
enabled on all of them:

- profiles: id (uuid, references auth.users), display_name, avatar_url,
  home_course, bio, handicap_index (numeric), location (geography point),
  city, created_at.
- handicap_records: id, user_id, source (one of 'manual','paste','screenshot'),
  value (numeric), raw_text, verified (boolean), created_at.
- swipes: id, swiper_id, target_id, direction ('like' or 'pass'), created_at,
  unique on (swiper_id, target_id).
- matches: id, user_a, user_b, created_at, unique unordered pair.
- tee_times: id, host_id, course_name, course_location (geography point),
  starts_at (timestamptz), players_needed (int), handicap_band_min,
  handicap_band_max, notes, status ('open','filled','cancelled'), created_at.
- hitchhike_requests: id, tee_time_id, requester_id, status
  ('pending','accepted','declined'), created_at, unique on (tee_time_id,
  requester_id).
- messages: id, match_id, sender_id, body, created_at.

Also create a private storage bucket named 'handicap-proofs'.

Policies: a user may read all profiles but update only their own; may read and
write only their own swipes, handicap_records, and messages; may read matches
and hitchhike_requests they are part of; may insert a tee_time as themselves
and update only tee times they host. Then generate the TypeScript types for the
schema and add a typed Supabase client at lib/supabase.ts reading the project
URL and anon key from environment variables.

Follow the bolt-build-discipline skill: no stubs, no placeholder data.
```

**Done when:** the migration runs cleanly in the Supabase SQL editor with no
errors; all seven tables and the storage bucket exist; `lib/supabase.ts`
exports a typed client; the generated types file lists every table and column
above.

---

## Prompt 3 — Authentication and onboarding

```
Build authentication and a first-run profile in the Expo app.

- Email/password sign-up and sign-in, plus Apple and Google sign-in via
  Supabase OAuth, on an auth screen that matches the theme tokens.
- Persist the session so a signed-in user lands straight on Match on relaunch,
  using a root layout that redirects unauthenticated users to the auth screen
  and authenticated users to the tabs.
- After first sign-up, show a two-step onboarding that writes to profiles:
  display_name, home_course, city, bio. Validate that display_name and city are
  non-empty before allowing continue.
- Handle loading, error, and signed-out states explicitly — no blank screens.

Follow the accessibility-baseline skill: every input has a visible label,
errors are tied to their field with aria-equivalent props and announced, and
focus moves to the first invalid field on submit.
```

**Done when:** a new user can sign up, complete onboarding, and land on Match;
the row appears in `profiles` in Supabase with the entered values; closing and
reopening the app keeps the user signed in; signing out returns to the auth
screen.

---

## Prompt 4 — Handicap import (manual, paste, and screenshot)

```
Build the handicap import flow. There is no direct account sync with any
third-party golf app — do not build one and do not claim one anywhere in the
copy. Support exactly these three paths, each writing a row to handicap_records
and updating profiles.handicap_index:

1. Manual: type a handicap index between 0 and 54.0; validate the range.
2. Paste: a multiline text box where the user pastes text copied from another
   golf app; parse the first number that falls between 0 and 54.0 and confirm
   the parsed value with the user before saving.
3. Screenshot: pick an image with expo-image-picker, upload it to the private
   'handicap-proofs' storage bucket under the user's own folder, then call a
   Supabase Edge Function named 'parse-handicap' that reads the image and
   returns a parsed index. Show the parsed value for confirmation before
   saving. Mark the record verified = true only when the user confirms.

Build the Edge Function 'parse-handicap' as part of this prompt. It must
return a JSON object { value: number | null, raw_text: string }. If no
parseable index is found, return value: null and let the app show "Could not
read a handicap from that image — enter it manually."

Every saved record sets source to 'manual', 'paste', or 'screenshot' to match
the path used.
```

**Done when:** all three paths save a row to `handicap_records` with the right
`source` value and update `profiles.handicap_index`; the screenshot path
uploads a file that appears in the `handicap-proofs` bucket; uploading an image
with no handicap shows the failure message rather than saving a wrong number;
no screen or copy mentions syncing an account from another app.

---

## Prompt 5 — Profile screen with handicap display

```
Build the profile screen (reachable from the Play tab header or a profile icon
on Match).

- Show the user's avatar, display_name, city, home_course, bio, and current
  handicap_index in the display type style on a navy header.
- List the user's handicap_records newest first, each showing value, source,
  verified state, and date. Pair the verified state with a text label and an
  icon, never colour alone.
- Include an "Improve handicap" action that reopens the import flow from
  prompt 4, and an edit action for display_name, city, home_course, and bio.
- Show an empty state when there are no records yet.

Follow the accessibility-baseline skill.
```

**Done when:** the screen shows the values written in prompts 3 and 4; adding a
new record through the action updates both the list and the header index
without a manual reload; the empty state renders for a user with no records.

---

## Prompt 6 — Nearby player discovery query

```
Build location-based discovery. No swipe UI yet — this prompt is the query and
its data layer only.

- Request foreground location permission with expo-location on first use of the
  Match tab, with a clear explanation before the OS prompt. If permission is
  denied, fall back to the user's profiles.city and show an inline notice.
- Write a query, as a Postgres function or a typed Supabase RPC named
  get_nearby_players, that returns profiles within 50 kilometres of the caller
  whose handicap_index is within 5 strokes of the caller's, excluding the
  caller themself and anyone the caller has already swiped on. Order by
  distance ascending. Return distance in kilometres with each row. Limit 50.
- If the caller has no handicap_index, return an empty list and let the UI
  prompt them to add one.

Follow the bolt-build-discipline skill: no stub data, prove the query works.
```

**Done when:** calling the RPC from a test screen returns nearby profiles
within 50 km sorted by distance; a profile 100 km away is excluded; a profile
with a handicap more than 5 strokes away is excluded; a user already swiped on
does not reappear; an empty list is what a user with no handicap gets.

---

## Prompt 7 — Swipe-to-match engine

```
Build the Match tab swipe interface on top of get_nearby_players.

- A card stack showing one candidate at a time: avatar, display_name, age-less
  profile (no age field), city, handicap_index, distance, and a one-line bio.
- Swipe right to like, left to pass, plus two visible buttons with accessible
  labels for the same actions so the feature is usable without gestures. Show
  the yellow accent on the like action.
- Each gesture writes a row to swipes. When a like creates a reciprocal pair,
  insert one row into matches with a unique unordered pair and show a "It's a
  match" confirmation with the matched player's name.
- Show empty, loading, and end-of-stack states. Announce match creation to
  screen readers.
- Follow the accessibility-baseline skill, including a full keyboard/assistive
  path equivalent to the swipe gestures.
```

**Done when:** swiping or tapping like/pass writes the correct `swipes` row;
liking a player who has already liked the user creates exactly one `matches`
row and shows the confirmation; swiping the same pair twice does not create
duplicate rows; the end-of-stack state appears when candidates run out.

---

## Prompt 8 — Matches list and chat

```
Build the Play tab's matches list and realtime chat.

- The Play tab lists the user's matches newest first: the other player's avatar
  and name, and the last message preview or "Say hello" if none.
- Opening a match shows a chat thread using Supabase realtime on messages,
  scrolled to the newest message, with a labelled input and send button.
  Messages a user sends appear immediately and without a manual refresh.
- Show an unread indicator driven by real data, not a hard-coded count.
- Show an empty state for a user with no matches yet.
- Follow the accessibility-baseline skill.
```

**Done when:** two signed-in accounts that have matched can exchange messages
and each sees the other's message appear without reloading; the matches list
shows the correct last-message preview; a user with no matches sees the empty
state.

---

## Prompt 9 — Open tee times and Hitchhike to join

```
Build the Hitchhike tab.

- A list of open tee times: course_name, formatted starts_at, host name and
  handicaps, players_needed, the handicap band, and distance from the user.
  Only status = 'open' and future starts_at are shown. Sort by starts_at.
- A "Post a tee time" form writing to tee_times: course_name, course_location
  from the user's current location, starts_at via a date-time picker,
  players_needed, handicap_band_min, handicap_band_max, notes. Validate
  starts_at is in the future and players_needed is 1–4.
- A "Hitchhike" action on each tee time that inserts a hitchhike_requests row
  for the current user and changes that card's button to a pending state. A
  user cannot request their own tee time.
- For a tee time the user hosts, show pending requests and accept or decline
  them; accepting increments the filled count and sets the tee time to 'filled'
  when players_needed is reached.
- Show empty and loading states.
- Follow the accessibility-baseline skill.
```

**Done when:** a posted tee time appears in another user's Hitchhike list; a
request creates a `hitchhike_requests` row and shows pending; the host can
accept, and the accepted tee time stops accepting requests once full; a past
tee time does not appear; a host cannot request their own tee time.

---

## Prompt 10 — Push notifications

```
Add push notifications with expo-notifications and Expo's push service.

- Request permission after the user has at least one match, not on launch, with
  a clear explanation first.
- Save each device's Expo push token to a push_tokens table (user_id, token,
  created_at) with row-level security limiting access to the owner.
- Send a push when: the user receives a new match, a new chat message, and an
  accepted or declined hitchhike request. Send these from Supabase Edge
  Functions or database webhooks.
- Tapping a match notification opens that chat; tapping a hitchhike
  notification opens the Hitchhike tab.
- Foreground notifications must respect prefers-reduced-motion equivalents:
  no animated banners that cannot be dismissed.

Follow the bolt-build-discipline skill and keep the change scoped to
notifications.
```

**Done when:** a second account liking the user produces a match notification
on the user's device; a new message produces a message notification; an
accepted request produces a notification; tapping a match notification opens
that chat thread; the token row appears in `push_tokens`.

---

## Prompt 11 — Polish, states, and accessibility pass

```
Do a pass over the whole app. Do not add new features — this prompt only fixes
what exists.

- Verify every screen against the accessibility-baseline skill: contrast
  ratios, visible focus, full keyboard/assistive paths, labelled inputs,
  semantic roles, and reduced-motion handling.
- Ensure every list, screen, and failure has an explicit empty, loading, and
  error state, and that errors are actionable rather than generic.
- Confirm the yellow accent is used only for primary actions and never as body
  text on light backgrounds.
- Confirm the same spacing, radii, and type tokens are used everywhere and no
  screen has hard-coded hex values.
```

**Done when:** every screen has three states (empty, loading, error) exercised;
no hard-coded colours remain; each interactive element has a visible focus
state; contrast passes for all text and meaningful icons.

---

## Prompt 12 — Seed data and end-to-end verification build

```
Prepare the app for a full end-to-end test. Do not change product behaviour.

- Add a seed script that creates eight demo profiles spread across two nearby
  cities with handicaps from 4 to 24, a handful of swipes that produce at least
  two mutual matches, and four open tee times with varied handicap bands. Write
  it so it can run against a development Supabase project only.
- Add a short VERIFY.md at the project root listing the end-to-end path: sign
  up, complete onboarding, import a handicap three ways, open Match, like a
  seeded player who has already liked you, confirm the match, send a message,
  open Hitchhike, join a tee time, and see it on the host's list.
- Produce a production build configuration for Expo (app.json with name
  Centorri Golf, slug centorri-golf, the brand colours as the app theme, and a
  splash screen in navy with the yellow accent).
```

**Done when:** the seed script runs and the demo data is visible in the app; a
tester following VERIFY.md completes every step without a dead end;
`npx expo start` and an Expo production build both succeed; app.json carries
the Centorri Golf name, slug, and brand colours.

---

## Definition of done for the brief

The build is complete when a tester who did not write the code can follow
`VERIFY.md` end to end on a physical device and every **Done when** check in
prompts 1 through 12 passes, with the two skills `bolt-build-discipline` and
`accessibility-baseline` switched on throughout.
