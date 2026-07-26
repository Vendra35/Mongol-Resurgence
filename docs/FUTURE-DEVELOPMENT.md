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

Read from *Legacy of Timur: An Age of Gunpowder*, a large published railroad
mod, on 2026-07-26. Analysis only — nothing copied.

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

**Counter-lesson:** that mod uses `any_country_in_hierarchy` /
`every_country_in_hierarchy` in 14 places and vanilla has **zero** uses of
either, anywhere. Popular and published is not attested. The citation rule
holds regardless of the source.

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
