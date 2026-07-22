# CLAUDE.md — Mongol Resurgence (EU5 Mod)

## What this is
A finished, working mod for Europa Universalis V. Alternate history, tightly anchored
to the real timeline: *when the Yuan were driven from China in 1368, what if the Mongol
tribes had genuinely reunified and launched a new wave of conquest westward?* The
player (or AI) rides a three-phase "railroad" from steppe unification to a restored
Mongol Empire, alongside three standalone late-steppe situations covering what
actually happened historically.

Full design spec: `docs/MOD-DESIGN-IDEA.md`. How-to and methodology:
`docs/EU5-MODDING-GUIDE.md`. Historical audit record: `docs/AUDIT-2026-07-21.md`.

## REQUIRED SETUP on a new machine
The workflow depends on a read-only reference tree **one level above this repo**:

```
<parent>/
├── Mongol Resurgence/       ← this repo (write here only)
├── The Prussian Destiny/      ← READ ONLY, a working, tested reference mod
└── EU5-Vanilla/               ← READ ONLY, junction → E:\SteamLibrary\steamapps\common\Europa Universalis V
    └── game/                   ← full vanilla install (~51k files)
```

On this machine these are two separate junctions (EU5-Vanilla → the Steam install, 
The Prussian Destiny → its own mod folder). 
If either is missing, recreate it before doing any mod work — **every rule below depends
on being able to grep vanilla**. Key vanilla paths used constantly:
`game/in_game/common/situations/readme.txt` (authoritative situation docs),
`game/in_game/map_data/definitions.txt` (region → area → province → location
hierarchy), `game/in_game/setup/countries/` (tags), `game/main_menu/common/`
(script values, modifier types, game rules).

## Architecture (as built)
Six situations, four namespaces, one state machine:

| Situation key | File | Window | Ends when |
|---|---|---|---|
| `mongol_resurgence` | MR_mongol_resurgence.txt | 1368–1420 | MGO holds Karakorum + the Gobi |
| `mongol_imperial` | MR_mongol_imperial.txt | 1420–1550 | MGO holds Samarkand + Dadu + Transoxiana |
| `mongol_dominance` | MR_mongol_dominance.txt | 1550–1650 | claimant holds MGE_f's nine locations → forms MGE |
| `mr_chahar_reunification` | MR_late_steppe.txt | 1604–1634 | one banner over the heartland |
| `mr_torghut_migration` | MR_late_steppe.txt | 1616–1630 | a horde reaches the Volga (post-trek) |
| `mr_dzungar_khanate` | MR_late_steppe.txt | 1634–1650 | consolidated + Dzungaria/Tarim/Zhetysu |

- Event namespaces: `mr_dominance` (lifecycle + hidden AI events 995–999),
  `mr_imperial` (campaign arc), `mr_history` (historical DHEs, 1335–1530),
  `mr_dominance_dhe` (horde-institutions DHEs), `mr_steppe` (late-steppe).
- Phase chaining via globals: `mr_phase_one_complete` → `mr_phase_two_complete` →
  `mr_railroad_complete`, with `mr_railroad_failed` set on **every** failure path
  (on_ending sets terminals directly; events set them redundantly).
- Every situation `can_end`s on **goal OR time expiry**; `on_ending` branches on the
  goal trigger, never on side-signals.
- AI railroad (Phase 1 `on_monthly`): cooldown + `ordered_neighbor_country` target
  selection (weakest first) + `declare_war_with_cb` via hidden event
  `mr_dominance.997`, with a fallback that clears invalidated targets.
- Failsafes force completion, PD-style: birth failsafe (~1375,
  `form_country = formable_country:MGO_f`); per-phase completion failsafes
  (`mr_failsafe_p1/p2/p3_fired`, 5 years before each deadline) that
  `change_location_owner` + `add_core` the goal territory. Guards: claimant
  `is_ai = yes` + `at_war = no`; locations taken only from AI owners.
- CBs are situation-granted (`create_enabled = no`): each wargoal's
  `allowed_locations` **covers every location its phase's end trigger demands**
  (Phase 3 grants both the westward and the silk-road CB — nine seats, nine regions).
- 17 modifiers in `main_menu/common/static_modifiers/MR_modifiers.txt`, all wired:
  phase buffs, historical-mode variants, success/failure (AI vs player), transition.
- Read-only vanilla hook: Chahar reacts to a live Tumu Crisis via
  `any_country = { has_variable = lost_emperor }`. Never write vanilla state.
- Deliberately NOT implemented (vanilla already has them): Tumu Crisis
  (`flavor_chi_mon`), Treaty of Ugra (`flavor_MOS`/`flavor_LIT`), Altan Khan's
  conversion (`buddhism_events.13`).

## Hard rules

### Verification
- **Citation rule:** no field/effect/trigger enters a file without a vanilla or PD
  `file:line` using it *in the same position and scope*. Existence is not enough —
  `add_mil` exists but is a **character**-scope skill effect; using it at country
  scope was a real bug here. Check scope, magnitude, and semantics.
- **Search before building.** Three proposed situations already existed in vanilla;
  17 designed modifiers sat unused while duplicates were written. Grep vanilla AND
  this mod before creating anything.
- **Geography is hierarchy, not names.** `map_data/definitions.txt` is the authority:
  region → area → province → location. Real traps hit here: `zhongdu` exists but is a
  frontier village (Beijing is `dadu`); `steppes_region` is the PONTIC steppe, not
  the Silk Road corridor (that is `khorasan_region`, which contains
  `transoxiana_area`); the Kazakh steppe is `zhetysu`/`desht_kipchak` areas.
- **Tags: defined ≠ on the map.** A `setup/countries` entry may hold no land at 1337.
  On-map at start: CHI, CHG, GLH, DLH, JLY, CHB, MZF, INJ, GRG. Emergent: TIM
  (`flavor_tim.8`), OIR (`flavor_chi.txt`), MGO/MGE (formables, this mod).
  Dead: HLG (zero vanilla script uses). `dynamic_historical_event` with an emergent
  tag is fine (vanilla uses `tag = TIM` 15×). Tags are always 3 letters.
- Do not port syntax from other Paradox games. EU5 is its own thing.

### Silent-failure rules (no error, no log, mechanic just doesn't exist)
- Verify directory names in vanilla before creating files (`on_action` not
  `on_actions`; `game_rules`/`static_modifiers` are **main_menu-only**).
- Every cross-reference must resolve: loc keys, rule options, hook names, gfx keys,
  `hint_tag`s (need definitions in `common/scriptable_hints/`, not just loc).
- Wargoal `allowed_locations` must cover the phase goal, or wars are won while the
  goal stays legally untakeable.
- Localisation splits by loader: game-rule names/settings → `main_menu/localization`
  (`rule_<key>`, `setting_<option>`, `setting_<option>_desc`); everything in-game →
  `in_game/localization`.

### Known EU5 specifics (each was a real bug here once)
- `country_exists = c:TAG`, never `exists = c:TAG`. `set_variable` takes
  `name` + `value`. `has_game_rule = option_name` (scalar).
- Events: block key IS the id (`ns.1 = {`), `namespace =` per file; no `picture`/
  `mean_time_to_happen`/`pre_trigger`/`scope`/`is_triggered_only`; use
  `dynamic_historical_event { tag from to monthly_chance }`, `image`/
  `illustration_tags`, `fire_only_once`, `hidden = yes`.
- Firing: `trigger_event_silently` / `_non_silently` only; on_action `events = {}`.
- Effects take **named script values** (`prestige_mild_bonus`,
  `government_power_ultimate_bonus`… defined in
  `main_menu/common/script_values/default_values.txt`), rarely raw numbers.
  `monthly_spawn_chance` is 0–1 (`monthly_spawn_chance_unique` = certain).
- Steppe-specific currencies exist: `add_horde_unity`, `add_tribal_cohesion`.
- Modifiers: `game_data = { category = country }` + types from
  `main_menu/common/modifier_type_definitions/` (no EU4 names like `prestige`,
  `stability_modifier`, `governing_capacity`).
- CBs point at `common/wargoals/` via `war_goal_type`; EU4 `po_*` flags don't exist.
- `owns` vs `controls`: events overwhelmingly use `owns` (ownership), `controls` is
  military occupation. Phase goals use `owns`.
- Files: UTF-8 **with BOM** (`efbbbf`), English only (comments included), `MR_`
  prefix, tabs for indentation.

### Tooling traps (macOS)
- BSD grep: `\b` in patterns can silently match nothing — a whole audit passed
  vacuously on it. Use `grep -F`, explicit patterns, or python3. Multi-line
  constructs (`set_variable = { ... }`) need python3/awk, never line-grep.
- Never trust a suspiciously clean negative result; prove the scan works on a
  known positive first. Run the harness in `docs/EU5-MODDING-GUIDE.md` §9 after
  any change.
- Reading the wiki PDFs in `docs/`: `pip3 install pypdf` (no pdftotext here). The
  wiki is pre-release and incomplete — **vanilla files win** when they disagree.

## Workflow
- Never write to a file without the author's approval. Audit first, report
  categorized (**definite / suspect / needs-decision**), fix only after approval,
  file by file.
- The mod is tested only on the author's Windows PC. Nothing can be run here —
  static verification is the only line of defence; never present it as a test result.
- Skills in `.claude/skills/`: `verify-eu5-syntax`, `verify-tags`, `audit-mod`.

## Language
All code, localisation and comments in English.
