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

## TEST LIST — a FRESH campaign, in this order

1. ~~**Does the init log go quiet?**~~ **DONE — MEASURED 2026-07-31.** All ten
   `initialize_from_bookmark.cpp` lines are gone for KAZ, IRA and MCH on a
   fresh campaign. One follow-up was needed and is also fixed and re-measured:
   `government.cpp:3544 Removing invalid policy 'polygyny' for 'KAZ Kazakh'`
   — the horde template's `marriage_law = polygyny` is gated on a pagan/hindu/
   indian country and KAZ is Sunni, so it is overridden with `muslim_marriage`
   the way vanilla's CHB and TIM override it. **A law arriving from an
   `include` is not guaranteed to fit the country that includes it.**
   That error also proved the additive file is genuinely loaded and merged:
   `polygyny` could only have reached KAZ through it.
2. **Do IRA and MCH spawn LEVEL WITH THEIR NEIGHBOURS?** This is the whole
   point of the new file, and it is a falsifiable prediction, not a hope.
   MEASURED by the author across earlier runs: **CRI came out of the Mongols
   already caught up**, while IRA and the Manchu heir were always behind. The
   only difference between them was the start block — so the mechanism is not
   a "catch-up" at all, it is simply EXISTING: a tag with a start block is
   instantiated at campaign creation and rides the world's age progression for
   313 years even while landless, whereas a tag with only an identity block
   does not exist until the moment it is handed land, and therefore starts
   from nothing.
   **Prediction: IRA and MCH now behave exactly like CRI.** If they do not,
   the mechanism is something else and the fallback is a curated
   `research_advance` list per heir (the only advance-granting effect EU5 has;
   no bulk grant is safe — the four `*_advance_definition` iterators have zero
   vanilla uses and nothing can filter them by age).
   Note `starting_technology_level` is NOT the lever here: it is an age-1-only
   knob (`0_age_of_traditions.txt:1`), 25 advances across 6 files carry it, and
   its only values are 1-4. MCH sits at 2 because
   `jianzhou_tribe_not_present` says so, which is where every Jurchen tribe on
   the map starts.
3. **Are the heirs the right faith?** CRI Sunni, MCH Tungusic Shamanist, IRA
   Shia — not Orthodox, not Tengri.
4. **Are the rulers named?** Haci, Jangir, Abbas, Aldar, Nurhaci, Erdeni,
   Abdullah — not generated strangers.
5. **What do the heirs render as?** "County of Kazakh" should be gone now that
   they have a government type. Check the country panel for each.
6. **Does the Qing take Manchuria at +32y and China at +48y?** MCH must appear
   at the Manchuria step now, not by forming Later Jin off a QNG spawn. And
   after the China step it should read "Qīng Empire" with the CHI flag.
7. Still never observed: **OIR (+26y) and CHG (+41y)**.
8. Still unmeasured: the **permanent Phase 1–3 reward modifiers** — strip,
   weaken or leave. Read what they actually give in
   `main_menu/common/static_modifiers/MR_modifiers.txt` before ruling.

---

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
