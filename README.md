# CSRR Faculty Media Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

An automation tool that finds and compiles the public scholarship of an entire faculty — op-eds, interviews, and media appearances — into clean Excel and Word reports. Built for the **Center for Security, Race and Rights (CSRR) at Rutgers Law School** to replace a manual, never-finished task with a repeatable pipeline.

This is an engineering/automation project, not a machine-learning one — and it's framed that way on purpose: it solved a real operational problem for a real stakeholder, end to end.

---

## The problem

A research center's influence lives partly in its faculty's public voice — the op-ed in a major paper, the cited interview, the podcast appearance. Tracking that across dozens of faculty and hundreds of outlets is exactly the kind of work that *should* be done regularly and almost never is, because doing it by hand is tedious and unbounded. CSRR needed an up-to-date, shareable record of its affiliates' media footprint for reporting, grant documentation, and communications — and needed it to be re-runnable, not a one-time spreadsheet that goes stale the next week.

## Where this fits

Media monitoring is a real, paid category — Cision and Meltwater sell enterprise contracts for roughly this capability at scale. The slice that's underserved is the *small institution* that has the same need (track our people's public work) without the budget or the appetite for an enterprise contract. A focused, self-hosted, free tool aimed at a known faculty list is a genuinely useful niche, and this is a working instance of it.

## What it does

```
CSRR website ──scrape──▶ faculty list ──search──▶ per-person media hits
                                                        │
                                       dedupe + filter to legitimate sources
                                                        │
                                   ┌────────────────────┴────────────────────┐
                                   ▼                                          ▼
                          Excel workbook                          Word report (per faculty)
```

1. **Pulls the faculty roster** directly from the CSRR website (with a maintained fallback list if the site layout changes).
2. **Searches each person's media footprint** across legitimate news and publication sources for op-eds, interviews, and appearances.
3. **Deduplicates and filters** results to credible outlets, with polite rate-limiting so it behaves on the open web.
4. **Generates two deliverables**: a structured Excel workbook (one row per appearance) and formatted Word reports — the formats the center actually circulates.

## Technical breakdown (the core of the project)

The engineering is the deliverable: a resilient, configurable scraper-and-reporter that a non-engineer can run.

- **Web scraping & resilience** (`requests` + `BeautifulSoup`) — parses the live faculty directory, tolerates layout drift via a fallback roster, and rate-limits with jitter so it's a good web citizen rather than a hammer.
- **Source discipline** — results are filtered to a curated set of legitimate publications and de-duplicated, because a media report is only useful if it's clean; noise and link-farm hits are actively excluded.
- **Document generation** — `pandas` + `python-docx` turn raw hits into the two artifacts the center uses: an Excel workbook for analysis and per-faculty Word reports for circulation. The tool ends at "here is the file you email," not "here is some JSON."
- **Operable by design** — a YAML config and an `argparse` CLI (including a 5-faculty quick-test mode) mean it's run by communications staff, not just its author. ~1,000 lines structured around that goal.

**Skills demonstrated:** practical web scraping and HTML parsing; building for resilience against a third-party site you don't control; automated document/report generation; CLI and config design for non-technical users; and scoping a tool tightly to one stakeholder's real workflow.

## Usage

```bash
pip install -r requirements.txt

python enhanced_faculty_media_tracker.py                 # full run -> Excel + Word
python enhanced_faculty_media_tracker.py --limit 5       # quick test on 5 faculty
python enhanced_faculty_media_tracker.py --help          # all options
```

Search window, sources, and output paths are set in the YAML config.

## Honest scope

This is deliberate, well-built automation, not AI: the matching is search-and-filter, not a learned model. It's included because shipping a reliable tool that a real organization depends on is its own engineering skill — and a related scraper + dataset for the same effort lives in [`mediabot_rulaw`](https://github.com/azrabano23/mediabot_rulaw).

## License

MIT — see [LICENSE](LICENSE). Author: **Azra Bano**, for Rutgers Law CSRR.
