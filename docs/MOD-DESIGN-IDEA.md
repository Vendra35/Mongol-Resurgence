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
- **AI railroad**: monthly loop picks the weakest valid neighbour holding Mongolian
  land (`ordered_neighbor_country`, `defensive_alliance_strength <` ours), then
  `declare_war_with_cb` via hidden `mr_dominance.997`; pacing ~1 war/decade on the
  historical rule, ~1/4yr otherwise; invalidated targets are cleared and re-picked.
- Ends when MGO owns Karakorum and has presence in both Gobi areas.

### Phase 2 — The Pax Mongolica (situation `mongol_imperial`, 1420–1550)
Mastery of the Silk Road and the hegemony contest with the Ming. The corridor is
**khorasan_region** (Transoxiana/Khwarazm/Zhetysu) plus north China — *not*
`steppes_region`, which is the Pontic steppe. Campaign beats from `mr_imperial.100–103`;
silk-road CBs granted against corridor powers. Ends when MGO owns Samarkand + Dadu
with Transoxiana presence.

### Phase 3 — The Silk Empire (situation `mongol_dominance`, 1550–1650)
The westward advance and the final formable. The end condition is exactly
**MGE_f's own nine required locations** (Karakorum, Sarai al-Jadid, Kazan, Samarkand,
Kaffa, Dadu, Shangyuan, Baxian, Guangzhou — nine different regions), so finishing the
phase means the Mongol Empire is genuinely formable; `on_ending` then forms MGE.
Two CBs are granted to cover both theatres: westward (russian/steppes/ural) and a
re-grant of the silk-road CB (the China/Transoxiana seats) — the Phase 2 grant
expires decades earlier.

## Two-layer failsafe system (as implemented)
**(a) Birth failsafe** (Phase 1 only): if no country organically takes the claim by
1375, the best-placed steppe horde is force-converted with
`form_country = formable_country:MGO_f` (hidden bookkeeping: `mr_dominance.998`).

**(b) Completion failsafes** (all three phases, 5 years before each deadline —
1415/1545/1645): if the goal is unmet, the goal territory is handed over outright —
`change_location_owner` + `add_core` by area/region iteration, rival hordes made
tributaries in Phase 1 — mirroring PD's `every_ownable_location_in_area` pattern.
Guards: fires only for an **AI** claimant that is **at peace**; takes locations only
from AI owners; each phase has its own one-shot flag (`mr_failsafe_p1/p2/p3_fired`).
`mr_dominance.999` then grants the means to hold the territory.

A human player who fails a phase is allowed to fail: every situation also ends on
**time expiry**, the failure branch fires (`mr_dominance.2/.127/.133` + AI/player
failure modifiers), and `mr_railroad_failed` is set on every failure path.

## The late-steppe situations (standalone, 1600s)
Vanilla has zero content for these (verified). They enrich the Phase 3 era and are
built on real tags (OIR/MGO/MGE) since the successor states have none:
- **Ligdan Khan and the Chahar** (1604–1634): the last Chinggisid's failed
  reunification — the dark mirror of Phase 1. Fires when the steppe is *fragmented*
  (including after a failed railroad; not when MGO/MGE dominates). Reacts read-only
  to a live vanilla Tumu Crisis (`has_variable = lost_emperor`).
- **The Torghut Migration** (1616–1630): the Kalmyk trek to the Volga — the Phase 3
  premise, historically real. Gated so it neither starts moot (a horde already on
  the Volga) nor ends before the trek happens (Urals beat gates the end).
- **The Dzungar Khanate** (1634–): the last steppe empire. Its steppe is the
  **Kazakh** steppe (`zhetysu_area`, khorasan_region). End trigger is strictly
  stronger than the consolidation beat so it cannot end the month the beat fires.

Deliberately **not** built (vanilla already implements them): Tumu Crisis
(`flavor_chi_mon.1–7` + `recapture_emperor`), Treaty of Ugra (`flavor_MOS`/
`flavor_LIT` + trust bias — its variables are transient, so no hook is possible),
Altan Khan's conversion (`buddhism_events.13`).

## Historical DHE layer (namespace `mr_history`, 1335–1530)
Real-history anchoring with `historical_info` boxes and `historical_option` markers:
the Yuan's last stand (CHI), the Ilkhanid succession (JLY/CHB/MZF/INJ/GRG — **not**
HLG, which has zero vanilla uses; the Ilkhanate died in 1335, pre-start), the
Chagatai schism (CHG), Tokhtamysh (GLH), the sack of Delhi (TIM vs DLH), the Oirat
challenge (OIR), Babur (TIM). Emergent-tag DHEs are valid (vanilla uses
`dynamic_historical_event tag = TIM` 15×).

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
| Mongol Empire | **MGE** via `MGE_f` (tier 4) | nine required locations (see Phase 3) |

## Game rule
`mr_railroad` (main_menu): `mr_railroad_historical` (default — DHE anchoring, slow
AI pacing, historical-mode modifiers) / `mr_railroad_divergent` (aggressive pacing) /
`mr_railroad_off`. Loc lives in **main_menu** yml (`rule_`/`setting_` convention).

## Naming
Files/variables `MR_`, triggers/vars `mr_`, CBs `cb_MR_*`, wargoals `MR_war_goal_*`,
namespaces as listed. Everything English, UTF-8 with BOM.
