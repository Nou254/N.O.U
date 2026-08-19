"""
Assessment configuration: modules, duration and scoring rules.

Per product requirements:
- Three compulsory modules: Mathematics, Propositional Logic, Programming Basics.
- The applicant chooses exactly FIVE elective modules from a list covering the
  technology world (including the named ones: Databases, Networks and
  Networking, Cyber Security, Web Development, UI Development).
- Every assessment lasts 3 hours 30 minutes.
- Each module contains QUESTIONS_PER_MODULE questions; every question is a
  real-world, scenario-based problem rather than a direct recall question.
- Pass: overall score >= 65% AND each compulsory module >= 45%.
- Results are emailed to the applicant 2 hours after submission.
"""

COMPULSORY_MODULES = [
    "Mathematics",
    "Propositional Logic",
    "Programming Basics",
]

ELECTIVE_MODULES = [
    "Databases",
    "Networks and Networking",
    "Cyber Security",
    "Web Development",
    "UI Development",
    "Cloud Computing",
    "Artificial Intelligence and Machine Learning",
    "DevOps and CI/CD",
    "Mobile Development",
    "Operating Systems",
    "Algorithms and Data Structures",
    "Distributed Systems",
    "Software Testing and QA",
    "API Design",
]

# Number of elective modules an applicant must choose (in addition to the
# three compulsory ones).
ELECTIVE_COUNT = 5

# Questions generated per module per assessment.
QUESTIONS_PER_MODULE = 20

# Duration of every assessment (minutes).
ASSESSMENT_DURATION_MINUTES = 210  # 3 hours 30 minutes

# Scoring rules.
PASS_THRESHOLD_PERCENT = 65
COMPULSORY_MIN_PERCENT = 45

# Results are emailed this long after submission.
RESULTS_EMAIL_DELAY_HOURS = 2
