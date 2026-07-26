# EU5 error.log — decoder

> **Purpose.** Every working session starts with log lines pasted from
> `Documents/Paradox Interactive/Europa Universalis V/logs/error.log`. Each
> signature below cost a real investigation once. Look it up here first; only
> grep vanilla when the signature is not in this table.
>
> **Every entry was decoded against a running game**, not inferred. Where a
> cause is still a hypothesis it says so.
>
> **This file is portable.** Nothing here is Mongol-Resurgence-specific; it is
> the first thing to copy into a new EU5 mod repo.

---

## How to read the log at all

- Two logs: `error.log` (script + GUI errors) and `debug.log`.
- Console `Log.ClearErrorLog` between checkpoints, console `error` to show.
- Prefix tells you the subsystem: `[game]` engine/database, `[cw]` Clausewitz
  core, `[cw_gui]` interface.
- **A silent load is not a working load.** The whole class this file exists for
  is content that loads without an error line *and without effect* — a wrong
  folder name, an unresolved loc key, a wargoal that does not cover the goal.
  The harness (`tools/verify_mod.py`) exists for those; the log only catches
  what the engine notices.

---

## Script errors

### `jomini_script_system.cpp:252 — Script system error! Invalid right side during comparison 'c'`
**Means:** a `c:TAG` on the RIGHT side of a comparison while that tag is not on
the map. Fires *every evaluation*, so a map mode can produce ~100k lines in a
few game-years.
**Fix:** identity → `tag = MGO` (plain string, never errors). Map modes →
`owner ?= { tag = MGO }` (block form resolves no link). Relations
(`is_subject_of`, `is_neighbor_of`, `top_owner`, `top_overlord_or_this`) →
put `country_exists = c:X` **in the same AND**, before the link; trigger ANDs
short-circuit.
**Related:** `owner = { … }` on an OWNERLESS location errors the same way —
always `owner ?= {`.

### `jomini_trigger.cpp:803 — is_in_scripted_geography: Inconsistent trigger scopes (country vs. location, province_definition, area, region, sub_continent, continent)`
**Means:** a location-scope trigger used in country scope, or the reverse. The
message names the trigger and both scope families.
**Fix:** know which family the trigger belongs to.

| Question | Country scope | Location scope |
|---|---|---|
| in this geography? | `has_presence_in = scripted_geography:X` | `is_in_scripted_geography = scripted_geography:X` |
| in this region? | `has_presence_in = region:X` | `region = region:X` |
| inside this realm? | `top_overlord_or_this ?= c:X` | `top_owner ?= c:X` (+ `has_owner = yes`) |

A country's seat is a location: `scope:C.capital ?= { is_in_scripted_geography
= … }`.

### `jomini_trigger.cpp:1673 — Illegal use of operator untyped at <file>:<line>, must be valid equality operator`
**Means:** that line is not a `key = value` pair at all. Almost always a
mangled line — a half-written statement, or a scripted edit that dropped the
left-hand side.
**Fix:** open the exact line. Ours were `scripted_geography:MR_geo_tibet` with
the `is_in_scripted_geography = ` prefix eaten by a bad regex. Brace counts
still balanced, so no other check caught it.

---

## Localisation

### `localization_reader.cpp:451 — Missing colon (:) separator at line N and column M`
**Means:** a loc entry is not `key: "value"` on ONE physical line. The entry is
**dropped entirely**, not just mis-rendered.
**Fix:** rejoin. Cause is nearly always a literal `\n` in a description that
became a real newline when the file was written by a script — escaping survives
exactly one layer, so build it explicitly (`chr(92) + "n"`) rather than counting
backslashes through a heredoc, a shell and a string literal.
**Guarded by:** harness check `loc lines are well formed`.

### `localization_util.cpp:103 — <key>: "Key With Spaces Instead Of Text"`
**Means:** the key has no localisation, so the engine invented a title-cased
string from the key itself. It is telling you the key it wanted.
**Fix:** add the key. Watch the engine-derived ones you did not write yourself:
`war_goal_<wargoal_key>` (+`_desc`) — with a wargoal named `MR_war_goal_x` that
is the double-prefixed `war_goal_MR_war_goal_x`; `rule_<key>`,
`setting_<option>` (+`_desc`); `hint_<key>` + `hint_<key>_hint_text`;
`STATIC_MODIFIER_NAME_/DESC_<key>`; `<situation_key>` + `_desc`;
`MODIFIER_TYPE_NAME_/DESC_<key>`.
**The trap that produced this here:** the keys existed — in
`in_game/localization/`. A mod loc file there with the same filename SHADOWS
the `main_menu` one, and every main_menu-only key renders raw. **All mod
localisation belongs under `main_menu/localization/<language>/`**; subfolders
are fine (vanilla has 414 files in them).

### `pdx_text_formatter.cpp:807 — Unknown formatting tag 'X'`
**Means:** `#X` markup the formatter does not recognise.
**Fix:** check your own text for stray `#` sequences and `|X]` specifiers.
**Confirmed vanilla-side here:** `'l'` appears when opening vanilla situation
panels too, with no mod loaded content involved. Before spending time on it,
open a vanilla panel and see whether it fires there as well.

---

## GUI

### `pdx_data_callstack.cpp:17 — No context supplied (Use SetDataContext), wanted context of type 'T' for 'T.Method'`
plus the downstream trio `pdx_gui_data_manager.cpp:233 FetchData failed`,
`pdx_gui_localize.cpp:140`, `pdx_data_localize_helper.cpp:290`.

**Means:** a widget needs a datacontext of type `T` and no ancestor pushes one.
The cited `<file>:<line>` is where the widget lives, **not** where the mistake
is.
**Fix:** find who was supposed to push that context.
**The case here:** `one_country_header_template` declares `block
"CountryContext"` **twice** — once empty for the portrait, once carrying the
default `datacontext = "[Country.GetGovernment]"` for the ruler-title strip. A
single `blockoverride` replaces BOTH, so the strip received a Country where it
needed a Government and logged on every frame. Fix used:
`blockoverride "one_country_ruler_title_visible" { visible = no }` — hiding the
strip, which vanilla's `reformation.gui:88` does for its own reasons. It cost
nothing visible because every widget in that strip is gated on
`[Government.HasRuler]` and was already rendering blank.
**General lesson:** a `blockoverride` applies to EVERY block of that name in
the template. Read the template before overriding.

### `pdx_gui_factory.cpp:624 — '<name>' is not a valid widget/type/property`
**Means:** invented widget or property.
**Fix:** grep vanilla `.gui` for the name; zero hits means it does not exist.
Ours: `textbox_single` (the real one is `text_single`, 3926 vanilla uses) and
`progress` (a progressbar's fill property is `value`, with `min`/`max`).

---

## Database / registry

### `generic_action_ai_list.cpp:82 — Action X is not explicitly listed in an ai list! This has performance considerations!`
**Means:** no `in_game/common/generic_action_ai_lists/` entry, so the AI
re-evaluates the action far more often than it needs to.
**Fix:** one file with `potential = { … }` + `actions = { X }`. Shape:
vanilla `rise_of_timur_list.txt`.

### `price_database.cpp:117 — Missing modifier type for price. <price>_cost_modifier`
**Means:** declaring a `common/prices/` entry also implies a modifier TYPE
named `<price_key>_cost_modifier`.
**Fix:** add it under `main_menu/common/modifier_type_definitions/`:
`{ color=bad  percent=yes  game_data={ category=country } }`. Shape: vanilla
`hussite_wars_actions_price_cost_modifier`.

### `modifier_type.cpp:1294 — Missing Icon for Modifier: <key>`
**Means:** no icon at `main_menu/gfx/interface/icons/modifier_types/<key>.dds`.
There is **no `icon` field** — the lookup is by filename convention.
**Fix:** ship a small `.dds` at that path, or accept it. **Cosmetic, and
vanilla omits some of its own** (it ships one for
`rot_select_core_region_price_cost_modifier` but not for
`rot_plan_invasion_price_cost_modifier`).

### `message_handler.cpp:421 — Failed to find message type: PERFORM_<action>_ACTION`
**Means:** a `type = situation` generic action sends a message when performed
and the message type is not registered. 149 of vanilla's 155 situation actions
register one.
**NOT FIXABLE IN A MOD.** The engine reads exactly one file for these,
`main_menu/gui/messagetypes.txt`, with 1348 vanilla entries. A differently
named file in that folder is silently ignored — verified: vanilla ships no
second `.txt` there, and a large published mod ships one that is dead. A file
with THAT name replaces all 1348.
**Accept:** one log line when the action fires, and no popup. The action works.

### `country_database.cpp:98 — <TAG> has the name 'empire' in it, which does not work for a tag, which would look silly as 'The Great TAG Empire Empire'`
**Means:** a country name containing "Empire". Rank titles compose as
`<prefix> <adjective> <rank noun>`, so the word doubles.
**Fix:** rename, or accept — it is a load-time cosmetic line. **Zero vanilla
country names contain "Empire".** Note the map label is built from
`<rank>_prefix` + `<TAG>_ADJ` + `<rank noun>` and never uses the country name
at all, so renaming may not change what you see on the map: an empire-rank
steppe horde reads "Great <Adj> Horde" whatever you call it.

---

## Adding to this file

When the game reports a signature that is not here, add a row **once you have
decoded it** — signature, what it actually means, the fix, and whether it is
fixable at all. If it turns out to be vanilla-side, say so explicitly and say
how it was confirmed; that saves the next session from re-investigating a
non-problem. Two entries above are exactly that.
