import markdown, pathlib, subprocess, sys

PAPER = pathlib.Path.home() / "workspace/mit-projects/nile-delta-system/paper"
CSS = """
@page { size: A4; margin: 2.4cm 2.2cm; @bottom-center { content: counter(page); font-size: 9pt; color: #444; } }
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 10.5pt; line-height: 1.5; hyphens: none; }
h1 { font-size: 19pt; line-height: 1.25; margin-bottom: 0.2cm; }
h2 { font-size: 13.5pt; margin-top: 0.9cm; border-bottom: 0.5pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; margin-top: 0.7cm; }
table { border-collapse: collapse; width: 100%; margin: 0.4cm 0; font-size: 9pt; }
th, td { border: 0.5pt solid #888; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eeeeee; }
p { margin: 0.25cm 0; text-align: justify; }
li { margin: 0.1cm 0; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }
pre { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; margin: 0.3cm 0 0.3cm 0.6cm; line-height: 1.45; }
"""

WALK_CSS = """
@page { size: A4; margin: 2.0cm 2.2cm; @bottom-center { content: counter(page); font-size: 9pt; color: #444; } }
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 10pt; line-height: 1.37; hyphens: none; }
h1 { font-size: 18pt; line-height: 1.25; margin-bottom: 0.2cm; }
h2 { font-size: 12.5pt; margin-top: 0.5cm; border-bottom: 0.5pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 11pt; margin-top: 0.6cm; }
table { border-collapse: collapse; width: 100%; margin: 0.35cm 0; font-size: 8.5pt; }
th, td { border: 0.5pt solid #888; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eeeeee; }
p { margin: 0.18cm 0; text-align: justify; }
li { margin: 0.1cm 0; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }
pre { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; margin: 0.3cm 0 0.3cm 0.6cm; line-height: 1.45; }
"""

names = ["User_Walkthrough_v8", "Academic_Paper_v8", "Ministry_Brief_v8", "Larson_Paper_v8"]
for name in names:
    src = (PAPER / f"{name}.md").read_text(encoding="utf-8")
    body = markdown.markdown(src, extensions=["tables", "fenced_code"])
    css = WALK_CSS if name in ("User_Walkthrough_v8", "Ministry_Brief_v8") else CSS
    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
    html_path = PAPER / f"{name}.html"
    html_path.write_text(html, encoding="utf-8")
    out = subprocess.run(["python3", "-m", "weasyprint", str(html_path), str(PAPER / f"{name}.pdf")],
                         capture_output=True, text=True)
    if out.returncode != 0:
        print(name, "WEASYPRINT FAILED", out.stderr[-500:])
        sys.exit(1)
    info = subprocess.run(["pdfinfo", str(PAPER / f"{name}.pdf")], capture_output=True, text=True).stdout
    pages = [l for l in info.splitlines() if l.startswith("Pages")][0]
    print(name, pages)
print("done")
