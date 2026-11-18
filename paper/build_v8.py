import markdown, pathlib, subprocess, sys

PAPER = pathlib.Path.home() / "workspace/mit-projects/nile-delta-system/paper"

SERIF = '"Times New Roman", "Liberation Serif", serif'
MONO = '"DejaVu Sans Mono", monospace'

# APA style for the Anusha paper: Times New Roman 12 point, one inch margins,
# page number top right, reference list with hanging indents.
APA_CSS = """
@page { size: A4; margin: 2.54cm; @top-right { content: counter(page); font-size: 10pt; color: #333; } }
body { font-family: %s; font-size: 12pt; line-height: 1.5; hyphens: none; }
h1 { font-size: 14pt; line-height: 1.3; text-align: center; margin-bottom: 0.3cm; }
h2 { font-size: 12pt; margin-top: 0.8cm; text-align: left; }
h3 { font-size: 12pt; margin-top: 0.6cm; font-style: italic; }
table { border-collapse: collapse; width: 100%%; margin: 0.4cm 0; font-size: 10pt; }
th, td { border: 0.5pt solid #888; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eeeeee; }
p { margin: 0.22cm 0; text-align: justify; }
li { margin: 0.1cm 0; }
code { font-family: %s; font-size: 10pt; }
pre { font-family: %s; font-size: 9.5pt; margin: 0.3cm 0 0.3cm 0.6cm; line-height: 1.4; }
.refs p { padding-left: 1.27cm; text-indent: -1.27cm; text-align: left; }
""" % (SERIF, MONO, MONO)

# Larson paper: same serif at 12 point, journal style page numbers.
LARSON_CSS = """
@page { size: A4; margin: 2.4cm 2.2cm; @bottom-center { content: counter(page); font-size: 9.5pt; color: #444; } }
body { font-family: %s; font-size: 12pt; line-height: 1.45; hyphens: none; }
h1 { font-size: 15pt; line-height: 1.3; margin-bottom: 0.2cm; }
h2 { font-size: 12.5pt; margin-top: 0.8cm; border-bottom: 0.5pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 12pt; margin-top: 0.6cm; }
table { border-collapse: collapse; width: 100%%; margin: 0.4cm 0; font-size: 10pt; }
th, td { border: 0.5pt solid #888; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eeeeee; }
p { margin: 0.22cm 0; text-align: justify; }
li { margin: 0.1cm 0; }
code { font-family: %s; font-size: 10pt; }
pre { font-family: %s; font-size: 9.5pt; margin: 0.3cm 0 0.3cm 0.6cm; line-height: 1.4; }
""" % (SERIF, MONO, MONO)

# Walkthrough: 11 point, tuned to hold exactly three pages.
WALK_CSS = """
@page { size: A4; margin: 2.0cm 2.2cm; @bottom-center { content: counter(page); font-size: 9pt; color: #444; } }
body { font-family: %s; font-size: 11pt; line-height: 1.36; hyphens: none; }
h1 { font-size: 17pt; line-height: 1.25; margin-bottom: 0.2cm; }
h2 { font-size: 12.5pt; margin-top: 0.5cm; border-bottom: 0.5pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; margin-top: 0.6cm; }
table { border-collapse: collapse; width: 100%%; margin: 0.35cm 0; font-size: 9pt; }
th, td { border: 0.5pt solid #888; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eeeeee; }
p { margin: 0.17cm 0; text-align: justify; }
li { margin: 0.1cm 0; }
code { font-family: %s; font-size: 9.5pt; }
pre { font-family: %s; font-size: 9.5pt; margin: 0.3cm 0 0.3cm 0.6cm; line-height: 1.4; }
""" % (SERIF, MONO, MONO)

# Ministry brief: 11 point, tuned to hold two pages.
BRIEF_CSS = """
@page { size: A4; margin: 1.9cm 2.0cm; @bottom-center { content: counter(page); font-size: 9pt; color: #444; } }
body { font-family: %s; font-size: 11pt; line-height: 1.34; hyphens: none; }
h1 { font-size: 16pt; line-height: 1.25; margin-bottom: 0.2cm; }
h2 { font-size: 12.5pt; margin-top: 0.45cm; border-bottom: 0.5pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; margin-top: 0.6cm; }
table { border-collapse: collapse; width: 100%%; margin: 0.3cm 0; font-size: 9pt; }
th, td { border: 0.5pt solid #888; padding: 2.5pt 5pt; text-align: left; vertical-align: top; }
th { background: #eeeeee; }
p { margin: 0.16cm 0; text-align: justify; }
li { margin: 0.1cm 0; }
code { font-family: %s; font-size: 9.5pt; }
pre { font-family: %s; font-size: 9.5pt; margin: 0.3cm 0 0.3cm 0.6cm; line-height: 1.4; }
""" % (SERIF, MONO, MONO)

CSS = {
    "User_Walkthrough_v8": WALK_CSS,
    "Academic_Paper_v8": APA_CSS,
    "Ministry_Brief_v8": BRIEF_CSS,
    "Larson_Paper_v8": LARSON_CSS,
}

names = ["User_Walkthrough_v8", "Academic_Paper_v8", "Ministry_Brief_v8", "Larson_Paper_v8"]
for name in names:
    src = (PAPER / f"{name}.md").read_text(encoding="utf-8")
    body = markdown.markdown(src, extensions=["tables", "fenced_code"])
    if name == "Academic_Paper_v8":
        marker = "<h2>References</h2>"
        head, sep, tail = body.partition(marker)
        if sep:
            body = head + marker + '<div class="refs">' + tail + "</div>"
    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS[name]}</style></head><body>{body}</body></html>"
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
