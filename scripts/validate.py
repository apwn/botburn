#!/usr/bin/env python3
"""Static QA for the public Botburn kit. Stdlib only."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILS = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global FAILS
    status = "PASS" if ok else "FAIL"
    if not ok:
        FAILS += 1
    suffix = f" — {detail}" if detail else ""
    print(f"{status}\t{name}{suffix}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    required = [
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
        "scripts/validate.py",
    ]
    missing = [p for p in required if not (ROOT / p).is_file()]
    check("required_files", not missing, "missing: " + ", ".join(missing) if missing else "13 paths")

    license_txt = read("LICENSE")
    check("license_mit", "MIT License" in license_txt and "Thomas Kanze" in license_txt)

    readme = read("README.md")
    skill = read("SKILL.md")
    qa = read("docs/QA-RESULTS.md")
    notes = read("docs/RELEASE-NOTES.md")
    sample = read("examples/sample-audit.md")
    method = read("docs/methodology.md")
    desc = read("description.txt")
    checklist = read("docs/QA-CHECKLIST.md")

    check("readme_tldr", bool(re.search(r"^## TLDR", readme, re.M)))
    check("readme_credit", "https://x.com/ThomasKanze" in readme)
    check("readme_install", "Attach" in readme and "SKILL.md" in readme and "save" in readme.lower())
    check("readme_version", "0.1.0" in readme and "early" in readme.lower())
    check("readme_repo_link", "https://github.com/apwn/botburn" in readme)
    check("readme_limitations", "Reporting limitations" in readme and "`<1%`" in readme)
    check("readme_not_just_coding", "not just coding" in readme.lower() or "not only coding" in readme.lower())
    check("readme_deep_dive", bool(re.search(r"^## Deep dive", readme, re.M)))
    check("readme_visual", "docs/assets/botburn-sample-audit.svg" in readme)

    check("skill_frontmatter_name", bool(re.search(r"^---\nname: Botburn\n", skill)))
    check("skill_frontmatter_description", "description:" in skill.split("---", 2)[1])
    check("skill_usage_review_first", "usage-review" in skill and "usage-review wins" in skill)
    check(
        "skill_managed_canvas",
        "Call `Skill` with name `canvas`" in skill and "managed canvas" in skill.lower(),
    )
    check(
        "skill_tldr_then_charts",
        "Largest-first charts" in skill and "Embedded view drilldowns" in skill and "Source details below" in skill,
    )
    check("skill_actual_data_only", "only when that view has **actual data**" in skill)
    check("description_matches_trigger", "where Grok Bot usage went" in desc)

    check("release_notes_draft", "draft" in notes.lower() and "0.1.0" in notes and "Not** published" in notes or "Not published" in notes)
    check("qa_not_all_accounts", "not" in qa.lower() and "all Grok Bot accounts" in qa)

    # Relative links and images
    md_files = [
        ROOT / "README.md",
        ROOT / "SKILL.md",
        ROOT / "docs/methodology.md",
        ROOT / "docs/QA-CHECKLIST.md",
        ROOT / "docs/QA-RESULTS.md",
        ROOT / "docs/RELEASE-NOTES.md",
        ROOT / "examples/sample-audit.md",
        ROOT / "examples/sample-dashboard-notes.md",
    ]
    link_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)")
    broken: list[str] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        for match in link_re.finditer(text):
            target = match.group(1) or match.group(2)
            target = target.split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            dest = (path.parent / target).resolve()
            try:
                dest.relative_to(ROOT.resolve())
            except ValueError:
                broken.append(f"{path.name} -> {target} (escapes repo)")
                continue
            if not dest.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    check("relative_links", not broken, "; ".join(broken) if broken else "ok")

    svg = ROOT / "docs/assets/botburn-sample-audit.svg"
    png = ROOT / "docs/assets/botburn-sample-audit.png"
    check("asset_svg", svg.is_file() and svg.stat().st_size > 0, f"{svg.stat().st_size}B")
    check("asset_png", png.is_file() and png.stat().st_size > 0, f"{png.stat().st_size}B")

    svg_ok = False
    svg_detail = ""
    try:
        tree = ET.parse(svg)
        root = tree.getroot()
        svg_ok = root.tag.endswith("svg")
        svg_detail = "well-formed svg"
    except ET.ParseError as exc:
        svg_detail = str(exc)
    check("svg_well_formed", svg_ok, svg_detail)

    # Example math (global shares)
    identities = [
        ("bots", [44, 21, 12, 9, 14], 100),
        ("activity", [55, 43, 2], 100),
        ("days", [22, 51, 27], 100),
        ("harbor_split", [28, 16], 44),
    ]
    math_ok = True
    math_detail = []
    for label, parts, total in identities:
        got = sum(parts)
        eq = got == total
        math_ok = math_ok and eq
        math_detail.append(f"{label} {parts}={'=' if eq else '!='}{total}")
        blob = readme + "\n" + sample
        for n in parts + [total]:
            if f"{n}%" not in blob:
                math_ok = False
                math_detail.append(f"missing {n}% in readme/sample")
    check("sample_math", math_ok, "; ".join(math_detail))

    # SVG bar scale: 500px track = 100%
    svg_text = svg.read_text(encoding="utf-8")
    expected_widths = {"Harbor": 220, "Quill": 105, "Other": 70, "Coach": 60, "Ops": 45}
    width_ok = True
    width_detail = []
    for name, width in expected_widths.items():
        if f">{name}<" not in svg_text and f">{name}</text>" not in svg_text:
            width_ok = False
            width_detail.append(f"missing label {name}")
        if f'width="{width}"' not in svg_text:
            width_ok = False
            width_detail.append(f"missing width {width} for {name}")
    check("svg_bar_scale", width_ok, "500px=100%; " + ", ".join(width_detail) if width_detail else "44/21/14/12/9")

    public_blob = "\n".join(
        [
            readme,
            skill,
            qa,
            notes,
            sample,
            method,
            desc,
            checklist,
            read("examples/sample-dashboard-notes.md"),
            license_txt,
        ]
    )
    forbidden = [
        ("private_canvas_url", r"cursor\.com/canvas"),
        ("workspace_path", r"/workspace/"),
        ("updateskill_chatter", r"\bUpdateSkill\b"),
        ("draft_skills_path", r"draft-skills"),
        ("once_hosted", r"once hosted"),
        ("all_accounts_tested", r"all accounts were tested|all accounts tested"),
    ]
    for name, pat in forbidden:
        hits = re.findall(pat, public_blob, flags=re.I)
        check(f"privacy_{name}", not hits, f"{len(hits)} hit(s)" if hits else "clean")

    invented = [
        r"\$\d",
        r"tokens? saved",
        r"saves? \d+%",
        r"savings % of",
    ]
    inv_hits = [p for p in invented if re.search(p, public_blob, re.I)]
    check("no_invented_costs_or_savings", not inv_hits, ", ".join(inv_hits) if inv_hits else "clean")

    check("lt1_preserved", "`<1%`" in sample and "`<1%`" in skill and "`<1%`" in method)

    print()
    if FAILS:
        print(f"{FAILS} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
