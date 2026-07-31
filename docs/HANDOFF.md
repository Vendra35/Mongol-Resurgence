# HANDOFF — resume here

Written 2026-07-31. Read this first, then `Debug-and-Test-Results.md` from the
bottom up (the 31.07 entry is the current one).

---

## The one thing that must not be forgotten

**A NEW CAMPAIGN IS MANDATORY.** This session added
`main_menu/setup/start/28_MR_countries.txt` and moved an identity block from
QNG to MCH. Setup is read exactly once, when a campaign is created. No existing
save — not even yesterday's — can show any of it.

---

## What this session did

Yesterday's live run left three symptoms. They turned out to have **one root
cause**, and the author's own observation is what proved it: *"it didn't happen
to Crimea, but it happened to IRA and MCH."*

**The root cause.** KAZ, IRA and QNG had identity blocks in
`in_game/setup/countries/` and **no start block** in
`main_menu/setup/start/10_countries.txt`. That combination occurs **zero times
in vanilla** — 2337 of 2337 real tags have both, and the only three exceptions
are the engine's reserved DUMMY/PIR/MER. Government type, heir selection,
capital, **map discovery**, laws, society values, parliament type,
`religious_school` and `starting_technology_level` all live in the start block.
CRI has a landless one (`10_countries.txt:4195-4222`); that is the entire
difference.

**Fixed.** New file `main_menu/setup/start/28_MR_countries.txt`, **no BOM**,
additive filename, shapes copied from vanilla's own landless blocks — KAZ from
TIM (`:48847`), IRA from FEZ (`:19464`), MCH from DNG (`:49828`). Each
capital verified to lie inside its own discovery template.

**QNG is not a tag.** Vanilla's Qing is MCH renamed (`flavor_MCH.txt`
:1024-1030). The old QNG registration worked only by luck: it spawned, matched
`MCH_f`'s jurchen potential because it held all of Manchuria, and the AI formed
Later Jin. The block now sits on MCH — which also buys the real Manchu coat of
arms, `map_MCH`, the six `country_MCH.txt` advances and the `flavor_MCH` chain.

**`form_country` re-tags when the target tag is free.** Measured on both
branches in one campaign. So the China theatre now runs **land first, seat and
rank next, proclamation last**, holding the country by `save_scope_as` rather
than by tag. That also makes it immune to vanilla's own `flavor_mch.17`
(`tag = MCH`, `monthly_chance = 100`), which can proclaim the Qing sixteen
years early on its own.

**A handover is not a release**, so `religion_definition` and
`culture_definition` are never read — they are release-time fields. Seven heirs
now write their identity by hand: `create_character` + `set_new_ruler` +
`change_religion` + `change_religion_for_ruler_and_family` + `change_culture`,
with historical names and `age = 35` rather than `birth_date`.

**Harness 34 → 36**, all green:
- the BOM check is **inverted** for `main_menu/setup/start/` (the one tree that
  refuses a BOM — a BOM there makes the file silently inert);
- **new:** `land is only handed to registered tags` — every
  `change_location_owner = c:X` must name a tag with an identity block.
  Formable targets (MGO) and `define_unique_country_tag` mints are exempt,
  because neither creates a country from nothing. **Break-tested**: pointing a
  handover at an unregistered tag is caught;
- **new:** `mod-registered tags have a start block`.

---

## TEST LIST — ALL CLOSED, MEASURED IN GAME 2026-07-31

The whole fourteen-theatre schedule was watched end to end on a fresh campaign
and came out right: Crimea, the Kazakhs, Persia, Manchuria, Dzungaria, Tibet,
China, Korea and the Tarim — each on its own date, with the right faith, an
era-correct named ruler, researched advances and a visible map.

What that settles, none of it inferred:

1. **The init barrage is gone.** Zero `initialize_from_bookmark.cpp` lines for
   KAZ, IRA and MCH.
2. **The technology question is answered, and it was never a catch-up
   mechanic.** A tag with a start block is instantiated at campaign creation
   and rides the world's age progression even while landless; a tag with only
   an identity block does not exist until it is handed land. IRA and MCH now
   behave exactly like CRI. No `research_advance` list was needed.
3. **Religion, culture, ruler and dynasty all take** from the hand-written
   identity block — Crimea Sunni with Islam III Giray, the Kazakhs Sunni with
   Jangir Borjigin.
4. **"County of Kazakh" is gone**, because government type now comes from the
   start block.
5. **The Qing arrive as MCH** and the proclamation runs last, after the land.
6. **Korea returns.** Its sweep had been buried inside `country_exists = c:KOR`
   — the only one of the fourteen written that way — so an annexed Joseon could
   never come back. Fixed; the guard now wraps only `cancel_subject`.
7. One follow-up surfaced and was fixed and re-measured on the way:
   `government.cpp:3544` removing `marriage_law = polygyny` from a Sunni KAZ.
   **A law arriving from an `include` is not guaranteed to fit the country that
   includes it.** That error was also the proof the additive setup file loads
   at all.

## Open decisions, none blocking

- **CHG's religion.** The tag's own database entry is `tengri`
  (`east_asia.txt:2224`) and that is what the partition writes. The real
  Yarkand Khanate was Muslim by 1650. Changing it is a design call, not a bug
  fix.
- **`horde_unity_hit_at_ruler_death = -25`** is still an unattested magnitude.
- **`MR_l_english.yml:311` overrides `rank_empire_horde` to "Empire"
  GLOBALLY**, so vanilla OIR reads "Oirat Empire" from 1337. Pre-existing.
- **The four sibling rebel-growth lines** in `MR_imperial_failure_ai/_player`
  and `MR_dominance_failure_ai/_player` (+0.0025) still want an explicit
  ruling.

---

## For the 1066 Test Mod (found while auditing it, NOT fixed — that repo's call)

- **DEFINITE:** `ABS` and `FAT` have no `parliament_type`. They are the only
  two landed country blocks in the entire game, mod or vanilla, in that state
  — the 2026-07-30 fix restated three of the four things a template supplies
  and missed the fourth. The string `parliament` appears nowhere in
  `build_setup.py` or its `verify_mod.py`.
- **SUSPECT:** nine landed tags whose capital they neither own nor claim
  (`AAL ETA FDL FRI HLG JLM ORM QUN SLD`) — vanilla ships nine of the same
  class, and all nine still discover their capital, so it is tolerated.
  `CAPITAL_FIXES` exists and was not applied to them.
- **SUSPECT:** `DUB` and `ULD` write `starting_technology_level = 3` over
  `gaelic_tribe`'s own `2`; all 29 vanilla users of that template write none.
- **SUSPECT:** nothing in either tool joins the identity registry to the start
  blocks. The correspondence holds by discipline. MR now has that check —
  porting it back is four lines.
