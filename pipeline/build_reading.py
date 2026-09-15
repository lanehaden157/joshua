"""Generate Joshua-reading.txt, Joshua-words.tsv, and candidate-boundaries.md
from pipeline/corpus/wlc/Josh.xml (morphhb 2.0.2 OSIS XML).

Ketiv/Qere: the running OSIS text carries the Ketiv word unpointed when a
Qere override exists (<note type="variant"><rdg type="x-qere">...). For the
reading text we substitute the pointed Qere form at that slot (what is
actually read aloud). For words.tsv we emit a row for every <w> element in
the file, Ketiv and Qere alike, each keeping its own OSHB id -- this is the
literal "one row per word" reading and is what the 10,083-element corpus
count refers to.
"""
import re
import xml.etree.ElementTree as ET

NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
SRC = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\pipeline\corpus\wlc\Josh.xml"
OUT_READING = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\Joshua-reading.txt"
OUT_WORDS = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\Joshua-words.tsv"
OUT_BOUNDARIES = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\candidate-boundaries.md"

tree = ET.parse(SRC)
root = tree.getroot()

book_div = root.find(".//o:div[@osisID='Josh']", NS)

reading_lines = []
word_rows = []
boundaries = []

def local(tag):
    return tag.split("}")[-1] if "}" in tag else tag

def walk_verse_content(verse_el, ref):
    """Walk a <verse> element's children in document order, building the
    reading-text tokens for this verse and emitting word rows."""
    tokens = []  # pointed surface strings to join for the reading line
    glue_next = False  # after maqqef, next word glues onto previous token (no space)

    def handle_w(w_el):
        wid = w_el.get("id")
        lemma = w_el.get("lemma", "")
        morph = w_el.get("morph", "")
        surface = "".join(w_el.itertext())
        return wid, lemma, morph, surface

    def push(text):
        nonlocal glue_next
        if glue_next and tokens:
            tokens[-1] = tokens[-1] + text
            glue_next = False
        else:
            tokens.append(text)

    children = list(verse_el)
    i = 0
    n = len(children)
    while i < n:
        el = children[i]
        tag = local(el.tag)
        if tag == "w":
            wid, lemma, morph, surface = handle_w(el)
            qere = None
            if i + 1 < n and local(children[i + 1].tag) == "note":
                qere = children[i + 1].find("o:rdg[@type='x-qere']/o:w", NS)
                if qere is not None:
                    i += 1  # consume the note too
            if qere is not None:
                q_wid = qere.get("id")
                q_lemma = qere.get("lemma", "")
                q_morph = qere.get("morph", "")
                q_surface = "".join(qere.itertext())
                # reading text uses the pointed qere form
                push(q_surface)
                # words.tsv: one row per <w>, ketiv (unpointed, as written) then qere
                word_rows.append((wid, ref, surface, lemma, morph))
                word_rows.append((q_wid, ref, q_surface, q_lemma, q_morph))
            else:
                push(surface)
                word_rows.append((wid, ref, surface, lemma, morph))
        elif tag == "seg":
            seg_type = el.get("type", "")
            seg_text = el.text or ""
            if seg_type == "x-maqqef":
                # glue directly onto previous token, and glue the next word too
                if tokens:
                    tokens[-1] = tokens[-1] + seg_text
                else:
                    tokens.append(seg_text)
                glue_next = True
            elif seg_type == "x-sof-pasuq":
                if tokens:
                    tokens[-1] = tokens[-1] + seg_text
                else:
                    tokens.append(seg_text)
            elif seg_type in ("x-pe", "x-samekh"):
                boundaries.append((ref, seg_type))
            else:
                # unknown seg type -- keep text, space-joined
                if seg_text.strip():
                    tokens.append(seg_text)
        elif tag == "note":
            pass  # editorial notes (BHS caveat) -- not part of running text
        else:
            pass
        i += 1

    # join tokens with single spaces, but maqqef already glued directly
    line = " ".join(t for t in tokens if t != "")
    line = re.sub(r" +", " ", line).strip()
    return line


for chapter_el in book_div.findall("o:chapter", NS):
    chap_osis = chapter_el.get("osisID")  # e.g. Josh.1
    chap_num = chap_osis.split(".")[1]
    for verse_el in chapter_el.findall("o:verse", NS):
        v_osis = verse_el.get("osisID")  # e.g. Josh.1.1
        v_num = v_osis.split(".")[2]
        ref = f"{chap_num}:{v_num}"
        line = walk_verse_content(verse_el, f"Josh.{chap_num}.{v_num}")
        reading_lines.append(f"Josh {ref}\t{line}")

with open(OUT_READING, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(reading_lines) + "\n")

with open(OUT_WORDS, "w", encoding="utf-8", newline="\n") as f:
    f.write("word_id\tref\tsurface\tlemma\tmorph\n")
    for wid, ref, surface, lemma, morph in word_rows:
        f.write(f"{wid}\t{ref}\t{surface}\t{lemma}\t{morph}\n")

with open(OUT_BOUNDARIES, "w", encoding="utf-8", newline="\n") as f:
    f.write("# Candidate paragraph-break boundaries (petuhah / setumah)\n\n")
    f.write("Raw list of every `x-pe` (petuhah, פ) and `x-samekh` (setumah, ס) "
            "marker in Joshua, from OSHB (morphhb 2.0.2), in document order. "
            "Not interpreted or grouped.\n\n")
    f.write("| # | Ref | Type |\n|---|---|---|\n")
    for idx, (ref, seg_type) in enumerate(boundaries, 1):
        label = "petuhah (פ)" if seg_type == "x-pe" else "setumah (ס)"
        # ref is like Josh.1.1 -- convert to Josh C:V
        parts = ref.split(".")
        display_ref = f"Josh {parts[1]}:{parts[2]}"
        f.write(f"| {idx} | {display_ref} | {label} |\n")

print(f"verses: {len(reading_lines)}")
print(f"word rows: {len(word_rows)}")
print(f"boundaries: {len(boundaries)} "
      f"(pe={sum(1 for _,t in boundaries if t=='x-pe')}, "
      f"samekh={sum(1 for _,t in boundaries if t=='x-samekh')})")
