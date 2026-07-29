#!/usr/bin/env python3
"""DHE flavor-pack scaffold generator — ported from the 1066 sister
project (2026-07-30) and adapted to this mod's conventions: packs are
THEMED (mr_court, mr_economy...) rather than per-country, files follow
the MR_<pack>_dhe_events.txt naming next to MR_dominance_dhe_events.txt,
and each pack gets its own loc file (unique filename — never a second
file named MR_l_english.yml, the duplicate-filename shadow rule).

What it does NOT do: triggers, effects, option bodies, design. Those
follow this repo's CLAUDE.md citation discipline. What it does: the
two-file skeleton with every measured trap pre-answered.

THE EIGHT MEASURED TRAPS (proven in the sister project and in this
mod's own test log):
1. `.entry` — the sixth loc key nobody would guess: the per-country DHE
   timeline panel reads <id>.entry (country_dhe_lateralview.gui:194);
   missing = the known localization_util.cpp:103 error, which THIS
   mod's own test log caught once already.
2. `fire_only_once` is GLOBAL and 3,206/3,232 vanilla DHEs carry it —
   omit only for a deliberately repeating event.
3. Option names are EXPLICIT — 14,427/14,427 vanilla options carry
   `name =`.
4. Chains fire via trigger_event_silently / trigger_event_non_silently
   (both attested); there is no plain `trigger_event`.
5. `every_neighbour_country` DOES NOT EXIST; the broadcast idiom is
   every_country + limit.
6. `?=` on EVERY nullable link in the event-level trigger — the DHE
   panel re-evaluates listed events' triggers CONTINUOUSLY, and an
   unguarded link floods jomini_script_system.cpp:252 (this repo's
   decoder has a whole entry on that error class).
7. Event ids 1-9999; this project bands them 1-99 beats / 100-199
   chains / 900-999 hidden machinery.
8. THE TRIGGER LAW: FLAVOR events SHOULD carry an event-level trigger
   (being swallowed when conditions fail is the point). RAILROAD beats
   carry NONE — guards inside options as if/limit (this mod's
   dominance chain follows that rule; keep it that way).

Usage:
    python tools/new_flavor.py <spec-key> [--out DIR]

The skeleton is INERT: every event's trigger is `always = no` behind an
`# ARM:` marker — a generated pack lands with zero test debt until an
author arms it.
"""
import os
import re
import sys

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = (1337, 1, 1)

# ---------------------------------------------------------------- specs ---
# key: {
#   "tag":    the DHE tag gate (MGO before the proclamation, MGE after;
#             a pack whose window spans the switch fields TWO events or
#             uses the later tag — has_or_had_tag in the TRIGGER covers
#             the rest),
#   "events": [(id, "short comment", "from", "to", monthly_chance), ...]
# }
SPECS = {
    # The T1 court pack (FUTURE-DEVELOPMENT.md, approved 2026-07-30):
    # "court": {
    #     "tag": "MGO",
    #     "events": [
    #         (1, "The Return of Bayan", "1370.1.1", "1385.1.1", 10),
    #         (2, "The Karakorum Debate", "1380.1.1", "1420.1.1", 5),
    #     ],
    # },
    "demo": {   # --out testing only; never generate into the repo
        "tag": "MGO",
        "events": [
            (1, "the first beat", "1370.1.1", "1400.1.1", 10),
            (100, "its continuation", "1370.1.1", "1410.1.1", 5),
        ],
    },
}

EVENT_TPL = """######################################
# {num} — {comment}
######################################

{ns}.{num} = {{
	type = country_event
	title = {ns}.{num}.title
	desc = {ns}.{num}.desc
	outcome = neutral
	fire_only_once = yes

	illustration_tags = {{
		10 = regular
		10 = interior
	}}

	dynamic_historical_event = {{
		tag = {tag}
		from = {frm}
		to = {to}
		monthly_chance = {chance}
	}}

	# ARM: replace `always = no` with the real gate (this is a FLAVOR
	# event — it SHOULD have one; trap 8). Every nullable link behind
	# ?= (trap 6). Remember the railroad-off game rule gate if this
	# pack must respect it: NOT = {{ has_game_rule = mr_railroad_off }}.
	trigger = {{
		always = no
	}}

	option = {{
		name = {ns}.{num}.a
		historical_option = yes
	}}

	option = {{
		name = {ns}.{num}.b
	}}
}}
"""

BOM = b"\xef\xbb\xbf"


def _date(s):
    p = s.split(".")
    if len(p) != 3 or not all(x.isdigit() for x in p):
        sys.exit(f"bad date {s!r} — expected Y.M.D")
    return tuple(int(x) for x in p)


def _write(path, text, bom):
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = text.replace("\r\n", "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write((BOM if bom else b"") + data)
    return path


def generate(key, out):
    spec = SPECS.get(key) or sys.exit(f"no spec named {key!r} in SPECS")
    tag, events = spec["tag"], spec["events"]
    if not re.fullmatch(r"[A-Z][A-Z0-9]{2}", tag):
        sys.exit(f"tag {tag!r} is not a 3-char uppercase tag")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
        sys.exit(f"spec key {key!r} must be a lowercase slug")
    ns = f"mr_{key}"

    seen = set()
    for num, comment, frm, to, chance in events:
        if not 1 <= num <= 9999:
            sys.exit(f"event id {num} outside the engine's 1-9999 range")
        if num in seen:
            sys.exit(f"event id {num} duplicated in the spec")
        seen.add(num)
        if not (_date(frm) < _date(to) and _date(to) > START):
            sys.exit(f"event {num}: window {frm}..{to} must be ordered "
                     "and end after the 1337.1.1 start")
        if not 0 < chance <= 100:
            sys.exit(f"event {num}: monthly_chance {chance} outside 1-100")

    header = (f"namespace = {ns}\n"
              f"# {ns} — SCAFFOLD (tools/new_flavor.py). Every event is\n"
              f"# INERT until its `# ARM:` gate is replaced; the trigger\n"
              f"# law and the eight traps are in the generator header.\n\n")
    body = header + "\n".join(
        EVENT_TPL.format(ns=ns, num=n, comment=c, tag=tag, frm=f, to=t,
                         chance=ch)
        for n, c, f, t, ch in events)

    written = []
    written.append(_write(
        os.path.join(out, "in_game", "events", "DHE",
                     f"MR_{key}_dhe_events.txt"),
        body, bom=True))

    loc = ["﻿l_english:"]
    for n, c, _f, _t, _ch in events:
        loc += [f' {ns}.{n}.title: "TODO — {c}"',
                f' {ns}.{n}.desc: "TODO"',
                f' {ns}.{n}.entry: "TODO — DHE timeline label (trap 1)"',
                f' {ns}.{n}.historical_info: "TODO"',
                f' {ns}.{n}.a: "TODO"',
                f' {ns}.{n}.b: "TODO"']
    written.append(_write(
        os.path.join(out, "main_menu", "localization", "english",
                     f"MR_{key}_dhe_l_english.yml"),
        "\n".join(loc) + "\n", bom=False))   # BOM is the ﻿ literal

    # ------------------------------------------------------ self-check ---
    for p in written:
        raw = open(p, "rb").read()
        if raw[:3] != BOM:
            sys.exit(f"BOM self-check failed on {p}")
        text = raw.decode("utf-8-sig")
        if text.count("{") != text.count("}"):
            sys.exit(f"brace balance self-check failed on {p}")
        if p.endswith(".yml"):
            for line in text.splitlines()[1:]:
                if line and not re.match(r'^ [A-Za-z0-9_.]+: ".*"$', line):
                    sys.exit(f"loc line shape self-check failed on {p}: "
                             f"{line!r}")
        else:
            if text.count("name = ") != 2 * len(events):
                sys.exit(f"explicit option-name self-check failed on {p}")

    print(f"flavor pack scaffold '{key}' ({tag}) written — "
          f"{len(written)} files:")
    for p in written:
        print("  " + os.path.relpath(p, out))
    print("""
STILL YOURS TO DO (the generator cannot):
  1. replace every `always = no` ARM gate with the real, ?=-guarded
     trigger — citation discipline applies, script docs first
  2. write the six loc values per event (ONE physical line each)
  3. option bodies: effects, ai_chance, chains
  4. illustration_tags weights per mood, or a real `image =`
  5. verify the namespace collides with nothing (vanilla's 361 + this
     mod's mr_dominance/mr_history/mr_steppe/mr_vanilla_* families)
  6. run tools/verify_mod.py and raise its min_counts in the SAME
     commit that arms the first event""")


if __name__ == "__main__":
    argv = sys.argv[1:]
    out = MOD
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) != 1:
        sys.exit("usage: python tools/new_flavor.py <spec-key> [--out DIR]")
    if argv[0] == "demo" and os.path.abspath(out) == os.path.abspath(MOD):
        sys.exit("the demo spec only generates outside the repo (--out)")
    generate(argv[0], out)
