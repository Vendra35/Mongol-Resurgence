## 2. Mod Design — What We Are Trying To Build

### Concept
An alternate-history scenario, anchored to real history, answering the question:
"When the Yuan dynasty was driven out of China in 1368 (the Northern Yuan), what if
the Mongol tribes had genuinely reunified and launched a new wave of conquest westward?"

### The 3 Situations
1. **"The Northern Yuan Resurgence"** (~1368–1420) — the unification of Mongolia.
2. **"The Pax Mongolica"** (~1420–1550) — dominance over the Silk Road, a war for
   hegemony against the Ming.
3. **"The Silk Empire"** (~1550–1650) — westward advance against Russia, the final formable.

### Tags — WARNING: these came from the wiki but need re-confirmation (there is a history of contradictory information)

| Concept | Tag (claimed) | Status |
|---------|---------------|--------|
| Yuan | CHI (there may also be a separate version called YUA — clarify) | Uncertain, confirm |
| Chagatai | CHG | Said to be wiki-confirmed |
| Ilkhanate | Not a single tag — HLG (Hulaguids) + an International Organization called the Ilkhanate | Said to be wiki-confirmed |
| Golden Horde (Jochi) | GLH | Confirmed |
| Oirat | OIR | Confirmed |
| **Mongolia** (the birth target of Situation 1) | **MGO** — tier 3 formable | ⚠️ At one point confused with "MGE", then corrected. The previous AIs (DeepSeek/Cline) created a `00_formable_countries.txt` for my Mongol mod, but we do not need to — the MGO_f Mongolia formable already exists in the vanilla game files, so there is no need to overwrite it. The Prussian Destiny mod has a `00_formable_countries.txt` because NGC, the North German Confederation, does not exist in vanilla, so I created it there. |
| **Mongol Empire** (the final formable of Situation 3) | **MGE** — tier 4 formable | ⚠️ At one point this was confused with "Moghulistan". Verify it independently yourself. |

**Verify this tag table from scratch, independently, as the very first task.** The
previous AIs (DeepSeek/Cline) made claims that contradict each other — do not trust them.

> **Verification status (2026-07-21):** `MGO_f` and `MGE_f` are both confirmed to
> exist as vanilla formables, and MGO correctly has no starting country entry. The
> Yuan (CHI vs YUA) and Ilkhanate (HLG + International Organization) questions remain
> open. See `AUDIT-2026-07-21.md`.

### Architectural Principle: Dynamic Birth (No Fixed Tag)
Because the Asian steppe between 1337 and 1368 is so chaotic — unlike Brandenburg or
the Teutonic Order, which survive safely inside the HRE — the actor in Situation 1 is
bound **not to a fixed tag but to a dynamic trigger**:

- Use vanilla's **Timur emergence event** (`flavor_tim.8`, the event that "births"
  Timur out of Chagatai) as the reference.
- Trigger logic: "whoever holds Karakorum + has a steppe horde government + belongs to
  the Mongol culture group" → that country becomes MGO via
  `create_country_from_cores_in_our_locations`, or if we cannot convert directly,
  `form_country = formable_country:MGO_f` is run (exactly the same pattern as
  Prussian Destiny's `form_country = formable_country:PRU_f`).

### Two-Layer Failsafe System
**(a) Birth failsafe — Situation 1 only:** if no country organically satisfies the
trigger conditions by roughly 1370 (shortly after 1368), forcibly convert the most
suitable candidate in the region — the country holding the most Mongolia/Gobi
territory, with a steppe horde government and Mongol culture — into MGO.

**(b) Completion failsafe — in all three situations:** exactly the same logic as
Prussian Destiny's `PD_brandenburg_rise_auto_conquest_yes` /
`PD_the_prussian_ascension_auto_conquest_yes`: **5 years before** each situation's end
date, if the objectives have not been met, force completion during those final 5 years
by handing the AI free territory, vassals or war victories. (In the Prussia mod this
was applied at dates like 1495/1632 — use the same 5-year buffer logic.)

### Language Rule
**The entire mod is in English.** Situation names, event titles and descriptions,
decision names, localisation text and in-code comments — everything in English.
Namespace: `mongol_resurgence`, using a naming scheme parallel to Prussian Destiny's
`the_prussian_destiny` / `PD` pattern.
