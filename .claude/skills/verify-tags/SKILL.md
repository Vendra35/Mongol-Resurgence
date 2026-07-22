---
name: verify-tags
description: Resolve EU5 country tags, formable countries, location, region and culture names against the vanilla game files and the wiki before they are used in mod code. Use whenever a tag like MGO/MGE/CHG/GLH, a formable, or a location/region identifier appears in a task, a design doc, or existing MR code. Tags are always exactly 3 letters.
version: 0.1.0
---

# Verify Tags and Named References

## Why this exists

The MOD-DESIGN-IDEA tag table is explicitly marked unverified, and its history is
contradictory: MGO was confused with MGE, MGE was confused with Moghulistan,
Ilkhanate turned out not to be a single tag at all. Earlier AI tools also invented
four-letter tags (`YUAN`, `CHAG`, `ILKH`, `TRSX`) that cannot exist. Location names
were wrong in ways that look plausible (`location:beijing` for what is actually
`location:zhongdu`, `location:sarai` for `location:sarai_al_jadid`).

A wrong tag does not error. The trigger just never matches, and the situation
silently never fires.

**Rule: every tag is exactly 3 letters. Never propose, accept, or write a
4-letter tag.**

## Reference paths

```
REF="../Reference EU5 vanilla and Prussian Destiny"
VANILLA="$REF/Europa Universalis V/game"
```

## Procedure

### Country tags

Vanilla country definitions live under the setup tree. Locate the authority for
the current version before searching:

```bash
find "$VANILLA/in_game" -type d -name 'countries' -o -type d -name 'country_definitions' | head
ls "$VANILLA/in_game/setup/countries/" 2>/dev/null | head
```

Then confirm the tag exists and read what it actually is:

```bash
grep -rn '\bMGO\b' "$VANILLA/in_game/" | head -20
```

Report: does it exist, what is its name/culture/government, and the `file:line`.

### Formable countries

Formables are a separate system from tags — a tag can exist without being
formable, and a formable has a `_f` suffix in its key (`MGO_f`, `PRU_f`).

```bash
grep -rn 'MGO_f' "$VANILLA/in_game/common/formable_countries/" | head
ls "$VANILLA/in_game/common/formable_countries/"
```

Note the tier. MGO is expected to be tier 3, MGE tier 4 — **verify, don't assume**.

Critically: **MGO's formable already exists in vanilla.** Do not create a
`00_formable_countries.txt` for it. PD has one only because North German
Confederation genuinely does not exist in vanilla. Adding a redundant file
overwrites working vanilla content.

### Locations, regions, areas, cultures, governments

Same discipline, different folders. Confirm the exact identifier string, not an
English name that resembles it:

```bash
grep -rn 'zhongdu' "$VANILLA/in_game/" | head
grep -rn 'mongolia_region' "$VANILLA/in_game/common/" | head
grep -rn 'mongolian_group' "$VANILLA/in_game/common/cultures/" | head
grep -rn 'steppe_horde' "$VANILLA/in_game/common/government_types/" | head
```

If a search returns nothing, the identifier is wrong — historical plausibility is
not evidence. Karakorum, Sarai and Beijing all have in-game names that differ
from their common English forms.

### When the game files are hard to search

The design doc suggests the wiki first for tags, because the setup files are
large and awkward to grep. That is reasonable — but the wiki is secondary
evidence. Order:

1. `https://eu5.paradoxwikis.com/Category:Country_lists` (WebFetch)
2. `https://eu5.paradoxwikis.com/Europa_Universalis_5_Wiki`
3. The regional wiki PDFs in `docs/` — Central and North Asian subcontinents,
   East Asian subcontinent, Eastern European subcontinent
4. Vanilla files, to confirm whatever the wiki claimed

**Whatever the wiki says must still be confirmed in the game files before it
enters code.** The wiki can lag the patch; the files cannot.

## Output format

| Concept | Claimed | Verified | Evidence | Verdict |
|---|---|---|---|---|
| Mongolia formable | MGO_f, tier 3 | ? | `file:line` | confirmed / wrong / not found |

Anything unresolved goes in **netleştirilmesi gereken** and is raised with the
user. Never fill a gap with a plausible guess.

## Lessons locked in from this project (all verified)

- **Right name, wrong place:** `location:zhongdu` exists — as a steppe-frontier
  village in `xinghe_province`. Beijing is `location:dadu` (34 script uses,
  `shuntian_province`). Existence-checking passes on the wrong location. The test
  is *script usage count* + the `definitions.txt` hierarchy
  (region → area → province → location), never historical plausibility.
- **Regions lie if you guess from names:** `steppes_region` is the PONTIC steppe
  (crimea/azov/lower_don/astrakhan). The Silk Road corridor is `khorasan_region`
  (contains `transoxiana_area`, `khwarazm_area`, `zhetysu_area`); the Kazakh steppe
  is `zhetysu`/`desht_kipchak`. Beijing's region is `north_china_region`
  (`beiping_area`). Derive membership from `definitions.txt`, e.g. python: find the
  province block containing the location, then walk back to the enclosing area and
  region declarations.
- **Defined ≠ on the map.** A `setup/countries` entry (colour/culture/religion) may
  hold zero land at 1337. On-map at start: CHI, CHG, GLH, DLH, JLY, CHB, MZF, INJ,
  GRG. **Emergent:** TIM (`flavor_tim.8`), OIR (`flavor_chi.txt`,
  `create_country_from_cores_in_our_locations`). **Dead:** HLG — zero script uses
  in all of vanilla (the Ilkhanate dissolved in 1335, before the game starts);
  events keyed to it can never fire. **Formable-only:** MGO (no setup entry by
  design), MGE (`MGE_f`, nine required locations).
- **Emergent tags in `dynamic_historical_event` are fine** — vanilla uses
  `tag = TIM` in dhe blocks 15× though TIM emerges mid-game. Multiple `tag =`
  lines in one dhe block are also vanilla-legal.
- **Formables define the goal.** `MGE_f`'s own `allow` block (nine locations across
  nine regions) is the ground truth for any "restore the empire" objective — an
  invented location list drifted from it and broke the endgame here once.

## The original tag table (RESOLVED — kept for history)

From `docs/MOD-DESIGN-IDEA.md`, all of this still needs independent confirmation:

| Concept | Claimed tag | Status |
|---|---|---|
| Yuan | CHI (or a separate YUA?) | unclear, resolve |
| Chagatai | CHG | claimed wiki-confirmed |
| Ilkhanate | HLG (Hulaguids) + an International Organization, not one tag | claimed wiki-confirmed |
| Golden Horde (Jochi) | GLH | claimed confirmed |
| Oirat | OIR | claimed confirmed |
| Mongolia | MGO, tier 3 formable, already in vanilla | previously confused with MGE |
| Mongol Empire | MGE, tier 4 formable | previously confused with Moghulistan |

Verify these from scratch. Do not carry forward the earlier tools' claims.
