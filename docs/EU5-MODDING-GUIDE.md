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
│   │   ├── generic_actions/  prices/                ← panel buttons + their cost
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

### Name your geography once: `common/scripted_geography/`
A named bundle of regions, areas, province_definitions and bare locations,
documented in vanilla's own `scripted_geography.info`. It is the single most
valuable thing we found late:

```
MR_geo_northern_marches = {
	region = { manchuria_region  tibet_region }
	area   = { bursol_area  omsk_area  kulykol_area }
}
```

| Ask it from | With |
|---|---|
| a country | `has_presence_in = scripted_geography:X` |
| a location / area / region | `is_in_scripted_geography = scripted_geography:X` |
| a country's seat | `scope:C.capital ?= { is_in_scripted_geography = … }` |
| iteration | `scripted_geography:X = { every_location_in_scripted_geography = { … } }` |
| the players | `[ShowScriptedGeographyName( … )]`, needs `<key>` loc |

Two rules learned by getting them wrong:
- **Atoms only, never a union.** Geographies do not nest (zero vanilla
  definitions reference another), so a "union" definition rewrites its members
  and reintroduces the duplication you are deleting. Callers `OR` the atoms.
- **One atom per separately-true condition, and per distinct boundary.**
  Putting eastern and western Gobi in one atom silently turned a goal that
  wanted BOTH into one that accepted either. Splitting khorasan from xinjiang
  was needed because one failsafe wants khorasan alone; splitting manchuria and
  tibet from the Siberian marches was needed because one cores and the other
  deliberately does not. An atom cannot be half-anything.

Before this the same region lists were written out 259 times across seven
files here, and changing a goal meant editing six places correctly.

### Choosing the cheapest construct that answers the question
`any_owned_location = { region = region:X }` walks a country's entire holdings
list. `has_presence_in = region:X` answers the same question directly (108
vanilla uses; it also takes `area:` and `sub_continent:`). We had 104 of the
first form and none of the second. Cheapest first:

| Construct | Iterates | Use when |
|---|---|---|
| `has_presence_in = region:X` | nothing (indexed) | "does this country hold anything in X" |
| `region:X = { any_ownable_location_in_region = { owner ?= … } }` | one region's locations | "does anyone **outside our realm** hold X" — the end-trigger shape |
| `ordered_neighbor_country` | neighbours | picking a war target |
| `any_country` / `every_country` | the whole map | only when the ANSWER must be a country |

**Subjecthood must walk the chain.** `is_subject_of = c:X` is true only for a
DIRECT vassal. Almost every question a mod asks is really "is this inside X's
realm", which includes a vassal's vassal:

| Scope | Use |
|---|---|
| country | `top_overlord_or_this ?= c:X` (19 vanilla uses) — also returns the country itself when it is independent, so a separate `tag = X` test is redundant |
| location | `has_owner = yes` + `top_owner ?= c:X` (156 vanilla uses, `conquistadors.txt:64`) |

Avoid `any_country_in_hierarchy` / `every_country_in_hierarchy`: a popular
published mod uses them but vanilla has **zero** uses anywhere, so they are
unattested. Getting this wrong is expensive and quiet — here it made goal
clauses ignore a sub-vassal's ground, had a failsafe seize its own
sub-vassal's land, and let the AI declare war on its own sub-vassal.

**A "we hold X" goal must mean the REALM holds X.** `c:X = { owns =
location:Y }` is true only when X holds Y *itself*, so a vassal holding the
prize deadlocks the goal — and a failsafe cannot rescue it, because a
well-written failsafe never takes land from its own subjects. Route every seat
check through one location-scope trigger instead.

Two details on the region-scan form. Use `owner ?=`, never `owner =`: regions
like khorasan and west China contain **unowned** locations, and the bare link
errors on them — with `?=` an ownerless location simply does not match, which is
what you want. And keep the `NOR` **flat**:

```
owner ?= { NOR = { AND = { country_exists = c:MGO             ← 2 independent
                           top_overlord_or_this ?= c:MGO }      members
                   AND = { country_exists = c:MGE
                           top_overlord_or_this ?= c:MGE } } }
```

`top_overlord_or_this` returns the country itself when it is independent, so it
subsumes a separate `tag =` member and covers the whole subject chain at once.
The earlier version of this example used `tag =` plus `is_subject_of` as four
flat members; that works for direct vassals only, and it taught two bugs we
actually shipped:

- **Folding a tag test into its own `is_subject_of`** (`AND = { tag = MGO
  is_subject_of = c:MGO }`) asks for a country that is its own vassal. Never
  true, so the `NOR` is always true, every owned location matches, the
  enclosing `NOT` is always false — the phase can never complete, not even
  after a failsafe hands over the whole goal territory. Nothing errors,
  nothing logs.
- **`is_subject_of` alone ignores a vassal's vassal**, so ground the claimant
  effectively ruled still blocked the goal.

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
while the goal stayed legally untakeable. It happened a second time, with one
region, and survived a manual review: **automate this check** (see §9). Note that
a goal *area* is covered if its parent *region* is listed, so the check has to
resolve area→region through `definitions.txt` rather than compare strings. Grant CBs from situation `on_start`
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
  - static modifiers → `STATIC_MODIFIER_NAME_<key>` (+ `_DESC_`);
  - generic actions → `<action_key>` + `_desc`, plus a key per `select_trigger`
    `name` and its `none_available_msg_key`, plus `<price_key>` for the
    `price = price:X` it spends, plus the `PERFORM_<action>_ACTION*` family.
    Those message keys look optional across the whole action set (46 of 354)
    but are effectively **mandatory for `type = situation`**: 149 of vanilla's
    155 situation actions define them, and the engine logs
    `message_handler.cpp:421` without one.
  - and beyond loc, the action needs an entry in
    `common/generic_action_ai_lists/` and a `<price>_cost_modifier` modifier
    type. See CLAUDE.md — three registries, three different error messages.
- **End conditions render as a CHECKLIST: one `custom_tooltip` per
  requirement, each text on ONE line.** The panel draws one tick per tooltip,
  so a single tooltip wrapped around every clause fights the widget — ours
  showed its text *and* the raw clause dump underneath. All eight vanilla
  situation end-condition tooltips are one compact sentence and none contains
  a newline. Put each requirement's tooltip inside its own scripted trigger
  and let the end trigger be a list of them.
- Situation panels: copy the closest vanilla `.gui` (`the_revolution.gui` is the
  simplest); a `blockoverride` naming a block that doesn't exist in the vanilla
  template renders *nothing*, silently. Panels read situation variables — set them.
- `hint_tag` needs a definition in `common/scriptable_hints/` (priority / hide /
  sort_priority), not just loc.
- Modifiers: `game_data = { category = country }` + types that exist in
  `main_menu/common/modifier_type_definitions/` — EU4 names (`prestige`,
  `stability_modifier`, `governing_capacity`, `global_unrest`) do not. The
  category decides which type family is legal: a `category = location` modifier
  takes the `local_*` family (`local_unrest`, `local_monthly_prosperity`), and
  one file may hold both categories — vanilla splits them across
  `country.txt`/`location.txt` by convention only.
- **Tooltips must not promise what the code does not do.** Ours said "removed
  upon the start of the 2nd Situation" for rewards that should have been
  permanent, and the code dutifully removed them — but the phases run
  back-to-back, so the player received a reward and lost it in the same instant.
  When buff and reward tiers coexist, be explicit about which is temporary
  (stripped by the granting phase's own `on_ending`) and which is not.

## 9. Verify like you don't trust yourself — because you shouldn't

Two of our audits reported "clean" on broken code: BSD grep's `\b` silently
matching nothing, and line-grep on multi-line constructs. Rules:
- Python over shell for anything multi-line; `grep -F` for literals.
- Writing files back: read AND write `utf-8-sig`. Reading with `utf-8-sig` and
  writing with `utf-8` silently strips the BOM off a file that needs one.
- Escaping survives exactly one layer. A literal `
` meant for a loc value
  has to still be a backslash and an `n` when it lands in the file; build it
  explicitly (`chr(92) + "n"`) rather than counting backslashes through a
  heredoc, a shell and a Python string literal.
- **Every check prints its item count** — a check that can only print nothing is
  indistinguishable from a check that ran on nothing.
- Prove a scan on a known positive before trusting its negative.

The harness that guards this mod (run after every change; adapt freely) checks:
braces balanced per file · situation fields ⊆ documented set · every referenced
loc key exists in the *correct* tree · every fired event defined · every defined
event reachable (fired or dhe) · scripted triggers / modifiers / hints resolve ·
no orphan modifiers · globals set↔read symmetric · situation vars cleaned in
on_ended · regions/areas exist in definitions.txt · **every goal region covered
by some wargoal's allowed_locations** · **no `any_owned_location` with a bare
geography predicate** · no duplicate event ids / loc keys · BOM on every file ·
advances/buildings/units exist in vanilla · no unguarded c:TAG comparison
patterns.
29 checks, one python script (`tools/verify_mod.py`, auto-detects the
reference-tree layout), seconds to run.

Two of those checks exist because a manual review missed the thing they now
catch. `caucasus_region` sat in the Phase 3 goal for months while **no wargoal
allowed taking it** — the phase was unwinnable and nothing errored. And a
`NOR` whose members had been folded into one self-contradicting `AND`
(`tag = MGO` *and* `is_subject_of = c:MGO` — a country cannot be its own vassal)
made Phases 2 and 3 unclosable, silently, in twenty places. **Write the check
the moment you fix the bug**, and prove it on the known positive: break the fix
again, watch the check fail, then restore. A check you have never seen fail is
a check you have not tested.

A harness only guards the shapes it knows. Two whole classes walked past a
green run and were caught by the game instead: **eleven localisation values
split across two physical lines** (a literal `
` that became a real newline —
the key-counting scan saw every key and reported clean while the game logged
`Missing colon (:) separator` and dropped all eleven), and **a generic action
missing its three side registries** (ai list, message type, price cost
modifier — three different engine errors). Both now have checks. The lesson is
not "add these two checks", it is: when the game finds something your harness
did not, the fix is two commits — the bug, and the check.

Also beware the harness itself going quietly vacuous. Three of ours selected
files by substring (`"/events/" in path`); on Windows `glob` returns
backslashes, so those checks scanned **zero** files and reported no problems for
as long as the repo was worked on from the Windows machine. The item counts were
printed the whole time — reading them is the point.

Beyond static checks, walk the **state machine** by hand: every failure path sets
its terminal state; nothing depends on an event having a recipient; no end
condition true at start; no branch unreachable. That review found bugs the
reference-integrity harness structurally cannot see.

## 10. Process

0. **Prove the reference tree is really there.** Every rule in this guide
   depends on grepping vanilla. Probe a known *file* (`in_game/map_data/
   definitions.txt`), never just the directory: ours was a junction that OneDrive
   emptied, so the folder existed, `-d` passed, and every citation check would
   have returned a confident zero hits.
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
| `is_in_region` | `region = region:x` inside location iterators |
| "does X own anything in region Y" | `has_presence_in = region:y` — **not** `any_owned_location = { region = … }` |
| province-scope `add_core` | location scope; integration uses `change_integration_level = core` |
| decisions | `common/generic_actions/` (`type = situation` for panel buttons) |
| `owns_or_controls` | `owns` (events use it 70:1 over `controls`) |
| 4-letter tags | never — 3 letters, always |
