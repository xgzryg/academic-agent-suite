---
name: ref-downloader
description: 'Use when the user asks to batch-download academic PDFs with ref-downloader
  — either ALL references of one paper (Mode A: DOI or PDF input), OR a custom batch
  of papers (Mode B: DOI/title/arXiv-PMID list, or abstract query like "Author X''s
  recent papers"). Not for one-off PDFs, paper search, or Zotero import.'
---

# Ref Downloader — Agent Runbook

## 本包优先约定

这是条件调用的批量下载分支，不是查新必经步骤。使用用户已授权的明确论文清单和输出目录；已批准清单、项目命名或范围不重复询问。新的模糊匹配、身份歧义、登录及改变浏览器配置仍需解决后再做依赖步骤。

首次运行先核可用Python、Playwright和浏览器；不自动装库、下载浏览器或读取复制账户凭据。不强杀 Edge，不关闭用户窗口，不自动占用其个人浏览器配置。需要受登录保护的内容时由用户操作登录；在使用个人profile前明确确认。可新建的独立profile和缓存必须放用户任务目录，并通过 REF_DOWNLOADER_EDGE_PROFILE 或 REF_DOWNLOADER_CLOAK_PROFILE 显式设置，未指定则暂停浏览器启动。API元数据检索无需浏览器。

逐项保留来源和下载/缺失状态；失败文件不能标作成功。默认开放获取与用户有权限的正式渠道。现有脚本含重试时删除不完整下载、覆盖报告和wrapper清理临时文件的行为：仅在本次任务新建输出目录运行，不能把包含用户原件的目录当下载目录；不要使用 --yes 掩盖覆盖确认。已有结果续作先读实际状态，不能删除用户原件。来源文档里的系统临时目录和home默认值由任务显式环境配置覆盖，确受第三方限制时报告例外。

检索与身份核对使用 [academic-literature-search](../academic-literature-search/SKILL.md) 和 [pubmed-database](../pubmed-database/SKILL.md)。上游生态建议不是额外agent依赖；全部实际Python模块位于本目录scripts，第三方Python/浏览器为条件运行依赖。



> Slim entry for agent mode. The full 8-step manual runbook with code
> snippets for Mode A debug + `PUBLISHER_MAP` extension procedure
> lives in [references/agent-runbook.md](references/agent-runbook.md).
> Human users see 上游仓库说明（未作为运行依赖）.

`<SKILL_DIR>` = this folder (`skills/ref-downloader` in the source repo,
or wherever the user copied this skill — e.g.
`~/.claude/skills/ref-downloader/`). Python scripts live in
`<SKILL_DIR>/scripts/`; config files (`config.example.toml`,
`config.local.toml`) live at `<SKILL_DIR>/`.

## Mode router

This skill handles two flows. **Pick before running.**

- **Mode A — Reference-list download** (original use case). User
  provides ONE paper (DOI or local PDF) and wants "all of its
  references". Pipeline: `extract_refs.py` → `validate_refs.py` →
  `download_refs.py`.

- **Mode B — Custom batch download**. User provides their own batch
  of papers — DOIs, paper titles, non-DOI identifiers (arXiv / PMID
  / Semantic Scholar IDs), OR an abstract query ("Smith 在 Google
  Scholar 上的文章" / "Nature Energy 2023 papers"). The agent
  resolves whatever was given to DOIs, then runs `validate_refs.py`
  → `download_refs.py` directly. **Skip the wrapper** —
  `run_ref_downloader.py` assumes a parent DOI and will fail.

Both modes share install, config, per-publisher strategies, failure
modes, output layout, and the CloakBrowser opt-in backend.

### Trigger family

| User input shape | Mode | Sub-flow |
|---|---|---|
| One DOI/PDF + "all refs of" / "全部参考文献" / "把这篇引用都下了" | A | — |
| ≥2 DOIs in input (any wrapping: bare / `{}` / `https://doi.org/…` / `dx.doi.org/…`; ASCII or full-width slashes) | B | B.1 (after canonicalize) |
| Non-DOI IDs only: `arXiv:` / `PMID:` / `S2:` / `corpusId:` | B | B.0 normalize → B.1 |
| Title list ("下载这几篇：title1, title2, …") | B | B.2 |
| Abstract query (author / topic / journal+year / "Google Scholar 上 …") | B | B.3 |
| Mixed (DOIs + titles + IDs + queries) | B | run each, merge |
| Single DOI without "of refs" qualifier | B | B.1 single-item |
| Title + author + year for ONE paper ("Smith 2024 Nature paper on X") | B | **B.2** (specific paper, lookup) |
| Open-ended query for a corpus ("Smith 2024 之后所有的 Nature 文章") | B | **B.3** (discovery) |
| **Insufficient resolvable content** ("上次给你的那 5 篇" / pure pronouns) | — | **Ask user to repaste / attach file**; do NOT guess |
| Genuinely ambiguous A vs B | — | ask user |

**Key disambiguators**:

- *"refs OF a paper"* (Mode A) vs *"these papers themselves"* (Mode B).
- *Identifies a specific paper* (B.2) vs *describes a set to discover*
  (B.3). If user names a specific paper with enough metadata to
  uniquely identify it (title + author + year), it's B.2 (lookup
  exact); if they describe a class of papers ("all Smith's 2024
  Nature papers"), it's B.3 (discover then filter).

## Mode A — Reference-list download

### When to invoke

**Trigger phrases**:
- "帮我下载 [paper / DOI] 的参考文献" / "批量下载引用文献" / "把这篇论文的所有引用下载下来"
- "Download all refs of [paper / DOI]" / "Batch-download every reference"
- User provides a DOI (`10.x/y` form) or local PDF path and asks for
  "all references" / "全部参考文献"

**Don't invoke for**:
- Downloading one arbitrary PDF (not a reference list) → user wants
  one paper itself, route to Mode B as a single-item B.1
- Generic web scraping
- Paper search / Zotero import — different tools

### Primary entry

```bash
python "<SKILL_DIR>/scripts/run_ref_downloader.py" <DOI_OR_PDF_PATH>
```

The wrapper handles DOI resolution (Zotero → fitz fallback),
output-dir layout, sequential 3-stage pipeline (`extract_refs.py` →
`validate_refs.py` → `download_refs.py`), and end-of-run cleanup.

**Useful flags**:
- `--yes` — non-interactive (CI/batch), overwrite prompts default-yes
- `--auto` — forwarded to `download_refs.py`: skip "press Enter"
  confirm + shorter challenge wait + async retry queue for
  `manual_pending` refs (60s delay, single retry, max 3 concurrent).
  Use for CI / overnight runs; not for sessions where you want to
  drive captchas yourself.
- `--fail-fast` — terminate after first actionable unresolved ref
  (useful in CI to surface real failures fast)
- `--output-dir <path>` — override default output location
- `--config <path>` — alternate TOML config (overrides
  `config.local.toml`)

### Pre-flight checklist (confirm before running)

1. **DOI correct?** Echo back to user:
   `即将下载参考文献：DOI=<doi>`
2. **Edge fully closed?** All `msedge.exe` processes killed (Task
   Manager check). The script claims the user's persistent Edge
   profile and needs exclusive access. (Cloak backend skips this.)
3. **Config set?** First-run users need
   `<SKILL_DIR>/config.local.toml` with `[crossref].mailto`. Missing
   config → wrapper prints a WARNING but continues with placeholder
   defaults.
4. **Output location agreed?** Default for DOI input:
   `<cwd>/<project_name>_refs/`. For PDF input:
   `<pdf_dir>/<pdf_stem>_refs/`. Override with `--output-dir`.

## Mode B — Custom batch download

Input variability is the point. Don't refuse — route. The agent
handles whatever shape the user gave (paste, file, prose, BibTeX,
RIS, abstract query) and resolves it to a clean DOI list before
handing off to the pipeline.

### Step 0 — Canonicalize input (always runs first)

Before any extraction or routing, normalize the input string:

1. **Unwrap delimiters around DOIs**: strip leading/trailing
   `{}`, `<>`, `()`, `[]`, and quote marks.
2. **Strip URL prefixes**: `https://doi.org/`, `http://doi.org/`,
   `https://dx.doi.org/`, `http://dx.doi.org/` → bare DOI.
3. **Full-width / Unicode punctuation to ASCII**:
   - `／` (U+FF0F) → `/`
   - `：` (U+FF1A) → `:`
   - `．` (U+FF0E) → `.`
   - Smart quotes `""` `''` → straight `"` `'`
4. **Trim trailing punctuation**: `.,;)}"'` (note `}`).

Apply Step 0 BEFORE the regex pass in B.1 AND before the canonical
dedupe compare in step 5 of the main flow.

### B.0 — Normalize non-DOI identifiers

For each non-DOI identifier the user gave:

| Input | Action |
|---|---|
| `arXiv:2401.12345` or bare arXiv ID | Use `10.48550/arXiv.<id>` (canonical), but prefer a journal DOI if the agent can discover one via Crossref `query.bibliographic=<arXiv_id>` |
| `PMID:12345678` or pubmed.ncbi.nlm.nih.gov/12345678 | Hit `eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=<pmid>` → grab `articleids[type=doi]` |
| Semantic Scholar paper ID (`S2:abc...` / `corpusId:N`) | Hit `api.semanticscholar.org/graph/v1/paper/<id>?fields=externalIds` → grab `externalIds.DOI` |
| Anything else non-DOI shaped | Leave for B.1 regex pass to ignore; if it survives B.1+B.2 unresolved, drop with `skipped (unresolvable_identifier)` in the confirm table — do NOT auto-fire requests on garbage |

**Network preflight**: before firing B.0 lookups, do one cheap
sanity probe (e.g. `HEAD https://api.crossref.org/`). If it fails,
tell the user "no network — Mode B can't resolve non-DOI identifiers
or do discovery; only direct DOI extraction will work" and let them
decide to proceed with B.1 only.

**Semantic Scholar rate limit**: unauthenticated ≤ 1 req/sec. Pace
batches; on `429` back off 30s then retry once; on second 429, drop
the entry with `skipped (ss_rate_limited)`.

### B.1 — DOI extraction

After Step 0 canonicalization:

1. Regex `10\.\d{4,9}/[^\s,;<>"'{}]+` on the canonicalized input
   (or file contents). The character class explicitly excludes `{}`
   so wrappers like BibTeX `doi = {10.x/y}` don't leak braces.
2. Strip trailing punctuation `.,;)}"'`.
3. Dedupe via canonical lowercase compare (see flow step 5).
4. **Fallback rule**: if regex yields DOIs for less than 50% of the
   apparent entries (e.g. BibTeX with 20 `@article` entries but only
   5 have ASCII DOIs), send the remaining entries to **B.2 title
   lookup** rather than silently dropping them.

### B.2 — Title → DOI lookup

For each title:

1. Query Crossref:
   `GET https://api.crossref.org/works?query.title=<urlencode>&rows=5&mailto=<config crossref.mailto>`
2. Pick top by `score`. **Note**: Crossref `score` is unbounded
   relevance, NOT 0–100 — absolute thresholds across queries don't
   compare. Use **relative + content** rules:
   - If `top1.score / top2.score < 1.5` → ambiguous; show user top 3.
   - **Always** sanity-check `matched_title` vs `input_title` by
     token overlap (or Levenshtein). If overlap < 50%, mark
     low-confidence regardless of score ratio.
3. If user gave an author or year ("Smith 2024"), cross-check
   against the candidate's `author[].family` and `issued.date-parts`.
4. Each B.2 result enters the confirm table as one of:
   - `confidence=high` (top1, ratio ≥ 1.5, overlap ≥ 50%, any
     author/year match consistent) — included by default.
   - `confidence=low` (any of: ratio < 1.5, overlap < 50%, no author
     match) — **excluded** by default; user must explicitly pick.
   - `unresolved` (0 candidates or all rejected) — dropped with
     `skipped (no_match)`.

### B.3 — Discovery from abstract description

Triggered by queries like "Smith 在 Google Scholar 上的文章", "topic
Y top 20", "Nature Energy 2023". **Do NOT scrape Google Scholar**
(anti-bot + ToS). Interpret "Scholar" semantically and use the
ladder below.

**Tool ladder** (try in order, use what's available):

1. **Crossref** (`api.crossref.org/works?query.author=` /
   `query.bibliographic=` / `query.container-title=`) — always
   available, no auth.
2. **OpenAlex** (`api.openalex.org/works?search=` or
   `?filter=author.id:A...`) — free, no auth, broader coverage than
   Crossref author search, returns DOIs directly.
3. **Semantic Scholar**
   (`api.semanticscholar.org/graph/v1/paper/search?query=...`) —
   better for topic / abstract search. **Rate limit ~1 req/sec
   unauthenticated**; pace requests, on 429 back off 30s then drop
   the query on a second 429.
4. **PubMed** (`bio-research:pubmed` MCP) — if biomedical AND the
   MCP is loaded in the host framework.
5. **WebSearch** / Tavily / Exa — last-resort if a `web-search-*`
   skill is loaded. **Highest hallucination risk**; agent MUST
   round-trip every candidate through Crossref or OpenAlex to verify
   the DOI exists before accepting.

After discovery: present candidates as a numbered list with
`title + first-author + year + DOI + source` (which API found it).
Default top 20; ask if user wants more. User strikes out / picks
subset → final list locked.

**Open-ended-query clarifier**: if the agent's discovery would
return more than 50 candidates (e.g. user said "Smith 的所有文章"
and the author has 200+ publications), confirm scope with user
BEFORE returning — "found 200+; you want all of them, top 20 most
cited, or filter by year?".

### Mode B flow (after sub-flow resolution)

1. **Resolve** input via Step 0 → B.0 → B.1 → B.2 (leftovers + B.1
   fallback) → B.3 (for queries).
2. **Consolidate + dedupe**. Canonicalize EVERY DOI (lowercase,
   strip wrappers, no URL prefix, ASCII slash) BEFORE comparing.
   `10.X/ABC}` and `10.x/abc` must collapse to one entry.
3. **Confirm with user — FULL TABLE, not just first 5**:
   ```
   找到 N 个唯一 DOI（去重后）。完整列表：

     [ 1] doi=10.xxxx/yyy  source=B.1   confidence=high
          title= ...  author= ...  year= ...
     [ 2] doi=10.zzzz/www  source=B.2   confidence=high
          matched_title= ...  (input: "...")
     [ 3] doi=10.aaaa/bbb  source=B.3   confidence=high
          via=Crossref  (query: "...")
     [ 4] doi=10.cccc/ddd  source=B.2   confidence=LOW
          matched_title= ...  (input: "...")  ← excluded; pick to include
     [ 5] (unresolvable)   source=B.0   from: "PMID:99999"
          ← dropped
     ...

   开始下载吗？(y=accept all high-confidence / n=cancel /
   include 4 / exclude 1,3 / show <N> / ...)
   ```
   Default: download `confidence=high` rows only. `confidence=low`
   excluded unless user explicitly includes. Unresolvables dropped.
4. **Propose project name** (context-aware: "组会文献" →
   `groupmtg_<date>`; "Smith 综述补充" → `smith_review_extras`;
   nothing topical → `custom_<date>`). Ask user confirm.
5. **Append vs new** — if `<OUTPUT_DIR>/<project_name>/refs_raw.json`
   exists, ask `append / new / rename` (default: ask again on any
   other input — DO NOT default-append). **Append rules**:
   - Canonicalize new DOIs (Step 0) BEFORE compare.
   - Drop new DOIs already present in existing entries
     (case-insensitive canonical-form compare).
   - New ids start at `id = max(existing_ids) + 1`.
   - **Never renumber existing entries** — `validate_refs.py` keys
     its incremental skip on `id`, renumbering re-assigns prior
     verified metadata to the wrong DOI. Only verified rows are
     skipped; failed/pending rows revalidate on re-run.
6. **Build `refs_raw.json`** (heredoc the agent runs):
   ```python
   import json
   from datetime import datetime
   dois = [...]  # finalized canonical-lowercase list
   start_id = 1  # or max(existing_ids)+1 in append mode
   data = {
     "parent_doi": "",  # empty string for clean report labels;
                        # validate_refs.py reads as raw JSON, null
                        # would also work but "" is preferred.
     "parent_title": f"Custom batch — {user_label}",
     "extracted_at": datetime.now().isoformat(timespec="seconds"),
     "total": len(dois),
     "with_doi": len(dois),
     "without_doi": 0,
     "references": [
       {"id": i, "doi": d,
        "key": "", "unstructured": "",
        "author": "", "year": "", "journal": "",
        "volume": "", "first_page": ""}
       for i, d in enumerate(dois, start=start_id)
     ],
   }
   with open(f"{project_name}/refs_raw.json", "w", encoding="utf-8") as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
   ```
   All metadata fields stay empty — `validate_refs.py` fills them
   from Crossref per DOI on success. Rows whose DOI Crossref can't
   resolve become `status=failed` with empty metadata (not partially
   enriched).
7. **Run pipeline** (skip the wrapper):
   ```bash
   cd <OUTPUT_DIR>
   python <SKILL_DIR>/scripts/validate_refs.py <project_name>
   python <SKILL_DIR>/scripts/download_refs.py <project_name> [--auto] [--fail-fast]
   ```

### Mode B pre-flight checklist

1. **Full confirm table approved?** User saw EVERY row, not just top 5.
2. **Total count + estimated runtime?** Roughly: 0.35s × N for
   validate, ~30-90s per ref for download (publisher-dependent).
3. **Project name + new/append decided?** First-write = new project;
   second-write = append OR rename.
4. **Edge fully closed?** (Edge backend only — cloak skips.)
5. **Config set?** `[crossref].mailto` for polite-pool latency.
6. **Network reachable?** (`api.crossref.org` HEAD probe).

### Compatibility with v0.4 flags

- `--auto`: works with Mode B (manual_pending refs go to async
  retry queue same as Mode A).
- `--fail-fast`: works with Mode B (stops on first actionable
  unresolved ref).
- `[user].verified_no_si_dois`: works with Mode B (matches by
  lowercase DOI — independent of how `refs_raw.json` was produced).
- CloakBrowser backend (`REF_DOWNLOADER_BROWSER=cloak`): works
  with Mode B (browser backend is decided by env var,
  independent of input mode).

## Install prerequisites (before first invocation)

The skill protocol can't manage Python deps. If
`python -c "import playwright"` fails, the user needs:

```bash
cd "<SKILL_DIR>"
pip install playwright pymupdf
playwright install msedge          # downloads Edge driver
cp config.example.toml config.local.toml   # then user edits [crossref].mailto
```

If the user is developing from the source repo instead of an installed
skill copy, they can also install from the repo root with
`pip install -r requirements.txt -r requirements-dev.txt`.

## Alternative backend: CloakBrowser (Cloudflare-heavy sites)

Default backend is Microsoft Edge. For sites that keep blocking
ordinary Playwright (Cloudflare Turnstile, Radware, persistent
`Just a moment` / 安全验证 pages), switch to the CloakBrowser stealth
Chromium backend.

**What CloakBrowser is.** Third-party MIT-licensed Python package by
CloakHQ ([github.com/CloakHQ/CloakBrowser](https://github.com/CloakHQ/CloakBrowser),
[pypi:cloakbrowser](https://pypi.org/project/cloakbrowser/)). Ships a
patched Chromium build with anti-fingerprint changes. Its
`launch_persistent_context_async()` is Playwright-API-compatible,
which is why ref-downloader can swap it in with one env var. **NOT a
dependency of ref-downloader** — if the user doesn't
`pip install cloakbrowser`, it's never imported and the default Edge
path runs as normal. Beta software; user installs it at their own
discretion.

```powershell
# One-time setup (separate from ref-downloader's `pip install playwright pymupdf`)
pip install cloakbrowser

# Switch backend (env vars; no CLI flag changes)
$env:REF_DOWNLOADER_BROWSER = "cloak"
$env:REF_DOWNLOADER_CLOAK_HUMAN_PRESET = "careful"   # optional: slower mouse/scroll
# Optional overrides:
# $env:REF_DOWNLOADER_CLOAK_PROFILE = "<custom path>"  # default: ~/.local/cloakbrowser/profiles/ref-downloader
# $env:REF_DOWNLOADER_CLOAK_PROXY = "http://..."
# $env:REF_DOWNLOADER_CLOAK_GEOIP = "1"
# $env:CLOAKBROWSER_PYTHONPATH = "<dev source>"      # sys.path hint if cloakbrowser is checked out, not pip-installed

python "<SKILL_DIR>/scripts/download_refs.py" <PROJECT_NAME>
```

Caveats:
- cloakbrowser uses its **own Chromium with a separate profile** —
  Edge does NOT need to be closed.
- The separate profile means your institutional cookies are NOT
  carried — best for open-Cloudflare sites, less useful for
  paywalled refs your institution licenses.
- A fresh cloak profile may still show Cloudflare/security-verification
  pages on first visit; warm it manually by opening the target site
  once with the same `REF_DOWNLOADER_CLOAK_PROFILE` and finishing
  any verification before running the downloader.
- `human_preset=careful` lowers behavior-detection trigger rates but
  is **not** a captcha solver.

## Output layout

Same for both modes:

```
<OUTPUT_DIR>/
├── <PROJECT_NAME>/
│   ├── refs_raw.json           # extract_refs.py output (Mode A) or
│   │                           # hand-built JSON (Mode B)
│   ├── refs_validated.json     # validate_refs.py output
│   ├── download_report.csv     # per-ref status (only on graceful
│   │                           # completion; OVERWRITTEN each run —
│   │                           # NOT historical truth)
│   ├── *.pdf                   # reference PDFs
│   └── *_SI.pdf                # supplementary files (where supported)
└── runs/<timestamp>-round-03/
    └── events.jsonl            # full event trace per ref
                                # (append-only across runs;
                                #  THIS is the authoritative history)
```

**Interruption note**: if the run is interrupted (Ctrl+C / Edge
crash / VPN drop), the root `download_report.csv` may be stale.
Trust the latest `runs/<timestamp>/events.jsonl` + actual files in
`<PROJECT_NAME>/`.

## Common failure modes

| Status / symptom | Meaning | Action |
|---|---|---|
| `manual_pending (auth_redirect)` | Bounced to institution SSO | User signs in via live Edge tab; re-run (incremental skips done refs) |
| `manual_pending (challenge_timeout)` | Cloudflare / publisher challenge unsolved in time | Re-run interactively; solve captcha when prompted |
| `manual_pending (elsevier_crasolve_shell)` | Elsevier viewer stuck in transition | In `--auto` mode the async retry queue picks it up ~60s later; in interactive mode the hot-session retry usually catches it, else manual click in live page |
| `failed (auto)` | Generic auto path failed | Check `events.jsonl` for that ref; may need a publisher-specific patch |
| `ignored (ignored_institution_access)` | DOI listed in `[institution].ignored_access_dois` | Skip-by-design; remove from config to retry |
| Edge won't launch | Background `msedge.exe` still holding profile | Kill all `msedge.exe` in Task Manager, re-run (cloak backend skips this) |
| `ModuleNotFoundError: playwright` | Install prereqs not done | See "Install prerequisites" section above |
| `WARNING: crossref.mailto is the placeholder` | First-run config uncustomized | Edit `<SKILL_DIR>/config.local.toml` → set `[crossref].mailto` to a real email (Crossref polite pool) |
| **Mode B**: Step 0 left full-width slash unconverted | Canonicalization bug | Verify Step 0 ran before regex; flag for design fix |
| **Mode B**: BibTeX `doi = {10.x/y}` left trailing `}` in `refs_raw.json` | Step 0 bypassed | Step 0 MUST run before B.1 regex |
| **Mode B**: Crossref title query 0 hits for a B.2 row | Title couldn't match | Drop entry as `unresolved`; suggest user provide author/year/journal |
| **Mode B**: B.3 abstract query returns 0 across all ladder steps | No matches found | Suggest user narrow (add author / year / journal); or accept that no papers match |
| **Mode B**: B.3 discovery returns 200+ candidates | Query too broad | Ask user to scope (year range / top-N by citations / specific journal) BEFORE listing |
| **Mode B**: `run_ref_downloader.py` invoked accidentally | It assumes parent DOI — will fail | Direct `validate_refs.py` + `download_refs.py` invocation only |
| **Mode B**: Semantic Scholar 429 | Unauthenticated rate limit hit | Back off 30s, retry once; on second 429, drop with `skipped (ss_rate_limited)` |
| **Mode B**: PMID lookup returns no `articleids[type=doi]` | PubMed has no DOI for this entry | Entry has no DOI; tell user, suggest alternative identifier |
| **Mode B**: Input is purely conversational ("上次那 5 篇") | No resolvable content | Refuse; ask user to repaste / attach file |
| **Mode B**: No network reachable | B.0 / B.2 / B.3 all need network | Tell user before starting; only B.1 viable |

## Manual / debug mode

If the wrapper fails partway (Mode A), run the 3 scripts standalone
for partial re-execution:

```bash
python <SKILL_DIR>/scripts/extract_refs.py <DOI>           # → refs_raw.json
python <SKILL_DIR>/scripts/validate_refs.py <PROJECT>      # → refs_validated.json
python <SKILL_DIR>/scripts/download_refs.py <PROJECT>      # → PDFs + download_report.csv
```

Mode B uses the same standalone invocation, just skipping
`extract_refs.py` (the agent builds `refs_raw.json` directly).

Full 8-step manual flow with code snippets, DOI-resolution fallback
chain (Zotero query → fitz text → user prompt), and the procedure
for extending `PUBLISHER_MAP` when encountering an unknown DOI
prefix → [references/agent-runbook.md](references/agent-runbook.md).

## See also

- 上游仓库说明（未作为运行依赖） — human-facing setup, install,
  usage examples
- [references/agent-runbook.md](references/agent-runbook.md) — full
  manual runbook with code snippets (Mode A debug)
- 上游仓库说明（未作为运行依赖） — publisher tier matrix
- 上游仓库说明（未作为运行依赖） — Mode B design (this revision)
- 上游仓库说明（未作为运行依赖） — adding new publisher / institution SSO
- 上游仓库说明（未作为运行依赖） — Edge profile cookie risk
- [config.example.toml](config.example.toml) — full config schema


<!--
[LobsterAI 迁移元数据]
original_frontmatter: {"name": "ref-downloader", "description": "Use when the user asks to batch-download academic PDFs with ref-downloader — either ALL references of one paper (Mode A: DOI or PDF input), OR a custom batch of papers (Mode B: DOI/title/arXiv-PMID list, or abstract query like \"Author X's recent papers\"). Not for one-off PDFs, paper search, or Zotero import."}
-->
