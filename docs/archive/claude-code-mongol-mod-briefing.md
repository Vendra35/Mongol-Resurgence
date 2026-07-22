# Claude Code Handover: Mongol Resurgence (Railroad) Mod Audit

> Paste this file as-is into Claude Code in VS Code. You should first have added to the
> workspace: (1) the EU5 vanilla game files, (2) your Prussian Destiny mod folder,
> (3) the modding guides you saved as PDFs from the EU5 Wiki (Mod Structure, Situation
> modding, Event modding, etc.), and (4) this file.

---

## 1. Your Role and the General Situation

I am developing a mod for Europa Universalis V called "Mongol Resurgence" (sometimes
also referred to as "Mongol Railroad"). This mod takes as its model the architecture of
another mod of mine, **Prussian Destiny** — which sits in the workspace, works, and has
been tested.

**Important:** the code for this mod was written so far with **Cline + DeepSeek V4 Pro
Thinking**, BUT it contained a large number of errors and is still not fully
trustworthy. The categories of error found/fixed so far:

- Invented 4-letter tags (`YUAN`, `CHAG`, `ILKH`, `MOG`, `TRSX`) — in EU5 tags are
  strictly 3 letters.
- Situation fields invented that do not exist in vanilla: `title`, `description`,
  `trigger` (at situation level), `targets`, `progress`, `completion`, `abort`,
  `actions`, `left_panel_content`, `ai_weight`, `sort_order`. These do NOT exist in
  Prussian Destiny's real code.
- Missing/incorrect parameter use such as `set_variable = { name = ... name = ... }`
  (the second parameter should be `value`).
- `country_exists = c:TAG` needs to be used instead of `exists = c:TAG`.
- Wrong location names (`location:zhongdu` instead of `location:beijing`,
  `location:sarai_al_jadid` instead of `location:sarai`).
- GFX/GUI references embedded inside the situation file (they need to be pulled out
  into separate `.gui` files).
- Other format errors were also found, such as the metadata format
  (`supported_game_version` instead of `version`).
- A move was made from `owns` to `controls`, but whether that change is correct (the
  difference in meaning between ownership and military control) has **not been
  confirmed** — check this yourself.

**Your task:** do not trust this code blindly. Audit every line — especially the syntax
and the tag/name references — by comparing it against the vanilla files and the wiki
guides I saved as PDFs. Do not guess. Search the vanilla files for anything you are
unsure about, and if necessary check `https://eu5.paradoxwikis.com/Modding`,
`https://eu5.paradoxwikis.com/Europa_Universalis_5_Wiki`,
`https://eu5.paradoxwikis.com/Category:Country_lists` and other relevant wiki pages
using your WebSearch/WebFetch tools.

---

## 2. How I Want You To Proceed

1. **Change nothing at first.** Read the existing Mongol mod files in the workspace,
   Prussian Destiny, and the vanilla reference files (situations, formable_countries,
   events, setup/countries).
2. **Verify the tag table independently** (the table above) — I think you should first
   look at the tags via the wiki at `https://eu5.paradoxwikis.com/Category:Country_lists`
   (with WebFetch), because finding them in the vanilla files first may be difficult. If
   you cannot find them on the wiki, then try to find them in the EU5 vanilla files at
   `../EU5-Vanilla/game`.
3. **Audit, one by one, whether the error categories listed above have genuinely been
   fixed.** Do not rely on grep/text scanning — think about whether it is logically
   correct (for example, evaluate whether the `owns`→`controls` change is right for our
   scenario).
4. **Report every problem you find to me, and do not write to the files until I approve.**
   Instead of one big "I fixed everything" report, I want a categorized list of findings:
   definite errors / suspect points / needs clarification.
5. Once the audit is finished and I have approved it, begin the fixes — proceed file by
   file, summarizing what you did at each step. Do not do it all silently in one pass.

When you are ready, report only the results of the **tag verification** and the
**error-category audit** first — do not start writing code yet.
