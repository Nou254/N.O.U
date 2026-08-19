"""
Shared question templates for the N.O.U. question banks.

Every category bank = 20 common + 20 category + 20 position + 20 practical
+ 20 professional = 100 questions. The common and professional parts are
generic (logic / critical thinking / general knowledge and ethics /
communication / judgement), so the SAME high-quality set is reused across all
categories; category / position / practical questions are authored uniquely
per category in bank_data_*.py.

Question format: (question_type, question_text, grading_notes)
"""

# ---------------------------------------------------------------------------
# A. COMMON ASSESSMENT (20) - logic, critical thinking, general knowledge.
#    Allowed types: scenario, written_explanation, debugging.
# ---------------------------------------------------------------------------
COMMON = [
    ("scenario",
     "You are given a new task with a one-week deadline. Halfway through, an "
     "urgent request arrives that will consume two full days. Describe exactly "
     "how you would manage both commitments and what you would communicate to "
     "each stakeholder.",
     "Covers prioritisation, transparent communication, renegotiating "
     "deadlines early rather than silently failing, and protecting quality."),
    ("written_explanation",
     "Explain the difference between solving the symptom of a problem and "
     "solving its root cause, using a real example you have experienced or can "
     "imagine in a technology work environment.",
     "Expects an example, a clear contrast between temporary fix and permanent "
     "fix, and awareness of trade-offs such as cost, risk and time."),
    ("scenario",
     "A colleague tells you they found a faster way to complete a task that "
     "skips an important quality-check step. They propose using it to meet a "
     "tight deadline. What do you do?",
     "Expects upholding quality and process, raising the concern respectfully, "
     "finding an alternative that preserves the check, and not blindly "
     "following shortcuts."),
    ("debugging",
     "A system worked correctly yesterday but fails today after no obvious "
     "change. List the first five diagnostic steps you would take, in order, "
     "and explain why each step matters.",
     "Expects checking recent changes/deployments, logs and error messages, "
     "data/input changes, environment and configuration, then isolating the "
     "failure boundary before fixing."),
    ("scenario",
     "You discover an error you made two weeks ago has cost the company a "
     "client. No one has noticed yet. What do you do, and why?",
     "Expects owning the mistake, reporting it promptly with a mitigation "
     "plan, and not concealing it - honesty and accountability."),
    ("written_explanation",
     "A project requires 40 hours of work but only 30 hours remain before "
     "launch. Describe the options available and which one you would choose "
     "and why.",
     "Expects weighing scope reduction, extra resources, quality risk and "
     "deadline negotiation; choosing a realistic option and justifying it."),
    ("scenario",
     "Two departments both claim your service is the top priority and both "
     "deadlines are tomorrow. How do you decide, and how do you handle the "
     "department you cannot help first?",
     "Expects using agreed business priority, escalating where needed, being "
     "transparent with both parties, and offering a partial or interim "
     "solution."),
    ("written_explanation",
     "Explain what it means to verify information before acting on it, and "
     "describe a situation where acting on unverified information caused a "
     "problem.",
     "Expects concrete example and recognition of verification methods "
     "(checking primary source, testing, confirming with owner)."),
    ("debugging",
     "You cannot reproduce a bug a client reports, but they are certain it "
     "happens daily. What are your next steps to understand and solve it?",
     "Expects gathering the exact steps, environment, screenshots/logs and "
     "timing; testing variations; not dismissing the report; setting up "
     "instrumentation to capture it."),
    ("scenario",
     "You are assigned to lead a small team for a short project. One member "
     "is not contributing. Describe how you would handle it in the first two "
     "days versus after a week.",
     "Expects early supportive check-in, clear expectations, then escalating "
     "through structure (reassignment, manager, documentation) while keeping "
     "the team productive."),
    ("written_explanation",
     "What does 'working smartly versus working hard' mean to you? Give a "
     "specific example where you improved a process rather than just spending "
     "more time on it.",
     "Expects process improvement, automation, reuse or simplification; a "
     "measurable before/after."),
    ("scenario",
     "Your manager gives instructions that you believe are technically "
     "flawed. The deadline is in three days. What do you do?",
     "Expects raising concerns with evidence, proposing alternatives, "
     "documenting the decision, and executing the agreed direction even if "
     "not your first choice."),
    ("written_explanation",
     "Describe a time you had to learn a completely new tool or technology "
     "quickly. What was your learning method, and what would you do "
     "differently next time?",
     "Expects a concrete method (docs, practice, mentorship, small projects) "
     "and honest reflection on improvement."),
    ("debugging",
     "A report that used to take 10 minutes now takes 3 hours. Nothing in the "
     "process was intentionally changed. How would you investigate, and what "
     "are the likely causes you would check first?",
     "Expects checking data volume growth, query/process changes, system "
     "load, resource exhaustion and locking; profiling before guessing."),
    ("scenario",
     "You accidentally shared confidential information with the wrong person "
     "in a message. What do you do immediately, and what prevents it from "
     "happening again?",
     "Expects immediate containment (retract/notify/security), honest "
     "reporting, and process safeguards (double-check recipients, access "
     "controls, training)."),
    ("written_explanation",
     "Explain the difference between urgent and important, and describe how "
     "you would schedule a day that contains both types of tasks.",
     "Expects a prioritisation framework (urgency vs importance) and a "
     "realistic scheduling approach that reserves focus time."),
    ("scenario",
     "A client requests a feature that conflicts with the company's stated "
     "standards or values. How do you respond while keeping the client "
     "relationship intact?",
     "Expects respectful refusal/alternative, explaining the reason tied to "
     "standards, offering compliant options, and escalating if pressured."),
    ("written_explanation",
     "Describe a situation where you had to make a decision with incomplete "
     "information. How did you reduce the risk of that decision?",
     "Expects identifying the unknown, gathering what is available, using "
     "assumptions explicitly, building checks/fallbacks, and reviewing after "
     "the outcome."),
    ("debugging",
     "Two team members changed the same configuration file yesterday, and "
     "now the environment is broken. Describe how you would determine which "
     "change caused the break, and how you would prevent this class of "
     "problem in future.",
     "Expects comparing versions/change history, reverting incrementally, and "
     "process controls (review, change management, versioning)."),
    ("scenario",
     "You realise a task will take longer than estimated with one day left. "
     "What do you do in the next hour, and what do you say to the person who "
     "is waiting for it?",
     "Expects immediate early warning, an honest status with a revised "
     "estimate and options, and never disappearing until the deadline."),
]

# ---------------------------------------------------------------------------
# E. PROFESSIONAL ASSESSMENT (20) - communication, ethics, teamwork,
#    judgement. Allowed types: scenario, written_explanation.
# ---------------------------------------------------------------------------
PROFESSIONAL = [
    ("scenario",
     "A teammate takes credit for work you did. Describe how you would handle "
     "this professionally, including what you would say and not say.",
     "Expects addressing it privately and factually, focusing on outcomes and "
     "fairness, not public confrontation or accusation."),
    ("written_explanation",
     "What does integrity mean in a professional workplace? Give a concrete "
     "example of a decision that tested your integrity and how you handled it.",
     "Expects honesty, consistency between words and actions, and a real "
     "example with reflection."),
    ("scenario",
     "You disagree strongly with a decision your team has already made "
     "together. The deadline is near. What do you do?",
     "Expects voicing the concern once with evidence, then committing to the "
     "team decision and giving full effort; avoiding sabotage or sulking."),
    ("written_explanation",
     "Describe how you would deliver bad news to a client - for example, a "
     "missed deadline or a failed delivery. What is your exact approach?",
     "Expects early notification, clear ownership, a plan to recover, empathy "
     "without over-promising, and follow-through."),
    ("scenario",
     "A junior colleague asks you to review their work, and you find several "
     "mistakes. How do you give the feedback so they improve without feeling "
     "attacked?",
     "Expects specific, behaviour-focused feedback, balancing strengths and "
     "gaps, inviting questions, and agreeing on next steps."),
    ("written_explanation",
     "Explain a situation where you had to adapt your communication style to "
     "a different audience (technical vs non-technical, executive vs "
     "colleague). What did you change and why?",
     "Expects concrete adaptation (jargon level, detail depth, format) and "
     "the reason behind it."),
    ("scenario",
     "You see a colleague break a company policy that could put data at risk. "
     "No one else noticed. What do you do?",
     "Expects addressing it directly or through the proper channel, with "
     "safety/data protection as the priority and the intent to help, not "
     "punish."),
    ("written_explanation",
     "How do you handle working with someone whose working style is very "
     "different from yours? Give a real or plausible example.",
     "Expects mutual understanding, adapting where reasonable, setting clear "
     "agreements, and focusing on the shared goal."),
    ("scenario",
     "You are the only person available to handle a customer complaint, and "
     "you do not have the authority to give the resolution they demand. What "
     "is your exact approach?",
     "Expects listening and empathy, setting realistic expectations, "
     "escalating properly, following up, and not over-promising."),
    ("written_explanation",
     "What does it mean to be accountable for your work? Describe a time you "
     "accepted responsibility for a failure and what you learned.",
     "Expects ownership of outcomes - good and bad - and a genuine lesson "
     "from the failure."),
    ("scenario",
     "Your team is behind schedule and tension is rising. As a team member, "
     "what can YOU do - without being the manager - to help the team "
     "recover?",
     "Expects initiative: offering help, removing blockers, improving "
     "communication, protecting morale, and focusing on shared success."),
    ("written_explanation",
     "Describe a time you had to manage a conflict between two colleagues or "
     "two stakeholders. What was your role and what was the outcome?",
     "Expects neutrality, listening to both sides, focusing on interests not "
     "positions, and a workable resolution."),
    ("scenario",
     "A manager asks you to do something that is not illegal but is clearly "
     "unethical. How do you respond?",
     "Expects a respectful but firm refusal, stating the ethical concern "
     "clearly, proposing an ethical alternative, and escalating if pressured."),
    ("written_explanation",
     "What is the difference between being polite and being honest in "
     "professional communication? Give an example where honesty was the more "
     "respectful choice.",
     "Expects recognising that false reassurance harms; honest, respectful "
     "directness builds trust."),
    ("scenario",
     "You have just delivered a project and a client immediately finds a "
     "significant issue. The team believes the issue was the client's fault. "
     "How do you respond?",
     "Expects focusing on resolution over blame, investigating facts, "
     "communicating constructively, and protecting the relationship."),
    ("written_explanation",
     "Explain how you stay calm and effective under pressure. Use a specific "
     "example from work, school or personal life.",
     "Expects concrete techniques (prioritisation, breathing, breaking down "
     "tasks, support) demonstrated through a story."),
    ("scenario",
     "A new team member struggles because the team's processes are poorly "
     "documented. What do you do to help them and improve the situation for "
     "everyone?",
     "Expects empathy, pairing/mentoring, and improving documentation or "
     "processes so the whole team benefits."),
    ("written_explanation",
     "What would you do if you realised you had promised a client something "
     "that cannot be delivered on time? Describe your communication plan.",
     "Expects immediate transparency, options for mitigation, revised "
     "timeline, and follow-through to rebuild trust."),
    ("scenario",
     "During a meeting, a senior person presents a plan with a flaw that you "
     "have already identified. How do you raise it without embarrassing them?",
     "Expects raising it constructively (e.g. 'one consideration'), "
     "preferably privately when appropriate, with evidence and alternatives."),
    ("written_explanation",
     "Describe what you believe makes a team high-performing, and the role "
     "you personally play in making that happen.",
     "Expects trust, clear goals, communication and accountability - and "
     "self-awareness about one's own contribution."),
]
