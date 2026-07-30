# CLAUDE.md — Mongol Resurgence (EU5 Mod)

## What this is
A finished, working mod for Europa Universalis V. Alternate history, tightly anchored
to the real timeline: *when the Yuan were driven from China in 1368, what if the Mongol
tribes had genuinely reunified and launched a new wave of conquest westward?* The
player (or AI) rides a three-phase "railroad" from steppe unification to a restored
Mongol Empire, alongside three standalone late-steppe situations covering what
actually happened historically.

Full design spec: `docs/MOD-DESIGN-IDEA.md`. How-to and methodology:
`docs/EU5-MODDING-GUIDE.md`. Audit records: `docs/AUDIT-2026-07-21.md`, `docs/AUDIT-2026-07-29.md`, `docs/AUDIT-2026-07-30.md`.
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
Seven situations, six namespaces, one state machine. End goals are the
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
| `mr_great_partition` | MR_great_partition.txt | opens on a flag, 1600–1720 | the Khaghan is gone from the map, **Karakorum** has left his realm, or `MR_cohesion_score < 40` |

- **THE GREAT PARTITION (`mr_great_partition`)** — the endgame, and the
  railroad's mirror. Phases 1–3 gather the four khanates; this runs the same
  seats in reverse. It opens on the flag `mr_partition_ready`, set **5 years**
  after Phase 3 succeeds by the delayed `mr_dominance.140` (was 30 until the
  user's balance pass), NOT on a calendar date: Phase 3 can close any time
  1550–1650 and a fixed start would leave a fast campaign idling for decades.
  With the delay that short, `current_date > 1600` in `mr_can_start_partition`
  is what actually sets the floor. `MR_cohesion_score` counts DOWN from 100 as
  uluses leave the realm, `mr_partition_concessions` is what the kurultai has
  bought back (a standing term, because the score is recomputed from scratch
  monthly). Three threshold beats (85/55/40) reach three DISJOINT audiences —
  the Khaghan, neighbours, distant spectators — and the 55 mark also grants
  neighbours `cb_MR_carve_the_ulus`, the only MR wargoal pointed AT the Mongols.
  `mr_partition.100` puts the kurultai's three moves to the Khaghan every five
  years; none is free. `on_ending` either releases the successors, each at its
  own threshold ordered by distance from Karakorum (Crimea 85 → Dzungaria 55),
  or grants the permanent `MR_the_ulus_endures`. **The successors are the
  polities that ACTUALLY EXISTED around 1650–1700 — KAZ, OIR, CRI, NOG, BSH,
  CHG — not the 1337 khanates**: a Golden Horde in 1650 would be a second piece
  of alternate history, and the point of this situation is the alternate
  timeline closing back onto the real map. They come back with plain
  `change_location_owner`; a landless-but-defined tag needs no formable
  (CONFIRMED IN GAME 2026-07-30: `is_historic` KAZ spawned — audit D2 closed).
  **FOURTEEN theatres, not six, and they run on a CLOCK** (added 2026-07-30
  after the first game test). The steppe six were only half the map: a
  "collapsed" empire still ran from Shiraz to Canton, because Persia, Iraq,
  Anatolia, all of China, Korea, Tibet, Manchuria and the Volga had no heir
  at all. Now each theatre returns to the power that actually held it around
  1650–1700 — CRI, KAZ, **IRA**, BSH, **RUS/MOS**, NOG, **TUR**, **QNG**
  (Manchuria first at +32y, China at +48y, as it happened), OIR, **TIB**,
  **KOR**, CHG — one scripted effect each in
  `in_game/common/scripted_effects/MR_partition_effects.txt`, called from BOTH
  `on_monthly` (on schedule) and `on_ending` (the final sweep), each guarded
  by its own `mr_returned_*` global so nothing fires twice. Only IRA and QNG
  needed new identity blocks; RUS is only ever named behind `country_exists`.
  **The clock is `mr_partition_momentum`**, a counter that existed from the
  start and was read by nothing. ORDER IS HISTORY, PACE IS THE CAMPAIGN: the
  real dates cannot be the gate, because the situation opens at 1600 at the
  earliest and Crimea 1441 / Kazakh 1465 / Safavid 1501 / Joseon 1392 are all
  in the past — every theatre would fire in month one. So elapsed months
  (+4y → +56y, four apart) set the pace and a backstop year ladder
  (1650 → 1702) keeps a late campaign inside the 1720 window.
  **Overlap order is load-bearing**: `kazan_area`, `bolghar_area` and
  `bashkiria_area` are all parented to `ural_region`, so `MR_geo_ural`
  CONTAINS the middle Volga and Bashkiria — those two run first or Russia
  swallows the Bashkirs. Same reason `MR_geo_pontic` (steppes+caucasus) and
  `MR_geo_xinjiang` (dzungaria+tarim) are NEVER used as partition theatres:
  each contains two successors. Hence the two new atoms, `MR_geo_caucasus`
  and `MR_geo_middle_volga`.
  **Why the clock had to exist at all**: cohesion falls only when the Khaghan
  LOSES ground and nothing in this mod makes a restored empire lose any, so
  the endgame was a 120-year no-op — and it was circular, since
  `cb_MR_carve_the_ulus`, the one lever pointed at the Mongols, is granted at
  cohesion 55, which you could only reach by having already lost five uluses.
  Now the schedule drives the secessions, the secessions drive cohesion, and
  cohesion fires the beats and the CB: 100 → 92 → 80 (beat 85) → 72 → 62 →
  54 (beat 55, CB) → 42 → 30 (beat 40, end).
  `on_ending`'s survival branch now also requires cohesion ≥ 70, or a gutted
  empire timing out at 1720 would collect `MR_the_ulus_endures`.
  **What the Khaghan is left holding: 379 locations, computed and independently
  re-computed** — `mongolia_region` 213 (Karakorum) + transoxiana 96 + khwarazm
  32 + badakhshan 38 (Samarkand). **Nothing at all in `steppes_region`.** Three
  atoms added 2026-07-30 for exactly that (`MR_geo_safavid_khorasan`,
  `MR_geo_kuban_and_yedisan`, `MR_geo_pontic_frontier`), FOLDED into the
  persia / crimea / north theatres rather than given slots of their own — three
  more slots would push the ladder to 17 entries and 1714 and buy nothing. The
  rump is the real 1700 map: Khalkha Mongolia, and Bukhara and Khiva, which
  were ruled by **Chinggisids** (Janids to 1747, Arabshahids to 1740). Two of
  the seven railroad seats survive, Karakorum and Samarkand; Sarai al-Jadid
  goes because New Sarai had been a ruin since 1395 and a 42-location exclave
  4000 km from Karakorum is not a settlement.
  **The Khaghan feels it**: three decline tiers (`MR_the_centre_cannot_hold` /
  `MR_the_uluses_drift` / `MR_khaghan_in_name_only`) granted inside the 85/55/40
  beats that already fire, each replacing the last, all three removed at the top
  of `on_ending` on EVERY exit — a pressure gauge, not a phase reward. **And the
  successors get 25 years of `MR_ulus_of_its_own`**, which is the clause that
  makes the schedule mean anything: a 14-location Crimea beside a superpower
  carrying permanent phase rewards is lunch, and the map churns back to a blob.
  Ranks are set at the handover with vanilla's `set_country_rank_effect` (an
  upgrade-only ratchet): IRA/TUR/RUS-or-MOS/QNG to empire, KAZ and QNG's first
  Manchurian step to kingdom; CRI, NOG, BSH, OIR, CHG, TIB and KOR already
  carry the right rank in vanilla's setup.
  **Its end trigger is three clauses, and the pair matters**: Karakorum out of
  the realm (the SEAT, read backwards from Phase 1's clause) OR
  `MR_cohesion_score < 40`. Karakorum alone can never fire in practice — it
  sits deeper in Asia than any European power reaches — so an empire that lost
  every western ulus but kept its seat would idle to the 1720 timeout and
  collect the survival reward; the cohesion floor is what makes the outer
  uluses matter. `mr_ulus_heartland_held` is no longer an end condition, only
  a 30-point cohesion input.
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
- **Game rules** (PD_config shape, `main_menu/common/game_rules/`), FIVE rules:
  master switch `mr_railroad` (on/off — all content checks
  `NOT mr_railroad_off`); `MR_mongol_resurgence_auto_conquest` (gates the P1
  completion failsafe); `MR_imperial_auto_conquest` (gates P2 + P3 failsafes);
  `MR_partition_schedule` (gates the Great Partition's timed secessions —
  default ON, because with it off the endgame is a no-op); and
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
  buff rule alone: P1 cooldown > 4/8/12 months (Terminator/Historical/
  Vanilla) with matching months_since_war gates, P2 > 4/8, P3 > 12/60 —
  the CODE's numbers are the spec (audit D2 ruling 2026-07-30: the user
  kept the fast pace; an older 6/12/24 + 12/36 figure lived here and in
  two file comments and matched nothing).
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
- 30 modifiers in `main_menu/common/static_modifiers/MR_modifiers.txt`, all wired:
  phase buffs (granted per buff rule, removed in the granting phase's
  `on_ending`), historical-mode variants, phase rewards (**PERMANENT** — never
  removed, and their tooltips say so), success/failure (AI vs player), the
  `MR_great_khan` + `MR_historically_needed` **character** modifiers, and six
  event-specific rewards (Forge of Warriors, Kurultai's Mandate, Western Ulus
  Restored, Seal of Chinggis, Volga Pastures, Dzungar Legacy). RULE: flavour
  events grant their OWN modifier — phase buffs/rewards belong to the
  situations and the buff rule alone, never re-granted by events.
- **Never hand the AI claimant a penalty it cannot fight, and rebellion is the
  one it cannot fight.** Nearly every buff and reward in this mod pushes
  `monthly_rebel_growth` DOWN on purpose: an AI Khaghan does not manage
  revolts, and a railroad that collapses into unrest it cannot suppress stops
  being a railroad. So no MR content may raise `monthly_rebel_growth` or
  `global_separatism` on the claimant — a `MR_kurultai_defied` written that way
  would have undone the whole policy through one 40%-`ai_chance` option.
  Costs go into currencies the AI survives (`monthly_legitimacy`,
  `monthly_horde_unity`, prestige, gold) and, better, into the situation's own
  gauge: the kurultai's defiance option subtracts from
  `mr_partition_concessions`, so the penalty lands as a faster collapse rather
  than as rebels. Same pressure, expressed where the situation can resolve it.
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
  **A progressbar reading a script variable MUST wrap `GetValue` in
  `FixedPointToFloat(...)`.** `value` takes a float; a script variable reads
  back as fixed-point, so the bare `…GetVariable('X').GetValue` resolves to 0
  and the bar sits empty forever — no error, no log line, the panel just looks
  finished-at-zero. Both MR bars shipped this way and the feature was written
  off as broken. Every vanilla bar that reads a script variable wraps it,
  with zero exceptions: `italian_wars.gui:326` is the same construct on a
  situation variable, `decline_of_majapahit.gui:196` the minimal form
  (`value = "[FixedPointToFloat(….GetVariable('demak_progress').GetValue)]"`).
  Scale with `Multiply_float(…, '(float)100')` only when the underlying value
  is 0–1 (the_revolution.gui:115); a score already stored 0–100 needs no
  scaling, just `min = 0` / `max = 100`.
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
- **A CAMPAIGN IN PROGRESS CANNOT GAIN A COUNTRY TAG.** The country database is
  minted once, when the campaign is created. A tag added to
  `in_game/setup/countries/` afterwards does not exist in that save no matter
  how many times the game is relaunched, and `change_location_owner = c:TAG`
  into it is a **silent no-op with no error line**. MEASURED 2026-07-30 by
  reading the player's own autosaves: KAZ sits at country id 2340 (the first id
  after vanilla's exactly 2339 identity blocks) because its block predated the
  campaign; IRA and QNG, added hours later, appear nowhere in a 679 MB save and
  the console answers `tag IRA` with "country is not valid". **Any change to
  `setup/countries` is a hard requirement to start a NEW campaign** — say so in
  the testing guide, because this failure is invisible and unrecoverable.
- **A `country_type = pop` country cannot own locations.** Vanilla's setup has
  448 of them (the nomad and tribe entities that hold POPS, not ground) and BSH
  is one. `change_location_owner` into a pop country is another silent no-op —
  measured 2026-07-30: Ufa was still Mongol at 1670 with `mr_returned_bashkiria`
  already set. Turn it into a landholder first, the way vanilla does when a
  horde settles: `change_country_type = location`
  (`government_conversion_events.10`). The legal values are
  `location, pop, building, army, navy` (triggers.log:3294). `army` is fine —
  that is what a steppe horde is.
- **`change_location_owner` alone is HALF a handover.** Vanilla writes the
  triple together, and its own situation-releases-successors code is the exact
  precedent: `change_location_owner` + `add_core` + `change_integration_level =
  core` (`fall_of_delhi.txt:299-301`, also `country_effects.txt:792-794`). Land
  arriving without it sits at `integration_conquered` — separatism, low control,
  low tax and manpower — which is why a "successor" handed 155 locations still
  looks and plays like a corpse. All 22 MR handover loops shipped without it.
- **An effect must never mark itself done unless it actually did something.**
  The partition's fourteen theatres each set a `mr_returned_*` global at the end
  regardless of whether a single location moved, so the one theatre whose tag
  could not instantiate sealed itself shut for the rest of the campaign. Guard
  the flag on the WORK, not on having run: each effect now sets its flag only
  when its geography atoms hold no claimant ground any more. A silent failure is
  survivable; one that marks itself done is not.
- **A formable is NOT a tag registration; EU5 has TWO country registries.**
  `in_game/setup/countries/` (2339 tag blocks in 45 files) is what makes
  `c:TAG` resolvable at runtime; `main_menu/setup/start/10_countries.txt` is
  what gives a country land, a ruler and a starting RANK. `common/formable_countries/`
  is neither — it supplies name/flag/adjective/colour to a country that already
  exists, and 94 of vanilla's 143 formable target tags appear in no registry at
  all. So a formable does not save you: `change_location_owner = c:IRA` still
  needs the identity block (measured here as `country_manager.cpp:206 Unknown
  country`, and measured fixed when KAZ spawned 2026-07-30). Corollary: a spawn
  by `change_location_owner` never runs the formable's `form_effect`, so
  anything that effect would have done — rank, modifiers — must be done by hand.
- **Rank is never automatic, and rank alone will not fix a bad country name.**
  `set_country_rank_effect = { rank = country_rank:rank_X }` is vanilla's
  upgrade-only ratchet (its `limit` is `country_rank_level < 2/3/4`), it
  bypasses the rank's own `allow` block (vanilla sets `rank_kingdom` on
  one-location revolters, `fall_of_delhi.txt:167`), and nothing in the engine
  promotes or demotes on its own. But the DISPLAYED name comes from two chained
  first-match tables — `country_name_construction.txt` picks the shape,
  `country_ranks.txt` picks the noun — and **`government type` decides more of
  it than rank does**. `rank_empire_tribe` ("Tribes") outranks every culture
  branch, so a tribe-government heir promoted to empire renders "Persian
  Tribes". A spawned tag with no authored government is the root cause of
  "County of Kazakh", and rank only moves it to "Sultanate of Kazakh".
  Note also `MR_l_english.yml` overrides `rank_empire_horde` to "Empire"
  GLOBALLY, which is why MGE reads right — and why vanilla OIR, a steppe horde
  that starts at `rank_empire`, reads "Oirat Empire" from 1337.
- **Some modifier tags silently no-op on the wrong government.**
  `monthly_legitimacy` and `monthly_horde_unity` bite only where
  `government_power` is that resource (`government_types/00_default.txt:100`),
  and there is no universal fallback — `monthly_government_power` is 0 of 2437
  tags. `horde_unity_hit_at_ruler_death` is worse: it is a NEGATIVE-is-worse
  tag whose steppe-horde base is `-50`, and the engine applies the succession
  hit only while the total is below zero (`_hardcoded.txt:3539`), so vanilla's
  `+50` in `horde_civil_war.txt:68` CANCELS the penalty. Writing `+50` to
  "punish" a Khaghan makes his successions painless.
  `ai_months_between_wars` is an additive DELTA, not an absolute count
  (`00_ai_personalities.txt:2-3`, and `:26` writes `-12`).
  `global_hostile_attrition` is `already_percent = yes` — `1` means one point,
  not 100%.
- **`add_country_modifier` takes a `size` multiplier, but do not reach for it
  to build a scaling debuff.** "size multiplies every value in the modifier" is
  inferred, never stated by `effects.log`, and a wrong inference corrupts every
  tag in the block at once. The guarded-swap variants need either a numeric
  `var:X = var:Y` (ZERO vanilla attestations — all three vanilla uses compare
  COUNTRIES) or `set_to_largest_and_extend`, attested only with a finite
  duration. Use a **tier ladder**: literal modifiers of increasing strength
  swapped with `mode = replace` as a variable crosses thresholds. Each tier is
  individually citable and individually readable in the tooltip.
- **`in_game/common/scripted_effects/` exists and is the answer to copy-pasted
  effect blocks** (vanilla ships 10+ files there; parameters are `$name$`
  substitution, `___test_effects.txt`). Note the trap: a scripted EFFECT and a
  scripted TRIGGER are both called as `X = yes` and nothing in the text tells
  them apart, so any tool resolving call sites must load BOTH definition sets —
  `verify_mod.py` failed exactly this way the first time the mod used one.
- **Every region contains ground that can NEVER have an owner, so a NEGATED
  ownership test reads it as lost.** `default.map` files 918 `lakes`, 1868
  `impassable_mountains` and 153 `non_ownable` locations, and
  `definitions.txt` puts them inside the ordinary province → area → region
  tree: `mongolia_region` alone holds 50 (`buir_nuur_province` carries
  `lake_buir`). A location-scope realm test that opens `has_owner = yes` is
  therefore only safe in the POSITIVE. Negated inside an iterator —
  `any_location_in_scripted_geography = { NOT = { mr_in_claimant_realm = yes } }`
  — "nobody can ever own this" becomes "we have lost this", and it is true on
  turn one, forever. **Shipped that way in all eight `mr_ulus_*_held` triggers
  and measured in game 2026-07-30: the Great Partition opened and resolved
  inside a single month.** The safe shape is the one the phase goals used all
  along, `owner ?= { … }`, which makes an ownerless location simply not match;
  `any_ownable_location_in_scripted_geography` also exists (triggers.log:1631)
  but only excludes UNOWNABLE ground, not merely-unowned. `verify_mod.py`
  fails on any reintroduction and carries a canary of the shipped shape.
- **A mod file whose path AND name match a vanilla file replaces it whole**,
  deleting everything it does not repeat, with no error. Under
  `in_game/common/` the escape is the database operation prefixes —
  `TRY_REPLACE:<key> = { … }` swaps ONE vanilla entry, `TRY_INJECT:<key>` adds
  fields to one. Attested in a working published mod on this machine (REAI:
  `generic_actions/zz_REAI_parliament_addon.txt:1`,
  `building_types/zz_REAI_building_adjustments_addon.txt:2`); measured across
  20 workshop mods as 599 `REPLACE:` / 295 `TRY_INJECT:` / 190 `INJECT:` /
  116 `TRY_REPLACE:`, **every one under `in_game/common/` and none under
  `setup/`**. Vanilla itself never uses them — this is a mod-side mechanism.
  Pick the SMALLEST entry that does the job: MR holds the AI Khaghan to the
  steppe by replacing `horde_list` (6 lines) rather than
  `steppe_horde_to_monarchy` (60). Full method:
  `../1066 Test Mod/.claude/skills/verify-vanilla-override/`.
- **Vanilla will settle the AI horde out from under the railroad.**
  `generic_actions/government_conversions.txt : steppe_horde_to_monarchy` is
  `ai_tick = monthly` with `ai_will_do = { value = 100 }` and vanilla's own
  comment *"They always want to do this"*; it needs only peace, a city capital
  of the country's culture and 25% home control, then arms a 15-year timer
  that `government_conversion_events.10` cashes in. The whole steppe advance
  tree is gated `government = steppe_horde`, so a settled Khaghan loses
  `horse_lords` and with it `a_steppe_horse_archers`, `a_a_urughs` and
  `always_allow_army_levies` — measured in game: it then cannot beat Ming
  China in Phase 3. MR's own advances and reforms carry no `government =`
  field on purpose and survive the transition either way. The AI is held
  until `mr_railroad_complete` (or `mr_railroad_failed`, or the master switch
  is off) by `generic_action_ai_lists/zz_MR_government_transition_addon.txt`;
  a HUMAN claimant keeps the choice.
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
- **`prev` is exactly ONE scope hop, and only scope-CHANGING blocks count as
  hops** — `if`/`limit`/`AND`/`OR`/`NOT` are transparent, so the nesting you
  read on screen is not the nesting `prev` walks. Two hops down
  (`c:MGO = { … situation:X = { var:target = { … prev } } }`) it lands on the
  **situation**, not on the claimant, and the engine says so precisely:
  `Left side and right side during comparison were of different types (left was
  'country', right was 'situation')` (`jomini_script_system.cpp:252`). Shipped
  wrong in all three railroad declare blocks; the truce check next to it was
  silently comparing against the same wrong scope, so the AI could be sent at a
  truced target. It is RARE in the log — the pacing gate above it short-circuits
  nearly every tick — so testing will not reliably surface it. Going up more
  than one hop: `save_scope_as` + `scope:x`, never `prev.prev` (zero vanilla
  uses; already the stated rule in the pasture blocks). When the claimant is a
  fixed tag, just name `c:MGO` with the usual `country_exists` guard.
  `verify_mod.py` now walks the scope stack and fails on any country-target
  `prev` that lands on a non-country scope; it carries a canary of the exact
  broken shape so the walker cannot pass vacuously.
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

## LAWS DISCOVERED DOWNSTREAM — read before any new MR work (added 2026-07-29)

The 1066 Test Mod (`../1066 Test Mod/docs/`) carries the LIVING law books:
`KNOWLEDGE.md`, `EU5-MODDING-GUIDE.md`, `EU5-ERROR-DECODER.md`. They contain
engine laws found AFTER this mod shipped, several of which correct or refine
what this repo believes. Read them before writing anything here. The ones
that bite THIS mod's content class directly:

- **"Subjects cannot declare war" is a VASSAL law only.** `tributary.txt:88`
  is `allow_declaring_wars = { always = yes }`, and vanilla ships
  monarchy-over-monarchy tributaries at setup. If MR ever creates subject
  relations, pick the type by this, not by the old blanket rule.
- **Empire rank kills the NAME key.** At `rank_empire` the name composes
  from ADJ+RANK and the NAME key is never read (first-match branch :117).
  Any future rank change for MGO/MGE silently changes how their names
  compose — check the whole chain, not the key you edited.
- **End-anchored one-liner regexes have TWO blind spots**: one-line blocks
  (already known here) AND trailing comments after the closing brace
  (`} #comment`). Every new harness check needs `(?:#[^\n]*)?` before its
  `\n` and an exact-count assertion.
- **The country_exists guard convention has a measured limit.** It is
  observed working for COUNTRY links (this repo's nine-session log), but
  vanilla's own `exists` guard does NOT suppress evaluation-logging for IO
  event-target links (decoder: the middle_kingdom entry). If MR ever touches
  `international_organization:` links, do not assume the guard transfers.
- **Landless-with-claims is Paradox's own standard shape** (13 such tags in
  the Balkans/Caucasus alone) — if the MGE resurrection arc is ever
  extended, claims-on-a-landless-tag is the attested vehicle.
- **Invented name keys are a proven mechanism** (a name key is just a loc
  key; seven shipped in the 1066 mod, screenshot-verified, with free
  language-row rendering) — if MR ever authors characters.
- **Comment words can collide with location tokens** (`van`, `split`,
  `kars` are real locations) — any script that scans ownership-list tokens
  must mask comments length-preservingly first.

A deep audit of this mod against those laws was launched 2026-07-29
(overnight Opus agent, categorized findings). If its report is not yet
reflected here, ask the user whether it landed, or re-run the audit brief
in `../1066 Test Mod/docs/HANDOFF.md`'s pending-items note.
