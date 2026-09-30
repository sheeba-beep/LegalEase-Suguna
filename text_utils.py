import html
import re

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()

def markdownish_to_html(text: str) -> str:
    text = sanitize_text(text)
    if not text:
        return "<p>No document available.</p>"
    output, in_list = [], False
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue
        if stripped.startswith("### "):
            if in_list: output.append("</ul>"); in_list = False
            output.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            if in_list: output.append("</ul>"); in_list = False
            output.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            if in_list: output.append("</ul>"); in_list = False
            output.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{html.escape(stripped[2:])}</li>")
        else:
            if in_list: output.append("</ul>"); in_list = False
            escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(stripped))
            output.append(f"<p>{escaped}</p>")
    if in_list:
        output.append("</ul>")
    return "\n".join(output)

def pdf_safe_text(text: str) -> str:
    for old, new in {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u00a0": " ",
    }.items():
        text = text.replace(old, new)
    return text
