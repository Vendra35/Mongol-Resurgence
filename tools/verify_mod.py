#!/usr/bin/env python3
"""MR mod verification harness — per EU5-MODDING-GUIDE §9.
Every check prints its item count; a check that finds nothing to scan FAILS."""
import re, sys, glob, os

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The read-only vanilla tree (see CLAUDE.md, REQUIRED SETUP). The repo is
# shared between two machines whose layouts differ, so VAN is resolved by
# DETECTION — env override first, then the known layouts — never by assuming
# one machine's path. Windows reads the Steam install DIRECTLY; the old
# EU5-Vanilla junction is a fallback only, because OneDrive has emptied it
# before (the directory still exists, so an os.path.isdir probe passes and
# every later grep silently returns nothing).
_parent = os.path.dirname(MOD)
_PROBE = os.path.join("in_game", "map_data", "definitions.txt")

def _usable(p):
    """A tree counts only if a known vanilla file is actually inside it."""
    return p is not None and os.path.isfile(os.path.join(p, _PROBE))

if os.environ.get("MR_VANILLA"):
    # An explicit override must be honoured or fail LOUD — silently falling
    # back to another tree is exactly the vacuous-pass class this harness
    # exists to prevent.
    VAN = os.environ["MR_VANILLA"]
    if not _usable(VAN):
        sys.exit(f"MR_VANILLA is set but has no {_PROBE} under it: {VAN}")
else:
    _candidates = [
        r"E:\SteamLibrary\steamapps\common\Europa Universalis V\game",  # Windows: Steam install, direct
        os.path.join(_parent, "EU5-Vanilla", "game"),  # Windows: legacy junction, fallback
        os.path.join(_parent, "Reference EU5 vanilla and Prussian Destiny", "Europa Universalis V", "game"),  # macOS layout
    ]
    VAN = next((p for p in _candidates if _usable(p)), None)
    if not VAN:
        sys.exit("vanilla reference tree not found — tried:\n  " + "\n  ".join(_candidates)
                 + "\nfix it before running (CLAUDE.md, REQUIRED SETUP), or set the MR_VANILLA env var")
fails = []

def check(name, count, problems, min_count=1):
    status = "OK " if not problems and count >= min_count else "FAIL"
    if count < min_count:
        problems = problems + [f"(scan vacuous: only {count} items — expected >= {min_count})"]
    print(f"[{status}] {name}: {count} items" + ("" if not problems else ""))
    for p in problems[:25]:
        print(f"       - {p}")
    if problems:
        fails.append(name)

# Paths are normalised to forward slashes the moment they leave glob. Several
# checks below select files by substring ("/events/", "/situations/"); on
# Windows glob returns backslashes, those substrings never matched, and three
# checks scanned zero files while reporting no problems. open() and relpath
# accept forward slashes on Windows, so normalising once here is enough.
def _np(p):
    return p.replace(os.sep, "/")

txt_files = sorted(_np(p) for p in glob.glob(MOD + "/in_game/**/*.txt", recursive=True) + glob.glob(MOD + "/main_menu/**/*.txt", recursive=True))
yml_files = sorted(_np(p) for p in glob.glob(MOD + "/**/*.yml", recursive=True))
all_files = txt_files + yml_files

def read(p):
    return open(p, encoding="utf-8-sig").read()

def strip_comments(s):
    return re.sub(r"#.*", "", s)

# ---- 1. BOM ----
probs = [os.path.relpath(p, MOD) for p in all_files if open(p, "rb").read(3) != b"\xef\xbb\xbf"]
check("BOM on every file", len(all_files), probs, min_count=10)

# ---- 2. braces balanced ----
probs = []
for p in txt_files:
    s = strip_comments(read(p))
    if s.count("{") != s.count("}"):
        probs.append(f"{os.path.relpath(p, MOD)}: {{={s.count('{')} }}={s.count('}')}")
check("braces balanced per file", len(txt_files), probs, min_count=5)

# ---- localization DB ----
loc_path = MOD + "/main_menu/localization/english/MR_l_english.yml"
loc_src = read(loc_path)
loc_keys = {}
dupes = []
for m in re.finditer(r"^ ([A-Za-z0-9_.]+):", loc_src, re.M):
    k = m.group(1)
    if k in loc_keys: dupes.append(k)
    loc_keys[k] = True
assert "mr_dominance.997.a" in loc_keys, "known-positive loc key missing — parser broken"
check("loc file parses (keys found)", len(loc_keys), [], min_count=100)
check("no duplicate loc keys", len(loc_keys), dupes, min_count=100)

# ---- loc file LINE STRUCTURE ----
# The key scan above happily ignores anything that is not a key line, so a
# value split across two physical lines passed every check while the game
# logged "Missing colon (:) separator" and dropped the entry. That is exactly
# what a literal backslash-n in a description turning into a real newline does.
probs = []
for i, line in enumerate(loc_src.split(chr(10)), 1):
    t = line.strip()
    if not t or t.startswith("#") or t == "l_english:":
        continue
    if not re.match(r"^ [A-Za-z0-9_.]+:\s", line):
        probs.append(f"line {i}: not a `key: value` line -> {t[:60]}")
    elif re.match(r'^ [A-Za-z0-9_.]+:\s*"', line) and not line.rstrip().endswith('"'):
        probs.append(f"line {i}: value opens a quote it never closes -> {t[:60]}")
check("loc lines are well formed", len(loc_src.split(chr(10))), probs, min_count=100)

# ---- generic actions: the registries a MOD can actually satisfy ----
# Declaring the action is not enough. Two of the three registries are moddable
# and are checked here (generic_action_ai_list.cpp:82,
# price_database.cpp:117).
#
# The third is NOT satisfiable and is deliberately not checked:
# message_handler.cpp:421 wants a PERFORM_<key>_ACTION entry, and the engine
# reads exactly one file for those — main_menu/gui/messagetypes.txt, 1348
# vanilla entries. A mod file with any OTHER name in that folder is ignored
# (verified: vanilla ships no second .txt there, and a popular published mod
# ships one that is silently dead), and a mod file with THAT name replaces all
# 1348. So the cost of an action is one log line at use and no popup. The
# action itself works.
acts = set()
for p_ in glob.glob(MOD + "/in_game/common/generic_actions/*.txt"):
    acts |= set(re.findall(r"^([A-Za-z_0-9]+) = \{", strip_comments(read(_np(p_))), re.M))
ai_listed = set()
for p_ in glob.glob(MOD + "/in_game/common/generic_action_ai_lists/*.txt"):
    body = strip_comments(read(_np(p_)))
    m = re.search(r"actions = \{([^}]*)\}", body)
    if m: ai_listed |= set(m.group(1).split())
prices, price_mods = set(), set()
for p_ in glob.glob(MOD + "/in_game/common/prices/*.txt"):
    prices |= set(re.findall(r"^([A-Za-z_0-9]+) = \{", strip_comments(read(_np(p_))), re.M))
for p_ in glob.glob(MOD + "/main_menu/common/modifier_type_definitions/*.txt"):
    price_mods |= set(re.findall(r"^([A-Za-z_0-9]+)\s*=\s*\{", strip_comments(read(_np(p_))), re.M))
probs = []
for a in sorted(acts):
    if a not in ai_listed: probs.append(f"{a}: not in any generic_action_ai_lists actions block")
for pr in sorted(prices):
    if pr + "_cost_modifier" not in price_mods:
        probs.append(f"{pr}: no {pr}_cost_modifier modifier type defined")
check("generic actions: ai list + price cost modifier", len(acts) + len(prices), probs, min_count=2)

# no stray in_game localization tree
stray = glob.glob(MOD + "/in_game/localization/**/*.yml", recursive=True)
check("no in_game localization files", 1, [os.path.relpath(p, MOD) for p in stray])

# ---- event ids defined / fired / loc'd ----
event_defs, event_dhe, opt_names, refs = {}, set(), [], []
code = {p: read(p) for p in txt_files}
for p, s in code.items():
    body = strip_comments(s)
    for m in re.finditer(r"^([a-z_]+\.\d+) = \{", body, re.M):
        event_defs.setdefault(m.group(1), os.path.relpath(p, MOD))
    if "dynamic_historical_event" in body:
        cur = None
        for line in body.splitlines():
            mm = re.match(r"^([a-z_]+\.\d+) = \{", line)
            if mm: cur = mm.group(1)
            if "dynamic_historical_event" in line and cur: event_dhe.add(cur)
fired = set()
for p, s in code.items():
    b = strip_comments(s)
    for m in re.finditer(r"trigger_event_(?:silently|non_silently) = ([a-z_]+\.\d+)", b):
        fired.add(m.group(1))
    # The DELAYED block form: trigger_event_silently = { id = X years = N }
    # (effects.log:10578, days/months/years). Matching only the scalar form
    # above reported every delayed event as unreachable — the same false
    # positive this harness produced when it was pointed at another mod.
    for m in re.finditer(r"trigger_event_(?:silently|non_silently) = \{[^}]*?\bid = ([a-z_]+\.\d+)", b, re.S):
        fired.add(m.group(1))
    # events fired from on_action `events = { ... }` lists
    for m in re.finditer(r"events = \{([^}]*)\}", b):
        fired |= set(re.findall(r"([a-z_]+\.\d+)", m.group(1)))
probs = [f"{e} fired but not defined" for e in sorted(fired - set(event_defs))]
check("every fired event is defined", len(fired), probs, min_count=10)
unreach = [e for e in event_defs if e not in fired and e not in event_dhe]
check("every defined event reachable (fired or DHE)", len(event_defs), [f"{e} ({event_defs[e]})" for e in sorted(unreach)], min_count=20)

# ---- event loc: title/desc/option names/historical_info ----
probs, count = [], 0
for p, s in code.items():
    if "/events/" not in p: continue
    body = strip_comments(s)
    for m in re.finditer(r"(?:title|desc|historical_info|name) = ([a-z_]+\.\d+\.[a-z_.0-9]+)", body):
        count += 1
        if m.group(1) not in loc_keys:
            probs.append(f"{m.group(1)} ({os.path.relpath(p, MOD)})")
check("event title/desc/option loc keys exist", count, sorted(set(probs)), min_count=50)

# ---- custom_tooltip text keys ----
# Keys may be dotted (PD-style event tooltip keys like
# mr_dominance_dhe.9.a.tt1), so the pattern must include '.'.
probs, count = [], 0
for p, s in code.items():
    body = strip_comments(s)
    for m in re.finditer(r"text = ([a-z_0-9.]+)", body):
        count += 1
        if m.group(1) not in loc_keys: probs.append(f"{m.group(1)} ({os.path.relpath(p, MOD)})")
    for m in re.finditer(r"custom_tooltip = ([a-z_0-9.]+)\s*$", body, re.M):
        count += 1
        if m.group(1) not in loc_keys: probs.append(f"{m.group(1)} ({os.path.relpath(p, MOD)})")
check("custom_tooltip/text loc keys exist", count, sorted(set(probs)), min_count=10)

# ---- situation name keys ----
sit_keys = []
for p, s in code.items():
    if "/situations/" not in p: continue
    for m in re.finditer(r"^([a-z_]+) = \{", strip_comments(s), re.M):
        sit_keys.append(m.group(1))
probs = []
for k in sit_keys:
    if k not in loc_keys: probs.append(f"{k} (situation name loc missing)")
    if k + "_desc" not in loc_keys: probs.append(f"{k}_desc (situation desc loc missing)")
check("situation <key>/<key>_desc loc", len(sit_keys), probs, min_count=6)

# ---- hint tags ----
hints_def = set(re.findall(r"^([a-z_0-9]+) = \{", strip_comments(read(MOD + "/in_game/common/scriptable_hints/MR_hints.txt")), re.M))
hint_refs = set()
for p, s in code.items():
    hint_refs |= set(re.findall(r"hint_tag = ([a-z_0-9]+)", strip_comments(s)))
probs = [f"{h} referenced but not defined" for h in sorted(hint_refs - hints_def)]
probs += [f"{h} loc missing" for h in sorted(hints_def) if h not in loc_keys]
check("hint tags defined + loc'd", len(hint_refs) + len(hints_def), probs, min_count=6)

# ---- scripted triggers resolve ----
trig_def = set(re.findall(r"^([A-Za-z_0-9]+) = \{", strip_comments(read(MOD + "/in_game/common/scripted_triggers/MR_scripted_triggers.txt")), re.M))
probs, count = [], 0
for p, s in code.items():
    for m in re.finditer(r"\b(mr_[a-z_0-9]+|MR_percent_of_army_balance) = yes", strip_comments(s)):
        n = m.group(1)
        if n.startswith(("mr_can_start", "mr_resurgence_end", "mr_imperial_end", "mr_dominance_end", "mr_chahar", "mr_torghut", "mr_dzungar", "mr_vanilla", "mr_resurgence_visible", "mr_imperial_visible", "mr_dominance_visible")) or n == "MR_percent_of_army_balance":
            count += 1
            if n not in trig_def: probs.append(f"{n} ({os.path.relpath(p, MOD)})")
check("scripted trigger refs resolve", count, sorted(set(probs)), min_count=10)

# ---- modifiers: refs defined, defs used, loc'd ----
mod_def = set(re.findall(r"^(MR_[A-Za-z_0-9]+) = \{", strip_comments(read(MOD + "/main_menu/common/static_modifiers/MR_modifiers.txt")), re.M))
mod_refs = set()
for p, s in code.items():
    mod_refs |= set(re.findall(r"(?:modifier = |remove_country_modifier = |has_country_modifier = )(MR_[A-Za-z_0-9]+)", strip_comments(s)))
probs = [f"{m} referenced but not defined" for m in sorted(mod_refs - mod_def)]
probs += [f"{m} defined but never referenced (orphan)" for m in sorted(mod_def - mod_refs)]
probs += [f"STATIC_MODIFIER_NAME_{m} loc missing" for m in sorted(mod_def) if "STATIC_MODIFIER_NAME_" + m not in loc_keys]
check("modifiers: refs<->defs<->loc", len(mod_def | mod_refs), probs, min_count=15)

# ---- game rules ----
rule_opts = set(re.findall(r"^\t([A-Za-z_0-9]+) = \{", strip_comments(read(MOD + "/main_menu/common/game_rules/MR_game_rules.txt")), re.M))
probs, count = [], 0
for p, s in code.items():
    for m in re.finditer(r"has_game_rule = ([A-Za-z_0-9]+)", strip_comments(s)):
        count += 1
        if m.group(1) not in rule_opts: probs.append(f"{m.group(1)} ({os.path.relpath(p, MOD)})")
rules = set(re.findall(r"^([A-Za-z_0-9]+) = \{", strip_comments(read(MOD + "/main_menu/common/game_rules/MR_game_rules.txt")), re.M))
for r in sorted(rules):
    if "rule_" + r not in loc_keys: probs.append(f"rule_{r} loc missing")
for o in sorted(rule_opts):
    if "setting_" + o not in loc_keys: probs.append(f"setting_{o} loc missing")
    if "setting_" + o + "_desc" not in loc_keys: probs.append(f"setting_{o}_desc loc missing")
check("game rule options: refs + loc", count, sorted(set(probs)), min_count=10)

# ---- wargoal loc ----
wg = set(re.findall(r"^(MR_war_goal_[a-z_]+) = \{", strip_comments(read(MOD + "/in_game/common/wargoals/MR_wargoals.txt")), re.M))
probs = []
for w in sorted(wg):
    if "war_goal_" + w not in loc_keys: probs.append(f"war_goal_{w} loc missing")
    if "war_goal_" + w + "_desc" not in loc_keys: probs.append(f"war_goal_{w}_desc loc missing")
check("wargoal war_goal_<key>(+_desc) loc", len(wg), probs, min_count=3)

# ---- CB <-> wargoal wiring + loc ----
cb_src = strip_comments(read(MOD + "/in_game/common/casus_belli/MR_casus_belli.txt"))
cbs = set(re.findall(r"^(cb_MR_[a-z_]+) = \{", cb_src, re.M))
probs = [f"{c} loc missing" for c in sorted(cbs) if c not in loc_keys]
probs += [f"wargoal {w} not defined" for w in re.findall(r"war_goal_type = ([A-Za-z_]+)", cb_src) if w not in wg]
check("CBs: loc + wargoal wiring", len(cbs), probs, min_count=3)

# ---- no any_owned_location with a bare geography predicate ----
# any_owned_location = { region = region:X } walks a country's whole
# holdings list; has_presence_in = region:X answers the same question
# with a purpose-built trigger (108 vanilla uses). All 104 of ours were
# the bare form and all were converted; this keeps them converted.
probs, count = [], 0
_bare = re.compile(r"any_owned_location = \{\s*(?:region|area) = (?:region|area):[a-z_]+\s*\}", re.S)
for p_, s_ in code.items():
    body = strip_comments(s_)
    count += body.count("any_owned_location")
    for _m in _bare.finditer(body):
        probs.append(f"{os.path.relpath(p_, MOD)}: use has_presence_in instead of {' '.join(_m.group(0).split())}")
# AUDIT 2026-07-29 (D5): len(code) was passed as the count — the check
# printed the FILE count while scanning zero occurrences. Prohibition
# checks count the pattern itself; zero occurrences IS the target state.
check("no any_owned_location with a bare geo predicate", count, sorted(set(probs)), min_count=0)

# ---- geography: regions/areas/locations exist in definitions ----
defs = read(VAN + "/in_game/map_data/definitions.txt")

# ---- goal territory must be legally takeable ----
# Every location a phase's goal trigger demands must be inside some wargoal's
# allowed_locations, or the war is won while the goal stays untakeable and the
# phase can never close. caucasus_region sat in the Phase 3 goal, reachable by
# no wargoal at all, until this check was written.
#
# Both sides now speak scripted_geography, so the comparison expands each named
# geography down to LOCATIONS and compares sets. That also catches the case a
# name-only check never could: a wargoal covering a region while the goal wants
# an area inside a different one.
_geo_src = ""
for p_ in glob.glob(MOD + "/in_game/common/scripted_geography/*.txt"):
    _geo_src += strip_comments(read(_np(p_)))

_region_locs, _area_locs, _prov_locs = {}, {}, {}
_cur_r = _cur_a = None
for _line in defs.split(chr(10)):
    m = re.match(r"\s*([a-z_0-9]+_region)\s*=\s*\{", _line)
    if m: _cur_r = m.group(1); _region_locs.setdefault(_cur_r, set()); _cur_a = None; continue
    m = re.match(r"\s*([a-z_0-9]+_area)\s*=\s*\{", _line)
    if m: _cur_a = m.group(1); _area_locs.setdefault(_cur_a, set()); continue
    m = re.match(r"\s*([a-z_0-9]+_province)\s*=\s*\{([^}]*)\}", _line)
    if m:
        _l = set(m.group(2).split())
        _prov_locs.setdefault(m.group(1), set()).update(_l)
        if _cur_a: _area_locs[_cur_a] |= _l
        if _cur_r: _region_locs[_cur_r] |= _l

def _expand(names):
    out = set()
    for n in names:
        if n in _region_locs: out |= _region_locs[n]
        elif n in _area_locs: out |= _area_locs[n]
        elif n in _prov_locs: out |= _prov_locs[n]
        else: out.add(n)
    return out

_geos = {}
for m in re.finditer(r"^([A-Za-z_0-9]+) = \{(.*?)^\}", _geo_src, re.M | re.S):
    _names = []
    for bm in re.finditer(r"(?:region|area|province_definition|location) = \{([^}]*)\}", m.group(2)):
        _names += bm.group(1).split()
    _geos[m.group(1)] = _expand(_names)

trg_src = strip_comments(read(MOD + "/in_game/common/scripted_triggers/MR_scripted_triggers.txt"))
wg_src = strip_comments(read(MOD + "/in_game/common/wargoals/MR_wargoals.txt"))

# what the wargoals can take, as locations
_cb = set()
_ALLOWED = "allowed_locations = " + chr(123) + "(.*?)" + chr(10) + chr(9)*2 + chr(125)
for _m in re.finditer(_ALLOWED, wg_src, re.S):
    _b = _m.group(1)
    for g in re.findall(r"scripted_geography:([A-Za-z_0-9]+)", _b):
        _cb |= _geos.get(g, set())
    _cb |= _expand(re.findall(r"scope:location\.(?:region|area) = (?:region|area):([a-z_0-9]+)", _b))

probs, count = [], 0
for _m in re.finditer(r"^(mr_p[23]_[a-z_]+|mr_resurgence_end_trigger) = \{(.*?)^\}", trg_src, re.M | re.S):
    for g in sorted(set(re.findall(r"scripted_geography:([A-Za-z_0-9]+)", _m.group(2)))):
        count += 1
        missing = _geos.get(g, set()) - _cb
        if missing:
            probs.append(f"{g} demanded by {_m.group(1)}: {len(missing)} locations no wargoal allows, e.g. {sorted(missing)[:4]}")
check("goal territory covered by a wargoal", count, probs, min_count=8)
probs, count = [], 0
geo_refs = set()
for p, s in code.items():
    b = strip_comments(s)
    geo_refs |= {("region", x) for x in re.findall(r"region:([a-z_0-9]+)", b)}
    geo_refs |= {("area", x) for x in re.findall(r"area:([a-z_0-9]+)", b)}
    geo_refs |= {("location", x) for x in re.findall(r"location:([a-z_0-9]+)", b)}
# Almost every geography name now lives inside the scripted_geography file as
# a BARE name in a region/area/province_definition/location block, which the
# prefix patterns above cannot see. Without this the check quietly fell from
# 40 items to 11 and a typo in that one file would have been unguarded — the
# exact vacuous-scan failure this harness exists to prevent.
for _kind, _members in re.findall(r"(region|area|province_definition|location) = \{([^}]*)\}", _geo_src):
    for _n in _members.split():
        geo_refs.add(("province" if _kind == "province_definition" else _kind, _n))
for kind, name in sorted(geo_refs):
    count += 1
    if not re.search(r"\b" + re.escape(name) + r"\b", defs):
        probs.append(f"{kind}:{name} not in definitions.txt")
assert ("region", "mongolia_region") in geo_refs  # known positive
check("regions/areas/locations exist", count, probs, min_count=25)

# ---- subjecthood must walk the whole chain ----
# is_subject_of is true only for a DIRECT vassal. Every question this mod asks
# about subjecthood is really "is this inside our realm", which must include a
# vassal's vassal — found in Phase 2 testing, where a sub-vassal's ground
# blocked the goal and the phase would not end. The same bug had the failsafe
# seizing a sub-vassal's land and the AI targeting its own sub-vassal.
# top_overlord_or_this (vanilla: hundred_years_war.txt:185) walks the chain and
# returns the country itself when it has no overlord.
# If a genuinely direct-vassal-only test is ever needed, say so in a comment on
# the same line and this check will let it through.
probs, count = [], 0
for p_, s_ in code.items():
    for _i, _l in enumerate(s_.split(chr(10)), 1):
        if "is_subject_of" not in _l: continue
        _code = _l.split("#")[0]
        if "is_subject_of" not in _code: continue          # a comment, fine
        count += 1
        if "direct" not in _l.lower():
            probs.append(f"{os.path.relpath(p_, MOD)}:{_i}: is_subject_of only "
                         f"matches a DIRECT vassal — use top_overlord_or_this, or "
                         f"note 'direct' in a comment if that is really the intent")
check("subjecthood walks the whole chain", count, probs, min_count=0)  # AUDIT 2026-07-29 (D5): same len(code) bug

# ---- everything we call exists in the ENGINE'S OWN documentation ----
# docs/EU5-Vanilla-Script-Docs/ is the output of the console commands
# `script_docs` and `dump_data_types`, run against the shipped game. It is the
# authority the citation rule was always appealing to: 1798 triggers and 1534
# effects, each with its **Supported Scopes**, 2436 modifier tags with their
# categories, plus event targets and on_actions.
#
# Regenerate after a game patch: launch with -debug_mode, open the console,
# run `script_docs` then `dump_data_types`, and copy the logs from the user
# folder over this directory.
BS = chr(92)
_SD = MOD + "/docs/EU5-Vanilla-Script-Docs"
if os.path.isdir(_SD):
    def _headed(fname, lvl):
        out = {}
        cur = None
        for _l in read(_np(os.path.join(_SD, fname))).split(chr(10)):
            if _l.startswith(lvl) and not _l.startswith(lvl + "#"):
                cur = _l[len(lvl):].strip(); out[cur] = []
            elif cur is not None:
                out[cur].append(_l)
        return out

    _trig = _headed("triggers.log", "## ")
    _eff = _headed("effects.log", "## ")
    _et = _headed("event_targets.log", "### ")
    _mods = {}
    for _l in read(_np(os.path.join(_SD, "modifiers.log"))).split(chr(10)):
        _m = re.match(r"Tag: ([a-z_0-9]+), Categories: (.*)", _l.strip())
        if _m:
            _mods[_m.group(1)] = {c.strip().lower() for c in _m.group(2).split(",") if c.strip()}
    _onact = set(re.findall(r"^([a-z_0-9]+):$", read(_np(os.path.join(_SD, "on_actions.log"))), re.M))

    # 1. modifier tags exist.
    # NOT their category: every tag in modifiers.log also carries "All", so a
    # category comparison can never fire — and it would be wrong anyway.
    # `siege_ability` is declared Unit yet works inside a category = country
    # static modifier here, so the category describes what a modifier AFFECTS,
    # not where it may be declared. A check that cannot fail is worse than no
    # check: it implies coverage it does not have.
    probs, count = [], 0
    _msrc = strip_comments(read(MOD + "/main_menu/common/static_modifiers/MR_modifiers.txt"))
    for _m in re.finditer(r"^([A-Za-z_0-9]+) = " + BS + "{(.*?)^" + BS + "}", _msrc, re.M | re.S):
        for _line in _m.group(2).split(chr(10)):
            _k = re.match(r"[ " + BS + "t]*([a-z_0-9]+) = ", _line)
            if not _k or _k.group(1) in ("game_data", "category"): continue
            count += 1
            if _k.group(1) not in _mods:
                probs.append(f"{_m.group(1)}: '{_k.group(1)}' is not a modifier tag the engine knows")
    check("modifier tags exist in engine docs", count, probs, min_count=50)

    # 2. on_action hooks
    probs = []
    _oa = strip_comments(read(MOD + "/in_game/common/on_action/MR_on_actions.txt"))
    _hooks = set(re.findall(r"^([a-z_0-9]+) = " + BS + "{", _oa, re.M))
    _own = _hooks & set(re.findall(r"^[ " + BS + "t]+([a-z_0-9]+)$", _oa, re.M))
    for _h in sorted(_hooks - _own):
        if _h not in _onact:
            probs.append(f"{_h} is not an on_action the engine declares")
    check("on_action hooks vs engine docs", len(_hooks), probs, min_count=2)

# ---- geography trigger matches the scope it sits in ----
# is_in_scripted_geography is a LOCATION trigger; has_presence_in is the
# COUNTRY one. Swapping them is silent in the harness and loud in game:
# "Inconsistent trigger scopes (country vs. location...)". 120 sites shipped
# the wrong one when the geography refactor landed.
_LOC_CTX = {"every_location_in_scripted_geography", "any_location_in_scripted_geography",
            "every_ownable_location_in_region", "any_ownable_location_in_region",
            "every_location_in_region", "any_location_in_region",
            "tooltip", "map_color", "secondary_map_color"}

def _is_loc_ctx(name):
    return name in _LOC_CTX or name.startswith("scope:location") or "capital" in name

probs, count = [], 0
for p_, s_ in code.items():
    stack = []
    for _i, _l in enumerate(s_.split(chr(10)), 1):
        _b = _l.split("#")[0]
        if " = scripted_geography:" in _b:
            count += 1
            _loc = any(_is_loc_ctx(x) for x in stack)
            _trig = _b.strip().split(" = ")[0]
            _want = "is_in_scripted_geography" if _loc else "has_presence_in"
            if _trig != _want:
                probs.append(f"{os.path.relpath(p_, MOD)}:{_i}: {_trig} in a "
                             f"{'location' if _loc else 'country'} scope, want {_want}")
        for _ in range(_b.count(chr(123))): stack.append(_b.strip().split("=")[0].strip())
        for _ in range(_b.count(chr(125))):
            if stack: stack.pop()
check("geography trigger matches its scope", count, probs, min_count=50)

# ---- every scripted geography is actually used ----
# A geography nobody references is either a leftover or a call site that was
# meant to use it and does not. Both are silent.
_defined = set(re.findall(r"^([A-Za-z_0-9]+) = \{", _geo_src, re.M))
_used = set()
for p, s in code.items():
    if "/scripted_geography/" in p: continue
    _used |= set(re.findall(r"scripted_geography:([A-Za-z_0-9]+)", strip_comments(s)))
probs = [f"{g} defined but never referenced" for g in sorted(_defined - _used)]
probs += [f"{g} referenced but not defined" for g in sorted(_used - _defined)]
check("scripted geographies defined <-> used", len(_defined), probs, min_count=5)

# ---- globals set<->read ----
gset, gread = set(), set()
for p, s in code.items():
    b = strip_comments(s)
    gset |= set(re.findall(r"set_global_variable = ([a-z_0-9]+)\s*$", b, re.M))
    gset |= set(re.findall(r"set_global_variable = \{\s*name = ([a-z_0-9]+)", b))
    gread |= set(re.findall(r"has_global_variable = ([a-z_0-9]+)", b))
    gread |= set(re.findall(r"remove_global_variable = ([a-z_0-9]+)", b))
probs = [f"{g} set but never read/removed" for g in sorted(gset - gread)]
probs += [f"{g} read but never set" for g in sorted(gread - gset)]
check("globals set<->read symmetric", len(gset | gread), probs, min_count=10)

# ---- situation vars cleaned in on_ended (aggregated across all files:
# events also write situation vars via situation:<key> = { set_variable }) ----
svars, removed = set(), set()
for p, s in code.items():
    b = strip_comments(s)
    if "/situations/" in p or "/events/" in p:
        svars |= set(re.findall(r"set_variable = \{\s*name = ([A-Za-z_0-9]+)", b))
    if "/situations/" in p:
        removed |= set(re.findall(r"remove_variable = ([A-Za-z_0-9]+)", b))
svars.discard("mr_temp_prestige")  # lives on countries; PD leaves temps too
probs = [f"{v} set but never removed in any on_ended" for v in sorted(svars - removed)]
check("situation vars cleaned in on_ended", len(svars), probs, min_count=5)

# ---- units/advances/buildings in events exist in vanilla ----
probs, count = [], 0
van_files = {
    "advance": glob.glob(VAN + "/in_game/common/advances/*.txt"),
    "building": glob.glob(VAN + "/in_game/common/building_types/*.txt"),
    "unit": glob.glob(VAN + "/in_game/common/unit_types/*.txt"),
}
van_cache = {k: "\n".join(read(p) for p in v) for k, v in van_files.items()}
for p, s in code.items():
    b = strip_comments(s)
    for m in re.finditer(r"has_advance = ([a-z_0-9]+)", b):
        count += 1
        if not re.search(r"^\s*" + m.group(1) + r"\s*=", van_cache["advance"], re.M): probs.append(f"advance {m.group(1)}")
    for m in re.finditer(r"building_type:([a-z_0-9]+)", b):
        count += 1
        if not re.search(r"^\s*" + m.group(1) + r"\s*=", van_cache["building"], re.M): probs.append(f"building {m.group(1)}")
    for m in re.finditer(r"type = (a_[a-z_0-9]+)", b):
        count += 1
        if not re.search(re.escape(m.group(1)), van_cache["unit"]): probs.append(f"unit {m.group(1)}")
check("advances/buildings/units exist in vanilla", count, sorted(set(probs)), min_count=10)

# ---- forbidden error-class patterns ----
probs, count = [], 0
for p, s in code.items():
    rel = os.path.relpath(p, MOD)
    for i, line in enumerate(strip_comments(s).splitlines(), 1):
        count += 1
        if re.search(r"\bthis = c:(MGO|MGE|OIR)\b", line):
            probs.append(f"this = c:TAG at {rel}:{i}")
        # `owner ?= c:TAG` is the banned bare link. `top_owner ?= c:TAG` is a
        # DIFFERENT trigger and is legitimate when a country_exists guard for
        # the same tag sits in the same AND — the realm test uses it.
        m2 = re.search(r"(?<!top_)owner \?= c:([A-Z]{3})", line)
        if m2:
            probs.append(f"owner ?= c:TAG at {rel}:{i}")
        m2 = re.search(r"top_owner \?= c:([A-Z]{3})", line)
        if m2:
            _lines = strip_comments(s).splitlines()
            _win = chr(10).join(_lines[max(0, i - 3):i - 1])
            if f"country_exists = c:{m2.group(1)}" not in _win:
                probs.append(f"UNGUARDED top_owner ?= c:{m2.group(1)} at {rel}:{i}")
        m = re.search(r"is_neighbor_of = c:(MGO|MGE)", line)
        if m:
            # allowed only when a country_exists guard for the same tag
            # appears on the immediately preceding non-empty lines (the
            # AND-guard idiom this mod uses everywhere).
            lines = strip_comments(s).splitlines()
            window = "\n".join(lines[max(0, i - 3):i - 1])
            if f"country_exists = c:{m.group(1)}" not in window:
                probs.append(f"UNGUARDED is_neighbor_of = c:{m.group(1)} at {rel}:{i}")
check("no unguarded c:TAG comparison patterns", count, probs, min_count=1000)

# ---- `prev` resolves to a country where a country is required ----
# `prev` is ONE scope hop up, and the hop is counted in scope-CHANGING blocks
# only — if/limit/AND/OR/NOT are transparent. Two hops down (claimant ->
# situation:X -> var:target) it therefore lands on the SITUATION, not on the
# claimant, and the engine says so: "Left side and right side during comparison
# were of different types (left was 'country', right was 'situation')",
# jomini_script_system.cpp:252. That shipped in all three railroad declare
# blocks. It is rare in the log because the pacing gate above it short-circuits
# nearly every tick, so it cannot be relied on to surface in testing.
_LINKS = {"owner", "top_owner", "ruler", "heir", "consort", "capital", "overlord",
          "top_overlord_or_this", "culture", "religion", "market", "province",
          "location", "area", "region", "this", "root", "prev", "from", "dynasty",
          "defender_leader", "attacker_leader", "employer", "country", "controller"}
_PREFIXED = re.compile(r"^(c|scope|var|situation|region|area|location|culture|religion|"
                       r"scripted_geography|province|continent|sub_continent|character|"
                       r"trait|building|government_type|culture_group|casus_belli):")
_ITER = re.compile(r"^(every|any|random|ordered)_")
# Scopes that are definitely NOT a country. `scope:`/`var:` are deliberately
# absent — their type is not knowable from the text, so they are never flagged.
_NOT_A_COUNTRY = re.compile(r"^(situation|region|area|location|scripted_geography|culture|"
                            r"religion|province|continent|sub_continent|character|dynasty|"
                            r"trait|building):|^(every|any|random|ordered)_"
                            r"(location|area|region|province|character|sub_unit|unit|"
                            r"building|advance|war|relation|goods)")
_NOT_A_COUNTRY_LINKS = {"capital", "ruler", "heir", "consort", "culture", "religion",
                        "market", "province", "location", "area", "region", "dynasty"}
# Positions whose right-hand side must be a COUNTRY.
_COUNTRY_TARGET = re.compile(
    r"^\s*(has_truce_with|top_overlord_or_this|is_subject_of|is_neighbor_of|is_at_war_with|"
    r"is_rival_of|is_allied_with|cancel_subject|target|first|second|this|overlord|owner|"
    r"top_owner)\s*\??=\s*prev\s*$")
_OPEN = re.compile(r"^\s*([A-Za-z0-9_:.\-]+)\s*\??=\s*\{\s*$")


def _prev_findings(src, rel):
    """Walk the scope stack; report country-target `prev` landing off-country."""
    found, seen, stack, depth = [], 0, [], 0
    for n, raw in enumerate(src.splitlines(), 1):
        line = re.sub(r"#.*", "", raw)
        if not line.strip():
            continue
        if _COUNTRY_TARGET.match(line):
            seen += 1
            parent = stack[-2][0] if len(stack) >= 2 else "<file root>"
            if _NOT_A_COUNTRY.match(parent) or parent in _NOT_A_COUNTRY_LINKS:
                found.append(f"{rel}:{n}: prev resolves to '{parent}', not a country"
                             f" -> {line.strip()[:48]}")
        m = _OPEN.match(line)
        if m:
            depth += 1
            k = m.group(1)
            if _PREFIXED.match(k) or _ITER.match(k) or k in _LINKS:
                stack.append((k, depth))
            continue
        depth += line.count("{")
        for _ in range(line.count("}")):
            if stack and stack[-1][1] == depth:
                stack.pop()
            depth -= 1
    return found, seen


# Known positive: the exact shape that shipped broken, so a parser that stops
# walking the stack cannot pass this check vacuously.
_canary = """
c:MGO = {
	if = {
		limit = {
			situation:mongol_resurgence = {
				var:mr_conquest_target_country = {
					NOT = {
						top_overlord_or_this ?= prev
					}
				}
			}
		}
	}
}
"""
assert _prev_findings(_canary, "canary")[0], "prev scope walker is broken — canary not flagged"
assert not _prev_findings(_canary.replace("?= prev", "?= c:MGO"), "canary")[0], \
    "prev scope walker false-positives on the fixed form"

probs, count = [], 0
for p, s in code.items():
    f, seen = _prev_findings(s, os.path.relpath(p, MOD).replace(os.sep, "/"))
    probs += f
    count += seen
# prev.prev / prevprev: zero uses anywhere in vanilla, so it is not attested
# syntax. save_scope_as + scope: is the way down more than one hop.
for p, s in code.items():
    for _ in re.finditer(r"\bprev\s*\.\s*prev\b|\bprevprev\b", strip_comments(s)):
        probs.append(f"{os.path.relpath(p, MOD)}: prev.prev is unattested syntax")
check("prev lands on a country where one is required", count, probs, min_count=8)

# ---- on_action hooks + events ----
oa = strip_comments(read(MOD + "/in_game/common/on_action/MR_on_actions.txt"))
probs = []
for e in re.findall(r"^\s+(mr_dominance\.\d+)$", oa, re.M):
    if e not in event_defs: probs.append(f"on_action fires undefined {e}")
check("on_action events defined", len(re.findall(r"mr_dominance\.\d+", oa)), probs, min_count=2)

print()
if fails:
    print(f"RESULT: {len(fails)} check(s) with findings: {', '.join(fails)}")
    sys.exit(1)
print("RESULT: all checks passed")
