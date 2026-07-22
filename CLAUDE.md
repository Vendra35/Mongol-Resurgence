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
In-game test plan: `docs/TESTING-GUIDE.md`. Static verification harness:
`tools/verify_mod.py` (run after every change; every check prints its count).

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
Six situations, four namespaces, one state machine. End goals are the
situations' red-lined REGIONS (PD-style): the phase completes when no country
outside the claimant's realm (itself or subjects) holds the goal regions.

| Situation key | File | Window | Ends when |
|---|---|---|---|
| `mongol_resurgence` | MR_mongol_resurgence.txt | 1368–1420 | MGO holds Karakorum + Gobi + ALL of mongolia_region |
| `mongol_imperial` | MR_mongol_imperial.txt | 1420–1550 | MGO holds Samarkand + Dadu + ALL of khorasan/xinjiang/north_china regions |
| `mongol_dominance` | MR_mongol_dominance.txt | 1550–1650 | claimant holds MGE_f's nine locations + a russian_region foothold → forms MGE |
| `mr_chahar_reunification` | MR_late_steppe.txt | 1604–1634 | one banner over the heartland |
| `mr_torghut_migration` | MR_late_steppe.txt | 1616–1630 | a horde reaches the Volga (post-trek) |
| `mr_dzungar_khanate` | MR_late_steppe.txt | 1634–1650 | consolidated + Dzungaria/Tarim/Zhetysu |

- Event namespaces: `mr_dominance` (lifecycle + AI events 995–999),
  `mr_imperial` (campaign arc), `mr_history` (historical DHEs, 1335–1530),
  `mr_dominance_dhe` (horde-institutions DHEs), `mr_steppe` (late-steppe).
- Phase chaining via globals: `mr_phase_one_complete` → `mr_phase_two_complete` →
  `mr_railroad_complete`, with `mr_railroad_failed` set on **every** failure path
  (on_ending sets terminals directly; events set them redundantly).
- Every situation `can_end`s on **goal OR time expiry**; `on_ending` branches on the
  goal trigger, never on side-signals.
- **Game rules** (PD_config shape, `main_menu/common/game_rules/`): master switch
  `mr_railroad` (on/off — all content checks `NOT mr_railroad_off`);
  `MR_mongol_resurgence_auto_conquest` (gates the P1 completion failsafe);
  `MR_imperial_auto_conquest` (gates P2 + P3 failsafes); `MR_mongol_buff_rule`
  (`MR_buff_disabled`/`_historical`/`_enabled`=Terminator — selects which phase
  buff AND the reward tier AND the P1 war pace); `MR_timeline_pacing_rule`
  (`MR_timeline_frontloaded`/`_strict_historical` — P1 war cadence 48 vs 120
  months). The birth failsafe is deliberately NOT rule-gated.
- AI railroad in **all three phases** (P1 the brandenburg_rise shape, P2/P3 the
  Ascension shape): cooldown + `ordered_neighbor_country` target selection
  (weakest first, holding goal-region land) → a war event in **PD-103/203
  shape**: visible, option A declares (`ai_chance` 100), option B postpones
  (player choice), `after` resets the slot and re-seeds the target variable
  with the claimant. No `is_ai` gate — human claimants get the events too.
  Fallbacks clear invalidated targets. Events: `mr_dominance.997` (P1,
  steppe-unification CB), `.993` (P2, silk-road CB), `.992` (P3 — picks
  westward vs silk-road CB by where the target's land lies). Pacing: P1
  48/120/24 months (frontloaded/strict/Terminator), P2-P3 60/12 (PD Ascension).
  Variables: `mr_conquest_*` (P1), `mr_imp_conquest_*` (P2),
  `mr_dom_conquest_*` (P3) — P2/P3 seed `target_country = c:MGO` in on_start
  (MGO exists there; P1 cannot, it seeds at Beat 104). P3 scopes its claimant
  dynamically (`random_country` over tag MGO/MGE — a player can form MGE
  mid-phase); its find-target uses
  `scope:mr_dom_claimant.offensive_alliance_strength`, the one construct
  without an exact PD twin — if P3 railroad wars never fire in testing, that
  line is suspect #1.
- The moment MGO first exists (Beat 104 / `mr_dominance.104`): a new **Borjigin
  Great Khan** is created and enthroned (create_character + `set_new_ruler` +
  `MR_great_khan` character modifier + conqueror trait — the vanilla Timur
  treatment from rise_of_timur.txt), the AI claimant gets
  `MR_mongol_preparing_for_conquest` (blocked_from_declaring_war), and the
  railroad's target variable is seeded. The preparing lock is re-granted to the
  AI claimant at P2 and P3 `on_start` and removed in every phase's `on_ending`
  — safe now because every phase has a declare loop fighting for it.
- Failsafes force completion, PD-style: birth failsafe (~1375,
  `form_country = formable_country:MGO_f`); per-phase completion failsafes
  (`mr_failsafe_p1/p2/p3_fired`, 5 years before each deadline) that
  `change_location_owner` + `add_core` the FULL goal territory (P2: khorasan +
  xinjiang + north_china regions; P3: the nine seat areas + ryazan_area as the
  Russian foothold). Guards: gated by the auto-conquest rules; claimant
  `is_ai = yes` + `at_war = no`; locations taken only from AI owners.
- CBs are situation-granted (`create_enabled = no`; grant years cover each full
  phase window — 130/100): each wargoal's `allowed_locations` **covers every
  location its phase's end trigger demands**. The silk-road wargoal also covers
  `xinjiang_region` (P2 goal) and `mongolia_region` (so a Karakorum lost after
  P1 stays legally retakable — neither P3 CB covered it before).
- 18 modifiers in `main_menu/common/static_modifiers/MR_modifiers.txt`, all wired:
  phase buffs (granted per buff rule, removed in `on_ending`), historical-mode
  variants, phase rewards (removed at the NEXT phase's `on_start`, as their
  tooltips promise), success/failure (AI vs player), transition
  (`MR_the_sleeping_horde` — AI-only, it blocks war declarations), and the
  `MR_great_khan` **character** modifier.
- Situation panels read live variables the situations compute monthly:
  `MR_mgo_score`/`MR_rival_score` (P1, PD-style strength scores) and
  `MR_mge_score`/`MR_dominance_score` (P2/P3, 0–100 goal progress). Headers use
  `GetVariable('mr_leading_country').GetCountry` — never `GetCountry('TAG')`,
  which does not resolve and leaves the portrait black.
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
- **ALL localisation lives in `main_menu/localization/english/MR_l_english.yml`
  — one tree, one file.** Vanilla's `in_game/localization` holds only the jomini
  engine fallback; a second mod loc file with the same filename SHADOWS the
  main_menu one and every main_menu-only key renders raw (this happened: rules,
  settings, modifier names all showed as keys in game).
- Engine-derived loc keys: situations `<key>` + `<key>_desc`; wargoals
  `war_goal_<wargoal_key>` (+`_desc`) — double prefix for `MR_war_goal_*`;
  rules `rule_<key>` / `setting_<option>` (+`_desc`); hints `hint_<key>` +
  `hint_<key>_hint_text`; modifiers `STATIC_MODIFIER_NAME_/DESC_<key>`.

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
- **`c:TAG` on the right side of any comparison errors every tick while the tag
  is off-map** (`Invalid right side during comparison 'c'` — MGO 1368–75, MGE
  for nearly all of Phase 3). Identity → `tag = MGO`; map modes →
  `owner ?= { tag = MGO }`; relations (`is_subject_of`/`is_neighbor_of = c:X`)
  → precede with `country_exists = c:X` in the SAME AND (short-circuit).
- War-declaring railroad events are visible with the declaration in **option A**
  and a postpone **option B** (PD 103 shape), never `hidden` with the war in
  `immediate` — a human claimant must be able to refuse.
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
