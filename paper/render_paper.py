import markdown, pathlib
src = pathlib.Path("Nile_Delta_Paper.md").read_text(encoding="utf-8")
html_body = markdown.markdown(src, extensions=["tables"])
css = """
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
"""
html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{html_body}</body></html>"
pathlib.Path("Nile_Delta_Paper.html").write_text(html, encoding="utf-8")
print("html written", len(html))
