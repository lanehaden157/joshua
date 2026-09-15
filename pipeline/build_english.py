"""Generate Joshua-english.txt from the WEB classic (WEBUS) USFM source.

Source: eBible.org eng-web (World English Bible Classic, USA spelling,
"Yahweh" for the divine name -- not eng-webp/eng-webbe, which render it
"LORD"). Public domain. USFM pulled from
https://ebible.org/Scriptures/eng-web_usfm.zip, book file
07-JOSeng-web.usfm.

Strips \\f ... \\f* footnotes (WEB's dagger/double-dagger markers) and
\\w word|strong="..."\\w* Strong's-number wrappers down to plain text.
Output shape matches Joshua-reading.txt: `Josh C:V<TAB>text`, one line
per verse -- a separate file, not a third column on the Hebrew file, so
existing readers of Joshua-reading.txt aren't affected by this addition.
"""
import re

SRC = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\pipeline\corpus\web\07-JOSeng-web.usfm"
OUT = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\Joshua-english.txt"
READING = r"C:\Users\laneh\OneDrive\Documents\Projects\Joshua\Joshua-reading.txt"

raw = open(SRC, encoding="utf-8").read()

# Strip footnotes entirely (they carry the dagger/double-dagger markers).
raw = re.sub(r"\\f \+.*?\\f\*", "", raw, flags=re.S)

# Tokenize on \c N and \v N markers, in document order.
marker_re = re.compile(r"\\c\s+(\d+)|\\v\s+(\d+)")
matches = list(marker_re.finditer(raw))

verses = []  # (chapter, verse, raw_text)
chapter = None
cur_verse = None
cur_start = None
for idx, m in enumerate(matches):
    seg_start = m.end()
    seg_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw)
    text = raw[seg_start:seg_end]
    if m.group(1) is not None:  # \c
        if cur_verse is not None:
            verses.append((chapter, cur_verse, cur_text))
        chapter = int(m.group(1))
        cur_verse = None
        cur_text = ""
    else:  # \v
        if cur_verse is not None:
            verses.append((chapter, cur_verse, cur_text))
        cur_verse = int(m.group(2))
        cur_text = text
if cur_verse is not None:
    verses.append((chapter, cur_verse, cur_text))


def clean(text):
    # \w word|strong="H1234"\w*  ->  word
    text = re.sub(r"\\w\s+([^|\\]+)\|[^\\]*\\w\*", r"\1", text)
    # any remaining USFM markers (\p, \m, stray \w*, etc.)
    text = re.sub(r"\\[A-Za-z0-9+]+\*?", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


lines = []
for chapter, verse, text in verses:
    lines.append(f"Josh {chapter}:{verse}\t{clean(text)}")

reading_line_count = sum(1 for _ in open(READING, encoding="utf-8"))
if len(lines) != reading_line_count:
    raise SystemExit(
        f"FAIL: {len(lines)} WEB verse lines != {reading_line_count} lines in "
        f"Joshua-reading.txt. Joshua's MT/LXX divergences are textual, not "
        f"renumbering -- a mismatch here means a bad download, not a real split."
    )

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {len(lines)} verses to {OUT}")
