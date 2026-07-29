# Mongol Resurgence — Future Development & Extension Guide

> How to grow this mod without breaking what works. Written for the two of us
> (and any future contributor) after the 2026-07 fix-and-audit pass left the
> codebase green. Companion docs: `../CLAUDE.md` (standing rules — read it
> FIRST), `EU5-MODDING-GUIDE.md` (method), `MOD-DESIGN-IDEA.md` (as-built
> design), `TESTING-GUIDE.md` (in-game verification).

---

## 1. The non-negotiables (inherited, summarized)

Every extension below lives or dies by the same five rules. They are stated in
full in `CLAUDE.md`; this is the checklist form:

1. **Citation rule.** No field/effect/trigger enters a file without a vanilla
   or Prussian Destiny `file:line` using it in the same position and scope.
   Existence is not enough — check scope, magnitude, semantics.
2. **The harness is the gate.** `python3 tools/verify_mod.py` after every
   change; it auto-detects the reference tree on both machines. A red check
   blocks the change. If you add a new *class* of content, extend the harness
   so it covers that class too (it grew from 19 to 29 checks this way), and
   prove the new check on a known positive before believing its green.
3. **Silent failure is the default failure.** New folder names, loc keys,
   hint tags, gfx keys — verify each against vanilla before creating.
   ALL localisation goes in `main_menu/localization/english/MR_l_english.yml`.
4. **Humans get a choice; the AI gets a railroad.** Never force-convert,
   lock, or rob a player: conversions are offered (`mr_dominance.11` is the
   template), railroad wars are postponable (PD-103 shape), failsafes are
   `is_ai`-gated on both claimant and victim.
5. **Update the paper trail.** Any shipped change touches: the code, the loc,
   `TESTING-GUIDE.md` (a row the Windows tester can actually check),
   `CLAUDE.md` (if a rule or architecture fact changed), and
   `Debug-and-Test-Results.md` gets its dated summary.

## 2. The extension workflow (use for every idea in §4)

```
1. Design on paper: concept, historical anchor, WHO sees it (AI/human/both),
   WHEN (phase/window), WHAT it grants, and how it ENDS.
2. Grep vanilla + PD for every construct the design needs. No citation → no
   construct → redesign around what exists.
3. Reuse a proven template from THIS repo (see the cookbooks in §3) — the
   repo's own in-game-tested files are your closest working reference, but
   remember: MR code is evidence only where it has actually been seen working
   in game; cite vanilla/PD for anything new.
4. Implement smallest-first: one event before an event chain, one modifier
   before a mechanic.
5. Run the harness. Fix to green.
6. Add the TESTING-GUIDE row(s): what to look at, when, what "working" means.
7. Update CLAUDE.md / MOD-DESIGN-IDEA.md if architecture changed.
8. Windows machine: real game test, error.log sweep (TESTING-GUIDE Track 8).
```

## 3. Cookbooks — how to add each kind of thing

Concrete recipes. Each names the best in-repo template file to copy from.

### 3.1 A fired story event (situation beat)
- Template: `mr_dominance.135` ("The Four Corners") — condition-triggered
  beat; or `mr_dominance.121` — momentum-timed beat.
- Steps: event block in the right namespace file → firing block in the
  situation's `on_monthly` (one-shot global `mr_beat_X_fired`, removed in
  `on_ended`) → loc `title/desc/a` → harness → TESTING-GUIDE row.
- Traps: `fire_only_once` + a one-shot global is the standard double guard;
  fire with `trigger_event_non_silently` for visible beats.

### 3.2 A dated historical event (DHE)
- Template: `mr_history.6` (two-sided: also fires a mirror event) or
  `mr_dominance_dhe.11` (flavour boon).
- Steps: `dynamic_historical_event { tag from to monthly_chance }` — chance
  is a PERCENT, `100` = fires the month the window opens and the trigger
  passes. Add a `<ns>.<id>.entry` loc key (terse headline) — the DHE
  timeline shows it. Multiple `tag =` lines are legal; if the window can
  outlive the MGE proclamation, list BOTH `tag = MGO` and `tag = MGE`, and
  never reference `c:MGO` in the effects (use `root`).
- Traps: date it to the real year; the mod's convention is "fires ON its
  historical date", not "sometime in a 30-year window".

### 3.3 A reward modifier
- Template: the EVENT-SPECIFIC REWARDS section of
  `main_menu/common/static_modifiers/MR_modifiers.txt`.
- Rules: every type must exist in `main_menu/common/modifier_type_definitions/`
  (the harness does NOT check this — grep it yourself); flavour events grant
  their OWN modifier, never a phase buff; loc keys
  `STATIC_MODIFIER_NAME_/DESC_<key>`; the harness flags orphans, so wire it
  the same commit you define it.

### 3.4 A game rule
- Template: `MR_mongol_buff_rule` in `main_menu/common/game_rules/MR_game_rules.txt`.
- Steps: rule block (options carry `flag = general_rule`) → loc `rule_<key>`,
  `setting_<option>`, `setting_<option>_desc` → every consumer checks
  `has_game_rule = <option>` — and EVERY option must have a code path
  (a tier without a branch silently kills the mechanic; the old
  buff-disabled pacing hole was exactly this).

### 3.5 A casus belli + wargoal
- Template: `cb_MR_westward_advance` + `MR_war_goal_westward_advance`.
- The COVERAGE RULE is the whole game: `allowed_locations` must cover every
  location any end trigger reachable through this CB demands. Region links
  (`scope:location.region`) and area links (`scope:location.area`,
  vanilla cite crusade_cb.txt:25) both work. Grant from situation
  `on_start` with `years` covering the full phase window; re-grant in later
  phases (grants expire).

### 3.6 A new situation
- Template: `mr_chahar_reunification` (small, complete) — then
  `MR_mongol_imperial.txt` for a railroad-bearing one.
- Checklist: `can_start` / `visible` / `can_end` (goal OR time-expiry!) /
  `on_start` / `on_monthly` / `on_ending` (branch on the GOAL trigger; set
  terminals directly) / `on_ended` (variable cleanup) / `tooltip` /
  `map_color` — plus a `gui/panels/situation/<key>.gui`, a
  `hint_tag` definition + loc, `<key>`/`<key>_desc` loc, and end-requirement
  tooltips in the `[ShowLocationName(...)]`/`[locations|e]` style.
- Trap: if any effect in `on_ending` can invalidate the end trigger's own
  preconditions (tag switch!), the phase-complete global must be set in
  `on_ending`'s success branch, not re-derived in `on_ended` — this was a
  real bug at the MGE proclamation.

### 3.6b A situation panel action (a button on the panel)
Template: `in_game/common/generic_actions/MR_actions.txt`; vanilla original
`generic_actions/rise_of_timur.txt:288` (`rot_select_core_region`).
1. `type = situation` + a `select_trigger { looking_for_a = situation }` whose
   `visible` names your situation(s) — that binding is what puts the button on
   the panel; the situation file itself needs no changes.
2. Further `select_trigger`s collect targets (`looking_for_a = region`, with
   `column = { data = … }` for the picker table).
3. `price = price:<key>` needs a `common/prices/` entry (`scaled_gold` etc.,
   vocabulary in that folder's `readme.txt`).
4. Loc: `<action_key>`, `_desc`, one key per `select_trigger` `name`, the
   `none_available_msg_key`, every `custom_tooltip` you cite, and the price
   key. The `PERFORM_*_ACTION_*` message keys are optional.
5. Gate the *effect* on whatever should make it lapse (ours: the Great Khan
   character modifier) and undo it in the situation's `on_monthly` when the
   gate stops being true.

### 3.6c A "the world reacts" event set
Template: `mr_dominance.20-28`; vanilla-adjacent original
`PD_events.txt:425/439/1126`.
Three recipients per phase — spectators (a stake, but no goal land), victims
(goal land), and the claimant itself for the alliance break
(`every_related_country = { type = alliance }` + `remove_relation`). Two rules
learned the hard way: exclude anyone who already got the phase's main opening
event so nobody is told twice, and fire the claimant's alliance break at the
moment the claimant EXISTS — for Phase 1 that is Beat 104, not `on_start`.

### 3.7 A GUI element
- Template blocks: `mongol_resurgence.gui` (two-country header),
  `mongol_imperial.gui` (one-country header + progressbar card).
- Rules: `one_country_header_template` exposes `CountryContext` +
  `character_portrait_anchor`; the two-country template exposes
  `First/SecondCountryContext` + `first_/second_character_portrait_anchor`.
  A blockoverride naming a block the template lacks is silently dropped.
  Widgets: `text_single`, `text_multi`, `progressbar` with `value`/`min`/
  `max`. The harness does NOT parse gui files beyond nothing — check brace
  balance yourself (python one-liner in TESTING-GUIDE's spirit).

## 4. Expansion tracks

Ordered roughly by value-for-effort. Each lists: concept, anchor, what to
touch, proven building blocks, pitfalls, size (S/M/L/XL).

**APPROVED PROGRAM (user, 2026-07-30 — "hepsini yapalım"):** T1, T2, T5
plus the five new tracks T11-T15 below are all green-lit. Build order:
T1 (via the new tools/new_flavor.py scaffold generator, ported from the
1066 sister project the same day) → T11 Tumu-mirror → T2 + T12 Jade
Seal → T13/T14 texture packs → T5 → T15 balance instrument. HARD GATE:
nothing touches mr_dominance.120/.130 (T2's files) until the
2026-07-30 six-lens audit report has been reviewed — its lens 4 examines
exactly those files. New tracks:

### T11 — "The Emperor in the Camp" (Tumu-mirror flagship DHE, S-M)
1449 inverted: at war with the Chinese empire and decisively winning →
capture the emperor; ransom / puppet / release triple choice. Anchor:
Esen Taishi capturing the Zhengtong Emperor at Tumu. Counterplay beat
against a dominant Great Chen (the 2026-07-29 observer's finding).
Pitfall: no imprisonment exists in EU5 — build it as modifier+event on
the enemy ruler (the proven construction class), and cite a war-score
trigger before designing around one.

### T12 — The Jade Seal / Borjigin legitimacy (M, pairs with T2)
"Who holds the Seal of the Great Khan": a variable-borne token granting
a legitimacy modifier; non-Borjigin usurpation (the Esen fate — dead
within two years) as the cautionary arc; rival khans contest the seal.

### T13 — Zud, the killing winter (S, repeatable texture)
Herd die-off event (slaughter early / raid south / appeal to the sky) —
the real motor of steppe eruptions. Small lasting choices, repeatable
(no fire_only_once; verify the random-pool route if pulsed).

### T14 — Ortoq partnerships and the paiza (S-M, economy texture)
Extends the Silk Road DHE: grant paiza to merchant houses → income now,
corruption events later. Anchor: the ortoq system of the Yuan.

### T15 — Power-ratio catch-up (S, balance instrument)
Replace/augment the flat observer-run buffs: the AI catch-up events
measure the claimant's army against the strongest China-culture power
and scale their grant by the gap — self-adjusting instead of
hand-tuned. Requires a cited army-size comparison trigger first.

### T1 — Deepen the existing arc with content (S–M each, do these first)
The skeleton is done; flesh is cheap now. Concrete, dated, cite-able ideas:
- **"The Return of Bayan"** (P1, ~1370): the last great Yuan chancellor
  reaches the steppe — create a court character (create_character, no
  set_new_ruler) with an admin trait. Anchor: Toghon Temür's exile court.
- **"The Ming Embassy"** (P1/P2 boundary): Ming demands tribute; choice —
  defiance (prestige, worse Ming relations later) vs feigned submission
  (gold, delay). Anchor: early Ming-Northern Yuan diplomacy, 1370s.
- **"Timur and the Khan"** (P2, fires if TIM exists and MGO borders it):
  the two conquerors circle each other — choice event mirroring
  `mr_history.5`'s Tokhtamysh dilemma. Anchor: Timur's steppe diplomacy.
- **"The Black Death Rides the Yam"** (any phase; READ-ONLY hook on
  vanilla's black_death situation state, same pattern as the Tumu hook —
  verify a persistent signal exists first, exactly like
  `mr_vanilla_tumu_crisis_active` did): plague reaches the horde via the
  trade routes it reopened. Anchor: 1340s plague vector debate — needs a
  LATER window here (fires only if the situation is still live).
- **"The Karakorum Debate"** (P3): a court disputation between faiths —
  flavor choice, small unique modifiers per pick. Anchor: Möngke's 1254
  inter-religious debate, revived by his heirs.
- **More rival-khan texture**: the P1 `mr_first_rival` scope is saved and
  scored monthly but has zero events of its own — a 2-3 event mini-arc
  ("The Rival Kurultai", "Defectors from the Rival Banner") firing for
  `scope:mr_first_rival` would make the race legible from both sides.

### T2 — The Kurultai succession mechanic (M)
Between phases, the throne passes (Adai, Altan). Turn each succession into a
CHOICE for humans: a kurultai event chain where the player picks the new
khan's emphasis — warlord (mil traits), lawgiver (adm), silk-road prince
(dip) — three options, each running the proven create+enthrone shape with a
different trait set; AI takes the historical pick via `historical_option`.
- Touch: `mr_dominance.120`/`.130` (split into offer → resolution events).
- Blocks: everything already exists (create_character multi-trait, strip-
  then-enthrone). Pitfall: keep `ruler ?= { remove_character_modifier }` in
  EVERY branch; keep exactly one enthronement per phase.

### T3 — Religion identity arc (M, care needed)
Tengri → Buddhism (historical) or defiant Tengri or Islam (Golden Horde
path) as a P2/P3 identity choice with small lasting modifiers.
- HARD RULE from CLAUDE.md: vanilla already implements Altan Khan's
  conversion (`buddhism_events.13`) — do NOT duplicate it. Hook read-only
  (has the claimant converted? `religion = religion:x` checks) and react,
  the way Chahar reacts to Tumu.
- Pitfall: `change_religion` is proven (mr_history.3), but pop-level
  conversion effects are NOT yet cited — grep before designing around them.

### T4 — Tributary empire layer (M–L)
The failsafes already create tributaries; nothing talks about them.
- Ideas: yearly "Tribute of the Five Snouts" pulse event for the claimant
  scaled by subject count; disloyal-tributary flavor; a "Raise the Tumens"
  call-tributaries-to-war event.
- Touch: `on_action` yearly pulse (the `mr_claimant_*_pulse` template) +
  events. Blocks: `make_subject_of`, `cancel_subject`, `subject_loyalty`
  modifier type — all proven. Pitfall: iterating subjects needs a cited
  iterator (`every_subject_country`? — verify in vanilla FIRST; it is not
  yet in this mod's proven set).
- The `docs/Subject type modding` wiki PDF covers custom subject types
  (a "Horde Tributary" with unique terms) — that is the L-sized version.

### T5 — Post-failure content: "The Shattered Steppe" (M)
`mr_railroad_failed` currently just ends the story. The late-steppe
situations cover 1604+; the 1420–1600 failure window is empty.
- Idea: one situation (or DHE chain) where the failed claimant fragments —
  mirrors of the real Northern Yuan's Oirat century: Esen's regency,
  the Dayan Khan reunification attempt (a second, harder chance arc).
- Blocks: `has_global_variable = mr_railroad_failed` as the gate; the
  chahar file is the perfect template (starts from fragmentation).
- Pitfall: keep it OUT of the success timeline — every trigger gated on
  the failed global, so the two stories can never run at once.

### T6 — A fourth frontier (L)
The user floated this during the P3 redesign. Two candidates:
- **The Middle Eastern Ilkhanate war** (1550–1650 depth): P3 already
  demands Persia; a dedicated situation could add Mamluk/Ottoman
  reactions, a Baghdad-restoration arc, Köse Dağ II flavor. Touch: new
  situation + CB coverage already exists (westward CB spans the theatre).
- **The Indian track** (TIM/DLH/Mughal collision): mr_history.8-9 already
  seed it. A situation where the empire and the Timurid-Mughal line race
  for Hindustan. Touch: new regions in CB coverage (verify
  `india`-side region keys in definitions.txt first — NOT yet in the
  proven set).
- Pitfall: both need the full situation checklist (§3.6) including GUI —
  budget accordingly.

### T7 — More knobs (S)
- Per-phase buff granularity (separate buff rule per phase) — pure
  game_rules + loc work, template exists.
- "Khan succession: choice vs historical" rule to gate T2.
- A "late start" compatibility rule (campaign started after 1368? P1
  can_start already handles dates, but a 1444-style bookmark start would
  need the birth failsafe date generalized).

### T8 — GUI upgrades (M)
- A P3 goal CHECKLIST card: ten `text_single` rows, each `visible` bound to
  a per-goal situation variable (set them in the same monthly block that
  computes `MR_dominance_score` — e.g. `MR_goal_tabriz = 1`). All widgets
  proven; the work is wiring ten variables + ten loc keys.
- Portrait polish: the score card could show the current Great Khan via
  `Country.GetGovernment.GetRulerOrRegent` datacontext (the template chain
  already resolves it — cite `country_header.gui:172`).

### T9 — Localization languages (S per language)
Copy `MR_l_english.yml` to `main_menu/localization/<lang>/MR_l_<lang>.yml`
with the `l_<lang>:` header — file NAME and header must both change.
Engine-derived keys stay identical. Do English LAST before release (it is
the fallback everyone sees).

### T10 — Release engineering (S–M)
- `.metadata/metadata.json`: bump `version` per release; `supported_game_version`
  per game patch. Add `thumbnail.png` (512², <1MB) before Workshop.
- **Vanilla patch upgrade checklist**: re-run the harness (it greps live
  vanilla, so definitions/units/advances drift is caught free); re-derive
  the situation field closed-set (`EU5-MODDING-GUIDE.md` §3); re-check the
  three read-only hooks (lost_emperor, black_death state if T1 lands,
  buddhism_events if T3 lands) — vanilla renames break silent hooks
  silently.
- **Save compatibility**: mid-save updates are safe for loc/modifier
  numbers; NOT safe for renamed globals/variables (old saves carry old
  names) or removed events that a save has pending. Rule: rename nothing
  that a save stores; add, don't mutate.
- **Coexistence with The Prussian Destiny**: no shared namespaces, keys or
  files — the mods are compatible by construction. Keep prefixes disjoint
  (`MR_`/`mr_` vs `PD_`/`pd_`) and this stays true.

## 5. Known debt & watch items (start here after each game test)

Carried from the 2026-07-23 and 2026-07-26 audit rounds; none block release,
all are documented in TESTING-GUIDE Track 8 / the tracks above:
1. RESOLVED 27.07: `Unknown formatting tag 'l'` is **vanilla-side, confirmed in
   game** — it appears with vanilla situation panels too. Not our text; nothing
   to fix. Original investigation kept below for the method.
1z. (historical) `Unknown formatting tag 'l'` log spam — believed vanilla-side; watch-only.
   Re-verified 2026-07-26 at byte level: the mod's `.yml` and `.gui` files
   contain no `#l`, no `|l]` and no unrecognised `#` tag at all, and none of
   the six `.gui` files carries a BOM (they match vanilla). **Decisive test:**
   open a vanilla one-country situation panel (Rise of the Ottomans, Rise of
   Timur) in the same build and read the log — if the line appears there too,
   close the item.
1b. `Government.*` "No context supplied" spam when the **P2/P3** panels are
   open (P1 is clean). Leading hypothesis: `one_country_header_template`
   declares `block "CountryContext"` **twice** — once for the portrait, once
   carrying the default `datacontext = "[Country.GetGovernment]"` for the
   ruler-title strip — and a single `blockoverride` replaces both, so the
   Government context never gets pushed. This would make it a vanilla template
   issue (every vanilla one-country panel does the same thing), which the
   author's observation that vanilla does *not* spam contradicts, so it is
   unconfirmed. Two discriminating tests: (a) open a vanilla one-country
   panel; (b) point our `CountryContext` at a hard-coded live tag instead of
   `GetVariable('mr_leading_country')` and see whether the spam stops.
   **Risk-free fix regardless of which theory is right:** switch P2/P3 to
   `two_countries_header_template` with the second portrait hidden — P1 uses
   that template and has never spammed.
2. P3 railroad suspect #1 if its wars never fire:
   `scope:mr_dom_claimant.offensive_alliance_strength`
   (`MR_mongol_dominance.txt`, find-target). Fallback plan: two fixed-tag
   branches.
3. The progressbar combo (`using = morale_progressbar_bar` + `min/max` +
   `value`) — each element vanilla-cited, the exact combination not; if the
   bar renders oddly, drop the mixin or the min/max pair.
4. `while count = 5` building stacks at one location (kurultai/armory) —
   PD-proven shape, but EU5 building-slot semantics are unverified; if the
   game caps construction, the surplus decrees are silently wasted (benign).
5. Design corner: a player who manually forms MGE during PHASE 1 (needs all
   nine formable seats by 1420 — practically impossible) fails the railroad
   by timeout. Guarded, error-free, accepted.
6. Cosmetic: the P3 panel rival can be the claimant's own tributary. (The
   Phase 1 version of this — MGO appearing as *both* claimant and rival — was
   fixed on 2026-07-26 by re-picking the rival monthly; Phase 3 picks its
   theatre rival once at `on_start` and could get the same treatment.)
7. Vanilla's "anything you conquer in your core region is auto-cored" rider
   lives in `on_location_changed_owner`, an on_action defined with an `effect`
   block. We reimplemented it in the situations' `on_monthly` instead, because
   redefining that on_action name in a mod would replace the vanilla block
   wholesale. If Paradox ever documents additive on_action merging, the
   monthly loop can be retired.
8. `MGE` is localised "Great Mongol Empire" by author decision (2026-07-26).
   No vanilla country name contains "Empire" — this is the exact string that
   produces the `MGE has the name 'empire'` load warning, because rank titles
   compose as "The Great <name> Empire". It is cosmetic: the map label is
   built from `rank_empire_horde_prefix` + `MGE_ADJ` + `rank_empire_horde`
   ("Great Mongol Horde") and never uses this name. Drop-in alternative if the
   warning becomes annoying: "Great Mongol State", the literal English of Yeke
   Mongol Ulus, which carries no trigger word.
9. RESOLVED 27.07, as unfixable. The engine reads only
   `main_menu/gui/messagetypes.txt`; a differently-named mod file there is
   ignored (our `MR_messagetypes.txt` was deleted, and a popular published mod
   ships an equally dead one). Adding `PERFORM_MR_select_core_region_ACTION`
   would mean shipping that exact filename and replacing vanilla's 1348
   entries. Accepted: one `message_handler.cpp:421` line when the action
   fires, and no popup. The action itself works.
10. `modifier_type.cpp:1294 Missing Icon for MR_select_core_region_price_cost_modifier`.
    Modifier-type icons are resolved by filename from
    `main_menu/gfx/interface/icons/modifier_types/<key>.dds`; there is no
    `icon` field to set. Vanilla ships one for
    `rot_select_core_region_price_cost_modifier` but NOT for
    `rot_plan_invasion_price_cost_modifier`, so the line is tolerated even
    upstream. Fixable any time by dropping a 5-6 KB .dds at that path.

## 5b. Techniques worth stealing from other mods

### Read from *Legacy of Timur: An Age of Gunpowder* (a railroad mod), 2026-07-26

Analysis only — nothing copied.

| Thing | Why it matters | Status here |
|---|---|---|
| `scripted_geography` | Name goal territory once instead of 259 times | **Adopted 27.07** |
| `top_owner` on a location | One link to the top of the ownership chain | **Adopted 27.07** |
| `auto_modifiers` (`potential_trigger` + `scales_with`) | A modifier that applies itself while a condition holds — no grant/remove bookkeeping. 149 vanilla definitions | Not adopted; would replace much of our modifier plumbing |
| Custom `peace_treaties` with `ai_desire` | Hands the goal territory over **at the peace table** instead of by decree. A far better railroad primitive than a failsafe | Not adopted; strong candidate for the overhaul |
| `area_preferences` (`preference_type = conquest`) | Steers AI appetite toward a theatre without scripting a single war. Also `TRY_REPLACE:` to override a vanilla entry | Not adopted |
| `scripted_effects` | The DRY tool we never used | Not adopted |
| `disasters` | Country-scope crisis with an inline `modifier` block and a 0-100 meter whose extremes end it three different ways | Not used at all |
| on_action family: `monthly_country_pulse`, `biyearly_country_pulse`, `on_winning_war`, `on_ending_war` (`scope:winner`/`loser`/`war`), weighted `random_events` | Event-driven instead of monthly polling | Only `yearly_country_pulse` used |
| `situation:X.var:Y` read from outside; variables on the `scope:war` object | One-shot guards that die with the war instead of polluting globals | Not adopted |

### Read from *Bronze Era* (a published TOTAL CONVERSION), 2026-07-27

Different animal from a railroad mod: it moves the whole game to the Late
Bronze Age. The findings below are the ones that decide how the planned
overhaul gets built.

**A total conversion does NOT repaint the map.** `in_game/map_data/
location_templates.txt` is a VANILLA file — 28,573 lines, one per location,
setting `topography`, `vegetation`, `climate`, `religion`, `culture`,
`raw_material`, `natural_harbor_suitability`. Bronze Era ships its own 28,575
line version. So you keep vanilla's location geometry and rewrite what every
location *is*. Locations meant to be wilderness simply get terrain and no
culture/religion, which is why most of their map is empty.
*Cost:* it is a whole-file override, so every patch that touches
location_templates.txt has to be re-merged. Budget for that.
*Consequence:* a location-painting tool is for authoring new location SHAPES —
a much bigger job that this mod did not need.

**Move the timeframe with `common/defines`, and keep the engine on POSITIVE
years.** They override `START_DATE`/`END_DATE` and remap the *display*:
internal year 1 = 1209 BC, `displayed BC year = 1210 - internal year`, with
`bronze_display_year` / `bronze_display_ad_year` country variables driving the
topbar while the real engine date stays visible as a secondary line. Their
stated reason, worth quoting: vanilla "timers, cooldowns, AI scheduling,
situations, institutions and saves assume a normal positive calendar in
several places". Ages are remapped onto the same internal scale. For a CK3-era
start (867/1066/1178) the dates are already positive, but the technique —
engine date internal, historical date presentational — is the one to copy for
any chronology shift.

**Country tags are not necessarily three letters.** Vanilla has 2217 tags and
every one is exactly 3. Bronze Era has 531: **471 five-letter, 47 four-letter,
13 three-letter** (`ALASI`, `AMURU`, `ASYRI`…), and they are used live in
script (`c:ALASI`, `tag = ASYRI`). So "3 letters" is a vanilla CONVENTION, not
an engine limit — which matters when an overhaul needs hundreds of new tags and
3-letter uniqueness becomes painful. NOT verified in a running game by us;
confirm before relying on it. Our own harness still treats 4+ as a finding,
correctly, because this mod uses vanilla tags.

**48 `common/` folders we have never touched.** They use: advances, age,
auto_modifiers, biases, building_categories, building_types, country_ranks,
cultures, culture_groups, customizable_localization, defines, diseases,
estate_privileges, formable_countries, gods, goods, goods_demand, holy_sites,
institution, international_organizations (+3 sub-systems), languages,
language_families, laws, levies, modifiers, peace_treaties,
production_methods, religions, religion_groups, religious_aspects/factions/
figures/focuses/schools, road_types, script_values, scripted_effects,
scripted_guis, subject_types, unit_types/categories/abilities/
formation_preference, historical_scores. That list IS the shape of the work.

**`scripted_guis`** — only 2 in vanilla and 2 here, for bespoke interactive
panels (ruins exploration, a Trojan War phase). Rare but available.

**They keep design docs in `docs/*.md` too** — 1028 lines on starting
technologies, 581 on their city-prestige system. Same discipline as this repo.

**COUNTER-EXAMPLE — do not copy their localisation.** They ship THREE loc
trees: a root-level `localization/` (26 files; vanilla has no such folder, so
those are almost certainly dead), `in_game/localization/` (13) and
`main_menu/localization/` (61). **25 filenames appear in more than one tree and
20 of those have DIVERGENT content** — `Bronze_city_razing_l_english.yml` is
32 KB in one and 9 KB in another. Whichever loads last wins and the other's
keys vanish. This is exactly the shadowing bug that cost this repo a debugging
session and produced our hard rule: **one tree, `main_menu/localization/`,
and never two files with the same name.** A published mod doing it wrong is
not a licence to.

**Counter-lesson:** that mod uses `any_country_in_hierarchy` /
`every_country_in_hierarchy` in 14 places and vanilla has **zero** uses of
either, anywhere. Popular and published is not attested. The citation rule
holds regardless of the source.

## 5c. The community toolchain, and three mechanisms we did not know

Surveyed 2026-07-27. Claims from third-party docs are marked as such; anything
labelled **verified** was checked against the vanilla files here.

### Tools other people already built
| Tool | What it is | Worth it? |
|---|---|---|
| **CWTools** (`tboby.cwtools-vscode`) | Paradox script language server for VS Code — live syntax and reference checking in the editor | **Yes, install first.** Bronze Era recommends it in `.vscode/extensions.json`. Catches in the editor what our harness catches after the fact |
| **EU5 ModHelper** (github.com/sinjako/EU5-Modhelper) | Browser tool, plain JS, no install. Browses 30+ game categories, edits values, stages changes, generates mod skeletons, handles UTF-8 BOM and `REPLACE:` syntax | Useful for bulk value edits and for seeing what a category contains. No map editing, no validation |
| **Community Mod Framework** (github.com/Europa-Universalis-5-Modding-Co-op) | Shared compatibility layer: a common in-game settings menu, dismissable alerts, `cmf_is_mod_active` mod-detection trigger, post-lobby/load hooks, country-transfer hook, a mod action log, and `cmf_suppress` for warnings. Declared as a dependency in `metadata.json` | Consider for the overhaul if coexisting with other mods matters. There is a wiki PDF for it already in `docs/` |

### Three engine mechanisms worth chasing

**1. `script_docs` and `dump_data_types` (console).** Reported to make the game
emit its own trigger/effect documentation and GUI data-type documentation.
**If true this is the biggest single workflow change available to us**: instead
of grepping vanilla to decide whether a construct exists and what scope it
takes, we would have the engine's own list. That is precisely the class of bug
that cost this repo a round on 2026-07-27 (`is_in_scripted_geography` is a
LOCATION trigger; we used it in country scope in 120 places). **Run these two
commands once and keep the output in the repo.** Not yet verified.

**2. Database operation prefixes.** A key can be written
`TRY_REPLACE:existing_key = { … }` to modify a vanilla database entry instead of
replacing the file. **Verified:** zero uses anywhere in vanilla (it never needs
them), but a published mod uses `REPLACE:` 12×, `TRY_REPLACE:` 9× and `INJECT:`
1×. Third-party docs give the conflict-resolution order as
`INJECT_OR_CREATE → REPLACE_OR_CREATE → TRY_INJECT → TRY_REPLACE → INJECT →
REPLACE`, resolved by operation type first and filename second.
**Why we care:** this may be the way out of whole-file overrides — the problem
that makes `location_templates.txt` patch-fragile and makes
`gui/messagetypes.txt` untouchable. Worth an experiment before the overhaul.

**3. `replace_paths` in `metadata.json` → `game_custom_data`.** Declares vanilla
paths the game should ignore entirely. **Verified present** in Bronze Era's
metadata, though they ship it empty. For a total conversion this is how you drop
all vanilla countries or setup wholesale rather than fighting them entry by
entry.

### And one fact that fixed a live error here
Modifier icons are **declared**, not conventional: `main_menu/common/
modifier_icons/` (4912 vanilla entries), `<type> = { positive = "path.dds" }`,
and the path may borrow another modifier's art — vanilla does this itself. That
cleared `modifier_type.cpp:1294` with no art authored. Full entry in
`EU5-ERROR-DECODER.md`.

## 5d. How another Claude-driven EU5 project is organised

`HLJSXK/eu5-modding-project` (the "Standard of Living" mod, 1.3.11) is run with
Claude Code and has the most developed process of anything surveyed. Read
2026-07-27.

### The structure worth copying — it solves our CLAUDE.md bloat
Their `CLAUDE.md` is **140 lines and stays that way**, because it holds only
RULES. The knowledge lives elsewhere and is COMPILED:

```
CLAUDE.md                     rules only, stable, ~140 lines
docs/knowledge/anti_patterns.yaml   structured: one entry per discovered trap
docs/knowledge/valid_enums.yaml     structured: enum whitelists
docs/knowledge/PROJECT_OVERVIEW.md  what exists NOW (not a changelog)
docs/knowledge/BRIEF.md             AUTO-GENERATED from the three above
scripts/gen_brief.py                the generator
```

`CLAUDE.md` says: *"For any non-trivial task, read `docs/knowledge/BRIEF.md`
first."* Ours is 438 lines and growing because rules and knowledge are fused.
**For the overhaul, split them from day one.**

### Four rules of theirs that are sharper than ours
1. **3-Step Resolution + a FORBIDDEN list.** Step 1 is "direct edit, only if
   100% certain"; then official defines; then vanilla/mod source. And a list of
   categories where **Step 1 is banned outright** — blockoverride block names,
   custom_tooltip key formats, GUI template structure, any enum, any modifier
   name, any scripted trigger not defined in the mod, loc encoding, GUI
   expression syntax. Our citation rule says "cite everything"; naming the
   categories where memory is *forbidden* is more enforceable.
2. **Declarative Verification.** Before writing in those categories, emit
   `**Verification** — Step [2/3], Reference: file:line, Quote: "..."`. If not
   found: `FAILED. Asking user.` **Then stop.** It moves the citation from a
   code comment into the transcript, where the user can audit it live.
3. **Knowledge Capture, automatic.** Triggered by using Step 2/3 OR by fixing a
   runtime engine error. When triggered you MUST update the yaml + the workflow
   table + the knowledge base + regenerate BRIEF — *"in the same response as
   the fix, before the task is marked complete. Do not wait for the user to
   ask."* This is the formalised version of what we do ad hoc.
4. **Bug Fix Rule.** A bug is fixed by correcting syntax, never by deleting the
   feature — removal only if both verification steps fail AND the user is told.
   A good guard against quietly narrowing scope.

### A tool we should steal outright
`error_log_filter.py` + `vanilla_error_filters.txt` (663 lines of known vanilla
noise) watches `error.log` and strips everything vanilla already emits, leaving
only your mod's errors. We burned time across three sessions on
`Unknown formatting tag 'l'` before confirming it was vanilla's. A filter list
answers that on day one. Their filter format:

```
contains:<text>          exact:<full entry>          regex:<python re>
```

### Verified against vanilla — and one of their claims is WRONG
This is the point of the citation rule, and it applies to good sources too.

| Their claim | Verdict |
|---|---|
| `location_rank` has **only 3** values: rural_settlement, town, city | **WRONG.** Vanilla uses four, and the missing one is the *second* most common: `city` 356, **`megalopolis` 279**, `town` 244, `rural_settlement` 121 |
| Icons can be drawn inline as `@icon_name!` from `main_menu/gui/shared/font_icons.gui` | **CONFIRMED** — 64 KB, 364 `texticon` entries. A whole icon mechanism we have never used; cheaper than a widget |
| Location `auto_modifiers` are non-functional; use `static_modifiers` | **PLAUSIBLE** — vanilla's auto_modifiers declare only admiral, dynasty, general, internationalorganization categories; no location, no country |
| Loc `.yml` must be UTF-8 **BOM** | Confirmed, matches our own rule |
| No `mean_time_to_happen` in EU5 | Confirmed, matches ours |
| Float literals read to 5 decimal places | Not verified |

### What their `reference_official_defines/` actually contains
Worth knowing precisely, because it looks like more than it is.

- `docs/data_types_*.txt` (2.9 MB total) — this is **`dump_data_types` output**:
  GUI/promote data types with return types, not script triggers. Useful for GUI
  work, but **it did not cover our case**: `HasRulerOrRegent`,
  `GetRulerOrRegent` and `GetRegencyInfo` — the three methods behind our
  situation-panel context bug — appear **zero** times.
- `changes_script_docs.md` (31 KB) — the 1.2 → 1.3 **diff** of the script
  documentation, not the documentation itself. Its structure is the useful
  part, because it tells us what the full `script_docs` output looks like:
  sections for **Scopes / Effects / Triggers / Event Targets / Iterators /
  On Actions / Modifiers**, and the header note confirms each element's entry
  carries its **scopes**. That is the thing we actually want, and it is still
  only obtainable by running the console command.
- `types/*.txt` — per-database type definitions (building_types, casus_belli,
  laws, peace_treaties, unit_types, international_organizations, institutions).

**Conclusion: still run `script_docs`.** The dump present here is the other
command's output and is only partially useful.

### One construct family found in that diff, worth remembering
`all_holy_sites_owned_by_or_below_of` — *"owned by the target country, its
subjects, **or its subjects' subjects**"*. So there is an `_or_below_of` naming
family for subject-chain questions, and vanilla's `conquistadors.txt` uses
`is_subject_or_below_of`. Next time the "whole realm" question comes up, look
for `*_or_below_of` before reaching for `top_overlord_or_this`.

## 6. Idea parking lot (unscoped one-liners)

Marco Polo-style traveler events on the restored Silk Road · a "Pax
Mongolica trade boom" scaling with market count · named historical generals
as recruitable characters (Arughtai, Esen as a RIVAL leader) · a Dzungar
PLAYABLE mini-railroad upgrading the existing situation · dynamic naming
(`mge_empire` government-form keys) for flavor titles · an achievements-like
hint chain using scriptable_hints · AI-only "comeback" buff when the
claimant loses Karakorum for 10+ years.

## 7. Definition of done (any extension)

- [ ] Every new construct carries a vanilla/PD citation (comment it in-file)
- [ ] `tools/verify_mod.py` fully green on BOTH machine layouts (29 checks)
- [ ] **A new invariant gets a new harness check, proven on a known positive**
      — break the fix, watch the check fail, restore. Two of the current
      checks exist because a manual review missed exactly what they catch
- [ ] Loc complete incl. engine-derived keys and DHE `.entry` keys
- [ ] Human-choice rule honored (no forced conversions/locks/thefts)
- [ ] TESTING-GUIDE row(s) added with dates and expected outcomes
- [ ] CLAUDE.md / MOD-DESIGN-IDEA.md updated if architecture moved
- [ ] Dated summary appended to Debug-and-Test-Results.md
- [ ] In-game test on the Windows machine, error.log swept (Track 8)
