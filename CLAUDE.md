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
In-game test plan: `docs/TESTING-GUIDE.md`. Extension roadmap and cookbooks:
`docs/FUTURE-DEVELOPMENT.md`. Static verification harness:
`tools/verify_mod.py` (run after every change; every check prints its count).

## REQUIRED SETUP on a new machine
The workflow depends on a read-only vanilla reference tree plus the Prussian
Destiny reference mod. **This repo is shared between TWO machines whose layouts
DIFFER** — neither is canonical. Always DETECT which one exists before using any
reference path; never assume, and never "fix" one layout's paths to the other's.

Windows machine — vanilla is read STRAIGHT FROM THE STEAM INSTALL. The old
`EU5-Vanilla/` junction under the parent proved unreliable (OneDrive emptied it,
leaving a directory that exists but contains nothing), so the Steam path is
tried first and the junction survives only as a fallback:

```
E:/SteamLibrary/steamapps/common/Europa Universalis V/
└── game/                       ← READ ONLY, full vanilla install (~51k files)

<parent>/
├── <this repo>/                ← write here only
├── The Prussian Destiny/       ← READ ONLY, working, tested reference mod
└── EU5-Vanilla/game/           ← legacy junction, fallback only, may be empty
```

macOS machine (one wrapper folder under the parent):

```
<parent>/
├── <this repo>/                                   ← write here only
└── Reference EU5 vanilla and Prussian Destiny/    ← READ ONLY
    ├── Europa Universalis V/game/                 ← full vanilla install
    └── The Prussian Destiny/                      ← reference mod
```

Detection snippet (bash; the skills use the same one). Note the `-f` probe on a
known file: a junction that exists but is EMPTY passes `-d` and silently yields
zero grep hits — exactly the vacuous-pass class this repo keeps getting bitten
by.

```bash
STEAM_VAN="/e/SteamLibrary/steamapps/common/Europa Universalis V/game"
if [ -f "$STEAM_VAN/in_game/map_data/definitions.txt" ]; then
	VANILLA="$STEAM_VAN"; PD="../The Prussian Destiny"
elif [ -f "../EU5-Vanilla/game/in_game/map_data/definitions.txt" ]; then
	VANILLA="../EU5-Vanilla/game"; PD="../The Prussian Destiny"
else
	VANILLA="../Reference EU5 vanilla and Prussian Destiny/Europa Universalis V/game"
	PD="../Reference EU5 vanilla and Prussian Destiny/The Prussian Destiny"
fi
```

`tools/verify_mod.py` auto-detects the same three candidates in the same order
(env var `MR_VANILLA` overrides all of them). If no tree resolves, fix that
before doing any mod work — **every rule below depends
on being able to grep vanilla**. Key vanilla paths used constantly:
`game/in_game/common/situations/readme.txt` (authoritative situation docs),
`game/in_game/map_data/definitions.txt` (region → area → province → location
hierarchy), `game/in_game/setup/countries/` (tags), `game/main_menu/common/`
(script values, modifier types, game rules).

## Architecture (as built)
Six situations, five namespaces, one state machine. End goals are the
situations' red-lined REGIONS (PD-style): the phase completes when no country
outside the claimant's realm (itself or subjects) holds the goal regions.

The conquest follows the real Mongol sequence: Phase 2 takes the north and
east (Manchuria — Jin, 1234; Tibet — Yuan protectorate, 1240s; North China,
Xinjiang, Khorasan), Phase 3 finishes it (Song China, 1279; Korea, which
submitted in 1259 and was NEVER annexed, so a Korean SUBJECT satisfies the
goal) alongside the western khanates.

**Goal territory is named ONCE, in `in_game/common/scripted_geography/`**
(`MR_geo_*`). Before that file the same region lists were written out 259 times
across seven files, and changing a goal meant editing six places correctly —
only one of which had a check. Now it is one list. Usage:
`has_presence_in = scripted_geography:X` (country),
`is_in_scripted_geography = scripted_geography:X` (location, area, region, and
via `scope:X.capital ?= { … }` a country's seat), and
`scripted_geography:X = { every_location_in_scripted_geography = { … } }` to
iterate. See vanilla `scripted_geography.info`.

THE RULE FOR THAT FILE: **atoms only, never a union.** Geographies do not nest
(zero vanilla definitions reference another), so a union would rewrite its
members and reintroduce the duplication. Callers `OR` the atoms they need. An
atom exists per distinct BOUNDARY, not per pretty name — khorasan and xinjiang
are separate because Phase 3's failsafe wants khorasan alone; manchuria, tibet
and the Siberian marches are separate because the Phase 2 failsafe cores the
steppe but deliberately not the settled ground; russian_lands and ural are
separate from western_reach because they are goals in their own right.

**Each goal group is ONE scripted trigger** (`mr_p2_*_cleared`,
`mr_p3_*_cleared`), called by both the end trigger and the situation's monthly
panel score. They were once written out twice in two different shapes — the
panel sweeping every country for its owned locations, the end trigger scanning
the regions — so the progress bar could read 100 on a phase that refused to
close. One definition, two callers, no drift. When a goal changes, edit the geography atom — every one of the six consumers
(goal trigger, wargoal `allowed_locations`/`allowed_subjugation`, CB-grant net,
AI find-target and fallback, failsafe handover, `tooltip`/
`secondary_map_color`) follows automatically.

| Situation key | File | Window | Ends when |
|---|---|---|---|
| `mongol_resurgence` | MR_mongol_resurgence.txt | 1368–1420 | MGO holds Karakorum + Gobi + ALL of mongolia_region |
| `mongol_imperial` | MR_mongol_imperial.txt | 1420–1550 | Samarkand + Dadu held, and `mr_p2_corridor_cleared` (khorasan+xinjiang) + `mr_p2_north_china_cleared` + `mr_p2_northern_marches_cleared` (manchuria+tibet+bursol/omsk/kulykol areas) → **MGE (Yeke Mongol Ulus) is PROCLAIMED in on_ending** (form_country bypasses MGE_f's allow; its form_effect grants empire rank + vanilla's 50y restoration modifier) |
| `mongol_dominance` | MR_mongol_dominance.txt | 1550–1650 | "The Four Khanates": the seven khanate seats (karakorum, dadu, samarkand, sarai_al_jadid, kazan, tabriz, baghdad) + russian_region foothold + cappadocia_area presence + `mr_p3_persia_cleared` / `_pontic_` (steppes+caucasus) / `_volga_` (kazan/bolghar/bashkiria areas) / `_mesopotamia_` (iraq_arabi) / `_song_china_` (east+west+south china) / `mr_p3_korea_in_the_fold` |
| `mr_chahar_reunification` | MR_late_steppe.txt | 1604–1634 | one banner over the heartland |
| `mr_torghut_migration` | MR_late_steppe.txt | 1616–1630 | a horde reaches the Volga (post-trek) |
| `mr_dzungar_khanate` | MR_late_steppe.txt | 1634–1650 | consolidated + Dzungaria/Tarim/Zhetysu |

- Event namespaces: `mr_dominance` (lifecycle + AI events 992–999),
  `mr_imperial` (campaign arc), `mr_history` (historical DHEs, 1337–1526,
  all firing ON their real dates via `monthly_chance = 100`; `.9` is Delhi's
  fired-only mirror of the 1398 sack), `mr_dominance_dhe` (horde-institutions
  DHEs 1–12; 9/10 are the heavy AI catch-up events mongolized from PD's
  pd_brandenburg_dhe.1/2, 11 the Ulugh Beg observatory, 12 the Yassa census —
  P2-window ones carry `tag = MGE` too so an early proclamation cannot orphan
  them), `mr_steppe` (late-steppe; `.2`, the Tumu reaction, is watched
  PRIMARILY by Phase 2's on_monthly — the crisis is ~1449 — with the Chahar
  watcher kept as fallback).
- Phase chaining via globals: `mr_phase_one_complete` → `mr_phase_two_complete` →
  `mr_railroad_complete`, with `mr_railroad_failed` set on **every** failure path
  (on_ending sets terminals directly; events set them redundantly).
- Every situation `can_end`s on **goal OR time expiry**; `on_ending` branches on the
  goal trigger, never on side-signals.
- **Game rules** (PD_config shape, `main_menu/common/game_rules/`), FOUR rules:
  master switch `mr_railroad` (on/off — all content checks
  `NOT mr_railroad_off`); `MR_mongol_resurgence_auto_conquest` (gates the P1
  completion failsafe); `MR_imperial_auto_conquest` (gates P2 + P3 failsafes);
  `MR_mongol_buff_rule` (`MR_buff_disabled`/`_historical`/`_enabled`=Terminator
  — selects the phase buff AND the reward tier AND the railroad war pace).
  The old `MR_timeline_pacing_rule` was REMOVED (the Mongol window IS the
  historical timeline); every buff tier has its own pacing branch — a tier
  without one silently kills the railroad. The birth failsafe is deliberately
  NOT rule-gated.
- AI railroad in **all three phases** (P1 the brandenburg_rise shape, P2/P3 the
  Ascension shape): cooldown + `ordered_neighbor_country` target selection
  (weakest first, holding goal-region land) → a war event in **PD-103/203
  shape**: visible, option A declares (`ai_chance` 100), option B postpones
  (player choice), `after` resets the slot and re-seeds the target variable
  with the claimant. No `is_ai` gate — human claimants get the events too.
  Fallbacks clear invalidated targets. Events: `mr_dominance.997` (P1,
  steppe-unification CB), `.993` (P2, silk-road CB), `.992` (P3 — westward CB
  if the target holds russian/steppes/ural/persia/anatolia land or
  iraq_arabi/armenian_highlands presence, silk-road CB otherwise). Pacing by
  buff rule alone: P1 6/12/24 months (Terminator/Historical/Vanilla) with
  matching months_since_war gates, P2 12/36, P3 12/60 (PD Ascension shape).
  Variables: `mr_conquest_*` (P1), `mr_imp_conquest_*` (P2),
  `mr_dom_conquest_*` (P3) — P2 seeds `target_country = c:MGO` in on_start;
  P3 seeds the claimant via if/else (c:MGE normally, c:MGO on the
  failed-proclamation fallback); P1 cannot seed early, it seeds at Beat 104.
  P3 scopes its claimant dynamically (`random_country` over tag MGE/MGO); its
  find-target uses `scope:mr_dom_claimant.offensive_alliance_strength`, the
  one construct without an exact PD twin — if P3 railroad wars never fire in
  testing, that line is suspect #1.
- **The succession of Great Khans**: Beat 104 (`mr_dominance.104`) creates and
  enthrones the first Borjigin Great Khan the moment MGO exists ("Batu",
  create_character + `set_new_ruler` + `MR_great_khan` +
  `MR_historically_needed` (is_immortal, 65y) character modifiers + four
  traits — the vanilla Timur treatment; multi-trait create_character per
  hussite_wars.txt:478). P2 on_start (`mr_dominance.120`) enthrones the
  second generation ("Adai"), P3 on_start (`mr_dominance.130`) the third
  ("Altan") — same shape, era-appropriate names, human and AI alike. The AI
  claimant gets `MR_mongol_preparing_for_conquest` (blocked_from_declaring_war)
  at Beat 104 and again at P2/P3 `on_start`, removed in every phase's
  `on_ending` — safe because every phase has a declare loop fighting for it.
- **MGO's birth has TWO paths**: organic (a free Mongol steppe horde that
  takes Karakorum, any time 1368+ — an AI converts on the spot, a HUMAN is
  offered the banner via `mr_dominance.11` and may decline, once) and the
  1375 failsafe, which picks the STRONGEST candidate in quality tiers — free
  AI horde at peace → free AI horde → anyone as absolute last resort (a
  subject is first released via `cancel_subject`, run by the overlord:
  _hardcoded.txt:4808). RULE: the mod never force-converts, locks or robs a
  human player — every conversion is offered, every railroad war postponable,
  every failsafe is_ai-gated on both claimant and victim, and the alliance-break
  events (`mr_dominance.24/.27/.28`) are is_ai-gated too. PD fires its
  equivalent at c:PRU unconditionally (the_prussian_ascension.txt:138), but PD
  has no such rule and we do; dissolving a player's treaties with no way to
  refuse is the same class of theft. It is also pointless for them — the break
  exists because the AI's declare event stalls on its own alliances.
- **Both P2 and P3 end machinery is dual-tag** (any_country over MGO/MGE +
  guarded is_subject_of pairs): under the Vanilla buff rule nothing carries
  `blocks_country_formation`, so a human claimant can legally form MGE
  mid-Phase-2 — a c:MGO-only end trigger made the phase unwinnable for
  exactly that player.
- Failsafes force completion, PD-style: birth failsafe (~1375,
  `form_country = formable_country:MGO_f`); per-phase completion failsafes
  (`mr_failsafe_p1/p2/p3_fired`, 5 years before each deadline) that
  `change_location_owner` the FULL goal territory, named by geography atom.
  `add_core` follows one policy in both phases: steppe and frontier are cored
  (heartland, xinjiang, the Siberian marches, north_china, and in P3 khorasan
  and Song China), settled ground the horde ruled but never lived in is NOT
  (manchuria, tibet, and in P2 khorasan) — free cores there over-feed the AI.
  **Phase 3 deliberately hands over the Phase 2 ground too**, not just its own
  goals: an AI that lost a war in 1600 would otherwise reach 1650 as a restored
  empire with holes in it. That costs nothing when Phase 2 held, because the
  limit only matches land owned by an AI that is neither the claimant nor its
  subject. Guards: gated by the auto-conquest rules; claimant
  `is_ai = yes` (P1's `at_war = no` gate was deliberately removed — an AI
  stuck in an endless war must not stall the handover; P2/P3 keep it);
  locations taken only from AI owners, always via `owner ?=` — the bare
  `owner =` link errors on ownerless locations.
- CBs are situation-granted (`create_enabled = no`; grant years cover each full
  phase window — 130/100): each wargoal's `allowed_locations` **covers every
  location its phase's end trigger demands**. The silk-road wargoal spans both
  eastern phases: khorasan + xinjiang + north_china + manchuria + tibet +
  bursol/omsk/kulykol areas (P2), east/west/south china + korea (P3), plus
  `mongolia_region` so a Karakorum lost after P1 stays legally retakable. The
  westward wargoal covers russian + steppes + ural + **persia + anatolia +
  caucasus regions** plus the **iraq_arabi and armenian_highlands areas**
  (`scope:location.area = area:X` — the same location→area link PD's
  find-target uses) for the P3 four-khanates goal. `caucasus_region` was a P3
  goal reachable by NO wargoal until this was audited — when a goal region is
  added, re-run the coverage cross-check, do not eyeball it.
- 26 modifiers in `main_menu/common/static_modifiers/MR_modifiers.txt`, all wired:
  phase buffs (granted per buff rule, removed in the granting phase's
  `on_ending`), historical-mode variants, phase rewards (**PERMANENT** — never
  removed, and their tooltips say so), success/failure (AI vs player), the
  `MR_great_khan` + `MR_historically_needed` **character** modifiers, and six
  event-specific rewards (Forge of Warriors, Kurultai's Mandate, Western Ulus
  Restored, Seal of Chinggis, Volga Pastures, Dzungar Legacy). RULE: flavour
  events grant their OWN modifier — phase buffs/rewards belong to the
  situations and the buff rule alone, never re-granted by events.
- **Panel variables are computed at the END of `on_monthly`, never the top.**
  Everything that can change what the panel should show — the beats, the birth
  failsafe, the completion failsafe — runs inside the same tick. Computed
  first, the panel lags a month behind its own situation. In testing that
  surfaced as a Phase 2 progress bar reading 0 while every end requirement was
  already green: the requirement list evaluates live when the panel opens, the
  bar only shows what the last tick wrote, and the failsafe had handed over the
  territory in between. All three phases now compute panel state last.
- Situation panels read live variables the situations compute monthly:
  `MR_mgo_score`/`MR_rival_score` (P1, PD-style strength scores) and
  `MR_mge_score`/`MR_dominance_score` (P2/P3, 0–100 goal progress). Headers use
  `GetVariable('mr_leading_country').GetCountry` — never `GetCountry('TAG')`
  for tags that can be off-map. **GUI template block names are exact**:
  `one_country_header_template` exposes `CountryContext` +
  `character_portrait_anchor` (country_header.gui:156/:160);
  `two_countries_header_template` exposes `FirstCountryContext`/
  `SecondCountryContext` + `first_/second_character_portrait_anchor`. Overriding
  a block name the template doesn't have is silently dropped — the P2/P3
  panels overrode the two-country names on the one-country template and got
  black portraits + Character-context log spam. Widgets: `text_single` (not
  `textbox_single`), `progressbar` with `value`/`min`/`max` (`progress` is not
  a property) — vanilla refs the_revolution.gui:112, italian_wars.gui:316.
- Read-only vanilla hook: Chahar reacts to a live Tumu Crisis via
  `any_country = { has_variable = lost_emperor }`. Never write vanilla state.
- Deliberately NOT implemented (vanilla already has them): Tumu Crisis
  (`flavor_chi_mon`), Treaty of Ugra (`flavor_MOS`/`flavor_LIT`), Altan Khan's
  conversion (`buddhism_events.13`).

## Hard rules
> **PORTABLE TO A NEW EU5 REPO:** everything from here to the end of
> `### Known EU5 specifics`, plus `## Workflow` and `## Language`, is
> general EU5 knowledge with nothing Mongol-specific in it. Lift those
> sections wholesale, together with `docs/EU5-MODDING-GUIDE.md`,
> `docs/EU5-ERROR-DECODER.md` and `tools/verify_mod.py`, as the seed for
> the next project. `## What this is`, `## REQUIRED SETUP` and
> `## Architecture` are specific to THIS mod and do not travel.


### Verification
- **`docs/EU5-Vanilla-Script-Docs/` is the authority.** It is the console output
  of `script_docs` and `dump_data_types` run against the shipped game: 1798
  triggers and 1534 effects **each with its `**Supported Scopes**`**, 2436
  modifier tags, 289 event targets with input/output scopes, and the on_action
  list with expected scopes. Look there FIRST — before grepping vanilla, which
  only ever showed what someone happened to use, never what is legal.
  Regenerate after a game patch: launch with `-debug_mode`, console
  `script_docs` then `dump_data_types`, copy the logs from the user folder.
  Two harness checks already read it.
  Worked example, the bug it would have prevented: `is_in_scripted_geography`
  → *Supported Scopes: location, province_definition, area, region,
  sub_continent, continent*; `has_presence_in` → *country*. The engine's error
  message was quoting that exact list back at us.
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
  tag is fine (vanilla uses `tag = TIM` 15×). Tags are always 3 letters **in vanilla** (2217 of 2217) and in this mod, so the
  harness treats 4+ as a finding. It is a CONVENTION, not an engine limit: a
  published total conversion ships 471 five-letter tags used live in script.
  Relevant only if a future project needs hundreds of new tags.
- Do not port syntax from other Paradox games. EU5 is its own thing.

### Silent-failure rules (no error, no log, mechanic just doesn't exist)
> When the game DOES report something, decode it with
> `docs/EU5-ERROR-DECODER.md` before investigating from scratch — every
> signature there cost a real investigation once.

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
- **A `generic_action` needs side registries.** Two a mod can satisfy:
  `in_game/common/generic_action_ai_lists/` (else
  `generic_action_ai_list.cpp:82`, and the AI re-evaluates the action
  constantly), and for its `price` a `<price_key>_cost_modifier` in
  `main_menu/common/modifier_type_definitions/` (else
  `price_database.cpp:117`).
  One it CANNOT: the `PERFORM_<key>_ACTION` message type
  (`message_handler.cpp:421`). The engine reads exactly one file for those,
  `main_menu/gui/messagetypes.txt` with 1348 vanilla entries — a mod file with
  any other name in that folder is silently ignored (a popular published mod
  ships one that is dead), and a file with that name replaces all 1348.
  Accepted cost: one log line when the action fires and no popup. The action
  works. Same class: modifier-type ICONS are looked up by convention from
  `main_menu/gfx/interface/icons/modifier_types/<key>.dds` — there is no
  `icon` field. Vanilla omits some of its own, so `modifier_type.cpp:1294` is
  a tolerated cosmetic line too.
- **Loc values must live on ONE physical line.** A literal `
` that becomes a
  real newline splits the value and the game logs `Missing colon (:)
  separator` and drops the entry — while a key-counting scan still sees every
  key and reports clean. Eleven descriptions shipped this way.
- Engine-derived loc keys: situations `<key>` + `<key>_desc`; wargoals
  `war_goal_<wargoal_key>` (+`_desc`) — double prefix for `MR_war_goal_*`;
  rules `rule_<key>` / `setting_<option>` (+`_desc`); hints `hint_<key>` +
  `hint_<key>_hint_text`; modifiers `STATIC_MODIFIER_NAME_/DESC_<key>`.

### Known EU5 specifics (each was a real bug here once)
- `country_exists = c:TAG`, never `exists = c:TAG`. `set_variable` takes
  `name` + `value`. `has_game_rule = option_name` (scalar). For saved
  scopes/variables BOTH forms are vanilla-attested: `exists = scope:x` is the
  canonical existence check (1950 vanilla uses) and `country_exists = scope:x`
  / `= var:x` adds the resolves-to-a-live-country guarantee (31+5 vanilla uses;
  PD's brandenburg_rise.txt:449 uses it on the railroad target var).
- Events: block key IS the id (`ns.1 = {`), `namespace =` per file; no `picture`/
  `mean_time_to_happen`/`pre_trigger`/`scope`/`is_triggered_only`; use
  `dynamic_historical_event { tag from to monthly_chance }`, `image`/
  `illustration_tags`, `fire_only_once`, `hidden = yes`. DHE `monthly_chance`
  is a PERCENT (float ok, max 100 = fires the month the window opens + trigger
  passes; 80 vanilla uses at 100). Every DHE event wants a
  `<ns>.<id>.entry` loc key (terse headline) for the DHE timeline.
- **Country tag names must not contain "Empire"** — no vanilla tag name does
  (MGE is vanilla-named "Mongolia"); country_database.cpp warns because rank
  titles compose as "The Great <name> Empire". Hence MGE = "Yeke Mongol Ulus".
- Selection idiom: `ordered_country` / `ordered_neighbor_country` with
  `order_by = military_strength`, `max = 1`, `check_range_bounds = no`
  (war_of_religions.txt:54-59). Breaking vassalage: `cancel_subject`, run by
  the OVERLORD with the subject as argument (`overlord ?= { cancel_subject =
  prev }`, _hardcoded.txt:4808); `make_independent`/`release_subject` do not
  exist as effects.
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
- **Never `any_owned_location = { region = region:X }`** — it walks a country's
  entire holdings list to answer a question `has_presence_in = region:X` answers
  directly (108 vanilla uses, region/area/sub_continent). All 104 in this mod
  were the bare form and all were converted; `verify_mod.py` now fails on any
  reintroduction. Related choice of iterator, cheapest first: `has_presence_in`
  (a predicate) → `region:X = { any_ownable_location_in_region = { owner ?= … } }`
  (asks "does anyone outside our realm hold this ground", the end-trigger
  shape) → `ordered_neighbor_country` (neighbours only) → `any_country` /
  `every_country` (the whole map — only when the ANSWER must be a country).
- `owns` vs `controls`: events overwhelmingly use `owns` (ownership), `controls` is
  military occupation. Phase goals use `owns`.
- **End conditions are a CHECKLIST: one `custom_tooltip` per requirement, each
  text ONE line.** The situation panel renders one tick per custom_tooltip, so
  a single tooltip wrapped around every clause fights the widget — Phase 3
  displayed its text *and* the raw clause-by-clause breakdown underneath.
  Vanilla's eight situation end-condition tooltips are each one compact
  sentence and none contains a newline. Each `mr_p2_*`/`mr_p3_*` goal trigger
  carries its own tooltip internally; the end triggers are just a list of
  them (P1 2 lines, P2 4, P3 9).
- **A "we hold X" goal must mean the REALM holds X.** `c:MGO = { owns =
  location:samarkand }` is true only when the claimant holds the seat itself,
  so a vassal holding Samarkand or Khanbaliq deadlocked the phase — and the
  failsafe could not break it, because it deliberately never takes land from
  the claimant's own subjects. Every seat and foothold now goes through the
  location-scope trigger `mr_in_claimant_realm` (`has_owner = yes` +
  `top_owner ?= c:MGO/MGE` behind `country_exists`). Note `top_owner` is a
  different trigger from `owner` and is legitimate; the harness knows.
- **One atom per separately-true condition.** Collapsing eastern + western
  Gobi into one geography turned a goal that wanted BOTH halves into one that
  accepted either; the same happened to Dzungaria + Tarim + Zhetysu. If two
  names sit in the same atom they can only ever be ORed.
- **`is_subject_of` matches only a DIRECT vassal.** Every question this mod asks
  about subjecthood is really "is this inside our realm", which must include a
  vassal's vassal — use `top_overlord_or_this ?= c:MGO`, vanilla's idiom for
  "MGO or anything under it" (`hundred_years_war.txt:185`,
  `situation_triggers.txt:80`). It also returns the country itself when it has
  no overlord, so a separate `tag = MGO` member is redundant. Shipped wrong in
  46 places: goal clauses refused to count a sub-vassal's ground (the phase
  would not end), the failsafe SEIZED a sub-vassal's land, and the AI targeted
  its own sub-vassal. On a LOCATION, the one-link form is `top_owner ?= c:MGO`
  (156 vanilla uses; guard ownerless with `has_owner = yes`, per
  `conquistadors.txt:64`). Avoid `any_country_in_hierarchy` /
  `every_country_in_hierarchy` — a popular published mod uses them but vanilla
  has ZERO uses anywhere, so they are unattested.
- **`c:TAG` on the right side of any comparison errors every tick while the tag
  is off-map** (`Invalid right side during comparison 'c'` — MGO 1368–75; MGE
  only until Phase 2 completes, now that the proclamation moved there).
  Identity → `tag = MGO`; map modes → `owner ?= { tag = MGO }`; relations
  (`is_subject_of`/`is_neighbor_of = c:X`) → precede with
  `country_exists = c:X` in the SAME AND (short-circuit). Same family:
  `owner = { ... }` in a location limit errors on OWNERLESS locations — always
  `owner ?= {` (the failsafe handover blocks all hit this).
- War-declaring railroad events are visible with the declaration in **option A**
  and a postpone **option B** (PD 103 shape), never `hidden` with the war in
  `immediate` — a human claimant must be able to refuse.
- Files: UTF-8 **with BOM** (`efbbbf`) for `.txt` and `.yml`. **`.gui` files are
  the exception and carry NO BOM** — vanilla ships 483 `.gui` files and only 49
  have one, so BOM-less is the house style there (PD's three do have one; it is
  not load-critical either way, and it is NOT the cause of the `[l]` formatting
  error). `tools/verify_mod.py` checks `.txt`/`.yml` only, deliberately.
  English only (comments included), `MR_` prefix, tabs for indentation.

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
