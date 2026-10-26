"""Arabic/English text utilities shared by the validator and the craft checks. Standard library only."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STOPWORDS = json.loads((HERE / "dialects.json").read_text(encoding="utf-8"))["stopwords"]

# ---------------------------------------------------------------- text tools
AR_MARKS = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭـ]")
EASTERN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
TAG_RE = re.compile(r"\[[^\]]*\]")
BREAK_RE = re.compile(r"<break\b[^>]*/?>", re.I)
PAUSE_RE = re.compile(r"(?<!\d)/(?!\d)")
AR_PREFIXES = ["وبال", "فبال", "وال", "بال", "فال", "كال", "لل", "ال", "و", "ف", "ب", "ل", "ك"]
ARABIC_CHAR = re.compile("[؀-ۿ]")
SLOT_RE = re.compile(r"\{\{(.*?)\}\}", re.S)  # «{{…}}»: a detail only the creator can fill in
SLOT_WORDS = 4  # an unfilled slot is timed as four spoken words


def normalize(text):
    """Lowercase, drop Arabic diacritics/tatweel, unify alef/ya/ta marbuta forms."""
    t = AR_MARKS.sub("", str(text)).translate(EASTERN_DIGITS)
    t = re.sub("[أإآٱ]", "ا", t)
    return t.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي").replace("گ", "ك").replace("چ", "ج").lower()


def strip_markup(text):
    """Remove ElevenLabs tags, <break> tags and '/' pause markers."""
    return PAUSE_RE.sub(" ", BREAK_RE.sub(" ", TAG_RE.sub(" ", str(text))))


def tokens(text):
    t = normalize(strip_markup(text))
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)
    return [x for x in re.findall(r"[\w%'’.-]+", t) if re.search(r"\w", x)]


SENT_RE = re.compile(r"(?:(?<!\d)\.|\.(?!\d)|[!?؟…\n])+")


def unslot(text):
    """The text without the body of any {{…}} slot (placeholder words are not the creator's words)."""
    return SLOT_RE.sub(" ", str(text))


def sentences(text):
    """Spoken sentences; '/' pause markers stay inside a sentence; slot bodies are dropped."""
    return [s.strip() for s in SENT_RE.split(unslot(text)) if tokens(s)]


def stem(tok):
    """Strip attached Arabic prefixes so «بالأداة» and «الأداة» compare equal."""
    tok = tok.strip(".'’-")
    if not ARABIC_CHAR.search(tok):
        return tok
    for p in AR_PREFIXES:
        if tok.startswith(p) and len(tok) - len(p) >= 3:
            return tok[len(p):]
    return tok


def _under_1000(n, lang, dialect):
    words = 0
    h, r = divmod(n, 100)
    if h:
        words += 1 if lang == "ar" else 2
    if r:
        if r <= 10 or r % 10 == 0:
            words += 1
        elif r < 20:
            words += 2 if (lang == "ar" and dialect == "msa") else 1
        else:
            words += 2 if lang == "ar" else 1
    return words


def number_words(n, lang, dialect=""):
    """Words a number takes when spoken: 199 -> 3 («مية وتسعة وتسعين», 'one hundred ninety-nine')."""
    if n == 0:
        return 1
    words = 0
    for scale in (10**9, 10**6, 10**3):
        g, n = divmod(n, scale)
        if g:
            if lang == "ar" and g in (1, 2):
                words += 1
            else:
                words += _under_1000(g, lang, dialect) + 1
    if n:
        words += _under_1000(n, lang, dialect)
    return words


def count_words(text, lang="ar", dialect=""):
    total = SLOT_WORDS * len(SLOT_RE.findall(str(text)))
    for tok in tokens(SLOT_RE.sub(" ", str(text))):
        if not re.search(r"\w", tok):
            continue
        m = re.fullmatch(r"(\d+)(?:\.(\d+))?(%?)", tok.strip(".-"))
        if m:
            total += number_words(int(m.group(1)), lang, dialect)
            if m.group(2):
                total += 1 if lang == "ar" else 1 + len(m.group(2))
            if m.group(3):
                total += 1
        else:
            total += 1 + tok.count("%")
    return total


def count_pauses(text):
    return len(PAUSE_RE.findall(BREAK_RE.sub(" ", SLOT_RE.sub(" ", str(text)))))


def key_terms(text, lang):
    stops = set(normalize(w) for w in STOPWORDS["ar" if lang == "ar" else "en"])
    out = {}
    for tok in tokens(unslot(text)):
        s = stem(tok)
        if len(s) >= 3 and s not in stops and tok not in stops and not s.isdigit():
            out.setdefault(s, tok)
    return out


def bigrams(text, lang):
    stops = set(normalize(w) for w in STOPWORDS["ar" if lang == "ar" else "en"])
    toks = [stem(t) for t in tokens(unslot(text))]
    return {(a, b) for a, b in zip(toks, toks[1:]) if (a not in stops or b not in stops) and len(a + b) >= 5}


def starts_with_any(text, phrases):
    t = " ".join(tokens(text))
    return next((p for p in phrases if t == normalize(p) or t.startswith(normalize(p) + " ")), None)


NEGATORS = {"مو", "مش", "ما", "ليس", "لا", "بدون", "مافي", "محد",
            "not", "no", "never", "can't", "cannot", "won't", "isn't", "aren't", "don't", "doesn't", "didn't", "without"}
# Words that sit between a negator and the phrase without changing the meaning («ما في أي شي مضمون»).
NEG_FILLERS = {"في", "اي", "شي", "شيء", "حاجه", "any", "anything", "thing", "really", "a", "an", "the"}
CLAUSE_RE = re.compile("[،,:؛;]")


def _flat(x):
    return [w for w in (tok.strip(".'’-").replace("’", "'") for tok in tokens(x)) if w]


def unnegated_hits(text, phrases):
    """contains_any, but a match is excused only when a negator is the nearest non-filler token
    directly before it, inside the same clause («مو مضمون», "no cure", «ما في أي شي مضمون»).
    'no risk, guaranteed results' still hits: the negator belongs to another clause."""
    negs = {normalize(n) for n in NEGATORS}
    clauses = [_flat(c) for sent in SENT_RE.split(str(text)) for c in CLAUSE_RE.split(sent)]
    out = []
    for p in phrases:
        q = _flat(p)
        if not q:
            continue
        for t in clauses:
            hit = False
            for i in range(len(t) - len(q) + 1):
                if t[i:i + len(q)] != q:
                    continue
                before = [w for w in t[:i] if w not in NEG_FILLERS]
                if not (before and before[-1] in negs):
                    hit = True
                    break
            if hit:
                out.append(p)
                break
    return out


def contains_any(text, phrases):
    """Whole-phrase matches; the phrase is tokenized like the text, so «١٠٠٪ مضمون» matches «100% مضمون»."""
    def flat(x):
        return " ".join(w for w in (tok.strip(".'’-") for tok in tokens(x)) if w)
    t = " " + flat(text) + " "
    out = []
    for p in phrases:
        q = flat(p)
        if q and " " + q + " " in t:
            out.append(p)
    return out
