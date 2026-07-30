# HANDOFF — resume here

Written 2026-07-30, end of the Great Partition work session. Read this
first, then `Debug-and-Test-Results.md` from the bottom up.

---

## State: everything is committed, working tree clean

```
821665b  Great Partition: the Khaghan feels it, the heirs survive it, the steppe goes home
f95e454  Great Partition: fix the ownerless-ground bug, and make history resume
8e5f064  Balance pass: faster P3 war pace, cheaper conquest, wider assimilation
```

`tools/verify_mod.py` — 34 checks, all green. **Nothing below has been
tested in game.**

---

## The one thing that must not be forgotten

**An existing save cannot test any of this.** `mr_partition_collapsed`
is already set in the save where the endgame was observed, and
`mr_can_start_partition` refuses to reopen a resolved partition. The
Great Partition and the horde lock both need a **fresh campaign**.

---

## What was done, in one paragraph each

**The bug that started it.** All eight `mr_ulus_*_held` triggers negated
`mr_in_claimant_realm` on a location. That trigger opens with
`has_owner = yes`, so the negation read "nobody can ever own this" as
"we have lost this" — and every geography atom contains lakes,
impassable mountains and non-ownable ground (heartland 50/263, tarim
34/88). The partition therefore opened and resolved inside one month.
Fixed to the `owner ?=` shape the phase goals always used.
`verify_mod.py` now fails on any reintroduction and carries a canary.

**History resumes.** Fourteen theatres return to the power that held
them around 1650-1700, on a clock driven by `mr_partition_momentum`
with a backstop year ladder. One scripted effect each in
`in_game/common/scripted_effects/MR_partition_effects.txt`, called from
both `on_monthly` (on schedule) and `on_ending` (final sweep).

**The Khaghan feels it.** Three decline tiers on the 85/55/40 beats,
removed at the top of `on_ending`. **The heirs survive it.**
`MR_ulus_of_its_own`, 25 years, on all fourteen. **Ranks** set with
vanilla's upgrade-only ratchet on five of them.

**The steppe goes home.** Three more atoms folded into existing
theatres. The Khaghan ends with **379 locations**: `mongolia_region`
213 plus transoxiana 96, khwarazm 32, badakhshan 38. Nothing in
`steppes_region`. Two seats survive, Karakorum and Samarkand.

**The horde stays a horde.** `TRY_REPLACE:horde_list` in
`in_game/common/generic_action_ai_lists/zz_MR_government_transition_addon.txt`
blocks vanilla's `steppe_horde_to_monarchy` for an AI MGO/MGE until
`mr_railroad_complete` (or `_failed`, or the master switch is off).

---

## UNFINISHED: heir government type and capital

A second workflow was running when the session ended. Its run id:

```
Workflow({scriptPath: "<session>/workflows/scripts/mr-heir-identity-wf_8c20f1b8-f99.js",
          resumeFromRunId: "wf_8c20f1b8-f99"})
```

Completed agents replay from cache; check
`<session>/subagents/workflows/wf_8c20f1b8-f99/journal.jsonl` for what
already finished before assuming anything is lost. If the run is gone,
the four research briefs are in the script file and can simply be
re-run.

**The question it was answering.** The heirs arrive with **no authored
government type and no authored capital**, because a tag brought onto
the map by `change_location_owner` is instantiated from its
`setup/countries` identity block alone and that block sets neither.
This is the root cause of "County of Kazakh" — rank only moves it to
"Sultanate of Kazakh"; **government type decides the noun, not rank**.
The user's ruling: author both.

**THE TRAP, and the reason this needed research rather than a quick
edit.** Nine of the fourteen heir tags are already alive on the 1337
map with their own capitals and governments — MOS, TUR, TIB, KOR, CHG,
OIR, CRI, NOG, BSH. Calling `set_capital` or `change_government_type`
on those would **move a living country's capital and rewrite its
government**. Only tags that spawn from nothing need authoring, and the
spec must mark the rest DO NOT TOUCH.

Other things that workflow was checking: whether an uncored 2050-location
QNG is a problem, whether a spawned country gets a ruler at all, and
what each heir literally renders as (`rank_empire_tribe` is "Tribes"
and outranks every culture branch, so a tribe-government heir at empire
rank reads "Persian Tribes").

---

## Open decisions, none blocking

- **`horde_unity_hit_at_ruler_death = -25`** is an unattested magnitude
  — vanilla only ever writes the `-50` base and a `+50` mitigation.
  Halve it to `-10` if the succession loss plays too hard.
- **`MR_l_english.yml:311` overrides `rank_empire_horde` to "Empire"
  GLOBALLY.** That is what makes MGE read right, but vanilla OIR starts
  at `rank_empire`, so "Oirat Empire" is on the map from 1337 with the
  mod installed. Pre-existing; decide whether it is intended.
- **The four sibling rebel-growth lines** in
  `MR_imperial_failure_ai/_player` and `MR_dominance_failure_ai/_player`
  (+0.0025). These are failure-state modifiers — the railroad is
  already over when they land — so they are defensible, but they want
  the same explicit ruling `MR_kurultai_defied` just got.
- **QNG ships no coat of arms**, so it will draw a generated one.
  Vanilla ships 280 landed tags the same way and errors nothing.
  Reusing the CHI arms is vanilla's own choice if fidelity matters.

---

## In-game test list, in priority order

1. **Does the schedule fire?** ~4 years after the partition opens
   Crimea should go, ~8 years Kazakh. If nothing moves, suspect the
   `var:mr_partition_momentum` comparison first.
2. **Do IRA and QNG reach the map?** Same probe KAZ passed. Two new
   identity blocks in `zz_mr_new_countries.txt`.
3. **Does the AI Khaghan stay a horde?** If it converts to monarchy
   before Phase 3 ends, the `TRY_REPLACE:` prefix did not take in
   `generic_action_ai_lists` — that folder is one step beyond where the
   prefixes have been measured. Plan B is `TRY_REPLACE:steppe_horde_to_monarchy`
   under `generic_actions/`, the folder REAI proves.
4. **Does the end-condition panel show three unticked lines** at the
   opening, and does the cohesion bar start at 100?
5. **Does the cohesion ladder run** 100 → 92 → 80 (beat 85) → 72 → 62
   → 54 (beat 55, and neighbours get `cb_MR_carve_the_ulus`) → 42 → 30
   (beat 40, and the situation ends)?
6. **`cancel_subject` on Korea** — first use of that construct in this
   mod.
7. **What the heirs are called**, and whether their country panels show
   a government type and a sane capital.

---

# UPDATE — after the first live Great Partition run (same day)

**Three more commits.** `821665b` decline tiers + grace + ranks + the last three
theatres; `e5b4b31` the three silent failures the live run exposed. Working tree
clean, 34 checks green.

## What the run proved WORKS — do not re-investigate

The schedule fires. `mr_partition_takeable` is sound (the Kuban and Yedisan,
which only the schedule can reach, went Crimean). The backstop date ladder is
what actually fires everything — the momentum clause has never fired anything in
a real campaign, because the situation opened 1650 and the backstops run
1650→1702. The grace modifier and the rank calls apply. KAZ revives from
landless.

## THE LAW THAT COST THE MOST TO LEARN

**A campaign in progress cannot gain a country tag.** The country database is
minted once, at campaign creation. IRA and QNG were added to `setup/countries`
after that save existed, so `c:IRA` does not exist in it at all and
`change_location_owner` into it did nothing, silently. Console `tag IRA` →
*"country is not valid"*. **Any change under `setup/countries` means a new
campaign is required to test it.**

## STILL UNWRITTEN — the heir identity pass

Specified in full, not yet in the code. The spec files are in the session
scratchpad under `agents/`, `-f99-09-FINAL-heir-identity-spec.md` being the
merged one, with a verified per-heir table.

The heirs arrive with **no government type, no capital, no culture, no
religion** — an identity block sets none of those at runtime. That is why CRI
came out **Orthodox** despite its block saying `sunni`, why names render as
"County of Kazakh", and why vanilla's `propose_ruler.txt:29` now errors forever
(see the decoder).

**THE TRAP:** five of the heirs are live 1337 countries with working capitals —
**MOS/RUS, NOG, TUR, TIB, KOR — DO NOT call `set_capital` on them.** Verified
capital keys for the ones that do need it: CRI `qarasuvbazar`, KAZ `shavgar`,
IRA `isfahan`, BSH `sterlitamak`, QNG `shenyang` then `dadu`, OIR `hoboksar`,
CHG `yarkand`. Several obvious guesses are wrong: `bakhchisaray` does not exist,
`ufa` is in `perm_area` and outside BSH's grant, `turkestan` is in
`transoxiana_area`, `gulja` goes to KAZ.

Also still open: the pacing table (the player finds the western theatres late),
the AI personality swap at partition start, whether to strip the permanent Phase
1–3 rewards, and successor map colours in the situation map mode.

## NEXT TEST — fresh campaign, in this order

1. Does Persia produce IRA on its backstop? (New campaign is the whole point.)
2. Does Ufa go Bashkir? (`change_country_type = location` fix.)
3. Do the successors hold their ground instead of dissolving? (cores fix.)
4. Does cohesion fall monotonically and reach 40? (ratchet + concessions cap.)
5. Do OIR (+40y) and CHG (+56y) spawn? Both are `country_type = army`, untested.
