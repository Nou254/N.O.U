"""
Unique category / position / practical questions for the question banks.
"""

CATS = {
    # ----------------------------------------------------------------- 26
    "Legal, Compliance & Governance": {
        "category": [
            ("written_explanation",
             "Explain the difference between a law, a regulation "
             "and a company policy.",
             "Law = enacted rule; regulation = agency "
             "rule under law; policy = internal rule."),
            ("scenario",
             "You discover the company may be violating a "
             "data protection law. How do you respond?",
             "Assess, document, escalate "
             "appropriately, remediate, report where "
             "required."),
            ("design",
             "Design a compliance program for a company "
             "handling customer data.",
             "Risk assessment, policies, training, "
             "monitoring, response, audit."),
            ("written_explanation",
             "Explain the difference between a contract and "
             "an agreement in legal terms.",
             "Enforceable mutual obligations vs "
             "broader term; elements of a "
             "contract."),
            ("scenario",
             "A client demands contract terms that are "
             "unreasonable. How do you handle "
             "negotiation?",
             "Identify core issues, counter "
             "professionally, escalate, document, "
             "protect interests."),
            ("short_answer",
             "What is the difference between confidentiality "
             "and non-disclosure?",
             "General duty vs specific NDA "
             "agreement; scope and enforcement."),
            ("written_explanation",
             "Explain the difference between compliance and "
             "ethics in business.",
             "Following rules vs doing right; "
             "gaps and grey areas."),
            ("design",
             "Design a contract review checklist for a "
             "service agreement.",
             "Parties, scope, price, terms, "
             "liability, termination, "
             "signatures."),
            ("scenario",
             "An employee signed a contract for the company "
             "without authority. How do you handle it?",
             "Assess validity, ratify or "
             "correct, train on authority, "
             "prevent."),
            ("written_explanation",
             "Explain the concept of 'duty of care' in a "
             "workplace context.",
             "Employer obligations to protect "
             "health, safety and wellbeing."),
            ("design",
             "Design a document governance framework "
             "(creation, storage, retention, disposal).",
             "Classification, controls, "
             "retention schedule, access, "
             "audit."),
            ("scenario",
             "A regulator requests documents. How do you "
             "respond?",
             "Verify scope, gather, "
             "coordinate with legal, "
             "respond timely, log."),
            ("written_explanation",
             "Explain the difference between copyright and "
             "trademark.",
             "Creative works vs brand marks; "
             "registration and enforcement."),
            ("design",
             "Design a data privacy impact assessment "
             "(DPIA) process for new projects.",
             "Trigger, data flows, risks, "
             "mitigations, approval."),
            ("scenario",
             "A data breach occurs. Describe the response "
             "and notification obligations.",
             "Contain, assess, notify "
             "regulator and affected, "
             "document, remediate."),
            ("short_answer",
             "What is the difference between a policy and a "
             "procedure in governance?",
             "Rule vs implementation steps; "
             "both needed."),
            ("written_explanation",
             "Explain the importance of board or "
             "management oversight in governance.",
             "Accountability, strategy "
             "alignment, risk oversight."),
            ("design",
             "Design an anti-corruption and bribery policy "
             "framework.",
             "Prohibitions, gifts, "
             "due diligence, reporting, "
             "training."),
            ("scenario",
             "A supplier offers you an expensive gift to "
             "win a contract. How do you respond?",
             "Decline, report, follow "
             "policy, document."),
            ("written_explanation",
             "Explain the difference between risk "
             "management and compliance.",
             "Managing all risks vs meeting "
             "obligations; overlap."),
        ],
        "position": [
            ("written_explanation",
             "As a compliance officer, describe how you "
             "would conduct a compliance risk "
             "assessment.",
             "Identify obligations, assess "
             "likelihood/impact, controls, "
             "report."),
            ("scenario",
             "A manager pressures you to approve a "
             "non-compliant practice. How do you "
             "respond?",
             "Refuse, document, escalate, "
             "protect compliance "
             "independence."),
            ("short_answer",
             "What is the difference between an audit and "
             "a review?",
             "Assurance level and depth; "
             "opinion types."),
            ("design",
             "Design a compliance training program for "
             "employees.",
             "Topics, delivery, "
             "attestation, refreshers."),
            ("written_explanation",
             "Explain how you would handle a whistleblower "
             "report.",
             "Confidentiality, "
             "investigation, protection, "
             "follow-up."),
            ("debugging",
             "A compliance report is consistently late. "
             "How do you fix the process?",
             "Owners, deadlines, "
             "automation, escalation, "
             "review."),
            ("short_answer",
             "What is the difference between a statute of "
             "limitations and a retention period?",
             "Legal claim window vs "
             "document holding rule."),
            ("design",
             "Design a third-party vendor due diligence "
             "process.",
             "Screening, risk "
             "assessment, contracts, "
             "monitoring."),
            ("written_explanation",
             "Explain how you would manage a regulatory "
             "change impacting the business.",
             "Track changes, assess "
             "impact, plan, train, "
             "implement, verify."),
            ("scenario",
             "A contract term is ambiguous and a dispute "
             "arises. How do you support resolution?",
             "Review intent, "
             "negotiate, mediation, "
             "document."),
            ("short_answer",
             "What is the difference between an indemnity "
             "and a warranty?",
             "Loss protection vs "
             "assurance of facts; "
             "remedies differ."),
            ("design",
             "Design a records retention schedule for a "
             "technology company.",
             "Categories, periods, "
             "legal basis, disposal."),
            ("written_explanation",
             "Explain how you would ensure employees "
             "actually follow policies.",
             "Training, "
             "communication, "
             "monitoring, "
             "enforcement."),
            ("debugging",
             "A policy is being violated repeatedly in "
             "one department. How do you investigate?",
             "Root cause, awareness, "
             "barriers, fix, "
             "monitor."),
            ("short_answer",
             "What is the difference between legal counsel "
             "and a compliance officer?",
             "Legal advice vs rule "
             "implementation; "
             "complementary."),
            ("design",
             "Design a governance framework for AI or "
             "data products.",
             "Principles, review "
             "process, controls, "
             "accountability."),
            ("written_explanation",
             "Explain how you would respond to a "
             "subpoena or legal request for records.",
             "Verify, coordinate, "
             "scope, produce, "
             "log."),
            ("scenario",
             "A competitor accuses your company of "
             "copying their product. How do you "
             "respond?",
             "Investigate, legal "
             "review, preserve "
             "evidence, respond "
             "appropriately."),
            ("short_answer",
             "What is the difference between a memorandum "
             "of understanding and a contract?",
             "Intention vs "
             "binding obligation; "
             "enforceability."),
            ("design",
             "Design a compliance monitoring and "
             "reporting dashboard.",
             "Obligations, status, "
             "risks, actions."),
        ],
        "practical": [
            ("practical",
             "Write a contract review checklist for a "
             "simple vendor agreement.",
             "Key clauses, red "
             "flags, process."),
            ("design",
             "Design a data subject access request (DSAR) "
             "workflow.",
             "Intake, verify, "
             "scope, respond, "
             "log."),
            ("practical",
             "Describe how you would document a "
             "compliance investigation.",
             "Chronology, "
             "evidence, findings, "
             "actions."),
            ("debugging",
             "A customer's data was emailed to the wrong "
             "recipient. How do you handle the breach "
             "assessment?",
             "Contain, assess "
             "risk, notify, "
             "remediate, "
             "report."),
            ("practical",
             "Write a confidentiality clause for a simple "
             "service agreement.",
             "Clear scope, "
             "duration, "
             "exceptions."),
            ("design",
             "Design a policy review and approval "
             "workflow.",
             "Draft, consult, "
             "approve, publish, "
             "review."),
            ("practical",
             "Describe how you would conduct a "
             "compliance self-assessment for a "
             "department.",
             "Checklist, evidence, "
             "gaps, plan."),
            ("debugging",
             "A contract was renewed automatically "
             "against the company's wishes. How do you "
             "handle it?",
             "Review terms, "
             "negotiate exit, "
             "calendar renewals, "
             "prevent."),
            ("practical",
             "Write a whistleblowing report intake "
             "template.",
             "Anonymous, "
             "structured, "
             "secure."),
            ("design",
             "Design a training attestation tracking "
             "system.",
             "Enrolment, "
             "completion, "
             "evidence, "
             "reporting."),
            ("practical",
             "Describe how you would prepare for a "
             "regulatory inspection.",
             "Documents, "
             "responses, roles, "
             "log."),
            ("debugging",
             "A data retention policy deleted records "
             "that were under legal hold. How do you "
             "respond?",
             "Assess impact, "
             "recover, fix "
             "holds, prevent."),
            ("practical",
             "Write a simple data processing agreement "
             "outline.",
             "Purpose, data, "
             "obligations, "
             "security."),
            ("design",
             "Design an incident logging and escalation "
             "process for compliance issues.",
             "Severity, owners, "
             "timelines, "
             "review."),
            ("practical",
             "Describe how you would verify that a "
             "policy is being followed in practice.",
             "Sampling, "
             "observation, "
             "interviews, "
             "evidence."),
            ("debugging",
             "A vendor contract lacks a liability cap, "
             "creating risk. How do you handle it?",
             "Negotiate, "
             "assess risk, "
             "approval, "
             "document."),
            ("practical",
             "Write a compliance risk register entry "
             "template.",
             "Risk, controls, "
             "owner, rating."),
            ("design",
             "Design a third-party data sharing approval "
             "process.",
             "Purpose, "
             "minimisation, "
             "contract, "
             "review."),
            ("practical",
             "Describe how you would conduct a contract "
             "termination process.",
             "Notice, "
             "obligations, "
             "transition, "
             "records."),
            ("debugging",
             "Employees bypass an approval control "
             "because it is slow. How do you fix the "
             "process, not the people?",
             "Simplify, "
             "automate, "
             "communicate, "
             "monitor."),
        ],
    },

    # ----------------------------------------------------------------- 28
    "Internship, Training & Entry-Level Technology": {
        "category": [
            ("written_explanation",
             "Describe a technology project you have "
             "completed or studied, and what you learned "
             "from it.",
             "Concrete project, clear learning, "
             "honest about challenges."),
            ("scenario",
             "You are given a task you have never done "
             "before with no instructions. How do you "
             "approach it?",
             "Break it down, research, ask "
             "questions, try small steps, ask for "
             "feedback."),
            ("design",
             "Design a simple weekly study or practice "
             "plan to improve a technical skill in two "
             "months.",
             "Specific goals, structured practice, "
             "measurement, adjustment."),
            ("written_explanation",
             "Explain the difference between a computer "
             "program and an operating system.",
             "Application vs system software; "
             "what each does."),
            ("scenario",
             "A senior colleague gives you feedback that "
             "is hard to hear. How do you respond?",
             "Listen, ask questions, thank them, "
             "act on it."),
            ("short_answer",
             "What is the difference between hardware and "
             "software? Give two examples of each.",
             "Physical vs logical; correct "
             "examples."),
            ("written_explanation",
             "Explain what the internet is in your own "
             "words and how a webpage reaches your "
             "screen.",
             "Network of networks; request, DNS, "
             "servers, browser rendering."),
            ("design",
             "Design a short tutorial that teaches a "
             "beginner one concept you know well.",
             "Clear steps, examples, common "
             "mistakes, practice."),
            ("scenario",
             "You are part of a team project and one "
             "member is not contributing. What do you "
             "do?",
             "Communicate, offer help, raise "
             "with the team, escalate if needed."),
            ("written_explanation",
             "Explain the difference between a beginner, "
             "intermediate and advanced level of skill in "
             "one technology you know.",
             "Concrete criteria for each level; "
             "what distinguishes them."),
            ("design",
             "Design your learning path to become "
             "employable in a technology role within six "
             "months.",
             "Skills, projects, portfolio, "
             "practice, job readiness."),
            ("scenario",
             "You submit an assignment with a mistake "
             "you did not notice. What happens and what "
             "do you do?",
             "Accept feedback, fix, learn a "
             "checking habit."),
            ("written_explanation",
             "Explain the difference between a file, a "
             "folder and a file system.",
             "Data unit, container, organising "
             "structure."),
            ("design",
             "Design a simple personal project that "
             "demonstrates three technical skills.",
             "Feasible, portfolio-worthy, "
             "skills clearly shown."),
            ("scenario",
             "A customer (or user) cannot understand your "
             "explanation. How do you explain it "
             "differently?",
             "Simplify, use analogy, check "
             "understanding, adapt."),
            ("short_answer",
             "What is the difference between a username, "
             "a password and a device?",
             "Identity, credential, hardware; "
             "why all matter."),
            ("written_explanation",
             "Explain what 'version control' is and why "
             "teams use it.",
             "Track changes, collaborate, "
             "rollback."),
            ("design",
             "Design a checklist for completing a "
             "technical task correctly the first time.",
             "Requirements, plan, build, test, "
             "review, submit."),
            ("scenario",
             "You are asked to present your work to the "
             "team for the first time. How do you "
             "prepare?",
             "Know the audience, structure, "
             "practice, invite questions."),
            ("written_explanation",
             "Explain the difference between a goal and a "
             "task, using an example.",
             "Outcome vs action; goals need "
             "tasks."),
        ],
        "position": [
            ("written_explanation",
             "As a trainee, describe how you would make "
             "the most of your first month in a "
             "technology company.",
             "Learn the product, build "
             "relationships, ask good "
             "questions, deliver small "
             "wins."),
            ("scenario",
             "Your supervisor is too busy to guide you. "
             "How do you keep learning?",
             "Self-study, peer support, "
             "scheduled check-ins, "
             "initiative."),
            ("short_answer",
             "What is the difference between an "
             "internship and a job?",
             "Learning focus vs "
             "performance focus; "
             "expectations."),
            ("design",
             "Design a 30-60-90 day plan for your first "
             "role as a technology assistant.",
             "Learn, contribute, "
             "own; milestones."),
            ("written_explanation",
             "Explain how you would ask for help "
             "effectively when stuck.",
             "Try first, prepare "
             "context, ask clearly, "
             "show what you tried."),
            ("debugging",
             "You follow instructions but the result is "
             "wrong. What do you do?",
             "Re-check steps, "
             "isolate the deviation, "
             "ask, document."),
            ("short_answer",
             "What is the difference between shadowing "
             "and doing?",
             "Observing vs practising; "
             "both part of "
             "learning."),
            ("design",
             "Design a personal skills checklist for an "
             "entry-level IT support role.",
             "Basics, tools, "
             "soft skills, "
             "priorities."),
            ("written_explanation",
             "Explain how you would handle being given "
             "more responsibility than expected.",
             "Assess, plan, ask "
             "for support, deliver, "
             "communicate."),
            ("scenario",
             "A colleague gives you feedback that you "
             "disagree with. How do you respond?",
             "Listen, ask for "
             "examples, reflect, "
             "discuss, decide."),
            ("short_answer",
             "What is the difference between a mentor "
             "and a manager?",
             "Development guide vs "
             "work supervisor; both "
             "can help."),
            ("design",
             "Design a simple daily standup update "
             "(what you did, what's next, blockers).",
             "Concise, honest, "
             "useful."),
            ("written_explanation",
             "Explain how you would track your own "
             "learning progress in a role.",
             "Goals, logs, "
             "feedback, review."),
            ("debugging",
             "You break something while learning. What "
             "do you do immediately?",
             "Inform, contain, "
             "fix or ask, learn."),
            ("short_answer",
             "What is the difference between a task and "
             "a project?",
             "Unit of work vs "
             "coordinated effort with "
             "a goal."),
            ("design",
             "Design an onboarding checklist for a new "
             "trainee joining your team.",
             "Accounts, tools, "
             "contacts, first "
             "tasks."),
            ("written_explanation",
             "Explain how you would demonstrate "
             "initiative without overstepping.",
             "Find gaps, propose, "
             "ask permission where "
             "needed."),
            ("scenario",
             "A team member does work you were "
             "expecting to do. How do you handle it?",
             "Communicate, "
             "clarify ownership, "
             "collaborate."),
            ("short_answer",
             "What is the difference between an "
             "apprenticeship and a traineeship?",
             "Formal trade training "
             "vs general work "
             "training."),
            ("design",
             "Design a weekly review habit for "
             "continuous improvement in a new role.",
             "What went well, "
             "what to improve, "
             "actions."),
        ],
        "practical": [
            ("practical",
             "Write a short email to a supervisor "
             "asking for feedback on your work.",
             "Professional, "
             "specific, easy to "
             "answer."),
            ("design",
             "Design a simple portfolio outline showing "
             "three projects you have done.",
             "Clear, skills shown, "
             "presentable."),
            ("practical",
             "Describe how you would troubleshoot a "
             "computer that will not connect to Wi-Fi.",
             "Logical steps, safe, "
             "escalate."),
            ("debugging",
             "You typed a command and got an error you "
             "do not understand. What do you do?",
             "Read the error, "
             "search, retry "
             "carefully, ask."),
            ("practical",
             "Write a daily learning log entry for a "
             "day of practice.",
             "What learned, "
             "challenges, next "
             "steps."),
            ("design",
             "Design a beginner project in a language "
             "or tool you know.",
             "Feasible, complete, "
             "documented."),
            ("practical",
             "Describe how you would set up a new "
             "laptop for basic use.",
             "Account, updates, "
             "software, security."),
            ("debugging",
             "A file you saved has disappeared. List "
             "the likely places to look.",
             "Folders, search, "
             "recycle bin, cloud, "
             "backups."),
            ("practical",
             "Write a short summary of a technical "
             "concept for a non-technical reader.",
             "Simple, accurate, "
             "engaging."),
            ("design",
             "Design a study schedule for a "
             "certification or course you are taking.",
             "Realistic, "
             "consistent, "
             "measurable."),
            ("practical",
             "Describe how you would prepare for a "
             "technical interview as a beginner.",
             "Fundamentals, "
             "practice problems, "
             "projects, soft "
             "skills."),
            ("debugging",
             "Your code/worksheet is 10 lines long and "
             "produces no output. What do you check "
             "first?",
             "Syntax, logic, "
             "print/output, "
             "environment."),
            ("practical",
             "Write a polite follow-up message after "
             "an internship application.",
             "Professional, "
             "brief, interested."),
            ("design",
             "Design a checklist for a group assignment "
             "with clear roles.",
             "Roles, tasks, "
             "timeline, review."),
            ("practical",
             "Describe how you would give a 5-minute "
             "presentation on a topic you know.",
             "Structure, "
             "practice, engage."),
            ("debugging",
             "A classmate's file will not open on your "
             "computer. What are the likely causes?",
             "Version, format, "
             "corruption, "
             "permissions."),
            ("practical",
             "Write a goal-setting plan for the next "
             "90 days of your training.",
             "Specific, "
             "measurable, "
             "reviewed."),
            ("design",
             "Design a simple FAQ for a tool or "
             "process you have learned.",
             "Real questions, "
             "clear answers."),
            ("practical",
             "Describe how you would ask a good "
             "question in a technical forum or chat.",
             "Context, what you "
             "tried, clear "
             "question."),
            ("debugging",
             "You finished a task but it is missing a "
             "requirement. What do you do?",
             "Acknowledge, fix, "
             "check requirements "
             "first next time."),
        ],
    },

    # ----------------------------------------------------------------- 29
    "General Technology Personnel": {
        "category": [
            ("written_explanation",
             "Explain the difference between a computer "
             "technician and a software developer.",
             "Hardware/software support vs "
             "building software; how they work "
             "together."),
            ("scenario",
             "A user's computer is slow. Describe your "
             "troubleshooting approach from start to "
             "resolution.",
             "Gather info, check resources, "
             "isolate cause, fix, verify, "
             "document."),
            ("design",
             "Design a technology setup for a small "
             "office with ten computers, internet and a "
             "printer.",
             "Network, Wi-Fi, security, "
             "maintenance, support."),
            ("written_explanation",
             "Explain the difference between a network, "
             "the internet and the cloud.",
             "Connected devices, global network, "
             "remote services."),
            ("scenario",
             "A customer asks you to fix something you "
             "have never handled. How do you respond?",
             "Be honest, research, use "
             "resources, ask for help, follow "
             "up."),
            ("short_answer",
             "What is the difference between a desktop "
             "and a laptop?",
             "Portability, performance, "
             "upgradability, use cases."),
            ("written_explanation",
             "Explain what a password manager is and why "
             "it improves security.",
             "Unique strong passwords, "
             "convenience, protection."),
            ("design",
             "Design a data backup routine for a small "
             "business.",
             "What to back up, frequency, "
             "location, testing, recovery."),
            ("scenario",
             "A customer is frustrated because a problem "
             "keeps recurring. How do you handle the "
             "relationship?",
             "Empathise, find root cause, "
             "fix properly, communicate, "
             "follow up."),
            ("written_explanation",
             "Explain the difference between a "
             "smartphone, a tablet and a computer.",
             "Form factor, OS, capabilities, "
             "use cases."),
            ("design",
             "Design a technology maintenance checklist "
             "for a small office.",
             "Updates, backups, cleaning, "
             "security, inventory."),
            ("scenario",
             "You spot a security risk (e.g. an open "
             "door for data loss) that nobody noticed. "
             "What do you do?",
             "Raise it, assess, fix or "
             "escalate, educate."),
            ("written_explanation",
             "Explain the difference between an email "
             "and a file attachment.",
             "Message vs file sent with it; "
             "risks and size."),
            ("design",
             "Design a simple inventory system for an "
             "office's computers and accessories.",
             "Tracking, labels, status, "
             "maintenance."),
            ("scenario",
             "Two people need to work on the same "
             "document. How do you set that up safely?",
             "Shared drive, version control "
             "or co-editing, permissions."),
            ("short_answer",
             "What is the difference between a browser "
             "and a search engine?",
             "Software vs service; "
             "relationship."),
            ("written_explanation",
             "Explain the importance of software updates "
             "and why people skip them.",
             "Security, fixes, features; "
             "addressing resistance."),
            ("design",
             "Design a simple training session for "
             "office staff on avoiding phishing.",
             "Examples, rules, practice, "
             "reporting."),
            ("scenario",
             "A client asks you to do something that "
             "could harm their own security. How do you "
             "respond?",
             "Advise, explain risk, propose "
             "safer option, respect decision."),
            ("written_explanation",
             "Explain how you would learn a new "
             "technology tool quickly for a task.",
             "Goal, resources, practice, "
             "apply, review."),
        ],
        "position": [
            ("written_explanation",
             "As a technology support assistant, describe "
             "how you would handle a first call from a "
             "confused user.",
             "Listen, gather details, "
             "guide step by step, confirm "
             "resolution."),
            ("scenario",
             "A user's printer stops working before a "
             "deadline. How do you respond?",
             "Prioritise, diagnose "
             "quickly, offer temporary "
             "solution, follow up."),
            ("short_answer",
             "What is the difference between "
             "troubleshooting and maintenance?",
             "Fixing problems vs "
             "preventing them; both "
             "needed."),
            ("design",
             "Design a help request form for a support "
             "team.",
             "Clear fields, problem "
             "description, priority, "
             "contact."),
            ("written_explanation",
             "Explain how you would document a problem "
             "and its solution for reuse.",
             "Steps, cause, fix, "
             "category, notes."),
            ("debugging",
             "A user cannot open an email attachment. "
             "List the likely causes in order.",
             "File type, size, "
             "permissions, software, "
             "corruption."),
            ("short_answer",
             "What is the difference between a shared "
             "drive and a cloud drive?",
             "Location and access "
             "model; when each is "
             "used."),
            ("design",
             "Design a first-week plan for a new "
             "technology assistant.",
             "Learn systems, meet "
             "people, handle basic "
             "tickets, build "
             "confidence."),
            ("written_explanation",
             "Explain how you would explain a technical "
             "issue to a non-technical manager.",
             "Simple terms, impact, "
             "what's needed, "
             "timeline."),
            ("scenario",
             "A user asks you to bypass a security "
             "control for convenience. How do you "
             "respond?",
             "Decline, explain why, "
             "offer safe alternative, "
             "escalate."),
            ("short_answer",
             "What is the difference between a "
             "permission and a password?",
             "Access rights vs "
             "credential; both "
             "control access."),
            ("design",
             "Design a simple weekly report of support "
             "work completed.",
             "Tickets, types, "
             "resolutions, follow-ups."),
            ("written_explanation",
             "Explain how you would handle a task that "
             "is above your current skill level.",
             "Be honest, break it "
             "down, get help, learn, "
             "deliver."),
            ("debugging",
             "A device shows 'storage full' but the "
             "user has few files. How do you "
             "investigate?",
             "Hidden files, cache, "
             "updates, system files, "
             "cleanup."),
            ("short_answer",
             "What is the difference between a ticket "
             "and a task?",
             "Support request vs "
             "assigned work; "
             "different flows."),
            ("design",
             "Design a user guide for a common office "
             "task (e.g. connecting a laptop to a "
             "projector).",
             "Clear steps, "
             "troubleshooting, "
             "friendly."),
            ("written_explanation",
             "Explain how you would keep your skills "
             "current in a fast-changing field.",
             "Learning habits, "
             "courses, practice, "
             "community."),
            ("scenario",
             "A colleague blames the IT team for a "
             "problem caused by their own mistake. How "
             "do you respond?",
             "Stay professional, "
             "investigate, resolve, "
             "avoid blame."),
            ("short_answer",
             "What is the difference between a "
             "shortcut and the original file?",
             "Link vs actual file; "
             "what happens if one "
             "breaks."),
            ("design",
             "Design a handover checklist for support "
             "staff at shift change.",
             "Open issues, "
             "priorities, notes, "
             "contacts."),
        ],
        "practical": [
            ("practical",
             "Describe the steps to connect a new "
             "computer to an office network.",
             "Cable/Wi-Fi, "
             "credentials, verify, "
             "security."),
            ("design",
             "Design a simple labelling scheme for "
             "office equipment.",
             "Consistent, findable, "
             "tracked."),
            ("practical",
             "Write a short guide for backing up files "
             "to a shared drive.",
             "Simple steps, "
             "verification."),
            ("debugging",
             "A monitor shows 'no signal'. List the "
             "checks in order.",
             "Power, cable, input, "
             "computer, hardware."),
            ("practical",
             "Describe how you would set up a new user "
             "account for an employee.",
             "Credentials, access, "
             "first login, "
             "handover."),
            ("design",
             "Design a maintenance log for an office's "
             "computers.",
             "Dates, actions, "
             "issues, owner."),
            ("practical",
             "Write a polite and clear ticket update "
             "to a user.",
             "Status, next step, "
             "timeline."),
            ("debugging",
             "A shared folder is inaccessible to one "
             "user. What do you check?",
             "Permissions, network, "
             "account, folder "
             "status."),
            ("practical",
             "Describe how you would scan a computer "
             "for viruses safely.",
             "Update, scan modes, "
             "quarantine, follow-up."),
            ("design",
             "Design a simple checklist to set up a "
             "new employee's workstation.",
             "Hardware, accounts, "
             "access, comfort."),
            ("practical",
             "Write a step-by-step for pairing a "
             "wireless mouse/keyboard.",
             "Clear, "
             "troubleshooting."),
            ("debugging",
             "A user cannot log in to the company "
             "portal. Describe your diagnosis.",
             "Credentials, network, "
             "account status, "
             "server."),
            ("practical",
             "Describe how you would organise cables "
             "in a shared office.",
             "Safety, labelling, "
             "accessibility."),
            ("design",
             "Design a simple hardware request form for "
             "employees.",
             "Item, reason, "
             "approval, delivery."),
            ("practical",
             "Write an email announcing a scheduled "
             "system maintenance.",
             "Clear timing, impact, "
             "preparation, "
             "contact."),
            ("debugging",
             "An application freezes on one computer "
             "but works on others. What do you check?",
             "Version, resources, "
             "settings, drivers, "
             "profile."),
            ("practical",
             "Describe how you would recover a "
             "forgotten password following policy.",
             "Identity check, "
             "reset, communicate."),
            ("design",
             "Design a simple inventory of "
             "software licences for an office.",
             "Product, licence, "
             "expiry, users."),
            ("practical",
             "Write a checklist for securely disposing "
             "of an old computer.",
             "Data wipe, "
             "recycling, records."),
            ("debugging",
             "A user's files are missing from their "
             "desktop. Where do you look and why?",
             "User profile, "
             "recycle, cloud, "
             "backups, "
             "search."),
        ],
    },
}
