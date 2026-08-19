"""
N.O.U. assessment framework (today.md - EMPLOYMENT ASSESSMENT FRAMEWORK).

The assessment is NOT one examination for every applicant. It is a five-part
structure driven by the applicant's professional category and position:

    A. Common Assessment      - logic & critical thinking + general knowledge
    B. Category Assessment    - knowledge of the selected professional field
    C. Position Assessment    - knowledge specific to the position
    D. Practical Assessment   - perform an actual task
    E. Professional Assessment- communication, ethics, teamwork, judgement

Scoring model (100 points, configurable per category):

    Logic & Critical Thinking                15%
    General Computer/Professional Knowledge   5%
    Category Knowledge                       25%
    Position Knowledge                       25%
    Practical Assessment                     25%
    Professional Judgement                    5%

Competency classification:

    0-49%   Not Qualified
    50-64%  Developing
    65-79%  Competent
    80-89%  N.O.U. Qualified
    90-100% Advanced

Question types (NO MULTIPLE CHOICE QUESTIONS AND ANSWERS):

    short_answer | written_explanation | scenario | practical |
    debugging | design | project
"""

# Question types permitted (today.md: "N:B NO MULTIPLE CHOICE QUESTIONS").
QUESTION_TYPES = [
    "short_answer",        # tests understanding
    "written_explanation", # tests reasoning
    "scenario",            # tests real-world decision-making
    "practical",           # tests actual ability
    "debugging",           # tests troubleshooting
    "design",              # tests solution architecture/design
    "project",             # tests the ability to produce a complete solution
]

# Assessment parts (order matters - applicants progress through them).
PARTS = ["common", "category", "position", "practical", "professional"]

# Default questions per part - 20 in total per assessment. Every assessment
# draws this many questions AT RANDOM from the category's pre-generated
# question bank (100 questions per career category = 20 per part), so the
# exam starts instantly and each applicant gets a randomized set.
QUESTIONS_PER_PART = {
    "common": 6,
    "category": 5,
    "position": 5,
    "practical": 2,
    "professional": 2,
}

# Question bank size per professional category (20 per part x 5 parts = 100
# questions stored per category; each assessment randomly draws 20 of them).
BANK_QUESTIONS_PER_PART = 20
BANK_SIZE_PER_CATEGORY = 100

# Question-type mix per part (which question types each part may draw from).
PART_QUESTION_TYPES = {
    "common": ["scenario", "written_explanation", "debugging"],
    "category": ["written_explanation", "scenario", "design", "short_answer"],
    "position": ["written_explanation", "scenario", "debugging", "short_answer", "design"],
    "practical": ["practical", "design", "project", "debugging"],
    "professional": ["scenario", "written_explanation"],
}

# Default part weights (percent) - mirrored on PersonnelCategory so admin can
# reconfigure per category.
DEFAULT_WEIGHTS = {
    "logic": 15,          # Logic & Critical Thinking
    "general": 5,         # General Computer/Professional Knowledge
    "category": 25,       # Category Knowledge
    "position": 25,       # Position Knowledge
    "practical": 25,      # Practical Assessment
    "professional": 5,    # Professional Judgement
}

# Competency bands (score %, label).
COMPETENCY_BANDS = [
    (90, "Advanced"),
    (80, "N.O.U. Qualified"),
    (65, "Competent"),
    (50, "Developing"),
    (0, "Not Qualified"),
]

# Overall duration in minutes (3 hours 30 minutes).
ASSESSMENT_DURATION_MINUTES = 210

# A score of 80%+ qualifies an applicant for consideration (not employment).
QUALIFYING_PERCENT = 80


def competency_band(percentage: float) -> str:
    """Map a 0-100 percentage to its competency classification."""
    for threshold, label in COMPETENCY_BANDS:
        if percentage >= threshold:
            return label
    return "Not Qualified"


def qualifies(percentage: float) -> bool:
    """An 80% score qualifies an applicant for consideration."""
    return percentage >= QUALIFYING_PERCENT


def weighted_percentage(part_scores: dict, weights: dict) -> float:
    """
    Compute the overall weighted percentage.

    part_scores: {part: percentage} for parts common/category/position/
        practical/professional.
    weights: {logic, general, category, position, practical, professional}.

    The scoring model:
        logic (common part)   -> 15%
        general (common part) -> 5%
        category              -> 25%
        position              -> 25%
        practical             -> 25%
        professional          -> 5%
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    # The common part covers both logic (15%) and general (5%).
    common_pct = part_scores.get("common", 0) or 0
    total = 0.0
    total += (w.get("logic", 0) or 0) * common_pct / 100.0
    total += (w.get("general", 0) or 0) * common_pct / 100.0
    total += (w.get("category", 0) or 0) * (part_scores.get("category", 0) or 0) / 100.0
    total += (w.get("position", 0) or 0) * (part_scores.get("position", 0) or 0) / 100.0
    total += (w.get("practical", 0) or 0) * (part_scores.get("practical", 0) or 0) / 100.0
    total += (w.get("professional", 0) or 0) * (part_scores.get("professional", 0) or 0) / 100.0
    return round(total, 2)


def recommend_alternative(part_scores: dict) -> str:
    """
    Recommend an alternative professional category when the applicant does not
    qualify for the applied position (today.md sec. 41: "the system should be
    capable of recommending an alternative category where the assessment
    evidence supports it").

    Uses the applicant's strongest assessment part to suggest a compatible
    field, e.g. strong practical/design -> UI/UX & Product Design.
    """
    scores = part_scores or {}
    strongest = max(
        scores,
        key=lambda p: (scores.get(p) or 0) if isinstance(scores.get(p), (int, float)) else 0,
    ) if scores else "position"

    mapping = {
        "practical": "UI/UX & Product Design",
        "design": "UI/UX & Product Design",
        "position": "General Technology Personnel",
        "category": "General Technology Personnel",
        "common": "IT Support & Technical Operations",
        "professional": "Administration & Operations",
    }
    return mapping.get(strongest, "General Technology Personnel")
