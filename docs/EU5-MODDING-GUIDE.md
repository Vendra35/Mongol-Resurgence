# Creating a Europa Universalis V Mod — A Field Guide

> Distilled from building **Mongol Resurgence**: a six-situation, 60-event
> scenario mod, rebuilt from a broken AI-generated codebase into a working one.
> Everything here was learned by hitting the failure, not by reading about it.
> Companion docs: `MOD-DESIGN-IDEA.md` (what we built), `AUDIT-2026-07-21.md`
> (what the broken version looked like), `../CLAUDE.md` (the standing rules).

---

## 1. The one principle that matters

**EU5 script fails silently.** A fabricated field, a misspelled folder, a dangling
localisation key, a wrong-scope effect — none of them error. The game loads your
mod, ignores the broken part, and the mechanic simply never exists. You will not
find out from the game; you find out from discipline.

So the entire method is: **never write a construct you cannot cite.** For every
field, effect, trigger, tag, and name: find a vanilla (or known-working mod) usage
in the *same position*, at the *same scope*, with the *same kind of value* — and
only then use it. "It looks right" and "EU4 does it this way" are how every bug in
the original codebase got there.

You need two reference trees next to your mod, and you will grep them constantly:

```
workspace/
├── YourMod/
└── Reference/
    ├── Europa Universalis V/game/     ← the vanilla install (~51k files)
    └── SomeWorkingMod/                ← a tested mod to copy patterns from
```

A working mod matters as much as vanilla: vanilla shows you what is *legal*,
a tested mod shows you how the pieces *fit together* (ours was Prussian Destiny).
But trust it critically — we inherited two real bugs from our reference mod
(`monthly_spawn_chance = 100` on a 0–1 field; Turkish comments riding along with
copied patterns).

## 2. Mod skeleton

```
YourMod/
├── .metadata/metadata.json            ← launcher manifest (+ thumbnail.png, 512², <1MB)
├── in_game/                           ← loaded entering the lobby
│   ├── common/
│   │   ├── situations/  scripted_triggers/  casus_belli/  wargoals/
│   │   ├── scriptable_hints/  on_action/            ← singular! not on_actions
│   │   └── ...
│   ├── events/<any_subfolders>/
│   └── gui/panels/situation/<situation_key>.gui
└── main_menu/                         ← loaded before the menu
    ├── common/game_rules/  static_modifiers/  script_values/
    └── localization/english/X_l_english.yml   ← ALL loc lives here (see §8)
```

Rules that cost us real bugs:
- **Folder names must match vanilla exactly.** `on_actions/`, or `game_rules/`
  under `in_game/` (it is main_menu-only), load as *nothing*, silently. Before
  creating any folder, confirm it exists in the vanilla tree at that level.
- **Every file: UTF-8 with BOM** (`efbbbf`). Vanilla and working mods have it on
  every single file. `printf '\xEF\xBB\xBF' | cat - file > tmp && mv tmp file`.
- **One localisation tree, one file** — everything in
  `main_menu/localization/<language>/`. Vanilla's `in_game/localization` holds
  only the jomini engine fallback, and a mod file there with the same filename
  SHADOWS the main_menu one (this happened — see §8). Never create
  `in_game/localization/` in a mod.
- metadata.json: `name, id, version, supported_game_version, short_description,
  tags, relationships, game_custom_data` — not EU4's `short_desc`/`dependencies`.

## 3. Situations — the campaign skeleton

`common/situations/readme.txt` **inside the vanilla tree** is the authoritative
field list — read it before writing one. The real field set:

```
monthly_spawn_chance   0–1 (use named values; monthly_spawn_chance_unique = fire when able)
can_start / can_end    triggers, root = situation
visible                trigger, root = country asking
on_start / on_monthly / on_ending / on_ended     effects, root = situation
map_color / secondary_map_color / tooltip        root = location
hint_tag               must ALSO be defined in common/scriptable_hints/
legend_key, custom_description, voters, resolution, international_organization_type
```

There is **no** `title`, `desc`, `trigger`, `targets`, `progress`, `completion`,
`abort`, `actions`, `icon`, `sort_order` — all of those are EU4/invented (the
original codebase used nine fabricated fields out of ten). Multiple situations per
file is fine; each situation key needs a matching `gui/panels/situation/<key>.gui`.

Design rules we validated the hard way:
- **`can_end` must be `goal OR time-expiry`.** Success-only end conditions mean a
  failed situation runs forever and your failure content is unreachable.
- **`on_ending` must branch on the goal trigger** — not on a side-signal like
  `country_exists` (a timeout with the country alive would fire the success event).
- Set your terminal globals (`x_complete` / `x_failed`) **directly in on_ending**,
  even if an event also sets them — events need a recipient; state must not.
- One-shot flags that gate per-phase behaviour must be **per-phase** — a shared
  `failsafe_fired` global meant only one of three failsafes could ever fire.
- An end trigger must be **stronger than the conditions at start**, or the
  situation can end the month it begins (two of ours did).
- Clean situation variables in `on_ended` (`remove_variable`) — the wiki notes
  they otherwise bloat the savefile.
- Drive story beats from `on_monthly` with a momentum variable + threshold checks
  guarded by one-shot globals; drive the *panel* via situation-scope variables
  your `.gui` reads (`GetVariable('...')`) — and update them when the leading
  actor changes.

## 4. Events

```
﻿namespace = my_mod                     ← first line, per file

my_mod.1 = {                           ← the KEY is the id; no country_event = { id = }
	type = country_event
	title = my_mod.1.title             ← plus desc / historical_info (all loc keys)
	outcome = neutral                  ← positive|negative|neutral (sound)
	fire_only_once = yes
	illustration_tags = { 10 = armed 10 = exterior }   ← or image = "gfx/...dds"
	dynamic_historical_event = {       ← THE dating mechanism
		tag = FRA                      ← multiple tag lines legal; emergent tags legal
		from = 1400.1.1   to = 1500.1.1   monthly_chance = 1
	}
	trigger = { ... }                  ← additional gate
	immediate = { hidden_effect = { ... } }
	option = {
		name = my_mod.1.a
		historical_option = yes        ← Historical-AI rule always picks this
		ai_chance = { factor = 60 }    ← vanilla's dominant form (1213 uses)
		add_prestige = prestige_mild_bonus
	}
}
```

Not in EU5 (all EU4): `picture`, `mean_time_to_happen`, `pre_trigger`,
`scope =`, `is_triggered_only`, `set_country_flag`, bare `trigger_event`.
Firing an event from script: `trigger_event_silently` / `trigger_event_non_silently`
only; from on_actions: an `events = { }` list. `hidden = yes` events auto-resolve
(rare in vanilla — 7 uses — but legal; give them an option and loc anyway).
`category = situation_event` pulls situation icons. `major = yes` broadcasts.

**Effects take named script values.** `add_prestige = 25` is wrong even though it
parses; vanilla uses `prestige_mild_bonus` (=10) etc., defined in
`main_menu/common/script_values/default_values.txt`, in tiers weak/mild/severe/
extreme/ultimate/radical — and not every effect has every tier. Verify the exact
name. Reward vocabulary worth knowing: prestige, stability, legitimacy,
government_power, army_tradition, cultural_influence, research_progress, gold,
manpower (block form), and for hordes: `add_horde_unity`, `add_tribal_cohesion`.

## 5. Geography and tags — where "it exists" is not enough

`map_data/definitions.txt` is the single source of truth, a nested hierarchy:
`region { area { province { locations } } }`. Learn to query it, because names
deceive:
- `location:zhongdu` exists — it is a frontier village. Beijing is `location:dadu`.
  The tell: **script usage count** (dadu 34, zhongdu 0) and the enclosing province.
- `steppes_region` is the *Pontic* steppe (Crimea/Azov/Astrakhan). The Silk Road
  corridor is `khorasan_region` (contains `transoxiana_area`); the Kazakh steppe
  is `zhetysu`/`desht_kipchak`.
- Tags: a `setup/countries` entry proves a tag is *defined*, not that it holds
  land at game start. Some tags only emerge via events
  (`create_country_from_cores_in_our_locations`), some are formable-only, and some
  are **dead** — defined but with zero script uses (our HLG: the Ilkhanate died
  in 1335, two years before the 1337 start).
- **Formables define endgame goals.** If your scenario ends in forming `XXX_f`,
  your end conditions must be (at least) that formable's own `allow` block —
  ours drifted and the empire was unformable at "victory".
- In-game screenshots of the region/area map modes are worth more than any wiki
  page for resolving names fast.
- **`c:TAG` is a runtime link, not a name.** Any comparison whose right side is
  `c:TAG` — `this = c:MGO`, `owner ?= c:MGO`, `is_neighbor_of = c:MGE` — throws
  `Invalid right side during comparison 'c'` in `error.log` *every evaluation*
  while that tag is not on the map. A `map_color` doing this spammed ~100k
  errors in seven game-years; a Phase 3 file comparing `this = c:MGE` did it for
  a whole century, because MGE only forms at the phase's end. The idioms:
  - identity → `tag = MGO` (string comparison, can never fail);
  - map modes → `owner ?= { tag = MGO }` (block form resolves no link);
  - relations (`is_subject_of` / `is_neighbor_of = c:X`) → precede with
    `country_exists = c:X` **in the same AND** — trigger ANDs short-circuit, so
    the link is never touched when the tag is absent.

## 6. Wars: casus belli + wargoals

EU5 splits EU4's CB into two files: the CB (`common/casus_belli/`) points via
`war_goal_type` at a wargoal (`common/wargoals/`) which owns the peace terms.
EU4's `po_*` flags, `badboy_factor`, `war_name =` on the CB — none exist.

```
cb_MY_conquest = {
	create_visible = { always = no }   ← script-granted, not diplo-screen
	create_enabled = { always = no }
	additional_war_enthusiasm_attacker = 1
	war_goal_type = MY_war_goal
	ai_will_do = { add = { desc = "BASE" value = 100 } }
}
MY_war_goal = {
	type = superiority
	attacker = {
		conquer_cost = 1               ← cheap so the AI can actually finish
		allowed_locations   = { scope:location.region = region:x_region }
		allowed_subjugation = { scope:loser.capital.region = region:x_region }
	}
	defender = { }
	ticking_war_score = 0.5
}
```

**The coverage rule:** `allowed_locations` must cover *every* location your
scenario's goal demands. Ours covered 2 of 9 required regions — wars could be won
while the goal stayed legally untakeable. Grant CBs from situation `on_start`
(`add_casus_belli = { target = scope:x type = casus_belli:cb_X years = N }`), and
re-grant in later phases: a `years = 50` grant from 1420 is long expired by 1600.

## 7. Railroading an AI (the PD pattern)

An AI will not conquer on theme without help. Three cooperating layers:

1. **Conquest loop** (situation `on_monthly`): a cooldown variable ticks; when no
   target is set, pick one — `ordered_neighbor_country` filtered
   (`is_rebel_country = no`, no truce/subject,
   `defensive_alliance_strength < our.offensive_alliance_strength`, holds goal
   land), `max = 1`, `order_by = { value = num_locations multiply = -1 }` (weakest
   first) — and store it on the situation. When the cooldown matures, fire the
   war event. Add a **fallback** that clears the slot when the stored target
   dies/subjects/truces, or the loop deadlocks.
   **The war event is NOT hidden and does NOT declare from `immediate`** — that
   railroads a human player into a war with no say (a real bug here). PD 103's
   shape: `immediate` zeroes the cooldown and saves the target scope; **option A**
   (`ai_chance` 100) carries the `declare_war_with_cb`; **option B**
   (`ai_chance` 0) postpones; `after` resets the target slot and re-seeds the
   target-country variable with the claimant's own tag (a country guaranteed to
   exist — never seed it with a tag that may not be on the map yet). Fire it
   with `trigger_event_silently`, and drop the `is_ai` gate from the loop so a
   human claimant gets the same event with a choice.
2. **Sustainment** (`common/on_action/`): register on the *real* hooks —
   `yearly_country_pulse = { on_actions = { my_pulse } }` (there is no
   `on_yearly_pulse`). Peace-time army top-ups and infrastructure for the AI
   claimant. This also covers the gaps *between* situations, when no `on_monthly`
   is ticking.
3. **Failsafes**: a *birth* failsafe (force-create the actor if nobody qualifies
   organically) and *completion* failsafes ~5 years before each deadline that hand
   the goal over outright — `every_ownable_location_in_area/_region` +
   `change_location_owner` + `add_core` (always `owner ?=` in the limit — the
   bare `owner` link errors on ownerless locations), subjects via
   `make_subject_of`. Buffs are not a failsafe; territory is. Guards: only for
   an **AI** claimant, only taking from **AI** owners, one-shot flag **per
   phase**. An at-peace gate on the claimant is optional — we dropped it where
   an endless AI war could stall the handover forever.

## 8. Localisation, GUI, hints

- **One tree, one file.** ALL localisation goes in
  `main_menu/localization/<language>/` — vanilla's `in_game/localization/`
  contains only the engine's `jomini` fallback, and PD (tested) ships a single
  main_menu file. This mod once split loc across `in_game` and `main_menu`
  files *with the same filename*; the in_game copy shadowed the main_menu one,
  so every main_menu-only key (`rule_*`, `setting_*`, several
  `STATIC_MODIFIER_NAME_*`) rendered as its raw key in game.
- Loc files: `﻿l_english:` once at the top, one leading space per key,
  `key: "value"`, `\n` for newlines, `#Y ...#!` colour markup. Duplicate keys —
  last one silently wins; audit for them.
- Every referenced key must exist: event `title`/`desc`/`historical_info`/option
  `name`s, `custom_tooltip` texts, modifier names, CB/wargoal names, hint names.
- **Key conventions the engine derives for you** (get them wrong and the UI
  shows raw keys):
  - situations → `<situation_key>` + `<situation_key>_desc`
    (vanilla `situations_l_english.yml`: `black_death`);
  - wargoals → `war_goal_<wargoal_key>` + `_desc` — with a `MR_war_goal_x`
    wargoal that means the double-prefixed `war_goal_MR_war_goal_x`;
  - game rules → `rule_<rule_key>`, `setting_<option>`, `setting_<option>_desc`;
  - hints → `hint_<key>` + `hint_<key>_hint_text`;
  - static modifiers → `STATIC_MODIFIER_NAME_<key>` (+ `_DESC_`).
- Situation panels: copy the closest vanilla `.gui` (`the_revolution.gui` is the
  simplest); a `blockoverride` naming a block that doesn't exist in the vanilla
  template renders *nothing*, silently. Panels read situation variables — set them.
- `hint_tag` needs a definition in `common/scriptable_hints/` (priority / hide /
  sort_priority), not just loc.
- Modifiers: `game_data = { category = country }` + types that exist in
  `main_menu/common/modifier_type_definitions/` — EU4 names (`prestige`,
  `stability_modifier`, `governing_capacity`, `global_unrest`) do not.

## 9. Verify like you don't trust yourself — because you shouldn't

Two of our audits reported "clean" on broken code: BSD grep's `\b` silently
matching nothing, and line-grep on multi-line constructs. Rules:
- Python over shell for anything multi-line; `grep -F` for literals.
- **Every check prints its item count** — a check that can only print nothing is
  indistinguishable from a check that ran on nothing.
- Prove a scan on a known positive before trusting its negative.

The harness that guards this mod (run after every change; adapt freely) checks:
braces balanced per file · situation fields ⊆ documented set · every referenced
loc key exists in the *correct* tree · every fired event defined · every defined
event reachable (fired or dhe) · scripted triggers / modifiers / hints resolve ·
no orphan modifiers · globals set↔read symmetric · situation vars cleaned in
on_ended · regions/areas exist in definitions.txt · wargoal coverage ⊇ goal
regions · no duplicate event ids / loc keys · BOM on every file · advances/
buildings/units exist in vanilla · no unguarded c:TAG comparison patterns.
22 checks, one python script (`tools/verify_mod.py`, auto-detects the
reference-tree layout), seconds to run.

Beyond static checks, walk the **state machine** by hand: every failure path sets
its terminal state; nothing depends on an event having a recipient; no end
condition true at start; no branch unreachable. That review found bugs the
reference-integrity harness structurally cannot see.

## 10. Process

1. **Read first, write nothing.** Vanilla + your working reference mod + the
   design doc.
2. **Search before building** — vanilla probably already has your feature (three
   of our planned situations existed: Tumu, Ugra, Altan Khan). Hook read-only
   (`has_variable` on vanilla state) instead of duplicating; check the variable
   *persists* — some are cleaned the moment their event resolves.
3. Audit → categorized report (**definite / suspect / needs-decision**) → approval
   → fix file-by-file. Never bulk-fix silently.
4. Commit in small labelled steps; keep docs in sync with code (this repo:
   `CLAUDE.md` = rules, `MOD-DESIGN-IDEA.md` = design, this file = method).
5. Test on a real install: mod into
   `Documents/Paradox Interactive/Europa Universalis V/mod/`, then read
   **error.log** — and remember everything that loads *without* an error line but
   also without effect: that's the silent-failure class this whole guide exists for.

## 11. EU4 → EU5 quick reference

| EU4 habit | EU5 reality |
|---|---|
| `country_event = { id = x.1 }` | `x.1 = {` — the key is the id |
| `mean_time_to_happen` | `dynamic_historical_event { from to monthly_chance }` |
| `picture = gfx_x` | `image =` path or `illustration_tags` |
| `is_triggered_only` / `pre_trigger` | don't exist (fired events just have no dhe) |
| `trigger_event = { id = }` | `trigger_event_silently` / `_non_silently` |
| `exists = c:TAG` | `country_exists = c:TAG` |
| `set_country_flag` | `set_variable` / `set_global_variable` |
| `add_mil = 100` (monarch power) | character-scope skill! use country effects + named values |
| `add_prestige = 25` | `add_prestige = prestige_mild_bonus` |
| CB `po_*` flags, `badboy_factor` | wargoal file: `allowed_locations`, costs, `ticking_war_score` |
| modifier `prestige = 0.25` | `monthly_prestige` etc. from modifier_type_definitions |
| `is_in_region` | `region = region:x` inside location iterators / `has_presence_in` |
| `owns_or_controls` | `owns` (events use it 70:1 over `controls`) |
| 4-letter tags | never — 3 letters, always |
