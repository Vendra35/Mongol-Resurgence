# Mongol Resurgence 1.1.0 - the Steam texts

Two fields, two formats: the **change notes** are plain text (BBCode would
print its tags literally); the **description's What's New** section is BBCode.
Upload only after the 1.1.0 test (docs/TESTING-GUIDE.md, Track 0b) has passed
and the release folder has been synced (the old `main_menu/setup/start/` must
be DELETED there, not only the new folder added).

## Change notes (plain text)

```
Mongol Resurgence 1.1.0 - updated for EU5 1.4 "Rio Salado"

*- Start a new campaign: the start-of-game data below applies only to a new game.
*- The Kazakhs, Safavid Persia, the Manchu and Bukhara get their start-of-game data again. 1.4 reads it from a new folder, so on 1.4 the old file was ignored and these heirs of the Great Partition came back as a "County of Kazakh" with no map knowledge.
*- The seven situations now end the 1.4 way, through outcomes. Every panel lists its possible endings - the goal and the deadline, and for the Great Partition the collapse, the empire enduring and the empire hollow at the deadline - with what each means and what it needs. Rewards and failure paths are unchanged.
*- The panels' old End Requirements card is gone; the hint button now sits on each outcome.
*- Complacency removed from two modifiers, as 1.4 removed the mechanic.
```

## Description - What's New (BBCode)

```
[h2]What's New - 1.1.0[/h2]
[list]
[*][b]Updated for EU5 1.4 "Rio Salado".[/b] Start a new campaign.
[*]The Kazakhs, Safavid Persia, the Manchu and Bukhara get their start-of-game data again (1.4 reads it from a new folder).
[*]The seven situations end the 1.4 way: every panel lists its possible endings, what each means and what it needs. Rewards and failure paths are unchanged.
[*]The old End Requirements card is gone from the panels; the hint button sits on each outcome.
[*]Complacency removed from two modifiers, as 1.4 removed the mechanic.
[/list]
```

Also bump nothing else: `.metadata/metadata.json` already reads 1.1.0 / 1.4.X.
