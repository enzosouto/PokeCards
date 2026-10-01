import re
from dataclasses import dataclass

from app.providers.cards.base import NormalizedCard
from app.providers.sales.base import NormalizedSale

NUMBER_MATCH = 40
SET_MATCH = 25
NAME_MATCH = 25
VARIANT_MATCH = 10
MIN_SALE_MATCH_SCORE = 40  # requires at least a number match, per spec section 5

_VARIANT_WORDS = {"ex", "gx", "v", "vmax", "vstar", "full art", "secret", "alt art"}


@dataclass
class ParsedQuery:
    name: str
    number: str | None
    set_hint: str | None
    variants: set[str]


def parse_query(text: str) -> ParsedQuery:
    text = text.strip()
    number_match = re.search(r"(\d+)\s*/\s*\d+|\b(\d+)\b(?!\S)", text)
    number = None
    remainder = text
    if number_match:
        number = number_match.group(1) or number_match.group(2)
        remainder = (text[: number_match.start()] + " " + text[number_match.end() :]).strip()

    words = remainder.lower().split()
    variants = {w for w in words if w in _VARIANT_WORDS}
    name_words = [w for w in words if w not in variants]
    name = " ".join(name_words).strip()

    return ParsedQuery(name=name, number=number, set_hint=None, variants=variants)


def score(card: NormalizedCard, parsed: ParsedQuery) -> int:
    total = 0
    if parsed.number and card.card_number.lstrip("0") == parsed.number.lstrip("0"):
        total += NUMBER_MATCH
    if parsed.set_hint and parsed.set_hint.lower() in card.set_name.lower():
        total += SET_MATCH
    card_name_lower = card.name.lower()
    if parsed.name and parsed.name in card_name_lower:
        total += NAME_MATCH
    if parsed.variants and all(v in card_name_lower for v in parsed.variants):
        total += VARIANT_MATCH
    return total


_GRADE_PATTERN = re.compile(
    r"\b(?:PSA|BGS|CGC|SGC|ACE|GMA)\s*\d+(\.\d+)?\b|\bGrade\s*\d+\b|\bGEM\s*MT\s*\d+\b",
    re.IGNORECASE,
)


def _title_numbers(title: str) -> set[str]:
    """All plausible card-number tokens in a listing title (x/y notation, #123, or bare digits).
    Titles often contain unrelated numbers (grade score, year, quantity) — checking membership
    instead of "the first number found" avoids matching the wrong one. Grading-company scores
    (PSA 10, CGC 9, Grade 10...) are stripped first since they read as bare digits otherwise
    and were the single biggest source of false matches."""
    cleaned = _GRADE_PATTERN.sub(" ", title)
    nums = {m.group(1) for m in re.finditer(r"(\d+)\s*/\s*\d+", cleaned)}
    nums |= {m.group(1) for m in re.finditer(r"#(\d+)\b", cleaned)}
    nums |= set(re.findall(r"\b(\d{1,4})\b", cleaned))
    return nums


def score_sale_title(card, title: str) -> int:
    """Duck-types Card/NormalizedCard. Scores whether `title` plausibly refers to `card`."""
    lowered = title.lower()
    total = 0

    target_number = card.card_number.lstrip("0") or "0"
    if any(n.lstrip("0") == target_number for n in _title_numbers(title)):
        total += NUMBER_MATCH

    if card.set_name and card.set_name.lower() in lowered:
        total += SET_MATCH

    name_tokens = card.name.lower().split()
    variants = {w for w in name_tokens if w in _VARIANT_WORDS}
    base_name = " ".join(w for w in name_tokens if w not in variants)
    if base_name and base_name in lowered:
        total += NAME_MATCH
    if variants and all(v in lowered for v in variants):
        total += VARIANT_MATCH

    return total


def filter_matching_sales(card, sales: list[NormalizedSale]) -> list[NormalizedSale]:
    """Keep only sales whose title plausibly refers to `card` (duck-types Card/NormalizedCard)."""
    return [s for s in sales if score_sale_title(card, s.title) >= MIN_SALE_MATCH_SCORE]
