---
name: audit-mod
description: Full read-only audit of the Mongol Resurgence mod against every known error class, producing a categorized findings report (kesin hata / şüpheli / netleştirilmesi gereken). Use when asked to review, audit, check or denetle the mod, before starting fixes, or after a batch of changes. Writes nothing.
version: 0.1.0
---

# Audit the Mongol Resurgence Mod

## Contract

**This skill writes nothing.** It produces a report. Fixes happen only after the
user reads the report and approves — file by file, summarizing each step, never
one silent bulk pass.

The existing MR code came from Cline + DeepSeek and is **guilty until proven
innocent**. Never cite an MR file as precedent for how EU5 works; it is the
subject of the audit, not a source.

## Reference paths

The repo is shared between two machines with different layouts — DETECT,
never assume (same snippet as CLAUDE.md and `tools/verify_mod.py`):

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

Probe a known FILE, not the directory: the legacy `EU5-Vanilla` junction has
been emptied by OneDrive before, and an empty directory passes `-d` while every
grep against it returns nothing — a silent vacuous audit.

Read-only. Never write under `$VANILLA` or `$PD`.

## Error classes to check

Work through all of these. Do not stop at the first category that produces hits.

### 1. Fabricated syntax

Use `verify-eu5-syntax`. For each mod file, derive the closed field set from the
vanilla equivalents and flag every field outside it.

Baseline measured on the situation files: nine of ten MR top-level fields are
fabricated (`title` `description` `trigger` `icon` `targets` `sort_order`
`progress` `completion` `abort`); only `visible` is real. Expect similar density
in events, on_actions and scripted_triggers — **check them, do not extrapolate**.

### 2. Tags and named references

Use `verify-tags`. Every tag 3 letters. Every `location:` / `region:` /
`culture:` / `government_type:` string confirmed to exist in vanilla.

```bash
# any 4-letter tag is an automatic finding
grep -rnoE 'c:[A-Z]{4,}' in_game/ main_menu/
```

### 3. Known specific bugs

```bash
grep -rn 'exists = c:' in_game/ main_menu/          # must be country_exists
grep -rn -A3 'set_variable' in_game/ | grep -c 'value ='   # every set_variable needs value
```

- `exists = c:TAG` → must be `country_exists = c:TAG`
- `set_variable` with `name` twice instead of `name` + `value`
- `owns` → `controls`: the swap was made but **never semantically validated**.
  Ownership and military control differ. For each site, decide which the
  scenario actually needs and report the reasoning — this is a thinking task,
  not a grep task.

### 4. GUI separation

GFX/GUI references must not be embedded inside situation files; they belong in
separate `.gui` files.

```bash
grep -rn 'gfx_\|icon =' in_game/common/situations/
```

### 5. File hygiene

```bash
# UTF-8 BOM — vanilla and PD have efbbbf on every file
for f in $(find in_game main_menu -type f); do
  [ "$(head -c3 "$f" | xxd -p)" != "efbbbf" ] && echo "NO BOM: $f"
done

# English-only, including comments (PD's own source has Turkish comments —
# they must not travel with copied patterns). Proper names like Möngke are fine.
grep -rnP '[çğışöüÇĞİŞÖÜ]' in_game/ main_menu/
```

Baseline: 11 files were missing the BOM, and all 3 `.gui` files carried Turkish
comments. Re-check rather than assuming these were fixed.

### 6. Metadata

Compare `.metadata/metadata.json` field-for-field against PD's working one —
`supported_game_version` not `version`, plus `name`, `id`, `short_description`,
`tags`, `relationships`, `game_custom_data`.

### 7. Naming consistency

`MR_` prefix on files and variables, `mongol_resurgence` namespace, paralleling
PD's `PD_` / `the_prussian_destiny`. Flag drift — mixed prefixes break nothing
loudly but make later greps unreliable.

### 8. Design-doc conformance

Beyond syntax, does the code implement what `docs/MOD-DESIGN-IDEA.md` describes?

- Dynamic birth trigger (Karakorum owner + steppe horde + Mongol culture),
  modeled on vanilla's `flavor_tim.8` Timur emergence
- Birth failsafe by ~1370 if nobody organically qualifies
- Completion failsafe in **all three** situations, 5 years before each end date,
  mirroring PD's `PD_brandenburg_rise_auto_conquest_yes` pattern
- Three phases with the right date ranges (1368–1420 / 1420–1550 / 1550–1650)

A syntactically perfect file that implements the wrong design is still a finding.

## Error classes added after later audit rounds (all found real bugs here)

### 9. Scope misuse (existence checks pass, code still wrong)
`add_mil` at country scope; `owner = root` where vanilla only uses `scope:X`/
`c:TAG`. For every effect: verify enclosing scope in 2–3 vanilla hits, not just
presence. See `verify-eu5-syntax` → THE SCOPE RULE.

### 10. Geography-for-intent
The name exists but is the wrong place: `zhongdu` vs `dadu`; `steppes_region`
(Pontic) used as the Silk Road corridor (`khorasan_region`). Check
`map_data/definitions.txt` hierarchy against the comment-stated intent.

### 11. Coverage: wargoals vs goals
Each wargoal's `allowed_locations` must cover every location its phase's end
trigger demands. Here the westward CB covered 2 of 9 required regions — wars could
be won while the goal stayed legally untakeable.

### 12. Reachability and terminal states
Simulate the state machine: can every event fire (defined+fired or dhe)? Can every
situation END on both success AND failure (goal OR time expiry in `can_end`)?
Does every failure path set the terminal global? Is any one-shot flag shared
across phases that should be per-phase (`mr_failsafe_pN_fired`)? Can an end
trigger already be true at `can_start` (instant-end)? Is any `on_ending` branch
keyed on a side-signal (`country_exists`) instead of the goal trigger?

### 13. Localisation tree (UPDATED after the shadowing incident)
ALL mod localisation lives in ONE file:
`main_menu/localization/english/MR_l_english.yml`. Vanilla's
`in_game/localization` holds only the jomini engine fallback — a second mod
loc file with the same filename there SHADOWS the main_menu one and every
main_menu-only key (rules, settings, modifier names) renders raw. Flag ANY
`in_game/localization` file in the mod as a finding.

### 14. Vacuous verification
BSD grep `\b` and line-grep on multi-line constructs both produced false "clean"
audits here. Every check must print a count; prove scans on a known positive.

## The standing harness

A ~19-check python harness exists (see `docs/EU5-MODDING-GUIDE.md` §9): braces,
situation field whitelist, loc binding (both trees), event definition/reachability,
trigger/modifier/hint resolution, global set↔read symmetry, situation-var cleanup,
region/area reality, wargoal coverage, duplicate ids/keys, BOM. Run it after every
change; silence on any check is only meaningful because each prints its item count.

## Report format

Three groups, most severe first. Every finding cites `file:line` and, where the
claim is "this is wrong", the reference `file:line` that shows what right looks
like.

**Kesin hata** — provably wrong. Fabricated field, nonexistent tag, 4-letter tag,
missing BOM. Evidence is conclusive.

**Şüpheli** — probably wrong, or right by accident. Semantically unvalidated
`controls`, a field that exists but at a different nesting depth, a pattern
copied from PD whose preconditions may not hold for MR.

**Netleştirilmesi gereken** — cannot be resolved from the reference tree. Needs
the user's decision or a wiki check. Never resolve these by guessing.

End with a count per category and a recommended fix order — usually: metadata and
hygiene first (cheap, unblocks testing), then fabricated syntax (largest), then
semantics, then design conformance.
