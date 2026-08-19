"""
Unique category / position / practical questions for the question banks.

Each category entry: {"category": [20], "position": [20], "practical": [20]}
Question format: (question_type, question_text, grading_notes)
"""

CATS = {
    # ------------------------------------------------------------------ 1
    "Software Development & Engineering": {
        "category": [
            ("written_explanation",
             "Explain the difference between a monolithic architecture and a "
             "microservices architecture. When would you choose each, and what "
             "are the main trade-offs?",
             "Accurate definitions, sensible selection criteria (team size, "
             "scale, deployment independence), honest trade-offs (complexity, "
             "network latency, observability)."),
            ("scenario",
             "A feature you shipped last week now causes a production "
             "outage at peak hours. Walk through your debugging approach from "
             "first alert to resolution.",
             "Ordered diagnosis: check deploy, logs, metrics, recent data "
             "changes; isolate; rollback or hotfix decision; post-mortem and "
             "prevention."),
            ("design",
             "Design the data model for a ride-hailing app that must track "
             "drivers, riders, trips, payments and ratings. Show the main "
             "entities, relationships and one indexing decision you would "
             "make.",
             "Sensible entities and FKs, trip/payment integrity, indexing for "
             "hot queries (driver location, trip history), awareness of "
             "concurrency (no double-booking)."),
            ("written_explanation",
             "What is the difference between an interface/abstract class and "
             "a concrete implementation, and why does depending on "
             "abstractions improve testability?",
             "Correct conceptual distinction; explains dependency injection, "
             "mocking, and swapping implementations without changing callers."),
            ("scenario",
             "A client wants a feature that will double the load time of the "
             "product. How do you communicate the trade-off and propose "
             "alternatives?",
             "Quantifies impact, proposes alternatives (lazy loading, "
             "progressive enhancement, caching), involves stakeholders in the "
             "decision, documents the choice."),
            ("short_answer",
             "Name and briefly explain three strategies for making a web "
             "application faster from the user's perspective.",
             "Any of: caching, CDN, minification/bundling, lazy loading, "
             "database indexing, connection pooling, code splitting, "
             "async processing."),
            ("written_explanation",
             "Explain what idempotency means in API design, why it matters "
             "for payment endpoints, and how you would implement it.",
             "Correct definition (same request effect repeats safely), "
             "payment retry safety, implementation via idempotency keys or "
             "unique constraints."),
            ("scenario",
             "Users report that a search page returns wrong results only for "
             "entries containing accented characters. What is your hypothesis "
             "and how do you confirm and fix it?",
             "Hypothesise encoding/collation issue; confirm with a minimal "
             "repro; fix at storage or query layer; add a regression test."),
            ("scenario",
             "Your team has no tests on a legacy module you must refactor. "
             "How do you make the change safely?",
             "Characterise behaviour with tests first, refactor in small "
             "steps, use feature flags where needed, keep changes reviewable, "
             "measure regressions."),
            ("written_explanation",
             "Explain version control workflows: what is the difference "
             "between Git merge and rebase, and when would you use each?",
             "Accurate mechanics of both; uses merge to preserve history, "
             "rebase to linearise before merging; aware of the dangers of "
             "rewriting shared history."),
            ("scenario",
             "A junior developer submits a pull request that works but "
             "violates several project standards. How do you handle the "
             "review?",
             "Specific, kind feedback; explains the why behind standards; "
             "offers pair time; blocks merge only where genuinely necessary."),
            ("design",
             "Design an authentication flow for a mobile app that must also "
             "support password reset. Describe the flow, storage, and one "
             "security consideration per step.",
             "Secure password hashing, session/token handling, reset with "
             "expiring links, rate limiting, no credential leakage in logs."),
            ("written_explanation",
             "What is the difference between synchronous and asynchronous "
             "programming? Give a real example of where async is necessary "
             "and where it is harmful.",
             "Clear contrast; async justified for I/O-bound work; harmful "
             "when it adds complexity without benefit (CPU-bound, small "
             "apps)."),
            ("scenario",
             "An API returns 500 errors for some users but not others. "
             "List the variables you would compare and the first three "
             "things you would check.",
             "Compare input data, locale/encoding, permissions, "
             "configuration flags, data volume; check logs, edge cases in "
             "input, and environment differences."),
            ("scenario",
             "You inherit a codebase with no documentation and a critical "
             "bug. How do you orient yourself and deliver the fix "
             "confidently?",
             "Reads entry points and tests, reproduces the bug, maps the "
             "affected path, writes a regression test, fixes minimally, "
             "documents findings."),
            ("written_explanation",
             "Explain the concept of 'technical debt'. Give an example of "
             "when taking on debt is wise and when it is reckless.",
             "Correct concept; wise when bounded, tracked and scheduled for "
             "repayment; reckless when unacknowledged and compounding."),
            ("scenario",
             "Two libraries both solve your problem: one is popular but "
             "unmaintained, the other is small and new. How do you decide?",
             "Criteria: maintenance, security, licence, community, "
             "fit-for-purpose, exit strategy; avoids judging by popularity "
             "alone."),
            ("design",
             "A mobile app syncs data to a server over unreliable networks. "
             "Design a strategy that never loses user data.",
             "Local-first storage, queue with retries and backoff, conflict "
             "resolution strategy, idempotent sync endpoints, user-visible "
             "sync status."),
            ("short_answer",
             "What is the difference between SQL injection and stored XSS? "
             "Give one prevention technique for each.",
             "Correct definitions (server-side data injection vs client-side "
             "script execution); parameterised queries and output encoding "
             "respectively."),
            ("written_explanation",
             "Explain how you would estimate a software task you have never "
             "done before. What makes your estimate credible?",
             "Decomposition, research spike, reference to similar work, "
             "explicit assumptions, buffer for unknowns, revisiting the "
             "estimate as information arrives."),
        ],
        "position": [
            ("written_explanation",
             "For a full-stack developer: explain how the frontend, backend "
             "and database interact in a typical request, and where you "
             "would place validation at each layer.",
             "Accurate request flow; validation at client (UX), server "
             "(security - always), and DB (integrity); explains why server "
             "validation is mandatory."),
            ("scenario",
             "As a backend developer you are asked to expose an endpoint "
             "that returns user data. What checks do you perform before "
             "shipping it?",
             "Authentication and authorisation, input validation, output "
             "sanitisation, rate limiting, pagination, logging without "
             "sensitive data, tests."),
            ("written_explanation",
             "Explain how you would structure a React or similar frontend "
             "application so it stays maintainable as it grows.",
             "Component decomposition, state management strategy, separation "
             "of concerns, consistent patterns, testing strategy."),
            ("debugging",
             "A web page renders fine in Chrome but breaks in Safari. What "
             "is your approach to diagnosing and fixing browser-specific "
             "issues?",
             "Check console errors, isolate the offending feature, consult "
             "compatibility tables, use vendor prefixes or polyfills, test "
             "across browsers."),
            ("scenario",
             "You are asked to integrate with a third-party payment API "
             "whose documentation is outdated. How do you proceed safely?",
             "Contract testing against sandbox, captures real responses, "
             "handles webhooks with signature verification, graceful "
             "failure paths, vendor support contact."),
            ("design",
             "Design the API for a simple banking app supporting transfers "
             "between accounts. Show the endpoints, and explain how you "
             "prevent double-spending during concurrent transfers.",
             "Endpoints (accounts, transfer with idempotency key, "
             "transaction/ledger), atomic DB transactions with row locks, "
             "idempotency keys, balances derived from ledger."),
            ("written_explanation",
             "What does 'code review' accomplish beyond finding bugs? "
             "Describe a review culture you would want to work in.",
             "Knowledge sharing, consistency, ownership, mentorship; "
             "respectful, timely, focused on the change not the author."),
            ("short_answer",
             "Explain the difference between a functional test, an "
             "integration test, and a unit test. Which one is usually "
             "fastest and why?",
             "Correct layers; unit tests fastest (no I/O); each has a "
             "purpose in the pyramid."),
            ("scenario",
             "You are responsible for a library used by ten other teams. A "
             "breaking change is needed. How do you roll it out?",
             "Deprecation cycle, migration guides, codemods, feature flags, "
             "versioning policy (semver), communication plan, support "
             "window."),
            ("written_explanation",
             "Explain the trade-offs between using an ORM and writing raw "
             "SQL. When would you use each?",
             "ORM: speed of development, safety, portability; raw SQL: "
             "complex queries, performance control; pragmatic mix."),
            ("design",
             "You must store and serve billions of short messages. Sketch "
             "the storage and retrieval design, including how you keep "
             "reads fast.",
             "Partitioning/sharding, time-based hot/cold storage, caching "
             "hot data, message IDs, pagination, archival strategy."),
            ("debugging",
             "A scheduled job that sends emails sometimes sends duplicates. "
             "Describe how you would find the cause and prevent it.",
             "Check retry logic and acknowledgements, idempotency of "
             "processing, locking/lease on job execution, outbox pattern, "
             "dedupe keys in the mail queue."),
            ("scenario",
             "Your application's database connection pool is exhausted "
             "during a traffic spike. What are your immediate and long-term "
             "fixes?",
             "Immediate: scale, kill runaway queries, increase pool within "
             "limits; long-term: connection reuse, query optimisation, "
             "caching, monitoring alerts."),
            ("written_explanation",
             "Explain how cookies and tokens (e.g. JWT) differ for "
             "authentication, and the security considerations of each.",
             "Cookie: browser-managed, CSRF considerations; JWT: stateless, "
             "XSS exposure risk, revocation difficulty; storage choices and "
             "expiry."),
            ("short_answer",
             "What is the difference between a process and a thread, and "
             "when would a language use each for concurrency?",
             "Correct definitions (memory isolation vs shared memory); "
             "examples like multi-process workers vs thread pools."),
            ("scenario",
             "A colleague wrote code that passes tests but you suspect a "
             "security flaw. How do you raise it and verify your suspicion?",
             "Checks the code against known vulnerability patterns, writes a "
             "proof-of-concept test, raises it factually, proposes fix and "
             "posture improvement."),
            ("design",
             "Design a feature flag system that lets a team turn off a "
             "broken feature without a deploy. Describe storage, "
             "evaluation, and rollout controls.",
             "Flag store (DB/config), SDK evaluation, percentage rollouts, "
             "kill switch with instant propagation, audit log of changes."),
            ("written_explanation",
             "Explain what caching is, where you would place caches in a "
             "web application, and the main danger of caching.",
             "Cache layers (browser, CDN, app, DB); invalidation and "
             "staleness as the main danger; appropriate TTLs and cache keys."),
            ("debugging",
             "A mobile app crashes on launch for 1% of users. How do you "
             "find the cause when you cannot reproduce it?",
             "Crash reporting with stack traces and device metadata, "
             "grouping by OS/device/version, targeted instrumentation, "
             "release bisect, staged rollout."),
            ("scenario",
             "Your team ships every two weeks, but the business wants "
             "faster delivery of one critical feature. How do you respond "
             "without breaking quality?",
             "Proposes options (feature flag, staged rollout, scoped "
             "release), protects testing and rollback, sets expectations "
             "honestly."),
        ],
        "practical": [
            ("practical",
             "Write a function that, given a list of integers, returns the "
             "largest product of any three numbers. Explain your approach "
             "and its time complexity.",
             "Handles negatives correctly (two negatives can multiply "
             "positive); O(n log n) or O(n) solution; correct edge cases."),
            ("design",
             "Design a URL shortener service. Describe the API, how you "
             "generate short codes, and how you handle analytics (click "
             "counts).",
             "API endpoints, collision-resistant code generation, "
             "redirect with 301/302, analytics via async counting, "
             "scalability notes."),
            ("practical",
             "You have a function that is called 10,000 times per second "
             "and it is slow because it queries the database each time. "
             "Show how you would fix it, including the code shape.",
             "Caching or batching, connection reuse, indexed query, "
             "memoisation; explains why and measures impact."),
            ("debugging",
             "Given this pseudo-code, find the bug: a function that "
             "computes the average of a list divides by the wrong value "
             "when the list has one element. Explain your fix.",
             "Spot division-by-zero or off-by-one; propose guard; explain "
             "how they found it (boundary analysis)."),
            ("practical",
             "Write SQL that returns the top 5 best-selling products per "
             "region from tables of products, sales and regions.",
             "Correct joins, window function (ROW_NUMBER) or correlated "
             "approach, correct grouping, handles ties sensibly."),
            ("design",
             "Sketch an architecture diagram (in words) for a real-time "
             "chat application with one million users. Include components "
             "and how messages flow.",
             "WebSocket/SSE gateway, message queue, chat service, storage, "
             "presence service, horizontal scaling, delivery/retry logic."),
            ("practical",
             "Write a function that checks whether a string is a valid "
             "palindrome, ignoring spaces, punctuation and case. Show a "
             "test case that would catch a naive implementation.",
             "Canonicalises input before comparison; test like 'A man, a "
             "plan, a canal: Panama' catches naive approach."),
            ("debugging",
             "A batch script fails only when it runs on the first day of "
             "the month. List the likely causes and the step you would "
             "take to confirm each.",
             "Date handling (zero-padded month), month-name lookups, "
             "reporting period boundaries, cron schedule edge cases; "
             "reproduces with a simulated date."),
            ("practical",
             "You are asked to optimise a page that loads 5 MB of images "
             "for a slow network. Describe the concrete techniques you "
             "would apply and their expected impact.",
             "Image formats (WebP/AVIF), compression, responsive sizes, "
             "lazy loading, CDN, caching; realistic impact estimates."),
            ("design",
             "Design a simple in-memory key-value store with TTL support. "
             "Describe the data structures and how expired keys are "
             "removed.",
             "Hash map + priority queue (or lazy expiration), O(log n) "
             "expiry, correct TTL semantics, memory bounds."),
            ("practical",
             "Write a function that merges two sorted arrays into one "
             "sorted array. Explain why the naive concat-and-sort is "
             "worse.",
             "Two-pointer merge in O(n+m); explains the complexity "
             "difference and where the technique is used (merge sort)."),
            ("debugging",
             "Users see stale data after an update. The cache is involved. "
             "Walk through how you would trace whether the problem is "
             "cache invalidation, a wrong cache key, or a propagation "
             "delay.",
             "Isolates each layer with direct checks, reproduces with fresh "
             "cache, reviews invalidation triggers and key composition."),
            ("practical",
             "Write a small REST endpoint (pseudo-code) that accepts a "
             "file upload, validates its type and size, stores it safely, "
             "and returns a URL. Note the security checks.",
             "MIME/extension validation, size limit, safe filename "
             "(random), virus scanning consideration, access control on "
             "the URL, no path traversal."),
            ("design",
             "Design a rate limiter for a public API. Describe the "
             "algorithm, storage, and how you return feedback to clients.",
             "Token bucket or sliding window; Redis or in-memory; "
             "429 with Retry-After; per-key limits; distributed "
             "considerations."),
            ("practical",
             "Given a binary tree, write a function to find its maximum "
             "depth. Explain the recursion and its complexity.",
             "Correct recursion or BFS; O(n) time; handles empty tree; "
             "explains stack depth risk on deep trees."),
            ("debugging",
             "A report generator runs out of memory on large datasets. "
             "Describe how you would diagnose whether the problem is the "
             "data load, the transformation, or the output step.",
             "Profiles each phase, streams instead of loading all rows, "
             "chunking, memory profiling, fixes the actual bottleneck."),
            ("practical",
             "Write a function that detects duplicate records in a "
             "dataset where duplicates are defined by a subset of fields. "
             "Show how you would handle large datasets.",
             "Hashing on the key subset, streaming with a set, "
             "explains memory trade-offs, handles data types safely."),
            ("design",
             "Design a notification system that sends email, SMS and "
             "push. Describe the components, delivery guarantees, and "
             "how you handle failures.",
             "Queue-based, provider abstraction, retry with backoff, "
             "dead-letter queue, dedupe, user preferences, template "
             "rendering."),
            ("practical",
             "Write a function that converts a number to its words form "
             "(e.g. 123 -> 'one hundred twenty-three'). Note the tricky "
             "cases.",
             "Handles teens, hundreds, thousands; correct hyphenation; "
             "edge cases at 0, 100, 1000, 1,000,000."),
            ("debugging",
             "You are given this code: 'total = sum(items) / len(items)'. "
             "Users report a crash. Identify the failure mode and write "
             "the corrected version with a guard.",
             "Division by zero on empty list; guards and returns "
             "sensible default; explains the fix."),
        ],
    },

    # ------------------------------------------------------------------ 2
    "UI/UX & Product Design": {
        "category": [
            ("written_explanation",
             "Explain the difference between usability and accessibility. "
             "Give an example where improving one also improves the other.",
             "Usability = ease of use for target users; accessibility = "
             "usable by people with disabilities; example like clear "
             "contrast helping everyone in sunlight."),
            ("scenario",
             "User testing reveals that 60% of users fail to find a "
             "critical feature on the first try. How do you approach "
             "redesigning it?",
             "Investigates why (labelling, placement, mental model), "
             "iterates with prototypes, re-tests, measures improvement "
             "with the same metric."),
            ("design",
             "Design a mobile checkout flow that minimises abandoned "
             "carts. Walk through the screens and the decisions behind "
             "each.",
             "Guest option, progress indication, minimal fields, payment "
             "autofill, error handling inline, reassurance (security, "
             "returns), confirmation."),
            ("written_explanation",
             "Explain the concept of a design system and its benefits for "
             "a team of multiple designers and developers.",
             "Consistent components, tokens, documentation; faster "
             "iteration, brand consistency, accessibility baked in, "
             "reduced handoff friction."),
            ("scenario",
             "A stakeholder insists on a design you believe is bad for "
             "users. How do you handle the disagreement using evidence?",
             "Respects their goal, presents user research/data, offers an "
             "A/B test, finds compromise, documents the decision."),
            ("short_answer",
             "What are the four principles of visual hierarchy, and how "
             "would you apply them to a dashboard?",
             "Size, colour, contrast, spacing/position; applies to "
             "prioritising the key metric on a dashboard."),
            ("written_explanation",
             "Explain the difference between qualitative and quantitative "
             "user research. When is each most valuable?",
             "Qualitative (interviews, usability tests) for why; "
             "quantitative (analytics, surveys, A/B) for what and how "
             "many; complementary."),
            ("scenario",
             "You have two weeks to redesign a page used by 100,000 "
             "people. You cannot run a full research cycle. What is your "
             "process?",
             "Heuristic review, analytics review, quick guerrilla tests, "
             "small scope, risk-managed rollout with metrics, plan "
             "follow-up research."),
            ("design",
             "Design an onboarding flow for a complex B2B product. How do "
             "you keep it short while teaching what matters?",
             "Progressive disclosure, task-based onboarding, skip options, "
             "contextual tooltips, early win, not an exhaustive tour."),
            ("written_explanation",
             "Explain what a design 'pattern' is in UX (e.g. accordions, "
             "breadcrumbs) and when following a familiar pattern beats "
             "inventing something new.",
             "Patterns leverage learned behaviour; use familiar patterns "
             "unless user research shows a problem they solve."),
            ("scenario",
             "A visually beautiful design fails usability testing. How do "
             "you reconcile aesthetics with function?",
             "Finds the specific conflicts, adjusts without destroying "
             "brand, uses hierarchy and spacing rather than ornament, "
             "tests again."),
            ("short_answer",
             "What is the difference between wireframes, mockups and "
             "prototypes?",
             "Wireframes = structure/skeleton; mockups = visual design; "
             "prototypes = interactive flow; each serves a different "
             "stage."),
            ("written_explanation",
             "Explain how you would measure the success of a UX redesign "
             "after launch.",
             "Baseline vs after: task success, time on task, error rate, "
             "conversion, support tickets, retention; ties to business "
             "goals."),
            ("design",
             "Design a form for onboarding new employees that collects "
             "complex data without overwhelming them.",
             "Chunking into sections, smart defaults, inline validation, "
             "progressive questions, save-draft, clear labels and help "
             "text."),
            ("scenario",
             "Two user groups have conflicting needs for the same screen. "
             "How do you design for both?",
             "Understands each group's tasks, finds common structure, "
             "uses personalisation/roles, tests both, escalates true "
             "conflicts to product decisions."),
            ("written_explanation",
             "Explain the importance of typography in interface design, "
             "including hierarchy and readability.",
             "Type hierarchy guides attention; readability (size, line "
             "height, contrast) affects comprehension; accessibility of "
             "type."),
            ("scenario",
             "Your company wants to copy a competitor's interface exactly. "
             "How do you respond?",
             "Explains legal/ethical risk, analyses what works and what "
             "doesn't, proposes differentiated design meeting the same "
             "user needs."),
            ("design",
             "Design a settings page for a privacy-focused app. What "
             "decisions make privacy controls easy and trustworthy?",
             "Plain-language labels, clear defaults, granular but "
             "comprehensible controls, explanations of consequences, "
             "easy reversal."),
            ("short_answer",
             "What is the difference between a modal and a non-modal "
             "dialog, and when is each appropriate?",
             "Modal blocks the page (confirmations, mandatory choices); "
             "non-modal floats (quick edits, previews); avoid modal overuse."),
            ("written_explanation",
             "Explain the double-diamond design process and which stage "
             "you find most challenging and why.",
             "Discover, define, develop, deliver; divergent and convergent "
             "phases; honest reflection on a stage."),
        ],
        "position": [
            ("written_explanation",
             "As a product designer, explain how you move from a vague "
             "problem statement to a testable prototype.",
             "Frames the problem, research, define requirements, sketch, "
             "prototype at right fidelity, test with users, iterate."),
            ("scenario",
             "A developer tells you a design is impossible to implement in "
             "the time available. How do you collaborate on a solution?",
             "Understands the technical constraint, prioritises design "
             "intent, explores alternatives together, adjusts scope, "
             "documents trade-offs."),
            ("short_answer",
             "What is an accessibility audit and what are the three most "
             "common issues you would look for?",
             "Audit against WCAG; common issues: low contrast, missing "
             "alt text/labels, keyboard navigation failures."),
            ("design",
             "Design a search experience for a large e-commerce site. "
             "Describe the search box behaviour, results page, filters "
             "and empty states.",
             "Instant suggestions, forgiving typo handling, filterable "
             "results, clear empty/error states, relevant sorting, mobile "
             "behaviour."),
            ("written_explanation",
             "Explain how you use user personas in your work and their "
             "limitations.",
             "Personas summarise research and guide decisions; "
             "limitations: stereotypes if not research-based, never a "
             "substitute for testing."),
            ("scenario",
             "You receive feedback from a usability test that contradicts "
             "the design direction you argued for. What do you do?",
             "Takes the evidence seriously, separates ego from work, "
             "revisits assumptions, iterates and re-tests."),
            ("short_answer",
             "What is the difference between UX writing and copywriting, "
             "and why does microcopy matter?",
             "UX writing guides users through the interface (buttons, "
             "errors, empty states); microcopy reduces friction and "
             "errors."),
            ("design",
             "Design a notification preference centre. How do you balance "
             "business needs with user control?",
             "Clear categories, sensible defaults, bulk actions, easy "
             "opt-out, explains value of each notification, honours "
             "choices."),
            ("written_explanation",
             "Explain how you hand off designs to developers so they are "
             "implemented accurately.",
             "Specs, tokens, component library, annotations for "
             "behaviour/state, responsive rules, availability for "
             "questions, QA of implementation."),
            ("scenario",
             "A start-up needs a complete design for a product in one "
             "week. How do you scope and deliver something useful?",
             "Focuses on core journey, reuses existing patterns, "
             "communicates scope honestly, delivers a working prototype "
             "and iterates later."),
            ("short_answer",
             "What is the difference between a persona, a journey map and "
             "a service blueprint?",
             "Persona = who; journey map = experience over time; service "
             "blueprint = frontstage/backstage operations supporting the "
             "experience."),
            ("design",
             "Design a tablet experience for a doctor to review patient "
             "records. What design decisions support accuracy and speed?",
             "Clear hierarchy, minimal taps to key info, legible "
             "typography, safe error handling, offline considerations, "
             "privacy (screen lock, minimal data)."),
            ("written_explanation",
             "Explain the role of motion and animation in UI design, and "
             "the dangers of overusing it.",
             "Motion guides attention, communicates state, eases "
             "transitions; overuse causes distraction, motion sickness, "
             "performance issues; respect reduced-motion settings."),
            ("scenario",
             "A client rejects your design because it 'doesn't pop'. "
             "How do you respond?",
             "Clarifies the real goal, shows how the design serves "
             "objectives, offers a controlled visual enhancement, "
             "protects usability."),
            ("short_answer",
             "What are micro-interactions and give three examples of "
             "effective ones?",
             "Small feedback moments; e.g. button press state, like "
             "animation, pull-to-refresh; they communicate results and "
             "delight."),
            ("design",
             "Design the empty state of a project management app for a "
             "new user. What makes it effective at onboarding?",
             "Explains value, offers a clear first action, template or "
             "sample, friendly tone, no dead ends."),
            ("written_explanation",
             "Explain how dark mode changes design decisions around "
             "colour, contrast and elevation.",
             "Reduced glare/contrast ratios, elevation via lighter "
             "surfaces, careful saturation, test both themes for "
             "accessibility."),
            ("scenario",
             "You discover a usability problem late in development, one "
             "week before launch. What is your judgement process?",
             "Assesses severity and impact, proposes minimal safe fix or "
             "launch-and-patch plan, communicates risk clearly, tracks "
             "the follow-up."),
            ("short_answer",
             "What is the difference between a style guide and a design "
             "system, and why does an organisation need both?",
             "Style guide = visual rules; design system = components + "
             "patterns + guidance working together; guides consistency "
             "and speed."),
            ("design",
             "Design an error-handling strategy for a payment form. "
             "Show the error states and the copy.",
             "Inline validation, specific actionable messages, preserves "
             "input, explains the fix, no blame, graceful on "
             "server errors."),
        ],
        "practical": [
            ("practical",
             "Sketch (describe in words) three alternative layouts for a "
             "product landing page and explain which you would test first "
             "and why.",
             "Three distinct, justified layouts; picks based on goal and "
             "risk; explains what metric the test measures."),
            ("design",
             "Design a responsive grid for a news website that works on "
             "mobile, tablet and desktop. Describe breakpoints and "
             "behaviour.",
             "Mobile-first thinking, sensible breakpoints, reflow rules, "
             "touch targets on mobile, performance considerations."),
            ("practical",
             "Conduct a heuristic evaluation of a checkout page described "
             "to you and list the top five usability problems with "
             "severity ratings.",
             "Applies Nielsen heuristics (visibility, match, error "
             "prevention...), prioritised by severity, actionable "
             "recommendations."),
            ("design",
             "Design a progress indicator for a 5-step application form "
             "including handling of the back button and validation "
             "failures.",
             "Clear step position, save on navigation, validation on "
             "continue, back preserves data, prevents losing work."),
            ("practical",
             "Write the microcopy (error message, empty state, loading "
             "state) for a password reset flow. Explain your tone "
             "choices.",
             "Clear, reassuring, actionable copy; explains tone aligned "
             "with brand and user anxiety level."),
            ("design",
             "Design a mobile navigation for an app with 15 sections. "
             "Justify your choice of pattern (tab bar, hamburger, "
             "bottom sheet, etc.).",
             "Rational choice based on frequency of access and depth; "
             "keeps core actions reachable; avoids burying critical "
             "features."),
            ("practical",
             "Given user research quotes, write a prioritised list of "
             "design changes for a dashboard. Explain your ranking.",
             "Prioritises by impact vs effort, groups related issues, "
             "ties each to the research quote."),
            ("design",
             "Design a card-based feed for a social app including "
             "states for loading, empty, and error. Describe each "
             "state.",
             "Skeleton loaders, meaningful empty state, retry-friendly "
             "error, content hierarchy in cards."),
            ("practical",
             "Create an accessibility checklist you would run on a "
             "completed screen before sign-off.",
             "Covers contrast, keyboard, focus, screen reader labels, "
             "touch targets, reduced motion, forms; realistic and "
             "specific."),
            ("design",
             "Design a first-run experience for a budgeting app that "
             "asks for sensitive financial data. How do you build "
             "trust?",
             "Clear value proposition, privacy messaging, progressive "
             "permissioning, demo mode option, transparent data "
             "handling."),
            ("practical",
             "You have raw interview notes from five users. Describe how "
             "you would turn them into insights and design "
             "requirements.",
             "Affinity mapping, pattern identification, separating "
             "quotes from interpretations, deriving requirements, "
             "validating with stakeholders."),
            ("design",
             "Design a two-factor authentication setup flow. Walk "
             "through the screens and the failure states.",
             "Clear setup steps, backup codes, device handling, "
             "recovery path, failure states with guidance."),
            ("practical",
             "A/B test two versions of a pricing page described to you. "
             "Define the hypothesis, metric, and how you would judge "
             "the result.",
             "Single clear hypothesis, primary metric, sample size "
             "awareness, statistical significance, decision rule."),
            ("design",
             "Design a search filter bar for a job-listing site with "
             "many filter dimensions. How do you keep it usable?",
             "Progressive disclosure, applied-filter chips, clear "
             "results count, mobile behaviour, easy reset."),
            ("practical",
             "Write user stories for a 'save for later' feature in a "
             "shopping app, including acceptance criteria.",
             "Well-formed stories, clear acceptance criteria, edge "
             "cases (guest users, saved items unavailable)."),
            ("design",
             "Design the confirmation and success screens for a hotel "
             "booking flow. What information and next steps are "
             "essential?",
             "Booking reference, key details summary, cancellation "
             "policy, calendar/reminder option, clear next steps, "
             "receipt."),
            ("practical",
             "Given a low-fidelity wireframe described to you, explain "
             "how you would turn it into a high-fidelity design and "
             "validate it before development.",
             "Adds visual design tokens, fills real content, builds "
             "interactive prototype, tests with users, iterates, "
             "then handoff."),
            ("design",
             "Design a settings screen with 30+ options for a "
             "developer tool. How do you organise them?",
             "Grouping by theme, search, sensible defaults, "
             "progressive disclosure of advanced options, save "
             "behaviour."),
            ("practical",
             "Describe how you would test a design decision with five "
             "users in two days using tools you know.",
             "Practical plan: recruit, scripted tasks, moderated or "
             "unmoderated, capture, analyse, act; realistic within "
             "constraints."),
            ("design",
             "Design a 'no results' page for a search that also "
             "suggests alternatives. Show the content strategy.",
             "Clear message, spelling suggestions, filters "
             "adjustment, related searches, popular items, easy "
             "retry."),
        ],
    },

    # ------------------------------------------------------------------ 3
    "Graphic Design & Digital Media": {
        "category": [
            ("written_explanation",
             "Explain the difference between vector and raster graphics, "
             "and when you would use each.",
             "Vector = resolution-independent paths; raster = pixels; "
             "logos/type in vector, photos in raster; correct use cases."),
            ("scenario",
             "A client wants a logo redesign but keeps asking for changes "
             "that make it worse. How do you manage the relationship and "
             "the project?",
             "Sets clear revision scope, presents rationale with each "
             "iteration, educates the client, documents decisions, "
             "manages scope creep professionally."),
            ("short_answer",
             "Explain the basics of colour theory: what are complementary "
             "and analogous colours, and how would you use them in a "
             "brand palette?",
             "Complementary = opposite hues (contrast); analogous = "
             "adjacent (harmony); applies a primary/secondary/accent "
             "structure."),
            ("written_explanation",
             "Explain what 'negative space' is and give an example of a "
             "famous design or logo that uses it well.",
             "Correct concept (space around/in elements); example like "
             "FedEx arrow; explains its effect."),
            ("design",
             "Design a poster for a technology conference. Describe your "
             "layout, hierarchy and colour choices.",
             "Clear hierarchy (title, date, speakers), readable at "
             "distance, coherent palette, purposeful composition."),
            ("scenario",
             "A marketing team wants to use a font you found is not "
             "licensed for commercial use. How do you respond?",
             "Explains legal risk, proposes licensed alternative with "
             "similar feel, educates on font licensing."),
            ("written_explanation",
             "Explain the rule of thirds and how it applies to "
             "photography and layout design.",
             "Grid dividing into 9; placing key elements on "
             "intersections; purposeful composition not decoration."),
            ("short_answer",
             "What is the difference between RGB and CMYK colour modes, "
             "and why does it matter for print vs screen?",
             "RGB additive for screens; CMYK subtractive for print; "
             "correct workflow to avoid colour mismatch."),
            ("design",
             "Design a social media campaign visual set (three posts) "
             "for a product launch. Describe the system that keeps them "
             "consistent.",
             "Consistent grid, typography, palette, logo use; each post "
             "suits its platform; clear message hierarchy."),
            ("written_explanation",
             "Explain what typography hierarchy is and how a designer "
             "creates it using size, weight and spacing.",
             "Guides reading order; scale, weight contrast, spacing; "
             "limited type families."),
            ("scenario",
             "A stakeholder asks you to 'make it pop' without specifics. "
             "How do you clarify the real requirement?",
             "Asks goal-oriented questions, shows concrete options, "
             "uses reference examples, aligns on measurable intent."),
            ("short_answer",
             "What is the difference between kerning, tracking and "
             "leading?",
             "Kerning = space between specific pairs; tracking = uniform "
             "spacing across text; leading = line spacing."),
            ("written_explanation",
             "Explain how you would maintain a consistent brand identity "
             "across print, web and video.",
             "Brand guidelines, design tokens, templates, quality "
             "checklists, version-controlled assets."),
            ("design",
             "Design an infographic that explains a complex data story. "
             "Describe the structure and how you ensure accuracy.",
             "Clear narrative flow, appropriate chart types, accurate "
             "data with sources, hierarchy and whitespace, no "
             "misleading scales."),
            ("scenario",
             "You are asked to reuse a photo you suspect is copyrighted "
             "without permission. How do you handle it?",
             "Refuses the risky use, sources licensed/CC images, "
             "educates on copyright, offers alternatives."),
            ("written_explanation",
             "Explain the concept of 'visual weight' and how you balance "
             "a composition.",
             "Elements attract attention by size, colour, contrast; "
             "balance creates stability; asymmetry as valid choice."),
            ("design",
             "Design an email newsletter header and hero for a brand. "
             "Describe the layout and how it adapts to mobile.",
             "Brand recognition, clear hierarchy, mobile-first "
             "stacking, sensible image/text ratio, clear CTA."),
            ("short_answer",
             "What is the difference between a serif and a sans-serif "
             "font, and when would you choose each?",
             "Serifs have strokes at letter ends (formal/body print); "
             "sans-serifs clean (digital/UI); context-dependent choice."),
            ("written_explanation",
             "Explain how you handle constructive criticism of your "
             "design work, with an example.",
             "Separates feedback from ego, asks clarifying questions, "
             "evaluates against goals, iterates, documents rationale."),
            ("design",
             "Design a brand identity package outline for a new "
             "company: what deliverables would you produce?",
             "Logo suite, colour palette, typography, brand guidelines, "
             "stationery/templates, usage rules, file formats."),
        ],
        "position": [
            ("written_explanation",
             "As a graphic designer, explain your process from brief to "
             "final deliverable for a magazine ad.",
             "Brief analysis, research, concepts, roughs, refine with "
             "feedback, final production files, print-ready specs."),
            ("scenario",
             "A client approves a design, then requests a complete "
             "direction change after the deadline. How do you handle "
             "scope and fees?",
             "Clarifies scope, discusses additional cost/timeline "
             "honestly, keeps relationship professional, documents the "
             "change."),
            ("short_answer",
             "What are the common file formats for print (PDF, EPS, "
             "TIFF) and web (SVG, PNG, WebP) and when is each used?",
             "Correct format-purpose mapping: PDF for final print, "
             "EPS vector, TIFF high-res; SVG scalable web, PNG "
             "transparency, WebP compression."),
            ("design",
             "Design a billboard for a fast-moving consumer brand. "
             "What constraints shape your design?",
             "Readability at distance and speed, minimal text, strong "
             "single idea, correct bleed/safe area, legible type."),
            ("written_explanation",
             "Explain how you prepare files for a print vendor, "
             "including bleed, crop marks, colour profiles and "
             "resolution.",
             "Bleed/crop marks, CMYK or correct profile, 300dpi, "
             "outlined text or embedded fonts, correct trim."),
            ("scenario",
             "Your brilliant concept fails in testing or with the "
             "target audience. How do you react and what do you do?",
             "Does not defend blindly; analyses why, iterates, tests "
             "again, learns from failure."),
            ("short_answer",
             "What is the difference between a raster image at 72 DPI "
             "and 300 DPI, and what does DPI actually mean?",
             "DPI = dots per inch output resolution; 72 insufficient "
             "for print; 300 typical for print; not same as pixel "
             "dimensions."),
            ("design",
             "Design a book cover for a business title. Describe your "
             "concept, typography and how it stands out on a shelf.",
             "Concept aligned with content, strong typography, "
             "thumbnail readability, appropriate genre conventions."),
            ("written_explanation",
             "Explain how you would design for an audience with visual "
             "impairments, including accessible colour and type.",
             "Contrast ratios (WCAG), legible type sizes, not relying "
             "on colour alone, alt text, testing."),
            ("scenario",
             "You have three projects due the same day and two are "
             "behind. How do you communicate and prioritise?",
             "Informs stakeholders early, reprioritises with them, "
             "protects quality on deliverables, negotiates timing."),
            ("short_answer",
             "What is the difference between a mood board and a style "
             "tile, and when do you use each?",
             "Mood board = inspiration/feel early; style tile = "
             "concrete palette/type/buttons for a specific design "
             "direction."),
            ("design",
             "Design packaging for a premium product. Describe the "
             "materials, structure and typography choices.",
             "Material perception, structural practicality, "
             "hierarchy (brand, product, claims), shelf impact, "
             "sustainability consideration."),
            ("written_explanation",
             "Explain how you handle a project with no brand guidelines "
             "where you must also establish the visual direction.",
             "Research the market and audience, propose a direction, "
             "get buy-in, document the emerging system."),
            ("scenario",
             "A developer says your design needs to be 'sliced' or "
             "adapted for a website and complains it is not web-ready. "
             "How do you collaborate?",
             "Understands technical constraints, adjusts for web "
             "(performance, responsive), agrees on export format, "
             "delivers assets properly."),
            ("short_answer",
             "What is the difference between a logo, a logotype and an "
             "icon, and why does an identity need clarity here?",
             "Logo = mark; logotype = text-based; icon = simplified "
             "symbol; each has usage rules and legibility needs."),
            ("design",
             "Design a set of icons for a mobile app's tab bar. "
             "Describe the style system and states.",
             "Consistent stroke/weight/style, grid alignment, "
             "recognisable shapes, active/inactive states, "
             "accessibility sizes."),
            ("written_explanation",
             "Explain the importance of a grid in layout design and "
             "when breaking the grid is justified.",
             "Grids bring order and consistency; breaking creates "
             "emphasis - deliberate and rare."),
            ("scenario",
             "You see a design by a colleague that you believe has a "
             "legibility problem. How do you give feedback?",
             "Raises it constructively, focuses on user impact with "
             "specifics, offers to help, respects ownership."),
            ("short_answer",
             "What is the difference between a poster and a flyer in "
             "design terms, and how does that change the design?",
             "Poster = viewed at distance/passive; flyer = held/read "
             "closely; affects type size, information density, "
             "format."),
            ("design",
             "Design an annual report cover and internal opening "
             "spread. Describe hierarchy and data presentation.",
             "Brand-forward cover, clear section navigation, "
             "readable data (charts with purpose), elegant "
             "whitespace, print-ready."),
        ],
        "practical": [
            ("practical",
             "You are given a poorly scanned logo to reuse. Describe the "
             "steps to restore it to a usable vector file.",
             "Assessment, image trace or redraw, clean paths, colour "
             "correction, deliver correct format."),
            ("design",
             "Design a 12-panel storyboard for a 30-second product "
             "video. Describe the key frames and the narrative arc.",
             "Clear beginning/middle/end, hook, product payoff, "
             "visual variety, timing notes."),
            ("practical",
             "Write a brief for a photographer for a brand shoot. "
             "Include mood, lighting, subjects and deliverables.",
             "Clear creative direction, technical specs, usage "
             "rights, logistics, approval process."),
            ("design",
             "Create a colour palette (name the hex values and their "
             "roles) for a trustworthy fintech brand.",
             "Palette with primary/secondary/accent/neutrals; "
             "contrast check; psychology aligned with trust."),
            ("practical",
             "Describe how you would prepare a 10-page brochure for "
             "print: file setup, proofing and vendor checks.",
             "Correct setup, proofing steps (colour, typos, "
             "layout), preflight, vendor communication."),
            ("design",
             "Design a responsive hero banner that works as a website "
             "header and a social media square. Describe adaptations.",
             "Core message preserved, composition adapts, "
             "safe areas respected, text legible in both crops."),
            ("practical",
             "A client provides a 100-word mission statement for a "
             "one-page flyer. Edit and structure it for readability.",
             "Concise hierarchy, scannable layout, headline/body "
             "split, preserves meaning, brand tone."),
            ("design",
             "Design an animated loading screen for an app in words, "
             "describing the motion and how it fits the brand.",
             "On-brand motion, appropriate duration, communicates "
             "state, respects reduced-motion preferences."),
            ("practical",
             "You must resize a campaign across 10 formats (billboard "
             "to mobile banner). Describe your workflow to keep "
             "quality and consistency.",
             "Design at largest size, master components, scale "
             "systematically, check legibility per format, "
             "flexible vs fixed elements."),
            ("design",
             "Design a menu for a restaurant that must be appetising, "
             "clear and quick to read. Describe layout and "
             "typography.",
             "Readable at low light, clear sections and prices, "
             "photography strategy, hierarchy by signature items."),
            ("practical",
             "Given a brand with blue primary, design a cohesive set "
             "of six social media post templates for different "
             "content types (quote, product, event, stat, etc.).",
             "Consistent system, varied layouts, on-brand, each "
             "template suited to its content type."),
            ("design",
             "Design an exhibition stand graphic for a tech booth. "
             "Describe what viewers see from 10 metres versus 1 "
             "metre.",
             "Big idea at distance, detail at close range, brand "
             "consistency, clear messaging, production "
             "practicalities."),
            ("practical",
             "Write the visual style guide section for a logo: clear "
             "space, minimum size, colour variants and misuse "
             "examples.",
             "Specific rules (measurements), acceptable variants, "
             "do/don't examples, file guidance."),
            ("design",
             "Design a magazine double-page spread for a feature "
             "article. Describe grid, pull quotes and image "
             "treatment.",
             "Strong grid, entry points, pull-quote treatment, "
             "image/type balance, page numbers and folio."),
            ("practical",
             "Describe your process for colour-correcting photos so "
             "they match across a campaign.",
             "Reference-based correction, consistent white "
             "balance, skin tones, export profile, quality "
             "control."),
            ("design",
             "Design a gift card or voucher with security features "
             "against forgery. Describe the visual and technical "
             "elements.",
             "Serial numbers, microprint or guilloche, tamper "
             "detection, brand consistency, usability of the "
             "redemption code."),
            ("practical",
             "A last-minute event needs a poster in two hours. "
             "Describe your efficient workflow and what you would "
             "prioritise.",
             "Template reuse, correct specs up front, hierarchy "
             "priority, quick internal check, delivery formats."),
            ("design",
             "Design an app icon that reads at 24 pixels and 512 "
             "pixels. Describe the concept and simplification "
             "process.",
             "One clear idea, bold shape, minimal detail, grid "
             "safe zone, platform guidelines, test at small "
             "sizes."),
            ("practical",
             "Describe how you would review another designer's file "
             "for production issues before it goes to print.",
             "Preflight checklist: fonts embedded, images linked "
             "and high-res, bleed, colour profile, overset text, "
             "proofing."),
            ("design",
             "Design a 'year in review' social graphic from a data "
             "set you invent. Describe the visualisation and "
             "storytelling.",
             "Honest, clear data visuals, narrative arc, brand "
             "consistency, mobile-first layout."),
        ],
    },

    # ------------------------------------------------------------------ 4
    "Game Development": {
        "category": [
            ("written_explanation",
             "Explain the difference between game design and game "
             "development, and how they depend on each other.",
             "Design = rules/experience/mechanics; development = "
             "implementation; a game needs both, and design must be "
             "feasible to develop."),
            ("scenario",
             "A game mechanic is fun in prototypes but causes "
             "exploits that ruin the economy in live play. How do you "
             "respond?",
             "Analyses the exploit, patches the mechanic, considers "
             "economy rebalancing, communicates with players, tests "
             "the fix."),
            ("design",
             "Design the core game loop of a casual mobile game. "
             "Describe the loop and what keeps players returning.",
             "Clear loop (action -> reward -> progression), short "
             "sessions, retention hooks (daily rewards, goals), "
             "monetisation that respects players."),
            ("written_explanation",
             "Explain the concept of 'juice' in game feel and give "
             "examples of how it is achieved.",
             "Screenshake, particles, sound, squash-and-stretch, "
             "coyote time, hit-stop; explains why feedback makes "
             "controls feel good."),
            ("scenario",
             "Your publisher pushes for a pay-to-win monetisation "
             "model you believe will drive players away. How do you "
             "respond?",
             "Presents data on player retention, proposes fairer "
             "models, protects core experience, documents the "
             "trade-off."),
            ("short_answer",
             "What is the difference between a game engine and a "
             "framework, and name common examples of each.",
             "Engine (Unity, Unreal, Godot) = integrated toolset; "
             "framework = library structure; correct usage and "
             "selection criteria."),
            ("written_explanation",
             "Explain the difference between a game's vertical slice "
             "and a prototype, and the purpose of each.",
             "Prototype tests one mechanic quickly; vertical slice "
             "demonstrates representative full experience for "
             "funding/pitch."),
            ("design",
             "Design a level for a puzzle game that teaches a new "
             "mechanic without text instructions. Describe the "
             "layout.",
             "Safe introduction, guided discovery, escalating "
             "complexity, no frustration spikes, optional "
             "challenge."),
            ("scenario",
             "Playtesting shows players are confused by your "
             "tutorial. What is your process for fixing it?",
             "Observes where they stall, redesigns tutorial "
             "(just-in-time, in-context), tests again, measures "
             "completion."),
            ("written_explanation",
             "Explain what 'game balance' means and how you would "
             "balance a character with an overpowered ability.",
             "Defines balance (fair, strategic choices); nerfs, "
             "counters, costs, counterplay; data-driven tuning."),
            ("short_answer",
             "What is the difference between a game state machine and "
             "an event-driven architecture in game code?",
             "State machine = explicit states/transitions; events = "
             "decoupled notifications; when each is appropriate."),
            ("design",
             "Design a boss fight that teaches the player a lesson "
             "about the game's core mechanics. Describe phases.",
             "Phases escalate the mechanic, telegraphs attacks, "
             "fair difficulty, teaches through gameplay."),
            ("written_explanation",
             "Explain how you would handle 'difficulty curve' design "
             "for players of different skill levels.",
             "Progressive difficulty, adaptive systems, difficulty "
             "options, failure that teaches, avoids unfair walls."),
            ("scenario",
             "Your game crashes on a specific older device during "
             "playtesting. How do you diagnose it?",
             "Reproduces with device specs, checks memory/GPU "
             "limits, reads crash logs, isolates the feature, "
             "optimises or falls back."),
            ("design",
             "Design a quest system for an open-world RPG. Describe "
             "the structure and how quests stay meaningful.",
             "Quest types, objectives, rewards, branching, "
             "integration with world state, avoids filler."),
            ("short_answer",
             "What is the difference between a 'game feel' and 'game "
             "mechanics'? Give an example of each.",
             "Mechanics = rules/actions; feel = the sensation of "
             "controlling them; example: jump mechanic vs jump "
             "weight/response."),
            ("written_explanation",
             "Explain what 'crunch' culture is in game development, "
             "why it is harmful, and how you would push back.",
             "Defines crunch; harms quality, health, retention; "
             "promotes planning, scope control, sustainable "
             "pacing."),
            ("design",
             "Design the first 5 minutes of a narrative game. "
             "Describe what the player experiences and why it "
             "hooks them.",
             "Hook, context without info-dump, a meaningful choice "
             "early, emotional or curiosity-driven pull."),
            ("scenario",
             "Two designers disagree on whether a mechanic should "
             "stay. As the person in the room, how do you help the "
             "team decide?",
             "Frames a testable question, sets criteria, runs a "
             "quick test, makes a data-informed call, moves on "
             "without grudges."),
            ("written_explanation",
             "Explain the importance of a 'design pillar' or design "
             "vision document for a game project.",
             "Defines what the game must be; guides every decision; "
             "prevents scope creep; aligns the team."),
        ],
        "position": [
            ("written_explanation",
             "As a game programmer, explain the typical game loop "
             "(update/render cycle) and why frame-rate independence "
             "matters.",
             "Update/draw with delta time; physics and logic "
             "independent of fps; explains jitter and fixed "
             "timesteps."),
            ("scenario",
             "As a game designer you are told a beloved feature must "
             "be cut for budget. How do you preserve its value?",
             "Prioritises the feature's core value, proposes "
             "simplified alternatives, communicates impact, "
             "protects player-facing quality."),
            ("short_answer",
             "What is the difference between a level designer and a "
             "world designer?",
             "Level = mission/space pacing and gameplay; world = "
             "overarching geography, lore and coherence; they "
             "overlap."),
            ("design",
             "Design a multiplayer matchmaking system. Describe how "
             "you balance queue times and fair matches.",
             "Skill-based matching, queue-time thresholds, "
             "latency consideration, party handling, "
             "player-abandonment handling."),
            ("written_explanation",
             "Explain how you would implement saving and loading in "
             "a game without breaking future updates.",
             "Versioned save data, schema migrations, safe "
             "write (atomic), corruption recovery, backwards "
             "compatibility."),
            ("scenario",
             "A game tester finds a bug where a player can fall "
             "through the world. Describe your triage and fix "
             "process.",
             "Reproduces, captures logs, checks collision and "
             "physics step size, fixes robustly, adds regression "
             "test, verifies edge cases."),
            ("short_answer",
             "What is the difference between a hitbox and hurtbox, "
             "and why does their placement matter?",
             "Hitbox = attack range; hurtbox = damageable area; "
             "placement creates fairness and game feel."),
            ("design",
             "Design an inventory system with weight limits and "
             "sorting. Describe the data model and UI.",
             "Item data model, capacity rules, sorting/filtering, "
             "quick-equip, clarity of item information."),
            ("written_explanation",
             "Explain the difference between deterministic and "
             "non-deterministic simulation and when multiplayer "
             "needs each.",
             "Deterministic = same input same output (lockstep); "
             "non-deterministic = client-authoritative with "
             "reconciliation; trade-offs in cheating and "
             "consistency."),
            ("scenario",
             "Your animation system causes characters to clip "
             "through walls. How do you investigate and fix?",
             "Checks animation root motion vs collision, blends, "
             "collision proxies, camera handling; fixes with "
             "constraints or state changes."),
            ("short_answer",
             "What is the difference between a game designer and a "
             "systems designer?",
             "Game designer = overall experience; systems "
             "designer = rules/economy/interactions of specific "
             "systems."),
            ("design",
             "Design the progression and upgrade system for an RPG. "
             "Describe how it stays interesting long-term.",
             "Meaningful choices, diminishing returns, "
             "build diversity, content gates, respec options."),
            ("written_explanation",
             "Explain how you debug performance issues in a game, "
             "from symptom to solution.",
             "Profiling (CPU/GPU/memory), identifying hot paths, "
             "draw calls, asset sizes, then targeted "
             "optimisation with measurement."),
            ("scenario",
             "Players exploit a trading system to duplicate items. "
             "How do you respond as a developer?",
             "Investigates the root cause, hotfixes, deals with "
             "existing duplicates (rollback/removal), adds "
             "server-side validation, communicates."),
            ("short_answer",
             "What is the difference between a shader and a "
             "material, and how do they relate?",
             "Shader = program controlling rendering; material = "
             "configured instance of shader with parameters."),
            ("design",
             "Design an audio system for a horror game including "
             "dynamic audio behaviour. Describe the design.",
             "Dynamic music layers, spatial audio, tension "
             "cues, audio that responds to game state, "
             "accessibility (subtitle/sound options)."),
            ("written_explanation",
             "Explain how you would make a game accessible to "
             "players with disabilities.",
             "Options: remapping, colour-blind modes, "
             "subtitles, difficulty scaling, motor "
             "accessibility, UI scaling."),
            ("scenario",
             "Your game's economy is broken because a drop rate "
             "was tuned wrong. Describe the fix process and how "
             "you avoid the same mistake.",
             "Data review, hotfix, player communication, "
             "economy simulation, automated tuning checks."),
            ("short_answer",
             "What is the difference between a game jam prototype "
             "and a production-ready feature?",
             "Prototype = proof of concept, throwaway; "
             "production = robust, performant, tested, "
             "maintainable."),
            ("design",
             "Design a tutorial for a real-time strategy game that "
             "is engaging rather than a lecture.",
             "Learn-by-doing missions, contextual prompts, "
             "progressive complexity, skippable, rewards "
             "mastery."),
        ],
        "practical": [
            ("practical",
             "Design (in words) the movement system for a platformer "
             "character including jump, coyote time and variable jump "
             "height. Explain each choice.",
             "Responsive feel: acceleration, air control, coyote "
             "time, jump buffering, variable height; justifies each."),
            ("design",
             "Design a simple enemy AI that patrols, detects the "
             "player and reacts. Describe the state machine.",
             "States (patrol, investigate, chase, attack), "
             "transition conditions, line-of-sight checks, "
             "fairness."),
            ("practical",
             "Write pseudo-code for a damage calculation that "
             "supports resistances, critical hits and damage over "
             "time.",
             "Layered modifiers applied correctly, deterministic, "
             "testable, handles edge cases."),
            ("design",
             "Design a minimap system for a large open world. "
             "Describe rendering, markers and performance.",
             "Pre-rendered or runtime, level-of-detail, marker "
             "management, occlusion handling, performance "
             "budget."),
            ("practical",
             "Given a scenario where a player can get stuck in a "
             "geometry corner, describe the fix and the testing "
             "you would do.",
             "Collision resolution improvement, push-out logic, "
             "kill-zones, regression tests, level review."),
            ("design",
             "Design a quest-giver NPC interaction system. "
             "Describe dialogue flow, branching and state.",
             "Dialogue trees, quest states, branching, "
             "save/load integration, replayability."),
            ("practical",
             "Write pseudo-code for an object pool used to spawn "
             "bullets without allocations. Explain why it helps.",
             "Pre-allocated pool, acquire/release, avoids GC "
             "spikes, used for high-frequency objects."),
            ("design",
             "Design a checkpoints and respawn system. Describe "
             "what state is saved and how death is handled.",
             "Checkpoint frequency, state snapshot, death "
             "feedback, no frustration, fair retry."),
            ("practical",
             "A level loads slowly. Describe how you would "
             "profile and fix it.",
             "Streaming, asset optimisation, async loading, "
             "loading screens with value, profiling evidence."),
            ("design",
             "Design a leaderboard system for an online game. "
             "Describe storage, cheating prevention and "
             "display.",
             "Server-authoritative scores, rate limiting, "
             "anomaly detection, seasonal resets, "
             "cross-platform identity."),
            ("practical",
             "Write pseudo-code for a camera that follows a "
             "player with smooth interpolation and handles "
             "walls.",
             "Smooth follow, collision-aware camera, "
             "adjustable feel, avoid jitter."),
            ("design",
             "Design a save-game system for a roguelike where "
             "death is permanent. Describe when and how saves "
             "happen.",
             "Save on run start/exit, prevent save-scumming, "
             "corruption safety, run state integrity."),
            ("practical",
             "Describe how you would implement a combo system in "
             "a fighting game, including input buffering.",
             "Input queue, buffering windows, cancel rules, "
             "forgiving timing, visual feedback."),
            ("design",
             "Design a match chat and report system. Describe "
             "moderation and player safety.",
             "Filters, report flow, mute options, automated "
             "moderation, evidence retention, appeals."),
            ("practical",
             "Write pseudo-code to interpolate a character's "
             "rotation smoothly toward a target angle.",
             "Angle wrapping, lerp/slerp, frame-rate "
             "independence, handles 180-degree cases."),
            ("design",
             "Design a day/night cycle for an open world. "
             "Describe lighting, gameplay effects and "
             "performance.",
             "Directional light, sky transitions, gameplay "
             "tie-ins, baked vs dynamic lighting, "
             "performance strategy."),
            ("practical",
             "A physics object jitters at rest. Describe the "
             "probable causes and the fix.",
             "Sleep thresholds, contact tolerance, fixed "
             "timestep, solver iterations, friction tuning."),
            ("design",
             "Design a co-op multiplayer session system. "
             "Describe joining, syncing and leaving.",
             "Host migration or dedicated, state sync, "
             "late-join handling, save consistency."),
            ("practical",
             "Write pseudo-code for a simple steering behaviour "
             "that makes an NPC move toward a target while "
             "avoiding an obstacle.",
             "Seek + avoidance, vector maths, smooth "
             "turning, no oscillation."),
            ("design",
             "Design a 'new game plus' mode. Describe what "
             "carries over and how difficulty scales.",
             "Carry-over rules, scaling curve, rewards, "
             "narrative integration, replay value."),
        ],
    },
}
