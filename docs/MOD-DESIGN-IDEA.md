# Mongol Resurgence — Design Specification (as built)

> Status: the mod is **finished and working**. This document describes the final
> design as implemented. The original draft's open questions are resolved inline.
> For the audit that shaped it, see `AUDIT-2026-07-21.md`; for methodology,
> `EU5-MODDING-GUIDE.md`.

## Concept
An alternate-history scenario, anchored to real history: *when the Yuan dynasty was
driven out of China in 1368 (the Northern Yuan), what if the Mongol tribes had
genuinely reunified and launched a new wave of conquest westward?* Historically
anchored but divergent — real 14th–17th-century events frame a railroad that
history did not take.

## The three-phase railroad

### Phase 1 — The Northern Yuan Resurgence (situation `mongol_resurgence`, 1368–1420)
The unification of Mongolia. **Dynamic birth, no fixed tag**: whoever holds the
heartland with a steppe-horde government and Mongol culture takes up the Chinggisid
claim, modelled on vanilla's Timur emergence (`flavor_tim.8`). MGO is born via the
vanilla formable `MGO_f` (tier 3 — already in vanilla; the mod adds **no**
formable_countries file).
- Momentum meter drives story beats (`mr_dominance.100–107`); mutual 25-year
  unification CBs among all steppe hordes create the competitive race (both
  directions, player included — intended, mirroring PD's BRA/TEU rivalry).
- **Organic birth**: a free Mongol steppe horde that takes Karakorum takes up
  the claim (`form_country` bypasses MGO_f's 85%-of-Mongolia allow, the PD
  dhe.4 pattern) — an AI converts on the spot, a HUMAN is offered the banner
  (`mr_dominance.11`) and may decline. The 1375 failsafe then picks the
  STRONGEST free AI horde (tiered: AI at peace → AI → anyone as absolute last
  resort, with `cancel_subject` freeing a last-resort vassal). The mod never
  force-converts a player who has not said yes.
- **AI railroad**: monthly loop picks the weakest valid neighbour holding Mongolian
  land (`ordered_neighbor_country`, `defensive_alliance_strength <` ours), then
  `declare_war_with_cb` via `mr_dominance.997` (visible; option B postpones);
  pacing rides the buff rule alone — Terminator ~6 months, Historical ~1 year,
  Vanilla ~2 years.
- Ends when MGO owns Karakorum and has presence in both Gobi areas.

### Phase 2 — The Pax Mongolica (situation `mongol_imperial`, 1420–1550)
Mastery of the Silk Road and the hegemony contest with the Ming. The corridor is
**khorasan_region** (Transoxiana/Khwarazm/Zhetysu) plus north China — *not*
`steppes_region`, which is the Pontic steppe. Campaign beats from `mr_imperial.100–103`;
silk-road CBs granted against corridor powers.

The eastern conquest follows the **real Mongol sequence**, split across the two
phases the way it actually ran. Phase 2 takes the north and east: **Manchuria**
(the Jin fell in 1234), **Tibet** (a Yuan protectorate from the 1240s), North
China, Xinjiang and Khorasan, plus the **bursol/omsk/kulykol** areas that square
off the Siberian frontier. Phase 3 finishes the job.

Ends when MGO owns Samarkand + Dadu and all three goal groups are cleared
(`mr_p2_corridor_cleared`, `mr_p2_north_china_cleared`,
`mr_p2_northern_marches_cleared`) — and **on success the Yeke Mongol Ulus (MGE) is
proclaimed immediately** in `on_ending` via `form_country = formable_country:MGE_f`
(bypasses the formable's allow block, the PD PRU_f pattern; MGE_f's form_effect
raises the country to empire rank). A new second-generation Great Khan is
enthroned at the phase's start (`mr_dominance.120`).

### Phase 3 — The Four Khanates (situation `mongol_dominance`, 1550–1650)
The westward finale of the PROCLAIMED empire — the phase opens with MGE on the
map, which also retires the old `c:MGE` error-spam class. The goal is the
historical empire at its height, not the formable's requirements: the claimant
owns the **seats of the four khanates** — Karakorum + Dadu (Yuan), Samarkand
(Chagatai), Sarai al-Jadid + Kazan (Golden Horde), **Tabriz + Baghdad
(Ilkhanate)** — and holds footholds in the **Russian lands** and in
**Cappadocia** (Kose Dag country, the deepest historical Mongol reach into
Anatolia). Six goal groups must be cleared of outside powers:
`mr_p3_persia_cleared`, `_pontic_` (steppes + caucasus), `_volga_`
(kazan/bolghar/bashkiria), `_mesopotamia_` (iraq_arabi), **`_song_china_`**
(east + west + south China, which fell in 1279 and completed what the Jin war
began) and **`mr_p3_korea_in_the_fold`**.

**Korea is a subject, not a conquest.** Goryeo submitted in 1259 and was never
annexed, and the shared goal clause already accepts subject-owned locations — so
a Korean state that is the claimant's vassal satisfies the goal and an
independent one does not, with no special-case code.

A third-generation Great Khan is enthroned at the phase's start
(`mr_dominance.130`), and the **court moves from Karakorum to Khanbaliq**
(`dadu`) as Kublai moved it in 1272 — the AI relocates and is told
(`mr_dominance.136`), a human is asked and may refuse (`.137`).

Two CBs cover the two theatres: westward (russian/steppes/ural/**persia/anatolia/
caucasus** + the iraq_arabi/armenian_highlands areas) and a re-grant of the
silk-road CB, which now also spans Song China and Korea — the Phase 2 grant
expires decades earlier.

## Situation actions
One player-facing action, **Claim the Khan's Own Pasture**
(`MR_select_core_region`), modelled field-for-field on vanilla's
`rot_select_core_region` — the "Select Core Region" button on the Rise of Timur
panel. It appears on the Phase 1 **and** Phase 2 panels: the claimant names a
region, everything it already holds there becomes core and gains
`MR_khans_own_pasture`, and whatever it takes there afterwards is cored as it is
taken. The gate is the **`MR_great_khan` character modifier** — the claim is the
Khan's, not the state's, and it lapses the moment he dies (vanilla gates the
same mechanic on Timur's `timmy_wants_to_play`).

The ongoing auto-core rider lives in the situations' `on_monthly`, not in
`on_location_changed_owner` where vanilla puts it: that on_action is defined
with an `effect` block, and redefining the name in a mod replaces the vanilla
block wholesale, taking a great deal of unrelated location-transfer logic with
it.

## The world reacts (immersion layer)
Modelled on PD's `pd_brandenburg.101/102/200/201/202`. Each phase's `on_start`
sends three kinds of message — `mr_dominance.20/21/28` (Phase 1),
`.22/23/24` (Phase 2), `.25/26/27` (Phase 3):
- **Spectators** — a stake in the theatre but no land the phase demands.
- **Victims** — they hold ground inside the goal regions and are being told what
  is about to ride over them.
- **Broken alliances** — the claimant's own treaties with powers standing on the
  goal regions are dissolved (`every_related_country` + `remove_relation`), so
  the railroad's declare event is never blocked by the claimant's own diplomacy.
  Phase 1's fires at **Beat 104**, when MGO is born, because no claimant exists
  when that phase opens.

Nobody is told the same news twice: the steppe powers that receive the opening
`mr_dominance.10` are excluded from the Phase 1 spectator and victim nets.

## Two-layer failsafe system (as implemented)
**(a) Birth failsafe** (Phase 1 only): if no country organically takes the claim by
1375, the best-placed steppe horde is force-converted with
`form_country = formable_country:MGO_f` (hidden bookkeeping: `mr_dominance.998`).

**(b) Completion failsafes** (all three phases, 5 years before each deadline —
1415/1545/1645): if the goal is unmet, the goal territory is handed over outright —
`change_location_owner` + `add_core` by area/region iteration, rival hordes made
tributaries in Phase 1 — mirroring PD's `every_ownable_location_in_area` pattern.
Phase 3 hands over the four-khanate seats' areas, both foothold areas, the whole
persia_region, the caucasus, and Song China + Korea. `add_core` is withheld where
free cores would over-feed the AI claimant: khorasan and tibet get ownership
only. Guards: fires only for an **AI** claimant (the Phase 1
at-war gate was deliberately removed — an AI stuck in an endless war must not
stall the handover); takes locations only from AI owners (`owner ?=`, never the
bare link); each phase has its own one-shot flag (`mr_failsafe_p1/p2/p3_fired`).
`mr_dominance.999` then grants the means to hold the territory.

A human player who fails a phase is allowed to fail: every situation also ends on
**time expiry**, the failure branch fires (`mr_dominance.2/.127/.133` + AI/player
failure modifiers), and `mr_railroad_failed` is set on every failure path.

## The late-steppe situations (standalone, 1600s)
Vanilla has zero content for these (verified). They enrich the Phase 3 era and are
built on real tags (OIR/MGO/MGE) since the successor states have none:
- **Ligdan Khan and the Chahar** (1604–1634): the last Chinggisid's failed
  reunification — the dark mirror of Phase 1. Fires when the steppe is *fragmented*
  (including after a failed railroad; not when MGO/MGE dominates). The read-only
  Tumu Crisis reaction (`has_variable = lost_emperor`) is watched PRIMARILY by
  Phase 2's on_monthly — the crisis is a ~1449 event and could never be live in
  the Chahar window; the Chahar watcher remains as a fallback only.
- **The Torghut Migration** (1616–1630): the Kalmyk trek to the Volga — the Phase 3
  premise, historically real. Gated so it neither starts moot (a horde already on
  the Volga) nor ends before the trek happens (Urals beat gates the end).
- **The Dzungar Khanate** (1634–): the last steppe empire. Its steppe is the
  **Kazakh** steppe (`zhetysu_area`, khorasan_region). End trigger is strictly
  stronger than the consolidation beat so it cannot end the month the beat fires.

Each late-steppe finale grants its own reward modifier — The Seal of Chinggis
(Chahar), The Volga Pastures (Torghut), The Dzungar Legacy (Dzungar) — never a
railroad phase buff. The same rule holds mod-wide: the flavour DHEs grant
The Forge of Warriors / The Kurultai's Mandate / The Western Ulus Restored,
while the phase buffs and phase rewards stay exclusively with the situations
and the buff rule. Phase **buffs** are temporary and are stripped by the
granting phase's own `on_ending`; phase **rewards** are permanent and are never
stripped — the phases run back-to-back, so the old "removed at the next phase's
on_start" behaviour meant a reward the player never actually kept.

Deliberately **not** built (vanilla already implements them): Tumu Crisis
(`flavor_chi_mon.1–7` + `recapture_emperor`), Treaty of Ugra (`flavor_MOS`/
`flavor_LIT` + trust bias — its variables are transient, so no hook is possible),
Altan Khan's conversion (`buddhism_events.13`).

## Historical DHE layer (namespace `mr_history`, 1337–1526)
Real-history anchoring with `historical_info` boxes, `historical_option` markers
and `.entry` keys for the DHE timeline. Every event fires ON its historical date
(`monthly_chance = 100`, percent semantics): the Ilkhanid succession ~1337
(JLY/CHB/MZF/INJ/GRG — **not** HLG, which has zero vanilla uses; the Ilkhanate
died in 1335, pre-start), the Chagatai schism ~1347, the Yuan's last stand ~1351
(Red Turban timing, NOT game start), Tokhtamysh ~1380, the sack of Delhi 1398
(two-sided: TIM gets the plunder, DLH gets the mirror event `mr_history.9`),
the Oirat challenge ~1435 (Esen), Babur ~1500. Emergent-tag DHEs are valid
(vanilla uses `dynamic_historical_event tag = TIM` 15×).

## Tag table (RESOLVED — all verified against setup/ + script usage)
| Concept | Tag | Notes |
|---|---|---|
| Yuan / China | **CHI** | on map 1337; `CHI_f` exists; no separate YUA |
| Chagatai | **CHG** | on map 1337 |
| Golden Horde | **GLH** | on map 1337 |
| Ilkhanate | **JLY, CHB, MZF, INJ, GRG** | successor states; HLG is dead (0 uses) |
| Delhi | **DLH** | not DEL |
| Oirat | **OIR** | emerges via `flavor_chi.txt` |
| Timurids | **TIM** | emerges via `flavor_tim.8` |
| Mongolia | **MGO** via `MGO_f` (tier 3) | formable-only; no setup entry by design |
| Mongol Empire | **MGE** via `MGE_f` (tier 4) | formable's own allow lists nine locations — bypassed: proclaimed via `form_country` at Phase 2's end |

## Game rules (main_menu, PD_config shape)
Four rules — loc lives in **main_menu** yml (`rule_`/`setting_` convention):
- `mr_railroad` (on/off): the master switch; all content checks
  `NOT mr_railroad_off`.
- `MR_mongol_resurgence_auto_conquest` (yes/no): gates the Phase 1 completion
  failsafe. The birth failsafe is deliberately NOT gated.
- `MR_imperial_auto_conquest` (yes/no): gates the Phase 2 + 3 failsafes.
- `MR_mongol_buff_rule` (`MR_buff_disabled`/`_historical`/`_enabled`): selects
  the phase buff tier, the reward tier, AND the AI railroad's war pace
  (Terminator ~6 months / Historical ~1 year / Vanilla ~2 years in Phase 1).
The separate timeline-pacing rule was removed: unlike Prussia, the Mongol
window IS the historical timeline.

## Naming
Files/variables `MR_`, triggers/vars `mr_`, CBs `cb_MR_*`, wargoals `MR_war_goal_*`,
namespaces as listed. Everything English, UTF-8 with BOM.
