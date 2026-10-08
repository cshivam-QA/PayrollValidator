"""Renders an XML file as indented, syntax-highlighted, collapsible HTML.

Every piece of file content (tag names, attribute names/values, text,
comments) goes through markupsafe.escape, so the file is only ever shown
as text and can never inject markup or script into the viewer page.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

from markupsafe import Markup, escape


def _local_name(name: str) -> str:
    # "{namespace-uri}tag" -> "tag"
    if isinstance(name, str) and name.startswith("{"):
        return name.split("}", 1)[1]
    return name


class _Renderer:

    def __init__(self):
        self.lines = 0
        self.out: list[str] = []

    def line(self, depth: int, body: str, cls: str = "", toggle: bool = False) -> None:
        self.lines += 1
        tog = '<span class="tog" title="Collapse / expand"></span>' if toggle else ""
        self.out.append(
            f'<div class="ln{(" " + cls) if cls else ""}" style="--d:{depth}">'
            f'<span class="no">{self.lines}</span>'
            f'<span class="code">{tog}{body}</span></div>'
        )

    def text_line(self, depth: int, text: str) -> None:
        self.line(depth, f'<span class="x">{escape(text)}</span>')

    @staticmethod
    def open_tag(el: ET.Element, self_closing: bool = False) -> str:
        parts = [f'<span class="p">&lt;</span><span class="t">{escape(_local_name(el.tag))}</span>']
        for name, value in el.attrib.items():
            parts.append(
                f' <span class="a">{escape(_local_name(name))}</span>'
                f'<span class="p">=</span><span class="v">"{escape(value)}"</span>'
            )
        parts.append('<span class="p">/&gt;</span>' if self_closing else '<span class="p">&gt;</span>')
        return "".join(parts)

    @staticmethod
    def close_tag(el: ET.Element) -> str:
        return (
            f'<span class="p">&lt;/</span><span class="t">{escape(_local_name(el.tag))}</span>'
            f'<span class="p">&gt;</span>'
        )

    def element(self, el: ET.Element, depth: int) -> None:
        if el.tag is ET.Comment:
            self.line(depth, f'<span class="c">&lt;!--{escape(el.text or "")}--&gt;</span>')
        elif el.tag is ET.ProcessingInstruction:
            self.line(depth, f'<span class="c">&lt;?{escape(el.text or "")}?&gt;</span>')
        else:
            children = list(el)
            text = (el.text or "").strip()

            if not children:
                if text:
                    self.line(
                        depth,
                        self.open_tag(el) + f'<span class="x">{escape(text)}</span>' + self.close_tag(el),
                    )
                else:
                    self.line(depth, self.open_tag(el, self_closing=True))
            else:
                self.out.append('<div class="blk">')
                self.line(
                    depth,
                    self.open_tag(el) + '<span class="ell">&hellip;' + self.close_tag(el) + "</span>",
                    cls="open",
                    toggle=True,
                )
                self.out.append('<div class="kids">')
                if text:
                    self.text_line(depth + 1, text)
                for child in children:
                    self.element(child, depth + 1)
                self.out.append("</div>")
                self.line(depth, self.close_tag(el), cls="close")
                self.out.append("</div>")

        tail = (el.tail or "").strip()
        if tail and depth > 0:
            self.text_line(depth, tail)


def render_xml(data: bytes) -> tuple[Markup, bool, int]:
    """Returns (html, parsed, line_count). If the file isn't well-formed XML
    it is shown as escaped raw text line by line instead, with parsed=False."""

    renderer = _Renderer()

    try:
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
        root = ET.fromstring(data, parser=parser)
    except ET.ParseError:
        for raw_line in data.decode("utf-8", errors="replace").splitlines():
            renderer.text_line(0, raw_line)
        return Markup("".join(renderer.out)), False, renderer.lines

    renderer.element(root, 0)
    return Markup("".join(renderer.out)), True, renderer.lines
