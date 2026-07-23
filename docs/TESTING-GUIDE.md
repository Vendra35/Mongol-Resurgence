# Mongol Resurgence — Testing Guide

A structured, phase-by-phase test plan for the mod. Run the tracks in order:
each later track assumes the earlier ones passed. Every checkpoint names the
file that implements the behavior, so a failure is immediately traceable.

Static verification cannot prove any of this — this document exists because
the only real test is the game on the Windows PC.

---

## 0. Setup for every test run

1. **Enable debug mode** (launch option `-debug_mode` or console `debug_mode`)
   so the console and error log are available.
2. **Logs** live in `Documents/Paradox Interactive/Europa Universalis V/logs/`:
   `error.log` (script errors) and `debug.log`. Console `Log.ClearErrorLog`
   clears the error count between checkpoints; console `error` shows errors.
3. **Useful console commands** (all verified against the wiki console page):
   - `observe` (or `ob`) — AI-only observer run
   - `tag MGO` — switch to a country / Ctrl+click a country to take control
   - `change_date <year>` — jump the date
   - `event mr_dominance.997 MGO` — fire an event at a target
   - `annex <TAG>` — instant annex (to fast-forward a conquest state)
   - `activate_situation <key>` / `monthly_situation <key>` — force-start a
     situation / manually tick one month of it
   - `YesMan` — AI accepts everything (useful for diplomacy states)
4. **Game rules to select at setup** (they only apply at game start):
   - *(MR) Mongol Resurgence Content* — Enabled
   - *(MR) Mongol Resurgence Conquest Automation* — Activated
   - *(MR) Imperial Expansion Conquest Automation* — Activated
   - *(MR) Mongol Military Buffs and Conquest Speed* — per track (below).
     This rule now ALSO sets the AI railroad's war pace (the separate
     Timeline & Pacing rule was removed): Terminator ≈ 6 months,
     Historical ≈ 1 year, Vanilla ≈ 2 years between Phase 1 wars.

**The standard full-campaign test** is an observer run started in 1337,
Historical buffs, left running with periodic checks at the checkpoint
dates below.

---

## Track 1 — Loading & localization (5 minutes, before anything else)

| # | Check | Expect | Implemented in |
|---|---|---|---|
| 1.1 | Game reaches main menu with the mod active | No crash; `error.log` has no `MR_` parse errors | everything |
| 1.2 | New-game screen → Game Rules | **Four** `(MR)` rules listed with **English names and descriptions** — no raw `rule_mr_railroad` / `setting_*` keys, and no Timeline & Pacing rule (removed) | `main_menu/common/game_rules/MR_game_rules.txt` + `main_menu/localization/english/MR_l_english.yml` |
| 1.3 | Situation list / hints in game | `Mongol Resurgence`, `Road to Empire`, `The Four Khanates`, `The Chahar Reunification`, `The Torghut Migration`, `The Dzungar Khanate` all show names and descriptions (no `mr_chahar_reunification` raw keys, no "TODO") | loc file, SITUATION NAMES section |
| 1.4 | `error.log` | ZERO `localization_util.cpp` errors for `war_goal_MR_*`, `mr_chahar_*`, `mr_torghut_*`, `mr_dzungar_*` | loc file |
| 1.5 | `error.log` | ZERO "variable … set but never used" warnings for `mr_history_*` | `MR_history_dhe_events.txt` (variables removed) |

---

## Track 2 — Phase 1: Mongol Resurgence (1368–1420)

Observer run from 1337. Buffs **Historical**.

| # | When | Check | Expect | Implemented in |
|---|---|---|---|---|
| 2.1 | 1337–1400 | Historical DHEs fire **on their real dates** (monthly_chance 100) | Ilkhanid succession ~1337 (one of JLY/CHB/MZF/INJ/GRG), Chagatai schism ~1347, Yuan decline ~1351 (NOT at game start — Red Turban timing), Tokhtamysh ~1380, Delhi sack ~1398 (TIM gets the loot event, DLH gets "The City of Ashes"), Oirat challenge ~1435, Babur ~1500. Each shows a DHE timeline `.entry` name, no `Mr history.N.entry` raw keys | `MR_history_dhe_events.txt` |
| 2.2 | ~1368 | Situation starts | `Mongol Resurgence` becomes active; opening event "The Eagle of the Steppe" goes to the steppe hordes | `MR_mongol_resurgence.txt` on_start |
| 2.3 | 1368 | Buff check | Steppe hordes have **Mongol Awakening** (historical buff), NOT "Mongol Warrior Spirit (Terminator)" — Terminator only under the Terminator rule | on_start buff branch |
| 2.4 | 1368–1375 | **error.log spam gone** | ZERO `Invalid right side during comparison 'c'` from `MR_mongol_resurgence.txt` (the old line-592 map_color spam) and from `MR_on_actions.txt` | map_color `owner ?= { tag = MGO }` |
| 2.5 | 1368–1375 | **Organic birth** | An **AI** horde that takes **Karakorum** becomes MGO on the spot; a **HUMAN** horde is offered the banner instead ("The Banner Offered" — accept to form MGO, decline to stay yourself). Otherwise the failsafe fires on 1375.1.1 and picks the **strongest free AI** horde (tiers: AI at peace → AI → anyone as absolute last resort, with a subject released by its overlord first) | on_monthly organic birth + `mr_dominance.11` + tiered birth failsafe |
| 2.6 | MGO+1 month | The Great Khan | "A New Khan Rises" fires; MGO's ruler is a **new ~30-year-old Borjigin** ("Batu") with **The Scourge of the Steppe** + **Historically Needed** modifiers and the Conqueror/Tactical Genius/Strategist/Cruel traits | `mr_dominance.104` |
| 2.7 | same month | AI lock | AI MGO has **Mongol War Preparations** (localized name, not a raw `STATIC_MODIFIER_NAME_` key) | beat-104 block + loc |
| 2.8 | ~1 year later | Railroad war | MGO declares a unification war on a weak Mongol neighbour with the *Unification of the Steppe* CB; war goal shows "**Unify the Steppe**", not a raw key | on_monthly declare + `mr_dominance.997` + wargoal loc |
| 2.9 | ongoing | War cadence (buff rule only) | Historical ≈ one war per year; Vanilla (no buffs) ≈ one per ~2 years; Terminator ≈ one per ~6 months | declare-block pacing OR |
| 2.10 | any time | Panel | Situation panel: dual portraits render (no black boxes), both cards show "Score: N" with **different** numbers for leader vs rival; the rival is the **strongest** other steppe horde, not a random distant one | `mongol_resurgence.gui` + monthly score block + ordered_country rival pick |
| 2.11 | 1415 | Completion failsafe | If goal unmet and MGO is AI: rest of mongolia_region transferred to MGO, surviving hordes become tributaries — **even mid-war** (the P1 at-peace gate was deliberately removed so an endless war cannot stall it; P2/P3 failsafes still require peace). **Re-run with the rule Deactivated: this must NOT happen** | on_monthly failsafe (rule-gated) |
| 2.12 | on success | Phase end | "The Rise of the Great Khan" fires; **phase buffs disappear** from every horde (check a rival khan's modifier list too); MGO gets the reward tier matching the buff rule; AI MGO gains The Sleeping Horde. **On a FAILED Phase 1 (timeout), AI MGO must NOT get The Sleeping Horde** — it would be war-locked forever with no Phase 2 to lift it | on_ending + `mr_dominance.1` + success-gated on_ended grant |
| 2.14 | ~1378+ | Census DHE | "The Count of the Herds" fires once MGO holds Karakorum — manpower burst (count the men) or gold + horde unity (count the herds) | `mr_dominance_dhe.12` |
| 2.13 | after end | Variables | Save file / console: situation variables (`mr_conquest_*`, `MR_mgo_score`…) are gone | on_ended |

---

## Track 3 — Phase 2: Road to Empire (1420–1550)

Continue the same observer run.

| # | When | Check | Expect | Implemented in |
|---|---|---|---|---|
| 3.1 | ~1420 | Situation starts | `Road to Empire` active; The Sleeping Horde and the Phase 1 reward modifier are **removed** from MGO; the phase buff matching the buff rule is applied; a **new second-generation Great Khan ("Adai")** is enthroned with the Scourge modifier and Conqueror/Born to the Saddle/Strategist traits | `MR_mongol_imperial.txt` on_start + `mr_dominance.120` |
| 3.2 | 1420+ | CBs granted | MGO has *Mastery of the Silk Road* CBs against holders of north_china / xinjiang / khorasan / persia land | on_start CB loop |
| 3.3 | any | Panel header | Portrait renders (NOT black) — the header now overrides the correct `CountryContext`/`character_portrait_anchor` blocks; the Character/`GetCourtCountry` error spam from `pdx_data_callstack` is **gone** while the panel is open. Also confirm no `'textbox_single' is not a valid widget` / `'progress' is not a valid widget` errors at game start | `mongol_imperial.gui` header + widget fixes |
| 3.4 | any | Progress card | "Imperial Expansion Progress" card shows a **score line and a working bar** that fills: +25 Samarkand, +25 Dadu, +25 Khorasan+Xinjiang cleared, +25 North China cleared. (This card is the phase's 0–100 goal meter — that is why it exists) | monthly `MR_mge_score` block + `text_single`/`progressbar value=` fix |
| 3.5 | map | Red lines | Goal drawing covers khorasan + **xinjiang** + north_china as one contiguous band (no gap in the middle) | secondary_map_color |
| 3.6 | 1545 | Completion failsafe | If goal unmet, AI, at peace: all three goal regions handed over. With *Imperial Expansion Conquest Automation* Deactivated: nothing happens | on_monthly failsafe (rule-gated) |
| 3.7 | on success | **THE PROCLAMATION** | The moment Phase 2 completes, **MGE is formed** (`form_country`, bypassing MGE_f's allow block): the claimant becomes the **Yeke Mongol Ulus** at empire rank, gains vanilla's *Restoration of the Mongol Empire* modifier (50y, from MGE_f's form_effect), and "The Yeke Mongol Ulus Proclaimed" fires. Imperial phase buff **and Mongol War Preparations** removed; Empire Fulfilled granted (not under Vanilla buffs). The country name must show "Yeke Mongol Ulus" — and the `MGE has the name 'empire'` warning must be gone from the logs | on_ending + `mr_dominance.125` |
| 3.8 | 1420–1550 | DHE layer | Wall Breakers / Silk Road Reborn / Imperial Encampment / **Karakorum Restored** fire for AI MGO (free buildings/units via *Khan's Decree*, Karakorum becomes a city with a market); **The Observatory of Samarkand** (~1424, Samarkand owned) fires for player AND AI | `MR_dominance_dhe_events.txt`, `mr_dominance.995/996` |
| 3.11 | ~1449 | **Tumu reaction (moved)** | If vanilla's Tumu Crisis goes live (`lost_emperor`), "The Emperor in a Tent" now fires DURING Phase 2 to the Mongol hordes — it was previously watched only by the 1604 Chahar situation and could never fire | P2 on_monthly Tumu watch |
| 3.9 | 1420+ | AI lock | AI MGO carries **Mongol War Preparations** for the whole phase (blocked from freelance wars) | on_start preparing grant |
| 3.10 | ~1 year in, then every ~5 | **Phase 2 railroad** | "The Horde Rides for the Silk Road" fires and MGO declares on a weak corridor neighbour with the silk-road CB (~yearly under Terminator). The AI expands into the corridor even though it cannot declare on its own | find/declare loops + `mr_dominance.993` |

---

## Track 4 — Phase 3: The Four Khanates (1550–1650)

MGE now exists from the phase's first day (proclaimed at Phase 2's close).

| # | When | Check | Expect | Implemented in |
|---|---|---|---|---|
| 4.1 | ~1550 | Situation starts | `The Four Khanates` active for **MGE**; Empire Fulfilled removed; Pax Mongolica (or historical variant) applied; a **third-generation Great Khan ("Altan")** enthroned with Tactical Genius/Inspiring Leader/Expansionist | `MR_mongol_dominance.txt` on_start + `mr_dominance.130` |
| 4.2 | 1550–1650 | **error.log** | ZERO `Invalid right side` errors from `MR_mongol_dominance.txt` — MGE existing from day one removes the old error class entirely; the MGO fallback stays guarded | tag = rewrites + P2-end formation |
| 4.3 | any | Panel | Header portrait renders from MGE; progress bar counts ten 10-point goals: Karakorum, Dadu, Samarkand, Sarai, Kazan, **Tabriz, Baghdad, Persia cleared**, Russian foothold, **Cappadocia foothold** | gui + `MR_dominance_score` |
| 4.4 | 1645 | Completion failsafe | If unmet, AI, at peace: upper_selenga/beiping/transoxiana/lower_don/kazan/**iraq_arabi/cappadocia**/ryazan areas **plus ALL of persia_region** handed to the claimant (rule-gated as in 3.6) | on_monthly failsafe |
| 4.5 | on success | The finale | "The Eternal Empire" fires; Pax Mongolica **and Mongol War Preparations** removed; Mongol World Order granted (not under Vanilla buffs); `mr_railroad_complete` set. (The on_ending form_country is now only a fallback — MGE should already exist) | on_ending |
| 4.6 | alt run | Failure | Let it time out (rules off): "The Empire Crumbles", failure modifiers, `mr_railroad_failed` set — and the late-steppe situations can then still fire | on_ending else |
| 4.7 | 1550+ | AI lock | AI claimant carries **Mongol War Preparations** for the whole phase | on_start preparing grant |
| 4.8 | ~1 year in, then every ~5 | **Phase 3 railroad — WATCH ITEM** | "The Ulus Calls for Riders" fires; the CB matches the target's land (Rus/Pontic/Ural/**Persia/Anatolia/Mesopotamia** theatre → *The Westward Advance*, the China/Transoxiana seats → *Mastery of the Silk Road*). **If no P3 railroad war EVER fires, the prime suspect is the claimant-scope comparison** (`scope:mr_dom_claimant.offensive_alliance_strength`, the one construct with no exact PD twin) — report it and it gets rewritten as two fixed-tag branches | find/declare loops + `mr_dominance.992` |
| 4.9 | any | Railroad continuity | The claimant scoping is dynamic (MGE normally, MGO on the failed-proclamation fallback); the war event's after-block re-seeds the target with the firing country | random_country claimant + 992 after |
| 4.10 | when true | The Four Corners | The month the claimant owns Karakorum + Dadu + Samarkand + Sarai simultaneously, "The Four Corners" fires once (major, prestige + horde unity) | P3 on_monthly + `mr_dominance.135` |

---

## Track 5 — Player-controlled MGO (the human experience)

Take the claimant (Ctrl+click or `tag`) before MGO forms, or play a horde from 1368.

| # | Check | Expect | Implemented in |
|---|---|---|---|
| 5.1 | Railroad events as a player | "The Kurultai Demands War" (P1), "The Horde Rides for the Silk Road" (P2) and "The Ulus Calls for Riders" (P3) all appear as **visible events with two options**; option B postpones the war (no war declared, targeting resets, event returns after the cooldown) | `mr_dominance.997/.993/.992` PD-103/203 shape |
| 5.2 | No AI lock | A human claimant NEVER has Mongol War Preparations, in any phase (can declare wars freely) | `is_ai` gates at beat-104 / P2 on_start / P3 on_start |
| 5.3 | No sleeping lock | After Phase 1 ends, a human MGO does NOT get The Sleeping Horde | on_ended `is_ai` gate |
| 5.4 | Failsafes don't rob the player | Own some mongolia_region land as a NON-claimant at the 1415 failsafe: your locations must NOT be transferred | failsafe `is_ai` owner filter |
| 5.5 | Great Khan as a player | On forming MGO you also get the new Borjigin ruler + Scourge modifier; at Phase 2 and Phase 3 starts the succession khans (Adai, Altan) replace your ruler too — this is the railroad's signature, human or AI | `mr_dominance.104/.120/.130` |
| 5.6 | Late-steppe rewards | Chahar success grants **The Seal of Chinggis**; the Torghut arrival grants **The Volga Pastures**; Dzungar consolidation grants **The Dzungar Legacy** — none of them re-grant the Phase 1 banner | `MR_late_steppe_events.txt` + MR_modifiers |
| 5.7 | The Banner Offered | Take Karakorum as a human horde pre-1375: "The Banner Offered" fires ONCE. Accept → you become MGO (and Beat 104 enthrones the Great Khan next month). Decline → you stay yourself, the event never returns, and the 1375 failsafe converts an **AI** horde instead — never you (unless zero AI Mongol hordes remain on the steppe) | `mr_dominance.11` + AI-preferring failsafe tiers |
| 5.8 | Self-formed MGE (Vanilla buffs) | Under *Vanilla (No Buffs)* — the only tier without `blocks_country_formation` — manually form MGE mid-Phase-2 with the nine formable seats: the phase must still be COMPLETABLE (end trigger and resolution are dual-tag) and Phase 3 must start normally | dual-tag `mr_imperial_end_trigger` + P2 on_ending |

---

## Track 6 — Late-steppe situations (1600s)

Fastest path: a fresh observer run, `change_date 1604` (or wait), with the
railroad failed or off-track so the steppe is fragmented.

| # | Check | Expect | Implemented in |
|---|---|---|---|
| 6.1 | Chahar (1604–1634) | Starts only when NO MGO/MGE dominates the heartland; "The Last Great Khan" fires; ends when one Mongol power holds Karakorum + a North China foothold | `MR_late_steppe.txt` + triggers |
| 6.2 | Chahar × Tumu | Fallback watcher only: the Tumu reaction normally fires from Phase 2 (~1449, see 3.11). The Chahar-era watcher can only matter in exotic runs where a crisis is somehow live after 1604 — `fire_only_once` on the event guarantees it never double-fires | `mr_vanilla_tumu_crisis_active` |
| 6.3 | Torghut (1616–1630) | Starts if a Mongol horde sits in xinjiang/khorasan and none owns Sarai; Urals beat ~4 years, Volga beat ~8; ends only after the Urals beat + Sarai owned | `MR_late_steppe.txt` |
| 6.4 | Dzungar (1634–1650) | Consolidation beat once a horde holds xinjiang + zhetysu presence; ends on Dzungaria+Tarim+Zhetysu after the beat | `MR_late_steppe.txt` |
| 6.5 | All three | Names/descs localized; timeout tooltips render; no `Invalid right side` from their visibility triggers (OIR/MGO/MGE may all be dead by now) | loc + `tag =` visibles |

---

## Track 7 — Rules-off and off-switch runs

| # | Check | Expect |
|---|---|---|
| 7.1 | Master rule **Off** | No MR situation ever starts, no MR DHE fires, no on_action pulse runs. `error.log` stays free of MR entries |
| 7.2 | Both auto-conquest rules **Deactivated**, buffs **Vanilla** | Situations still run and can succeed organically or fail on timeout; no territory is ever auto-transferred; no MR buff modifiers ever appear |
| 7.3 | Terminator buffs | Warrior Spirit (Terminator) applied; railroad wars every ~6 months; the AI is visibly monstrous |

---

## Track 8 — Log hygiene (after any full run)

Grep `error.log` for these; all should be **absent**:

- `Invalid right side during comparison 'c'` anywhere in `common/situations/MR_*`
  or `common/on_action/MR_*`
- `localization_util` errors mentioning `MR_`, `mr_`, `war_goal_MR`,
  `mr_history` (the `.entry` keys now exist)
- `set but never used` mentioning `mr_history_`
- `pdx_data_callstack` / `EVENT_CHARACTER_FOREIGN` spam while an MR situation
  panel is open
- `country_database.cpp` — `MGE has the name 'empire' in it` (renamed to
  Yeke Mongol Ulus)
- `pdx_gui_factory` — `'textbox_single' is not a valid widget` /
  `'progress' is not a valid widget`
- `Event target link 'owner' returned an invalid object` (failsafes now use
  `owner ?=`)

**Known, harmless, watch-only:** `Unknown formatting tag 'l'` while a
situation panel is open. It is emitted by a vanilla-localized string for the
horde ruler/regency (the mod's own text contains no `#l` — verified
byte-level); expect it to appear for the P2/P3 panels too now that their
headers render. If it ever changes from log noise to a visible text glitch,
bisect by temporarily blanking the header text elements.

Anything new that appears with `MR_` in the path: report it with the exact
line, the date it started, and what was on screen — that is the next bug.
