"""
Unique category / position / practical questions for the question banks.
"""

CATS = {
    # ----------------------------------------------------------------- 14
    "Project & Product Management": {
        "category": [
            ("written_explanation",
             "Explain the difference between a project, a program "
             "and a portfolio.",
             "Project = temporary effort; program = group of "
             "related projects; portfolio = all work aligned to "
             "strategy."),
            ("scenario",
             "A project is behind schedule with a fixed deadline. "
             "Describe how you assess and respond.",
             "Earned value/remaining analysis, identify "
             "critical path, options (scope, resources, "
             "time), stakeholder communication."),
            ("design",
             "Design a project plan outline for delivering a new "
             "mobile app in three months.",
             "Phases, milestones, dependencies, resources, "
             "risks, governance."),
            ("written_explanation",
             "Explain the difference between the waterfall and "
             "agile approaches, and when each is appropriate.",
             "Sequential vs iterative; when requirements are "
             "stable vs evolving; trade-offs."),
            ("scenario",
             "A key stakeholder is not engaged and decisions are "
             "delayed. How do you handle it?",
             "Identify their interest, tailor "
             "communication, escalate appropriately, "
             "document impacts."),
            ("short_answer",
             "What is the difference between a milestone and a "
             "deliverable?",
             "Milestone = point in time marker; deliverable "
             "= tangible output."),
            ("written_explanation",
             "Explain how you would manage scope creep when a "
             "client keeps adding requests.",
             "Change control process, impact analysis, "
             "prioritisation, communication, signed "
             "changes."),
            ("design",
             "Design a risk management plan for a project with a "
             "tight budget.",
             "Risk register, likelihood/impact, "
             "mitigation, owners, review cadence."),
            ("scenario",
             "A team member is underperforming and the deadline "
             "is near. What do you do?",
             "Supportive conversation, clear expectations, "
             "redistribute work, involve HR if needed, "
             "protect the team."),
            ("written_explanation",
             "Explain the difference between a Gantt chart and a "
             "network diagram (CPM/PERT).",
             "Gantt = timeline visual; network = "
             "dependencies and critical path."),
            ("short_answer",
             "What is the difference between a product owner and "
             "a project manager?",
             "Product owner = product value and backlog; "
             "project manager = delivery, scope, budget, "
             "stakeholders."),
            ("design",
             "Design a stakeholder communication plan for a "
             "six-month project.",
             "Stakeholder map, channels, cadence, "
             "content, escalation."),
            ("written_explanation",
             "Explain the concept of the 'triple constraint' "
             "(scope, time, cost) and how it has evolved.",
             "Trade-offs between scope/time/cost; quality "
             "as a fourth constraint."),
            ("scenario",
             "A critical vendor fails to deliver on time. How do "
             "you respond?",
             "Assess impact, expedite or replace, "
             "negotiate, communicate, mitigate."),
            ("design",
             "Design a sprint planning and review cadence for an "
             "agile team of six.",
             "Planning, daily standup, review, "
             "retrospective; clear goals and "
             "definition of done."),
            ("written_explanation",
             "Explain how you would track and report project "
             "progress to executives honestly.",
             "Metrics, status, risks with "
             "recommendations, no sugar-coating, "
             "actionable."),
            ("short_answer",
             "What is the difference between a work breakdown "
             "structure and a task list?",
             "WBS = deliverable-oriented decomposition; "
             "task list = flat list of activities."),
            ("design",
             "Design a project retrospective process that "
             "produces real improvement.",
             "Safe environment, data, what went well / "
             "poorly, action items with owners."),
            ("scenario",
             "The business changes strategy mid-project. How do "
             "you adapt?",
             "Reassess priorities, re-plan, communicate "
             "impact, update governance, stay "
             "aligned."),
            ("written_explanation",
             "Explain what a 'minimum viable product' (MVP) is "
             "and how you decide what goes in it.",
             "Smallest valuable release for learning; "
             "prioritisation by value, risk and "
             "effort."),
        ],
        "position": [
            ("written_explanation",
             "As a project manager, describe how you would kick "
             "off a new project successfully.",
             "Charter, team, roles, plan, "
             "communication, success criteria, "
             "alignment."),
            ("scenario",
             "Two team leads disagree on the technical "
             "approach. As the PM, how do you help?",
             "Facilitate a decision, ensure data/evidence, "
             "escalate if needed, document, move "
             "forward."),
            ("short_answer",
             "What is the difference between a product roadmap "
             "and a release plan?",
             "Roadmap = strategic themes/timeline; release "
             "plan = specific features per release."),
            ("design",
             "Design a project status report template that "
             "executives can read in one minute.",
             "Summary, status colour, key metrics, "
             "risks, decisions needed."),
            ("written_explanation",
             "Explain how you would manage a project where "
             "requirements change every week.",
             "Agile backlog, change control, "
             "prioritisation with business, fixed "
             "timebox with flexible scope."),
            ("debugging",
             "A project consistently misses its estimates. How "
             "do you diagnose and fix estimation?",
             "Compare estimates to actuals, find bias, "
             "use historical data, adjust methods."),
            ("short_answer",
             "What is the difference between leading and "
             "lagging indicators on a project?",
             "Leading = predictive (velocity); lagging = "
             "outcome (defects found)."),
            ("design",
             "Design a stakeholder engagement plan for a "
             "project with a resistant user group.",
             "Identify concerns, build champions, "
             "communication, involvement, quick "
             "wins."),
            ("written_explanation",
             "Explain how you would run a daily standup that "
             "is valuable and short.",
             "Focus on progress, blockers, plan; "
             "surface issues; keep it timeboxed."),
            ("scenario",
             "A sponsor wants a status report that hides "
             "problems. How do you respond?",
             "Report honestly, explain the value of "
             "visibility, offer framing that is "
             "constructive but truthful."),
            ("short_answer",
             "What is the difference between a risk and an "
             "issue?",
             "Risk = potential future problem; issue = "
             "current problem."),
            ("design",
             "Design a change management plan for rolling out "
             "a new system to 500 employees.",
             "Communication, training, support, "
             "champions, feedback loop, adoption "
             "measurement."),
            ("written_explanation",
             "Explain how you would prioritise features as a "
             "product manager with limited resources.",
             "Value vs effort, strategic fit, "
             "customer feedback, data, stakeholder "
             "input."),
            ("debugging",
             "A project team is demotivated and attrition is "
             "rising. What do you investigate?",
             "Workload, clarity, recognition, "
             "conflict; fix causes, protect "
             "morale."),
            ("short_answer",
             "What is the difference between velocity and "
             "capacity in agile?",
             "Velocity = historical throughput; "
             "capacity = available team time."),
            ("design",
             "Design a product discovery process for a new "
             "feature.",
             "User research, problem definition, "
             "ideation, validation, MVP scope."),
            ("written_explanation",
             "Explain how you would manage a distributed "
             "team across time zones.",
             "Overlap hours, async communication, "
             "clear documentation, rituals that "
             "work."),
            ("scenario",
             "A client rejects the delivered project. How do "
             "you handle the acceptance process?",
             "Understand the gap, work through "
             "acceptance criteria, plan fixes, "
             "agree on resolution."),
            ("short_answer",
             "What is the difference between a release and a "
             "deployment?",
             "Release = making available to users; "
             "deployment = installing code; "
             "related but distinct."),
            ("design",
             "Design a lessons-learned process that teams "
             "actually use.",
             "Psychological safety, data, structured "
             "review, actions with owners, "
             "follow-up."),
        ],
        "practical": [
            ("practical",
             "Write a project charter outline for a website "
             "redesign project.",
             "Purpose, scope, stakeholders, "
             "success criteria, constraints."),
            ("design",
             "Design a one-week sprint plan for a small team "
             "with defined goals and deliverables.",
             "Prioritised backlog, capacity, "
             "definition of done, review."),
            ("practical",
             "Create a risk register with five realistic "
             "risks for a software delivery project.",
             "Probability/impact, mitigation, "
             "owner, trigger."),
            ("debugging",
             "A project's burn-down chart is flat. What does "
             "it mean and what do you do?",
             "Work not completing or not "
             "tracked; investigate, re-plan, "
             "communicate."),
            ("practical",
             "Write the agenda for a project kickoff "
             "meeting.",
             "Purpose, scope, roles, plan, "
             "communication, decisions."),
            ("design",
             "Design a prioritisation matrix for ten "
             "feature requests.",
             "Criteria (value, effort, risk), "
             "scoring, ranking, rationale."),
            ("practical",
             "Describe how you would estimate a two-week "
             "feature using story points or hours, "
             "including validation.",
             "Decomposition, team input, "
             "calibration with history."),
            ("debugging",
             "A critical dependency is delayed. Describe "
             "your contingency planning.",
             "Impact, alternatives, float "
             "analysis, mitigation, "
             "communication."),
            ("practical",
             "Write a one-page project one-pager for "
             "stakeholders.",
             "Goal, scope, timeline, team, "
             "status, risks, contact."),
            ("design",
             "Design a product roadmap for a calendar app "
             "with three themes over two quarters.",
             "Themes, timeboxes, goals, "
             "dependencies, flexibility."),
            ("practical",
             "Describe how you would run a sprint "
             "retrospective that produces actionable "
             "improvements.",
             "Format, safety, data, action "
             "items, owners, follow-up."),
            ("debugging",
             "A project's costs are 20% over budget. "
             "Describe your analysis and response.",
             "Variance analysis, causes, "
             "options, approval, tracking."),
            ("practical",
             "Write a RACI matrix for a small project "
             "(responsible, accountable, consulted, "
             "informed).",
             "Correct roles for key "
             "activities."),
            ("design",
             "Design a feature request intake process for "
             "a product team.",
             "Template, triage, "
             "prioritisation, communication, "
             "metrics."),
            ("practical",
             "Describe how you would communicate a "
             "schedule slip to stakeholders.",
             "Early, honest, with options "
             "and revised plan."),
            ("debugging",
             "A team reports 100% capacity but delivery "
             "is slow. How do you investigate?",
             "Track where time goes, "
             "interruptions, rework, "
             "context switching."),
            ("practical",
             "Write a definition of done for a user "
             "story.",
             "Coded, tested, reviewed, "
             "documented, accepted."),
            ("design",
             "Design a project governance structure with "
             "escalation paths.",
             "Steering committee, decision "
             "rights, escalation "
             "thresholds."),
            ("practical",
             "Describe how you would run a requirements "
             "prioritisation workshop.",
             "Preparation, criteria, "
             "facilitation, decisions, "
             "actions."),
            ("debugging",
             "A project was delivered on time but the "
             "business value is missing. How do you "
             "diagnose?",
             "Check original goals vs "
             "delivered, benefit "
             "measurement, lessons."),
        ],
    },

    # ----------------------------------------------------------------- 15
    "Technical Documentation & Knowledge Management": {
        "category": [
            ("written_explanation",
             "Explain the difference between user documentation "
             "and developer documentation, and who each serves.",
             "User = how to use; developer = how to "
             "integrate/extend; different audiences, "
             "depth, tone."),
            ("scenario",
             "A developer asks you to document a feature that "
             "keeps changing. How do you handle versioning?",
             "Document the current state, version "
             "with releases, change log, keep "
             "accuracy over completeness."),
            ("design",
             "Design a documentation structure for a SaaS "
             "product's help centre.",
             "Getting started, tutorials, how-to, "
             "reference, troubleshooting, FAQ - "
             "findable and navigable."),
            ("written_explanation",
             "Explain the difference between an API reference "
             "and an API guide.",
             "Reference = exhaustive endpoints/params; "
             "guide = concepts and workflows."),
            ("scenario",
             "A documentation search returns poor results. How "
             "do you improve findability?",
             "Better headings, synonyms, "
             "metadata/tags, restructuring, user "
             "feedback."),
            ("short_answer",
             "What is the difference between a README and a "
             "getting-started guide?",
             "README = quick orientation; "
             "getting-started = step-by-step first "
             "run."),
            ("written_explanation",
             "Explain how you would document a complex process "
             "so a new employee can follow it without help.",
             "Task-based steps, screenshots, "
             "troubleshooting, prerequisites, "
             "glossary, testing by a novice."),
            ("design",
             "Design a knowledge base strategy for a company "
             "with support, sales and engineering teams.",
             "Ownership, taxonomy, publishing "
             "workflow, search, maintenance, "
             "metrics."),
            ("scenario",
             "Engineers rarely update documentation because "
             "they are busy. How do you build the habit?",
             "Reduce friction (templates, docs-as-"
             "code), make it part of definition of "
             "done, celebrate contributions."),
            ("written_explanation",
             "Explain the difference between a style guide and "
             "a documentation template.",
             "Style guide = tone/voice/grammar rules; "
             "template = structure for a document "
             "type."),
            ("short_answer",
             "What is the difference between a tutorial and a "
             "how-to guide?",
             "Tutorial = learning-oriented, builds "
             "skills; how-to = task-oriented, "
             "solves a problem."),
            ("design",
             "Design a documentation review and approval "
             "process.",
             "Authors, reviewers, accuracy "
             "check, publication, feedback "
             "loop."),
            ("scenario",
             "Users are calling support because documentation "
             "is confusing. How do you identify and fix the "
             "problem articles?",
             "Support ticket analysis, article "
             "feedback, analytics, rewrite, "
             "measure."),
            ("written_explanation",
             "Explain the concept of docs-as-code and its "
             "benefits.",
             "Docs in version control, review, "
             "build, publish; quality and "
             "collaboration."),
            ("design",
             "Design a release notes process that informs "
             "users without overwhelming them.",
             "Categories (new, fixed, changed), "
             "audience-aware, links to details, "
             "cadence."),
            ("short_answer",
             "What is the difference between an FAQ and a "
             "troubleshooting guide?",
             "FAQ = common questions; "
             "troubleshooting = systematic problem "
             "resolution."),
            ("scenario",
             "A product team changes terminology mid-project. "
             "How do you manage the impact on docs?",
             "Glossary of terms, update "
             "systematically, cross-reference, "
             "communicate."),
            ("written_explanation",
             "Explain how you measure the quality and "
             "effectiveness of documentation.",
             "Feedback, support deflection, "
             "search/usage analytics, freshness, "
             "accuracy audits."),
            ("design",
             "Design a documentation onboarding package for "
             "new developers joining a codebase.",
             "Architecture overview, setup, "
             "workflow, conventions, pointers."),
            ("scenario",
             "A critical document contains incorrect security "
             "instructions. What do you do?",
             "Fix immediately, flag the error, "
             "verify related docs, notify "
             "affected users."),
        ],
        "position": [
            ("written_explanation",
             "As a technical writer, describe how you would "
             "document a new API from scratch.",
             "Understand the API, structure "
             "(overview, auth, endpoints, errors, "
             "examples), validate with developers, "
             "publish."),
            ("scenario",
             "A developer hands you code with no explanation "
             "and expects documentation. How do you get what "
             "you need?",
             "Ask targeted questions, run the code, "
             "read tests, pair briefly, draft and "
             "validate."),
            ("short_answer",
             "What is the difference between a reference "
             "manual and a user manual?",
             "Reference = lookup-oriented; user "
             "manual = task-oriented."),
            ("design",
             "Design a documentation template for standard "
             "operating procedures (SOPs).",
             "Purpose, scope, prerequisites, "
             "steps, safety, troubleshooting, "
             "owner."),
            ("written_explanation",
             "Explain how you would conduct an information "
             "architecture review of a help centre.",
             "User tasks, navigation test, "
             "labelling, search analysis, "
             "restructure."),
            ("debugging",
             "Users cannot find an important article in the "
             "knowledge base. How do you diagnose why?",
             "Search terms, titles, taxonomy, "
             "links, analytics; fix and "
             "verify."),
            ("short_answer",
             "What is the difference between plain language "
             "and simplified technical English?",
             "Plain = clear for the audience; "
             "STE = controlled vocabulary for "
             "translation/safety."),
            ("design",
             "Design a documentation plan for a software "
             "release (what docs, who writes, when).",
             "Release notes, updated guides, "
             "API changes, review, publish "
             "timeline."),
            ("written_explanation",
             "Explain how you keep documentation accurate "
             "when the product changes weekly.",
             "Docs-as-code, owner, automated "
             "checks, update cadence, "
             "deprecation notices."),
            ("scenario",
             "A subject matter expert gives you incorrect "
             "information. How do you verify?",
             "Check primary sources, test "
             "yourself, ask another expert, "
             "flag the discrepancy."),
            ("short_answer",
             "What is the difference between a changelog and "
             "release notes?",
             "Changelog = developer-oriented detail; "
             "release notes = user-oriented "
             "summary."),
            ("design",
             "Design a documentation style guide for a "
             "company.",
             "Voice, tone, grammar, formatting, "
             "terminology, examples."),
            ("written_explanation",
             "Explain how you would document an error message "
             "so users can act on it.",
             "What happened, why, what to do, "
             "where to get help."),
            ("debugging",
             "A tutorial no longer works after a product "
             "update. Describe your triage and fix.",
             "Reproduce, update steps, validate, "
             "note version, prevent recurrence."),
            ("short_answer",
             "What is the difference between a knowledge base "
             "article and a wiki page?",
             "KB = curated, reviewed; wiki = "
             "collaborative, organic."),
            ("design",
             "Design a documentation feedback system that "
             "produces useful signals.",
             "Feedback buttons, analytics, "
             "surveys, triage, action loop."),
            ("written_explanation",
             "Explain how you would document a legacy system "
             "with no source developers available.",
             "Observe, run, interview users, "
             "reverse-engineer, mark "
             "assumptions."),
            ("scenario",
             "Marketing wants documentation that oversells "
             "features. How do you respond?",
             "Keep accuracy, propose "
             "marketing-friendly framing that is "
             "truthful, align."),
            ("short_answer",
             "What is the difference between inline "
             "documentation and external documentation?",
             "Inline = in code/comments; external = "
             "guides/manuals; complementary."),
            ("design",
             "Design a documentation maintenance schedule for "
             "a product with quarterly releases.",
             "Ownership, review cadence, "
             "update triggers, metrics."),
        ],
        "practical": [
            ("practical",
             "Write a getting-started guide outline for a "
             "developer tool.",
             "Install, quick start, next "
             "steps, troubleshooting."),
            ("design",
             "Design an API reference page template for an "
             "endpoint (method, path, params, responses).",
             "Complete and accurate "
             "structure with examples."),
            ("practical",
             "Rewrite a poorly worded error message "
             "('Error 403 occurred') into a helpful one.",
             "Plain language, cause, "
             "action."),
            ("debugging",
             "A support article has a 90% 'no' feedback "
             "rate. Describe how you would fix it.",
             "Read the article, test the "
             "steps, rewrite, re-test, "
             "measure."),
            ("practical",
             "Write a release note entry for a bug fix and "
             "a new feature.",
             "Clear, audience-appropriate, "
             "categorised."),
            ("design",
             "Design a documentation information "
             "architecture for a product with 200 "
             "articles.",
             "Taxonomy, navigation, search "
             "strategy, maintenance."),
            ("practical",
             "Describe how you would add screenshots to "
             "documentation effectively (when, how, "
             "alt text).",
             "Supports steps, current, "
             "accessible."),
            ("debugging",
             "Two articles contradict each other about a "
             "setting. How do you resolve?",
             "Verify with product/engineers, "
             "update both, add cross-"
             "reference."),
            ("practical",
             "Write a documentation review checklist.",
             "Accuracy, clarity, "
             "completeness, style, "
             "links."),
            ("design",
             "Design a knowledge base homepage for "
             "self-service.",
             "Search-first, popular "
             "articles, categories, "
             "support contact."),
            ("practical",
             "Describe how you would convert a 30-minute "
             "screencast into useful documentation.",
             "Extract steps, write "
             "concise text, screenshots, "
             "structure."),
            ("debugging",
             "A document references a feature that was "
             "removed. What is your process?",
             "Find all references, "
             "update or remove, verify "
             "links."),
            ("practical",
             "Write a glossary entry for a technical term "
             "in plain language.",
             "Definition, context, "
             "example."),
            ("design",
             "Design a documentation onboarding flow for "
             "a new support agent.",
             "Key articles, search "
             "skills, escalation, "
             "practice."),
            ("practical",
             "Describe how you would test a tutorial's "
             "accuracy from scratch.",
             "Follow every step in a "
             "clean environment, note "
             "discrepancies, fix."),
            ("debugging",
             "A link in documentation returns 404. "
             "Describe your fix and prevention.",
             "Fix link, scan for "
             "broken links, automate "
             "checks."),
            ("practical",
             "Write a template for a product FAQ.",
             "Real questions, clear "
             "answers, links to "
             "detail."),
            ("design",
             "Design a documentation analytics dashboard "
             "(views, search, feedback).",
             "Metrics that inform "
             "improvement."),
            ("practical",
             "Describe how you would write documentation "
             "for a non-technical audience about a "
             "technical feature.",
             "Plain language, "
             "analogies, examples, "
             "glossary."),
            ("debugging",
             "Support tickets mention a feature "
             "documentation fails to explain. How do "
             "you respond?",
             "Analyse tickets, write "
             "the missing doc, link it, "
             "measure deflection."),
        ],
    },

    # ----------------------------------------------------------------- 16
    "IT Support & Technical Operations": {
        "category": [
            ("written_explanation",
             "Explain the difference between a help desk and a "
             "service desk, and how they serve users.",
             "Help desk = incident-focused; service desk = "
             "broader service management (requests, "
             "changes, SLAs)."),
            ("scenario",
             "A senior executive's laptop fails right before an "
             "important presentation. Describe your response.",
             "Priority handling, quick diagnosis, "
             "spare/loaner, communicate calmly, "
             "recover data, follow-up."),
            ("design",
             "Design an IT support ticketing process from "
             "submission to closure.",
             "Intake, categorisation, SLA, "
             "assignment, resolution, user "
             "confirmation, knowledge capture."),
            ("written_explanation",
             "Explain the difference between a proactive and a "
             "reactive support approach, with examples.",
             "Proactive = monitoring, maintenance, "
             "prevention; reactive = responding to "
             "reports."),
            ("scenario",
             "A user reports the same issue twice after you "
             "said it was fixed. How do you handle it?",
             "Re-open, investigate root cause, "
             "verify properly, communicate "
             "clearly, apologise if needed."),
            ("short_answer",
             "What is the difference between an incident and a "
             "service request?",
             "Incident = unplanned disruption; request = "
             "pre-approved service (new laptop)."),
            ("written_explanation",
             "Explain how you would troubleshoot a computer "
             "that will not turn on.",
             "Power source, cables, indicators, "
             "peripherals, hardware, then "
             "document."),
            ("design",
             "Design an onboarding IT checklist for a new "
             "employee's first day.",
             "Account, device, access, email, "
             "software, training, support "
             "introduction."),
            ("scenario",
             "Multiple users report slow computers after a "
             "software update. How do you respond?",
             "Confirm pattern, gather data, "
             "rollback or patch, communicate, "
             "prevent recurrence."),
            ("written_explanation",
             "Explain what an SLA is and how you would "
             "measure compliance.",
             "Service level agreement targets; "
             "measured metrics, reporting, "
             "escalation."),
            ("short_answer",
             "What is the difference between remote support and "
             "on-site support?",
             "Remote = via tools/network; on-site = "
             "physical; when each is needed."),
            ("design",
             "Design a knowledge base of common solutions for "
             "a support team.",
             "Capture process, categories, "
             "searchability, update ownership."),
            ("scenario",
             "A user is frustrated and angry about a recurring "
             "problem. How do you de-escalate?",
             "Listen, acknowledge, take ownership, "
             "set expectations, follow through."),
            ("written_explanation",
             "Explain how you would handle a malware infection "
             "on a user's machine.",
             "Isolate, scan/clean, check for "
             "spread, reset credentials, educate, "
             "prevent."),
            ("design",
             "Design a password and account lifecycle "
             "management process.",
             "Creation, MFA, rotation, offboarding, "
             "audit."),
            ("scenario",
             "A critical system fails outside business hours. "
             "Describe your escalation process.",
             "On-call procedure, severity, "
             "communication, resolution, "
             "post-incident."),
            ("written_explanation",
             "Explain the difference between break-fix support "
             "and managed services.",
             "Reactive vs proactive contracted "
             "service; scope and pricing "
             "differences."),
            ("short_answer",
             "What is the difference between a software "
             "patch and an update?",
             "Patch = fix; update = enhancement/version; "
             "both need testing and rollout."),
            ("design",
             "Design a device lifecycle management plan "
             "(procurement to disposal).",
             "Standardisation, tracking, "
             "maintenance, refresh, secure "
             "disposal."),
            ("scenario",
             "A user requests software that poses a security "
             "risk. How do you handle the request?",
             "Explain risk, propose alternatives, "
             "escalate decision, document."),
        ],
        "position": [
            ("written_explanation",
             "As a help desk analyst, describe how you would "
             "handle a first-contact support call.",
             "Greet, identify, gather details, "
             "troubleshoot, resolve or escalate, "
             "close with confirmation."),
            ("scenario",
             "You are supporting a user who cannot explain "
             "the problem clearly. How do you extract what "
             "you need?",
             "Ask guided questions, ask for "
             "screenshots, replicate, narrow "
             "down."),
            ("short_answer",
             "What is the difference between a ticket "
             "priority and its SLA?",
             "Priority = importance; SLA = time "
             "target tied to priority."),
            ("design",
             "Design a remote troubleshooting playbook for "
             "common issues (no network, slow PC, printer).",
             "Step-by-step, safe commands, "
             "escalation points."),
            ("written_explanation",
             "Explain how you would prioritise tickets when "
             "everything is 'urgent'.",
             "Objective criteria (impact, "
             "number affected), communicate "
             "expectations, escalate."),
            ("debugging",
             "A user's email is not receiving messages. "
             "Describe your diagnosis.",
             "Check storage, rules, server "
             "status, spam, delivery logs, "
             "test."),
            ("short_answer",
             "What is the difference between an on-premise "
             "and a cloud-managed device?",
             "Where it is hosted/patched; "
             "management model differs."),
            ("design",
             "Design an asset management process for 200 "
             "laptops.",
             "Inventory, tracking, "
             "assignments, maintenance, "
             "disposal."),
            ("written_explanation",
             "Explain how you would handle a user's data "
             "backup and recovery request.",
             "Backup source, restore process, "
             "verification, retention, "
             "documentation."),
            ("scenario",
             "A printer is down in a busy office. Describe "
             "your triage and the user communication.",
             "Diagnose, inform users with "
             "ETA, fix or escalate, follow "
             "up."),
            ("short_answer",
             "What is the difference between a soft reboot "
             "and a hard reset, and when is each "
             "appropriate?",
             "Graceful vs forced; hard reset "
             "last resort (data risk)."),
            ("design",
             "Design a software deployment process for "
             "rolling out updates to company devices.",
             "Pilot group, testing, staged "
             "rollout, rollback, "
             "communication."),
            ("written_explanation",
             "Explain how you would secure a user's laptop "
             "that will be used on public Wi-Fi.",
             "VPN, firewall, updates, "
             "physical security, awareness."),
            ("debugging",
             "A user's VPN connects but they cannot access "
             "files. Describe your diagnosis.",
             "Check authentication, routes, "
             "permissions, firewall, DNS."),
            ("short_answer",
             "What is the difference between a golden image "
             "and a standard build?",
             "Golden image = ready-to-deploy "
             "template; standard build = "
             "specification."),
            ("design",
             "Design a user offboarding checklist that "
             "revokes access completely.",
             "Accounts, devices, data, "
             "badges, audit."),
            ("written_explanation",
             "Explain how you would document a complex "
             "support resolution for reuse.",
             "Clear steps, root cause, "
             "category, knowledge base, "
             "review."),
            ("scenario",
             "A user is about to lose data because their "
             "drive is failing. How do you respond?",
             "Stop usage, image the drive, "
             "recover data, replace, "
             "verify."),
            ("short_answer",
             "What is the difference between a warranty and "
             "a support contract?",
             "Warranty = manufacturer; "
             "support = service agreement; "
             "overlap."),
            ("design",
             "Design a shift handover process for a support "
             "team.",
             "Open tickets, ongoing issues, "
             "notes, priorities, "
             "escalations."),
        ],
        "practical": [
            ("practical",
             "Write a step-by-step guide for connecting a "
             "printer over Wi-Fi for a non-technical user.",
             "Clear, safe, complete "
             "steps."),
            ("debugging",
             "A laptop is slow to boot. Describe your "
             "diagnosis and likely fixes.",
             "Startup programs, disk "
             "health, updates, malware, "
             "hardware."),
            ("practical",
             "Describe how you would back up a user's "
             "files before a repair.",
             "Identify data, copy to "
             "safe location, verify, "
             "restore."),
            ("design",
             "Design a first-day IT welcome email for a "
             "new employee.",
             "Accounts, support contact, "
             "key systems, tips."),
            ("practical",
             "Write a password reset procedure for a "
             "help desk.",
             "Identity verification, "
             "reset, communication, "
             "follow-up."),
            ("debugging",
             "A user cannot connect to Wi-Fi while others "
             "can. Describe your steps.",
             "Check device settings, "
             "forget/reconnect, drivers, "
             "MAC filter, AP."),
            ("practical",
             "Describe how you would image a new laptop "
             "for deployment.",
             "Standard image, "
             "personalisation, "
             "verification."),
            ("design",
             "Design a hardware maintenance schedule for "
             "an office.",
             "Cleaning, updates, "
             "health checks, "
             "replacement plan."),
            ("practical",
             "Write the steps to safely remove a USB "
             "drive and why it matters.",
             "Eject, verify, avoid "
             "data loss."),
            ("debugging",
             "A user's screen is flickering. List the "
             "likely causes in order.",
             "Cable, driver, hardware, "
             "power, environmental."),
            ("practical",
             "Describe how you would handle a lost "
             "company phone.",
             "Remote wipe, report, "
             "replacement, security "
             "check."),
            ("design",
             "Design a remote support session checklist "
             "(consent, security, tools).",
             "Consent, screen sharing, "
             "secure connection, notes."),
            ("practical",
             "Write a troubleshooting flow for 'no "
             "internet' on a desktop.",
             "Physical, network, "
             "software, ISP, "
             "escalation."),
            ("debugging",
             "A shared drive is full. How do you "
             "investigate and resolve?",
             "Find large files, "
             "archive, quotas, "
             "communication."),
            ("practical",
             "Describe how you would set up a new "
             "workstation from scratch.",
             "Hardware, OS, updates, "
             "software, accounts, "
             "verify."),
            ("design",
             "Design a support SLAs table for a small "
             "company (response and resolution by "
             "priority).",
             "Realistic targets, "
             "owners, reporting."),
            ("practical",
             "Write a step-by-step to map a network drive "
             "for a user.",
             "Correct path, "
             "credentials, "
             "persistence."),
            ("debugging",
             "A user's Outlook/email is slow. Describe "
             "your diagnosis.",
             "Mailbox size, add-ins, "
             "network, server, repair."),
            ("practical",
             "Describe how you would dispose of an old "
             "computer with sensitive data.",
             "Data wipe, certificate, "
             "recycling, audit."),
            ("design",
             "Design a support team weekly reporting "
             "process.",
             "Volume, resolution, "
             "SLA, feedback, "
             "trends."),
        ],
    },

    # ----------------------------------------------------------------- 17
    "Hardware & Electronics": {
        "category": [
            ("written_explanation",
             "Explain Ohm's law and how you would use it to "
             "select a resistor for an LED circuit.",
             "V=IR; correct calculation with current "
             "limit and voltage drop."),
            ("scenario",
             "A circuit you built works on a breadboard but "
             "fails when soldered. Describe your diagnosis.",
             "Check solder joints, shorts, component "
             "orientation, thermal damage, power "
             "issues."),
            ("design",
             "Design a power supply section for a device that "
             "needs 5V from a battery. Describe the "
             "components and decisions.",
             "Regulator selection (linear vs buck), "
             "capacitance, protection, efficiency, "
             "load."),
            ("written_explanation",
             "Explain the difference between analog and digital "
             "signals, with a real example of each.",
             "Continuous vs discrete; example like "
             "microphone vs button input."),
            ("scenario",
             "A device intermittently resets itself. Describe "
             "how you would investigate.",
             "Power stability, brownouts, watchdog, "
             "electromagnetic interference, thermal."),
            ("short_answer",
             "What is the difference between a resistor and a "
             "potentiometer?",
             "Fixed vs adjustable resistance; use cases "
             "for each."),
            ("written_explanation",
             "Explain what a microcontroller is versus a "
             "microprocessor, and when you would choose each.",
             "MCU = integrated, low-power, embedded; MPU "
             "= general computing; selection criteria."),
            ("design",
             "Design the input/output section of a device that "
             "reads buttons and drives LEDs. Describe the "
             "circuit decisions.",
             "Pull-up/pull-down, debouncing, current "
             "limiting, GPIO protection."),
            ("scenario",
             "A colleague proposes using a component rated "
             "below the required voltage. How do you respond?",
             "Explain the failure risk, verify the "
             "spec, propose correct part, document."),
            ("written_explanation",
             "Explain the difference between AC and DC, and "
             "where each is used.",
             "Alternating vs direct; mains and "
             "transmission vs electronics/batteries."),
            ("short_answer",
             "What is the difference between a capacitor and an "
             "inductor?",
             "Store electric vs magnetic energy; "
             "filtering behaviour differs."),
            ("design",
             "Design a battery charging circuit concept for a "
             "Li-ion cell, including the safety considerations.",
             "Charge control (CC/CV), protection (over-"
             "voltage, temperature), no over-discharge."),
            ("scenario",
             "A prototype overheats under load. Describe your "
             "diagnosis and mitigation.",
             "Measure current, find losses, check "
             "thermal path, add heatsink/ventilation, "
             "reduce load."),
            ("written_explanation",
             "Explain how a transistor works as a switch, with "
             "a simple application example.",
             "Base/gate controls current flow; example "
             "driving a relay or LED."),
            ("design",
             "Design a sensor interface for reading a "
             "temperature sensor into a microcontroller.",
             "Sensor type, signal conditioning, "
             "conversion (ADC), calibration, noise "
             "handling."),
            ("short_answer",
             "What is the difference between a fuse and a "
             "circuit breaker?",
             "One-time vs resettable protection; "
             "selection and response time."),
            ("written_explanation",
             "Explain how you would test a newly assembled "
             "PCB before powering it fully.",
             "Visual inspection, continuity, short "
             "check, power-on with current limit, "
             "incremental bring-up."),
            ("design",
             "Design an ESD protection approach for a product "
             "with exposed connectors.",
             "TVS diodes, filtering, grounding, "
             "handling procedures, testing."),
            ("scenario",
             "A supplier proposes a cheaper component that is "
             "not an exact equivalent. How do you evaluate "
             "it?",
             "Compare specs (voltage, current, "
             "tolerance, temperature), test, decide "
             "with data."),
            ("written_explanation",
             "Explain the concept of signal integrity and why "
             "it matters at higher speeds.",
             "Reflections, crosstalk, impedance; "
             "matters for high-speed digital design."),
        ],
        "position": [
            ("written_explanation",
             "As a hardware engineer, describe your process "
             "for taking a circuit from schematic to working "
             "prototype.",
             "Schematic review, layout, fabrication, "
             "assembly, bring-up, testing, "
             "iteration."),
            ("scenario",
             "A customer returns a device that fails only in "
             "high humidity. How do you investigate?",
             "Environmental testing, conformal "
             "coating check, moisture ingress "
             "paths, corrosion."),
            ("short_answer",
             "What is the difference between a schematic and a "
             "PCB layout?",
             "Schematic = logical connections; layout = "
             "physical placement and routing."),
            ("design",
             "Design the power tree for a device with 3.3V "
             "digital, 5V analog and a motor rail.",
             "Regulation stages, isolation of noisy "
             "rails, decoupling, sequencing."),
            ("written_explanation",
             "Explain how you would debug a board that draws "
             "too much current on first power-up.",
             "Current-limited supply, thermal "
             "imaging, section isolation, shorts, "
             "reversed parts."),
            ("debugging",
             "A device communicates intermittently over "
             "UART. Describe your diagnosis.",
             "Baud rate mismatch, wiring, ground, "
             "logic levels, noise, firmware."),
            ("short_answer",
             "What is the difference between through-hole and "
             "surface-mount components?",
             "Assembly method, size, thermal, "
             "suitability for production."),
            ("design",
             "Design a motor driver section for a small "
             "robot, including protection.",
             "Driver selection, flyback diodes, "
             "current limits, thermal, control "
             "interface."),
            ("written_explanation",
             "Explain how you would choose a battery for a "
             "portable device given power and runtime "
             "requirements.",
             "Capacity, voltage, chemistry, size, "
             "discharge rate, safety."),
            ("scenario",
             "A firmware change makes a hardware feature "
             "unstable. How do you coordinate the fix?",
             "Isolate hardware vs software, reproduce, "
             "align on interface/timing, fix and "
             "test together."),
            ("short_answer",
             "What is the difference between I2C and SPI?",
             "Bus topologies, speed, pins, "
             "addressing; when each is used."),
            ("design",
             "Design an enclosure cooling strategy for a "
             "device with a 5W heat source.",
             "Ventilation, heatsink, fan or passive, "
             "thermal simulation or test."),
            ("written_explanation",
             "Explain how you would measure and verify the "
             "accuracy of a sensor in a product.",
             "Reference comparison, calibration, "
             "tolerance analysis, environmental "
             "factors."),
            ("debugging",
             "A PCB has a hairline crack that causes "
             "intermittent failures. How do you find it?",
             "Visual/optical inspection, flex "
             "testing, thermal cycling, X-ray, "
             "isolation."),
            ("short_answer",
             "What is the difference between a voltage "
             "regulator and a voltage reference?",
             "Regulator = supplies power; reference = "
             "precision voltage for measurement."),
            ("design",
             "Design a watchdog and fail-safe strategy for an "
             "embedded device that must never fail silently.",
             "Watchdog timer, brownout detection, "
             "safe state, health reporting."),
            ("written_explanation",
             "Explain how you would test a product for "
             "electromagnetic compatibility (EMC).",
             "Emissions and immunity tests, standards, "
             "shielding/filtering, pre-compliance."),
            ("scenario",
             "A batch of boards fails QC at a specific step. "
             "How do you triage?",
             "Correlate failures, inspect the step, "
             "process or component analysis, "
             "corrective action."),
            ("short_answer",
             "What is the difference between a logic analyzer "
             "and an oscilloscope?",
             "Many digital channels/timing vs analog "
             "waveforms; complementary tools."),
            ("design",
             "Design a hardware-in-the-loop test setup for an "
             "embedded controller.",
             "Simulated sensors, actuators, test "
             "scenarios, automation."),
        ],
        "practical": [
            ("practical",
             "Calculate the resistor value needed to run an "
             "LED at 20mA from a 5V supply (LED forward "
             "voltage 2V). Show your working.",
             "R = (5-2)/0.02 = 150 ohms; correct "
             "formula and reasoning."),
            ("design",
             "Design a button input circuit with debouncing "
             "for a microcontroller.",
             "RC filter or software debounce, "
             "pull-up, rationale."),
            ("practical",
             "Describe how you would use a multimeter to "
             "check for a short on a board.",
             "Resistance/continuity mode, isolate "
             "sections, verify."),
            ("debugging",
             "A circuit's output voltage is lower than "
             "expected. List the checks in order.",
             "Supply, components, load, "
             "connections, meter."),
            ("practical",
             "Write a plan to safely prototype a circuit "
             "with mains power involved.",
             "Isolation, fuse, current limit, "
             "no bare wires, procedure."),
            ("design",
             "Design a low-battery indicator circuit for a "
             "battery-powered device.",
             "Voltage divider + comparator/ADC, "
             "hysteresis, LED or signal."),
            ("practical",
             "Describe how you would measure the power "
             "consumption of a prototype.",
             "Series current measurement, "
             "data logging, average vs peak."),
            ("debugging",
             "An analog sensor reading is noisy. How do you "
             "stabilise it?",
             "Filtering, shielding, grounding, "
             "averaging, decoupling."),
            ("practical",
             "Calculate the power dissipated by a 10 ohm "
             "resistor carrying 0.5A.",
             "P = I^2 R = 2.5W; correct and "
             "safety margin."),
            ("design",
             "Design a simple two-transistor or IC-based "
             "buzzer driver circuit.",
             "Current drive, protection, "
             "control input."),
            ("practical",
             "Describe the steps to bring up a brand-new "
             "board safely.",
             "Visual, power checks, "
             "programming, peripheral "
             "tests."),
            ("debugging",
             "A connector pin is not making contact. How do "
             "you diagnose?",
             "Continuity, pin inspection, "
             "crimping, replacement."),
            ("practical",
             "Write a test procedure for verifying a 7-"
             "segment display module.",
             "Power, segment check, "
             "common pin, control."),
            ("design",
             "Design a temperature-controlled fan circuit "
             "concept for a PC or enclosure.",
             "Sensor, control (PWM or "
             "switch), hysteresis, "
             "fail-safe."),
            ("practical",
             "Describe how you would calibrate a "
             "temperature sensor against a reference.",
             "Two-point calibration, "
             "linearisation, error "
             "recording."),
            ("debugging",
             "A motor spins in the wrong direction. What are "
             "the possible causes and fixes?",
             "Polarity, wiring, driver "
             "logic, firmware."),
            ("practical",
             "Write a checklist for reworking a bad solder "
             "joint.",
             "Flux, iron tip, clean, "
             "verify, inspect."),
            ("design",
             "Design a simple battery voltage monitoring "
             "circuit with an LED threshold.",
             "Divider, comparator, "
             "hysteresis, calibration."),
            ("practical",
             "Describe how you would measure the ripple on a "
             "power supply output.",
             "Oscilloscope AC coupling, "
             "probe technique, load "
             "condition."),
            ("debugging",
             "Two wires that should be isolated show "
             "continuity. What is happening and how do you "
             "confirm?",
             "Solder bridge, damaged "
             "insulation, wrong net; "
             "verify visually and with "
             "measurement."),
        ],
    },
}
