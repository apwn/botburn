#!/usr/bin/env python3
"""Static + scenario QA for the public Botburn kit. Stdlib only.

  python3 scripts/validate.py           # this checkout
  python3 scripts/validate.py --selftest  # negative fixtures must FAIL
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "SKILL.md",
    "LICENSE",
    "description.txt",
    "docs/methodology.md",
    "docs/QA-CHECKLIST.md",
    "docs/QA-RESULTS.md",
    "docs/RELEASE-NOTES.md",
    "docs/assets/botburn-sample-audit.svg",
    "docs/assets/botburn-sample-audit.png",
    "examples/sample-audit.md",
    "examples/sample-dashboard-notes.md",
    "examples/fixtures/nested-denominator.md",
    "examples/fixtures/plan-windows.md",
    "scripts/validate.py",
]

DAY_NAMES = {
    "Mon": ("Mon", "Monday"),
    "Tue": ("Tue", "Tuesday"),
    "Wed": ("Wed", "Wednesday"),
    "Thu": ("Thu", "Thursday"),
    "Fri": ("Fri", "Friday"),
    "Sat": ("Sat", "Saturday"),
    "Sun": ("Sun", "Sunday"),
}


def _check(out: list, name: str, ok: bool, detail: str = "") -> None:
    out.append((name, ok, detail))


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def _png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def _md_files(root: Path) -> list[Path]:
    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if ".git" in p.parts:
            continue
        if p.suffix.lower() in {".md", ".txt"}:
            files.append(p)
    return files


def collect_checks(root: Path) -> list[tuple[str, bool, str]]:
    out: list[tuple[str, bool, str]] = []
    missing = [p for p in REQUIRED if not (root / p).is_file()]
    _check(out, "required_files", not missing, "missing: " + ", ".join(missing) if missing else f"{len(REQUIRED)} paths")

    def safe_read(rel: str) -> str:
        p = root / rel
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    license_txt = safe_read("LICENSE")
    readme = safe_read("README.md")
    skill = safe_read("SKILL.md")
    qa = safe_read("docs/QA-RESULTS.md")
    notes = safe_read("docs/RELEASE-NOTES.md")
    sample = safe_read("examples/sample-audit.md")
    method = safe_read("docs/methodology.md")
    desc = safe_read("description.txt")
    checklist = safe_read("docs/QA-CHECKLIST.md")
    dash = safe_read("examples/sample-dashboard-notes.md")
    nested_fx = safe_read("examples/fixtures/nested-denominator.md")
    windows_fx = safe_read("examples/fixtures/plan-windows.md")

    _check(out, "license_mit", "MIT License" in license_txt and "Thomas Kanze" in license_txt)

    _check(out, "readme_tldr", bool(re.search(r"^## TLDR", readme, re.M)))
    _check(out, "readme_credit", "https://x.com/ThomasKanze" in readme)
    _check(out, "readme_install", "Attach" in readme and "SKILL.md" in readme and "save" in readme.lower())
    _check(out, "readme_version", "0.1.0" in readme and "early" in readme.lower())
    _check(out, "readme_repo_link", "https://github.com/apwn/botburn" in readme)
    _check(out, "readme_limitations", "Reporting limitations" in readme and "`<1%`" in readme)
    _check(out, "readme_not_just_coding", "not just coding" in readme.lower() or "not only coding" in readme.lower())
    _check(out, "readme_deep_dive", bool(re.search(r"^## Deep dive", readme, re.M)))
    _check(out, "readme_visual", "docs/assets/botburn-sample-audit.svg" in readme)
    _check(
        out,
        "readme_windows",
        "current-week only" in readme and "last_7_days" in readme,
        "current plan vs historical",
    )
    _check(
        out,
        "readme_nested_denom",
        "Filtered" in readme and "global denominator" in readme.lower(),
    )

    _check(out, "skill_frontmatter_name", bool(re.search(r"^---\nname: Botburn\n", skill)))
    fm = skill.split("---", 2)
    _check(out, "skill_frontmatter_description", len(fm) >= 3 and "description:" in fm[1])
    _check(out, "skill_usage_review_first", "usage-review" in skill and "usage-review wins" in skill)
    _check(
        out,
        "skill_managed_canvas",
        "Call `Skill` with name `canvas`" in skill and "managed canvas" in skill.lower(),
    )
    _check(
        out,
        "skill_tldr_then_charts",
        "Largest-first charts" in skill
        and "Embedded view drilldowns" in skill
        and "Source details below" in skill,
    )
    _check(out, "skill_actual_data_only", "only when that view has **actual data**" in skill)
    _check(out, "skill_schema_discover", "Discover the live schema" in skill)
    _check(out, "description_matches_trigger", "where Grok Bot usage went" in desc)

    _check(
        out,
        "release_notes_draft",
        "draft" in notes.lower() and "0.1.0" in notes and ("Not** published" in notes or "Not published" in notes),
    )
    qa_flat = re.sub(r"\s+", " ", qa)
    _check(out, "qa_not_all_accounts", "not" in qa_flat.lower() and "all Grok Bot accounts" in qa_flat)

    md_files = [p for p in _md_files(root) if p.suffix == ".md"]
    link_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)")
    broken: list[str] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        for match in link_re.finditer(text):
            target = (match.group(1) or match.group(2)).split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            dest = (path.parent / target).resolve()
            try:
                dest.relative_to(root.resolve())
            except ValueError:
                broken.append(f"{path.name} -> {target} (escapes repo)")
                continue
            if not dest.exists():
                broken.append(f"{path.relative_to(root)} -> {target}")
    _check(out, "relative_links", not broken, "; ".join(broken) if broken else "ok")

    svg = root / "docs/assets/botburn-sample-audit.svg"
    png = root / "docs/assets/botburn-sample-audit.png"
    _check(out, "asset_svg", svg.is_file() and svg.stat().st_size > 0, f"{svg.stat().st_size}B" if svg.is_file() else "missing")
    _check(out, "asset_png", png.is_file() and png.stat().st_size > 0, f"{png.stat().st_size}B" if png.is_file() else "missing")

    svg_ok, svg_detail, svg_w, svg_h, svg_text = False, "missing", 0, 0, ""
    if svg.is_file():
        svg_text = svg.read_text(encoding="utf-8")
        try:
            tree = ET.parse(svg)
            el = tree.getroot()
            svg_ok = el.tag.endswith("svg")
            svg_w = int(float(el.attrib.get("width", "0")))
            svg_h = int(float(el.attrib.get("height", "0")))
            svg_detail = f"well-formed svg {svg_w}x{svg_h}"
        except (ET.ParseError, ValueError) as exc:
            svg_detail = str(exc)
    _check(out, "svg_well_formed", svg_ok, svg_detail)

    png_dim = _png_size(png) if png.is_file() else None
    if png_dim and svg_w and svg_h:
        _check(out, "png_matches_svg_size", png_dim == (svg_w, svg_h), f"png {png_dim[0]}x{png_dim[1]} vs svg {svg_w}x{svg_h}")
    else:
        _check(out, "png_matches_svg_size", False, "could not read png/svg size")

    identities = [
        ("bots", [44, 21, 12, 9, 14], 100),
        ("activity", [55, 43, 2], 100),
        ("days", [22, 51, 27], 100),
        ("harbor_split", [28, 16], 44),
    ]
    math_ok, math_detail = True, []
    blob = readme + "\n" + sample
    for label, parts, total in identities:
        eq = sum(parts) == total
        math_ok = math_ok and eq
        math_detail.append(f"{label} {parts}={'=' if eq else '!='}{total}")
        for n in parts + [total]:
            if f"{n}%" not in blob:
                math_ok = False
                math_detail.append(f"missing {n}% in readme/sample")
    _check(out, "sample_math", math_ok, "; ".join(math_detail))

    expected_widths = [("Harbor", 220, 44), ("Quill", 105, 21), ("Other", 70, 14), ("Coach", 60, 12), ("Ops", 45, 9)]
    width_ok, width_detail = True, []
    last_pct = None
    for name, width, pct in expected_widths:
        if name not in svg_text:
            width_ok = False
            width_detail.append(f"missing label {name}")
        if f'width="{width}"' not in svg_text:
            width_ok = False
            width_detail.append(f"missing width {width} for {name}")
        if last_pct is not None and pct > last_pct:
            width_ok = False
            width_detail.append(f"not largest-first at {name}")
        last_pct = pct
    _check(out, "svg_bar_scale", width_ok, "500px=100%; " + ", ".join(width_detail) if width_detail else "44/21/14/12/9 largest-first")

    # Days title must not overlap the Tue column (title y + font vs rect y).
    clip_ok, clip_detail = True, "ok"
    if svg_ok:
        ns = {"svg": "http://www.w3.org/2000/svg"}
        try:
            tree = ET.parse(svg)
            root_el = tree.getroot()

            def local(tag: str) -> str:
                return tag.split("}", 1)[-1]

            title_bb = None
            for t in root_el.iter():
                if local(t.tag) != "text":
                    continue
                if (t.text or "").strip().startswith("Days in window"):
                    x = float(t.attrib["x"])
                    y = float(t.attrib["y"])
                    size = float(t.attrib.get("font-size", "15"))
                    w = 0.62 * size * len((t.text or "").strip())
                    title_bb = (x, y - size, x + w, y + 2)
                    break
            cols = []
            for r in root_el.iter():
                if local(r.tag) != "rect":
                    continue
                h = float(r.attrib.get("height", "0"))
                w = float(r.attrib.get("width", "0"))
                if h >= 40 and 20 <= w <= 90:
                    x = float(r.attrib["x"])
                    y = float(r.attrib["y"])
                    cols.append((x, y, x + w, y + h))
            if title_bb is None or not cols:
                clip_ok, clip_detail = False, "missing days title or columns"
            else:
                hits = []
                tx0, ty0, tx1, ty1 = title_bb
                for i, (x0, y0, x1, y1) in enumerate(cols):
                    if tx0 < x1 and tx1 > x0 and ty0 < y1 and ty1 > y0:
                        hits.append(i)
                if hits:
                    clip_ok, clip_detail = False, f"days title overlaps column(s) {hits}; title={title_bb}"
                else:
                    clip_detail = f"title {title_bb} clear of {len(cols)} columns"
        except Exception as exc:
            clip_ok, clip_detail = False, str(exc)
    _check(out, "svg_days_title_clear", clip_ok, clip_detail)

    # Day TLDR must name the max day in the table (Tue 51%, not Wednesday).
    day_rows = re.findall(r"^\| (Mon|Tue|Wed|Thu|Fri|Sat|Sun) \| (\d+)% \|", sample, re.M)
    day_ok, day_detail = False, "no day table"
    if day_rows:
        mx_name, mx_pct = max(day_rows, key=lambda r: int(r[1]))
        matters = sample.split("### What matters", 1)[-1].split("### ", 1)[0]
        aliases = DAY_NAMES[mx_name]
        named = any(a in matters for a in aliases)
        wrong = [a for n, als in DAY_NAMES.items() if n != mx_name for a in als if a in matters and n in dict(day_rows)]
        # Allow mentioning other days only if not claimed as the spike percent.
        spike_wrong = bool(re.search(rf"({'|'.join(a for n, als in DAY_NAMES.items() if n != mx_name for a in als)})\s+\*?\*?{mx_pct}%", matters))
        day_ok = named and not spike_wrong
        day_detail = f"max {mx_name} {mx_pct}% in What matters={named} spike_wrong={spike_wrong}"
    _check(out, "sample_day_consistency", day_ok, day_detail)

    # Nested Harbor: 28+16=44; if heartbeat == routines parent, other named integer % on that line are double-count.
    nest_ok, nest_detail = True, "ok"
    m = re.search(r"Harbor \*\*(\d+)%\*\* \(chats (\d+)% \+ routines (\d+)%\)", sample)
    if not m:
        nest_ok, nest_detail = False, "missing Harbor (chats + routines) identity"
    else:
        h, chats, routines = map(int, m.groups())
        if chats + routines != h:
            nest_ok, nest_detail = False, f"{chats}+{routines}!={h}"
        hb = re.search(r"Site heartbeat \*\*(\d+)%\*\*", sample)
        if not hb:
            nest_ok, nest_detail = False, "missing Site heartbeat"
        elif int(hb.group(1)) != routines:
            nest_ok, nest_detail = False, f"heartbeat {hb.group(1)} != routines parent {routines}"
        # Integer percents on the paused-tails sentence must not be extra 1% points.
        paused = re.search(r"Paused Harbor routines[^\n]*", sample)
        if paused and re.search(r"(?<!<)\b1%", paused.group(0)):
            nest_ok, nest_detail = False, "paused tails listed as 1% on top of parent"
        if "`<1%`" not in sample:
            nest_ok, nest_detail = False, "missing <1% tails"
        if "2% unlabeled" not in sample and "2% gap" not in sample:
            nest_ok, nest_detail = False, "Harbor 16+26 vs 44 gap not disclosed"
    _check(out, "sample_nested_recon", nest_ok, nest_detail)

    _check(out, "fixture_nested", "16% of all Grok Bot usage" in nested_fx and "not 16% of Harbor" in nested_fx)
    _check(
        out,
        "fixture_windows",
        "current-week only" in windows_fx and "last_7_days" in windows_fx and "partial" in windows_fx.lower(),
    )

    public_parts = [
        readme, skill, qa, notes, sample, method, desc, checklist, dash, nested_fx, windows_fx, license_txt, svg_text,
    ]
    public_blob = "\n".join(public_parts)
    forbidden = [
        ("private_canvas_url", r"cursor\.com/canvas"),
        ("workspace_path", r"/workspace/"),
        ("updateskill_chatter", r"\bUpdateSkill\b"),
        ("draft_skills_path", r"draft-skills"),
        ("once_hosted", r"once hosted"),
        ("all_accounts_tested", r"all accounts were tested|all accounts tested"),
        ("email", r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}"),
    ]
    for name, pat in forbidden:
        hits = re.findall(pat, public_blob, flags=re.I)
        _check(out, f"privacy_{name}", not hits, f"{len(hits)} hit(s)" if hits else "clean")

    invented = [
        (r"\$\d", "dollar figure"),
        (r"\d[\d,]*\s+tokens\b", "token count"),
        (r"coding\s+\d+%", "coding percent"),
        (r"saves?\s+\d+%", "savings percent"),
        (r"savings % of", "savings of"),
    ]
    inv_hits = [label for pat, label in invented if re.search(pat, public_blob, re.I)]
    _check(out, "no_phantom_telemetry", not inv_hits, ", ".join(inv_hits) if inv_hits else "clean")

    _check(out, "lt1_preserved", "`<1%`" in sample and "`<1%`" in skill and "`<1%`" in method)
    _check(out, "lt1_not_charted", "<1%" not in svg_text and "0.5%" not in svg_text)

    rec_ok = "no further justified change" in sample and "No hour-of-day" in sample
    _check(out, "sample_recommendations", rec_ok, "heartbeat only; no unevidenced waking-hours rec")

    return out


def print_report(results: list[tuple[str, bool, str]]) -> int:
    fails = 0
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        if not ok:
            fails += 1
        suffix = f" — {detail}" if detail else ""
        print(f"{status}\t{name}{suffix}")
    print()
    if fails:
        print(f"{fails} check(s) failed")
        return 1
    print("all checks passed")
    return 0


def _copy_kit(dst: Path) -> None:
    for rel in REQUIRED:
        src = ROOT / rel
        dest = dst / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def _expect_fail(dst: Path, check_name: str) -> str | None:
    results = {name: ok for name, ok, _ in collect_checks(dst)}
    if check_name not in results:
        return f"{check_name} not in report"
    if results[check_name]:
        return f"{check_name} unexpectedly PASS"
    return None


def selftest() -> int:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)

        def kit(name: str) -> Path:
            p = base / name
            _copy_kit(p)
            return p

        # 1. missing required file
        d = kit("missing")
        (d / "SKILL.md").unlink()
        err = _expect_fail(d, "required_files")
        if err:
            errors.append("missing-file: " + err)

        # 2. broken relative link
        d = kit("broken-link")
        readme = d / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("./SKILL.md", "./nope.md"), encoding="utf-8")
        err = _expect_fail(d, "relative_links")
        if err:
            errors.append("broken-link: " + err)

        # 3. math identity broken
        d = kit("bad-math")
        sample = d / "examples/sample-audit.md"
        sample.write_text(sample.read_text(encoding="utf-8").replace("Quill 21%", "Quill 20%"), encoding="utf-8")
        err = _expect_fail(d, "sample_math")
        if err:
            errors.append("bad-math: " + err)

        # 4. private canvas URL
        d = kit("canvas-url")
        qa = d / "docs/QA-RESULTS.md"
        qa.write_text(qa.read_text(encoding="utf-8") + "\nhttps://cursor.com/canvas/store-deadbeef/abc\n", encoding="utf-8")
        err = _expect_fail(d, "privacy_private_canvas_url")
        if err:
            errors.append("canvas-url: " + err)

        # 5. phantom telemetry
        d = kit("phantom")
        (d / "README.md").write_text(
            (d / "README.md").read_text(encoding="utf-8") + "\nSaved 20% and 12,000 tokens; coding 40%.\n",
            encoding="utf-8",
        )
        err = _expect_fail(d, "no_phantom_telemetry")
        if err:
            errors.append("phantom: " + err)

        # 6. Wednesday vs Tue spike
        d = kit("wrong-day")
        text = (d / "examples/sample-audit.md").read_text(encoding="utf-8")
        text = text.replace("Tuesday **51%**", "Wednesday **51%**")
        (d / "examples/sample-audit.md").write_text(text, encoding="utf-8")
        err = _expect_fail(d, "sample_day_consistency")
        if err:
            errors.append("wrong-day: " + err)

        # 7. nested double-count 1% tails
        d = kit("double-count")
        text = (d / "examples/sample-audit.md").read_text(encoding="utf-8")
        text = text.replace(
            "Paused Harbor routines (plugin watch, ship kickoff, route recheck): **`<1%`** tails.",
            "Paused Harbor routines (plugin watch, ship kickoff, route recheck): 1% + 1% + `<1%` tails.",
        )
        (d / "examples/sample-audit.md").write_text(text, encoding="utf-8")
        err = _expect_fail(d, "sample_nested_recon")
        if err:
            errors.append("double-count: " + err)

        # 8. days title overlapping a column
        d = kit("clip")
        svg = (d / "docs/assets/botburn-sample-audit.svg").read_text(encoding="utf-8")
        svg = svg.replace('y="575"', 'y="640"', 1)  # drop title into Tue bar (y=608 h=102)
        (d / "docs/assets/botburn-sample-audit.svg").write_text(svg, encoding="utf-8")
        err = _expect_fail(d, "svg_days_title_clear")
        if err:
            errors.append("clip: " + err)

    if errors:
        print("SELFTEST FAIL")
        for e in errors:
            print("  " + e)
        return 1
    print("SELFTEST PASS — 8 negative fixtures failed as required")
    print("  missing SKILL.md → required_files")
    print("  broken ./nope.md → relative_links")
    print("  Quill 20% → sample_math")
    print("  cursor.com/canvas URL → privacy_private_canvas_url")
    print("  tokens/coding%/saves% → no_phantom_telemetry")
    print("  Wednesday 51% vs Tue table → sample_day_consistency")
    print("  paused tails 1% on 16% parent → sample_nested_recon")
    print("  days title y into Tue column → svg_days_title_clear")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    return print_report(collect_checks(ROOT))


if __name__ == "__main__":
    sys.exit(main())
