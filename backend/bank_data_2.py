"""
Unique category / position / practical questions for the question banks.
"""

CATS = {
    # ------------------------------------------------------------------ 5
    "Database & Data Engineering": {
        "category": [
            ("written_explanation",
             "Explain the difference between a relational database and a "
             "NoSQL database. When would you choose each?",
             "Correct definition of relational (tables, joins, ACID) vs "
             "NoSQL (document/key-value/graph, flexible schema, scale); "
             "sensible selection criteria."),
            ("scenario",
             "A slow query that used to run in milliseconds now takes "
             "minutes. Describe your diagnosis steps.",
             "Check query plan, index usage, data growth, locking and "
             "concurrency, then targeted fix with re-measurement."),
            ("design",
             "Design a database schema for an e-commerce platform with "
             "products, customers, orders and payments. Show the main "
             "tables and key decisions.",
             "Sensible normalisation, order line items, payment "
             "integrity, appropriate constraints, indexing strategy, "
             "audit trail."),
            ("written_explanation",
             "Explain ACID properties and give a real example where "
             "each one matters.",
             "Atomicity, consistency, isolation, durability - each "
             "defined with a concrete scenario (e.g. funds transfer)."),
            ("scenario",
             "A developer wants to drop an index because inserts are "
             "slow. How do you evaluate the request?",
             "Measures read vs write trade-off, checks query patterns "
             "and EXPLAIN plans, proposes alternatives, documents the "
             "decision."),
            ("short_answer",
             "What is the difference between an inner join, a left join "
             "and a full outer join? Give a result example for each.",
             "Accurate semantics and a correct small example showing "
             "unmatched rows handling."),
            ("written_explanation",
             "Explain database normalisation up to third normal form "
             "with a simple example.",
             "1NF (atomic values), 2NF (no partial dependency), 3NF "
             "(no transitive dependency) - correct example and "
             "rationale."),
            ("design",
             "Design a data warehouse schema (star schema) for sales "
             "analytics. Show facts and dimensions.",
             "Fact table with measures and FKs, dimension tables, "
             "grain definition, slow-changing dimension awareness."),
            ("scenario",
             "A backup job fails intermittently at 2 AM. What are your "
             "first diagnostic steps?",
             "Check logs and exit codes, disk space, lock contention, "
             "job overlap, retention cleanup, then fix and monitor."),
            ("written_explanation",
             "Explain what database replication is, the difference "
             "between synchronous and asynchronous replication, and "
             "their trade-offs.",
             "Correct concepts; sync = consistency, higher latency; "
             "async = performance, possible data loss; use cases."),
            ("scenario",
             "Your database runs out of disk space during peak hours. "
             "What do you do immediately and long-term?",
             "Immediate: free space safely, pause non-critical jobs; "
             "long-term: monitoring, archiving, retention, capacity "
             "planning."),
            ("short_answer",
             "What is an index and why does it speed up reads? What are "
             "the costs of too many indexes?",
             "Index = sorted structure for lookup; trade-offs: write "
             "overhead, storage, maintenance."),
            ("written_explanation",
             "Explain the difference between OLTP and OLAP workloads, "
             "and how they influence schema design.",
             "OLTP = many small transactions (normalised); OLAP = "
             "analytical queries (denormalised/star); design follows "
             "workload."),
            ("design",
             "Design a migration strategy for moving a database from "
             "one server to another with minimal downtime.",
             "Pre-copy, sync phase, cutover plan, verification, "
             "rollback plan, communication window."),
            ("scenario",
             "Users report 'deadlock' errors in a banking application. "
             "Explain what a deadlock is and how you would find and "
             "fix it.",
             "Defines deadlock (two transactions waiting on each "
             "other); uses lock ordering, shorter transactions, "
             "retry logic, monitoring."),
            ("written_explanation",
             "Explain what a transaction isolation level is and the "
             "difference between READ COMMITTED and SERIALIZABLE.",
             "Defines isolation; read committed allows non-repeatable "
             "reads, serializable prevents them at cost of "
             "concurrency."),
            ("scenario",
             "A team stores all application logs in the same "
             "relational database as business data. What problems do "
             "you anticipate and what would you recommend?",
             "Identifies performance and bloat issues; recommends "
             "separate log store (ELK, time-series), retention policy."),
            ("short_answer",
             "What is the difference between a primary key and a "
             "unique constraint?",
             "Primary key identifies rows, one per table, not null; "
             "unique constraint allows nulls and can be multiple."),
            ("written_explanation",
             "Explain ETL vs ELT and when you would use each in a data "
             "pipeline.",
             "Transform before vs after loading; ETL for structured "
             "targets, ELT for warehouse/cloud scale; trade-offs."),
            ("design",
             "Design a system that stores time-series sensor data "
             "efficiently. Describe storage choices and query "
             "strategy.",
             "Time-series DB or partitioned tables, downsampling, "
             "retention, appropriate indexing, ingestion batching."),
        ],
        "position": [
            ("written_explanation",
             "As a database administrator, describe your process for "
             "applying a patch or upgrade to a production database "
             "with minimal risk.",
             "Backup, test on staging, change window, rollback plan, "
             "verification, post-change monitoring."),
            ("scenario",
             "As a database developer, you must add a column to a very "
             "large table without locking it for hours. How do you do "
             "it?",
             "Online DDL/ALGORITHM=INPLACE, shadow table or phased "
             "approach, maintenance window, testing."),
            ("short_answer",
             "What is a covering index and when would you create one?",
             "Index containing all columns needed by a query so no "
             "table lookup; for hot read paths."),
            ("design",
             "Design a connection pooling strategy for an application "
             "with variable load. Describe the parameters you would "
             "tune.",
             "Min/max pool size, timeout, idle timeout, "
             "validation; matches pool to workload."),
            ("written_explanation",
             "Explain how you would design a backup and recovery "
             "strategy for a database with an RPO of 5 minutes and "
             "RTO of 1 hour.",
             "RPO/RTO definitions; continuous binary log shipping or "
             "incremental backups, restore testing, documentation."),
            ("scenario",
             "A query that ran fine in staging is catastrophically slow "
             "in production. What differs and how do you find it?",
             "Data volume, statistics, parameter sniffing, hardware "
             "differences; reproduce with production-like data, "
             "compare plans."),
            ("short_answer",
             "What is the difference between sharding and partitioning, "
             "and when would you use each?",
             "Partitioning = within one server (management/performance); "
             "sharding = across servers (scale); use cases."),
            ("design",
             "Design the schema for a multi-tenant SaaS application. "
             "Describe how you isolate tenant data.",
             "Shared schema with tenant_id vs schema-per-tenant "
             "trade-offs; indexing, security, backup isolation."),
            ("written_explanation",
             "Explain how you ensure data integrity when data arrives "
             "from multiple source systems.",
             "Validation, transformation rules, primary key mapping, "
             "reconciliation, error queues, monitoring."),
            ("debugging",
             "A nightly data load creates duplicate records only on "
             "Mondays. How do you investigate?",
             "Checks idempotency of load, weekend scheduling overlap, "
             "source data differences; adds dedupe key and tests."),
            ("short_answer",
             "What is the difference between a clustered and a "
             "non-clustered index?",
             "Clustered = table data order; non-clustered = separate "
             "structure pointing to rows; one clustered per table."),
            ("scenario",
             "A developer accidentally ran a DELETE without a WHERE "
             "clause on a production table. What do you do?",
             "Stops further writes, restores from backup/point-in-time, "
             "verifies data, investigates access controls and "
             "safeguards."),
            ("design",
             "Design a data quality monitoring system. What checks "
             "would you run and how often?",
             "Freshness, completeness, uniqueness, range checks, "
             "schema drift; alerts and dashboards."),
            ("written_explanation",
             "Explain how you would handle a slowly growing table that "
             "is queried frequently.",
             "Partitioning by time, archiving, covering indexes, "
             "summaries/caching, review access patterns."),
            ("debugging",
             "A read replica is 30 minutes behind the primary. Describe "
             "your diagnosis.",
             "Check replica load, large transactions, network, "
             "replication lag monitoring, promotion readiness."),
            ("short_answer",
             "What is a foreign key and why is it important?",
             "Enforces referential integrity between tables; prevents "
             "orphan records."),
            ("scenario",
             "Your team needs to export data to a client weekly. How do "
             "you design a reliable and secure export?",
             "Automated job with audit, masking sensitive fields, "
             "encryption, delivery confirmation, retention."),
            ("design",
             "Design the database for a food delivery app including "
             "orders, riders and live tracking.",
             "Order lifecycle, rider assignment, location storage "
             "(point or time-series), notification triggers, "
             "indexing."),
            ("written_explanation",
             "Explain the CAP theorem and what it means for choosing "
             "between consistency and availability.",
             "Consistency/Availability/Partition tolerance - you can "
             "pick two; practical implications for distributed "
             "databases."),
            ("debugging",
             "A column was renamed in an upstream system and your "
             "load breaks. Describe your handling and prevention.",
             "Detects schema drift, alerts, mapping table, automated "
             "validation, communication with upstream."),
        ],
        "practical": [
            ("practical",
             "Write SQL to find employees who earn more than their "
             "manager from a single employees table with a manager_id "
             "column.",
             "Self-join with alias, correct comparison, handles "
             "nulls."),
            ("design",
             "Design a database for a library with books, members and "
             "loans. Show tables, constraints and one index decision.",
             "Sensible schema, loan date/return tracking, unique "
             "constraints, index on active loans."),
            ("practical",
             "Given a table with millions of rows, write SQL that "
             "efficiently returns the latest record per user.",
             "Window function (ROW_NUMBER) or correlated subquery; "
             "efficient plan with proper index."),
            ("debugging",
             "A query returns 1,000 rows in staging but 0 in "
             "production. List the likely causes and how you would "
             "confirm each.",
             "Data differences, case sensitivity/collation, "
             "timezone, environment config; confirms with queries."),
            ("practical",
             "Write a function (pseudo-code) that safely inserts a "
             "record with a unique constraint and retries on "
             "conflict.",
             "Handles duplicate gracefully, returns existing record, "
             "avoids raising user-facing errors."),
            ("design",
             "Design a caching layer in front of a database that "
             "stores frequently read product data. Describe cache "
             "keys, TTL and invalidation.",
             "Key design, TTL strategy, invalidation on write, "
             "stampede protection, monitoring."),
            ("practical",
             "Write SQL that paginates a large result set efficiently "
             "using keyset pagination instead of OFFSET.",
             "WHERE id > last_seen ORDER BY id LIMIT n; explains why "
             "it scales better."),
            ("debugging",
             "An import job succeeds but loads 5% fewer rows each "
             "week. How do you find the discrepancy?",
             "Reconciliation counts, row-level comparison, checksum, "
             "logging of skipped rows, source changes."),
            ("practical",
             "Write a query to detect orphaned records (rows in a "
             "child table with no parent).",
             "LEFT JOIN with IS NULL or NOT EXISTS; explains "
             "performance considerations."),
            ("design",
             "Design an event-driven data pipeline where a new order "
             "updates inventory, analytics and notifications.",
             "Event bus, consumers with own storage, exactly-once or "
             "idempotent processing, failure handling, ordering."),
            ("practical",
             "Write SQL that computes a running total of sales per "
             "month.",
             "Window function with ORDER BY and unbounded preceding "
             "rows."),
            ("debugging",
             "Your database CPU is at 100% but no user-facing slowness "
             "is reported. How do you find the cause?",
             "Active queries, expensive plans, maintenance jobs, "
             "replication; correlate with monitoring, then "
             "optimise."),
            ("practical",
             "Write a pseudo-code ETL step that cleans a name field "
             "with inconsistent capitalisation.",
             "Normalise case, trim whitespace, handle empty and "
             "null, apply deterministically."),
            ("design",
             "Design the tables and flows for a financial ledger that "
             "must never lose a transaction.",
             "Append-only ledger, transaction entries, reconciliation, "
             "idempotency, audit."),
            ("practical",
             "Given two tables, write SQL to find customers who made "
             "a purchase in the last 30 days but not in the previous "
             "30.",
             "Date filters with correct boundaries and JOINs or "
             "EXCEPT."),
            ("debugging",
             "A scheduled maintenance task that truncates old logs "
             "has not run in a month. Describe your diagnosis and "
             "prevention.",
             "Check job scheduler, permissions, disk locks, error "
             "alerts; add monitoring and manual trigger."),
            ("practical",
             "Write a query that ranks products by sales within each "
             "category.",
             "RANK/DENSE_RANK window partitioned by category."),
            ("design",
             "Design a system that stores user activity events for "
             "analytics while keeping the transactional database "
             "fast.",
             "Separate event store, streaming pipeline, batch "
             "aggregation, retention, decoupling from OLTP."),
            ("practical",
             "Write a pseudo-code function that performs a backup and "
             "verifies its integrity.",
             "Backup command, checksum verification, restore test, "
             "alerting on failure."),
            ("debugging",
             "Two applications write to the same table with "
             "conflicting schemas. Describe how you resolve the "
             "conflict.",
             "Identify owner, align schemas via migration, "
             "governance, access controls, monitoring."),
        ],
    },

    # ------------------------------------------------------------------ 6
    "Data Analytics & Business Intelligence": {
        "category": [
            ("written_explanation",
             "Explain the difference between descriptive, diagnostic, "
             "predictive and prescriptive analytics, with an example "
             "of each.",
             "Correct definitions: what happened, why, what will "
             "happen, what to do - with coherent examples."),
            ("scenario",
             "You present an analysis showing sales are declining, and "
             "a stakeholder disputes the data. How do you respond?",
             "Shows methodology and sources, checks data quality "
             "claims, invites verification, focuses on the finding "
             "not the ego."),
            ("design",
             "Design a KPI dashboard for an e-commerce business. What "
             "metrics would you show and why?",
             "Balanced set (revenue, conversion, traffic, retention, "
             "support), aligned to business goals, clear "
             "hierarchy."),
            ("written_explanation",
             "Explain the difference between correlation and causation, "
             "with an example of why it matters.",
             "Correct distinction; example like ice cream sales and "
             "drowning; explains confounders."),
            ("scenario",
             "Your report shows an anomaly in a key metric. Describe "
             "your investigation process.",
             "Verify data integrity, segment, compare periods, "
             "check external factors, form and test hypotheses."),
            ("short_answer",
             "What is the difference between a KPI, a metric and a "
             "dimension?",
             "KPI = metric tied to a goal; metric = measure; "
             "dimension = attribute for slicing."),
            ("written_explanation",
             "Explain the difference between a bar chart and a "
             "histogram and when you would use each.",
             "Bar = categories; histogram = distribution of "
             "continuous values; correct usage."),
            ("design",
             "Design a weekly business review report structure for "
             "an operations team. What sections would it have?",
             "Executive summary, key metrics, variances vs target, "
             "drivers, actions, appendix - actionable not just "
             "informative."),
            ("scenario",
             "A colleague asks you to change a number in a report to "
             "make the team look better. How do you respond?",
             "Refuses to falsify, explains integrity, offers to "
             "investigate the real driver, documents the request."),
            ("short_answer",
             "What is the difference between a pivot table and a "
             "lookup?",
             "Pivot = summarise/aggregate by dimensions; lookup = "
             "retrieve matching value from another table."),
            ("written_explanation",
             "Explain how you would define a 'churned customer' and "
             "why the definition matters for analysis.",
             "Definition must be measurable and business-aligned "
             "(e.g. 90 days inactivity); different definitions "
             "change results dramatically."),
            ("design",
             "Design a customer segmentation analysis. Describe the "
             "data, methods and how you would validate the segments.",
             "Data selection, segmentation approach (RFM, "
             "clustering), validation (distinctness, stability, "
             "actionability)."),
            ("scenario",
             "Your data is incomplete for 20% of records. How do you "
             "decide whether to proceed with the analysis?",
             "Assesses bias risk, imputation options, sensitivity "
             "analysis, discloses limitations, decides with "
             "stakeholders."),
            ("written_explanation",
             "Explain the difference between mean, median and mode, "
             "and when the median is a better choice.",
             "Correct definitions; median robust to outliers "
             "(e.g. salaries)."),
            ("design",
             "Design an A/B test for a pricing page change. Describe "
             "the hypothesis, metrics and duration.",
             "Clear hypothesis, primary and guardrail metrics, "
             "sample size, test duration, decision criteria."),
            ("short_answer",
             "What is the difference between a line chart and an area "
             "chart, and when is each useful?",
             "Line = trends; area = magnitude over time; "
             "readability caveats."),
            ("written_explanation",
             "Explain what 'data storytelling' is and why it matters "
             "for decision-making.",
             "Structures data into a narrative with context and "
             "recommendation; drives action rather than just "
             "information."),
            ("scenario",
             "A report is delivered late every week because of manual "
             "steps. How do you improve it?",
             "Automates the pipeline, validates output, documents, "
             "schedules, alerts on failure, hands back time."),
            ("design",
             "Design an analysis to determine why a new feature is "
             "underused.",
             "Usage funnel, user feedback, onboarding review, "
             "segmentation, hypothesis testing, recommendations."),
            ("written_explanation",
             "Explain the importance of data quality for analytics and "
             "how you would measure it.",
             "Accuracy, completeness, consistency, timeliness; "
             "measurement via checks and sampling."),
        ],
        "position": [
            ("written_explanation",
             "As a data analyst, explain how you would take a vague "
             "business question and turn it into a measurable "
             "analysis.",
             "Clarifies the goal, defines metrics and dimensions, "
             "agrees on scope with stakeholder, delivers actionable "
             "insight."),
            ("scenario",
             "You find a data quality issue that invalidates a report "
             "already sent to executives. What do you do?",
             "Informs immediately with correction plan, quantifies "
             "impact, fixes root cause, prevents recurrence."),
            ("short_answer",
             "What is the difference between a measure and a "
             "calculated field, and when do you create one?",
             "Measure = raw aggregation; calculated = derived "
             "logic; used when raw data isn't sufficient."),
            ("design",
             "Design a monthly sales performance report for a sales "
             "manager. Describe the layout and metrics.",
             "Target vs actual, trends, pipeline, by-team and "
             "by-rep, alerts on outliers, actionable."),
            ("written_explanation",
             "Explain how you validate the accuracy of a new "
             "dashboard before publishing it.",
             "Reconciles against source, tests edge cases, "
             "peer review, compares to known values."),
            ("scenario",
             "Two departments define 'active customer' differently "
             "and their numbers conflict. How do you resolve it?",
             "Facilitates a shared definition, documents it, "
             "makes it a single source of truth, educates "
             "users."),
            ("short_answer",
             "What is a funnel analysis and what does it help you "
             "find?",
             "Tracks progression through steps; finds where users "
             "drop off."),
            ("design",
             "Design a cohort analysis for customer retention. "
             "Describe how you would build and present it.",
             "Cohort definition, retention table, correct time "
             "alignment, insights on retention patterns."),
            ("written_explanation",
             "Explain how you communicate a complex analysis to a "
             "non-technical executive in under five minutes.",
             "Bottom line up front, visual over tables, one "
             "recommendation, offer detail as follow-up."),
            ("debugging",
             "A dashboard shows yesterday's number that contradicts "
             "the source system. How do you find which is wrong?",
             "Re-run query, check timezone and refresh timing, "
             "check aggregations, compare raw vs displayed."),
            ("short_answer",
             "What is the difference between a snapshot table and a "
             "transaction table, and why does history matter?",
             "Snapshot = state at a point; transaction = events; "
             "history enables trend and cohort analysis."),
            ("scenario",
             "Your manager asks for the same report every day but "
             "never acts on it. What do you do?",
             "Checks if it's still needed, proposes automation, "
             "suggests a deeper analysis or kill decision."),
            ("design",
             "Design an alerting system for business metrics that "
             "notifies the right people without alert fatigue.",
             "Thresholds, anomaly detection, severity routing, "
             "cooldowns, actionable alerts, tuning."),
            ("written_explanation",
             "Explain the difference between SQL and Python for data "
             "analysis. When would you use each?",
             "SQL for querying/aggregating; Python for "
             "statistics, modelling, complex transformations; "
             "often combined."),
            ("debugging",
             "Your forecast is wildly wrong this month. What are the "
             "first things you check?",
             "Data recency, external shocks, model assumptions, "
             "parameter changes, outliers; re-validate."),
            ("short_answer",
             "What is the difference between a slicer and a filter "
             "in a BI tool?",
             "Both filter; slicers are visible, reusable "
             "interactive controls."),
            ("design",
             "Design a product analytics framework for a mobile app "
             "(activation, retention, referral...).",
             "Defines events, funnels, north-star metric, "
             "cohorts, tooling, actionable cadence."),
            ("written_explanation",
             "Explain how you would measure the impact of a "
             "marketing campaign with observational data.",
             "Before/after, control group, regression or "
             "difference-in-differences, caveats about "
             "confounders."),
            ("scenario",
             "You are asked to produce an analysis in 2 hours with "
             "messy data. How do you prioritise?",
             "Scopes the key question, focuses on the critical "
             "metric, cleans only what matters, notes "
             "limitations, delivers."),
            ("design",
             "Design a self-service analytics layer for a company "
             "so non-analysts can answer their own questions.",
             "Governed semantic layer, certified datasets, "
             "templates, training, guardrails on "
             "performance."),
        ],
        "practical": [
            ("practical",
             "Write SQL to compute monthly revenue with a running "
             "cumulative total.",
             "Correct aggregation and window function."),
            ("design",
             "Design a dashboard for a call centre showing "
             "performance. List the metrics and their layout.",
             "Answer rate, wait time, resolution, CSAT, agent "
             "utilisation; hierarchy and drill-down."),
            ("practical",
             "Given a dataset of transactions, describe (with "
             "pseudo-code) how you would detect suspicious "
             "patterns for fraud review.",
             "Rules, velocity checks, anomaly scoring, "
             "prioritisation, human review loop."),
            ("debugging",
             "A report total doesn't match the sum of its rows. "
             "List the possible causes.",
             "Duplicate rows, joins multiplying rows, rounding, "
             "filters on subtotal vs total, null handling."),
            ("practical",
             "Write pseudo-code for an A/B test analysis that "
             "checks whether a metric difference is meaningful.",
             "Correct test selection, significance, effect "
             "size, practical significance, caveats."),
            ("design",
             "Design a churn prediction approach using available "
             "customer data. Describe features, model and use.",
             "Feature engineering (usage, recency, support), "
             "model choice, validation, actioning with "
             "retention team."),
            ("practical",
             "Write SQL to compute the number of active users per "
             "day from a login log table.",
             "Correct distinct count by date."),
            ("debugging",
             "Your cohort table shows 120% retention in month "
             "three. What is likely wrong?",
             "Duplicate user IDs, cohort boundary error, "
             "counting wrong, date joins."),
            ("practical",
             "Describe how you would forecast next month's sales "
             "using 12 months of history, including validation.",
             "Appropriate method (moving average, trend, "
             "seasonality), holdout validation, error "
             "measurement, limitations."),
            ("design",
             "Design a survey analysis plan: define the goal, "
             "questions, and how you would present results.",
             "Clear objectives, unbiased questions, analysis "
             "plan, visual presentation, honesty about "
             "sample."),
            ("practical",
             "Write a query that returns the top 3 products by "
             "revenue per region.",
             "Window function or correlated approach, correct "
             "grouping."),
            ("debugging",
             "A table join returns 10 times more rows than "
             "expected. What is the cause and how do you "
             "verify?",
             "One-to-many join expansion; verifies with "
             "counts and distinct keys."),
            ("practical",
             "Describe how you would clean a dataset with "
             "duplicate customer records (one customer, two "
             "rows).",
             "Matching rules, dedupe key, canonical record, "
             "merging fields, audit."),
            ("design",
             "Design an analysis to compare the performance of "
             "two sales teams fairly.",
             "Fair comparison (territory, lead quality, "
             "seasonality), metrics, adjusts for "
             "confounders."),
            ("practical",
             "Write SQL to find the weekday with the highest "
             "average order value.",
             "DATE_FORMAT/DAYOFWEEK grouping with AVG."),
            ("debugging",
             "Your visualisation shows negative revenue. List "
             "possible causes.",
             "Refunds not handled, data entry errors, "
             "currency mixing, date issues, aggregation "
             "errors."),
            ("practical",
             "Describe how you would present a 50-row analysis "
             "table to executives so they can act on it.",
             "Summarise, highlight key rows, visualise "
             "trends, recommendations, detail on request."),
            ("design",
             "Design a product usage analysis for a SaaS "
             "feature adoption study.",
             "Define adoption, usage segments, correlate "
             "with retention/revenue, actionable insights."),
            ("practical",
             "Write pseudo-code that flags outlier transactions "
             "for review using mean and standard deviation, "
             "and explain the limitations.",
             "Z-score or IQR approach, explains why "
             "assumptions can fail, manual review loop."),
            ("debugging",
             "A dashboard fails to refresh at 6 AM. Describe "
             "your diagnosis and fix.",
             "Check scheduled job, dependencies (data "
             "arrival), permissions, logs, alerts; "
             "resilience."),
        ],
    },

    # ------------------------------------------------------------------ 8
    "Cybersecurity": {
        "category": [
            ("written_explanation",
             "Explain the CIA triad and give a real-world example "
             "where each property was violated.",
             "Confidentiality, integrity, availability - each "
             "defined and exemplified."),
            ("scenario",
             "An employee clicks a link in a phishing email and "
             "enters their password. Describe the immediate and "
             "long-term response.",
             "Containment (reset credentials, kill session), "
             "investigation, user education, detection "
             "improvements."),
            ("design",
             "Design a layered (defence-in-depth) security "
             "architecture for a small company's web application.",
             "Network controls, host controls, application "
             "controls, data controls, monitoring - layered "
             "not single-point."),
            ("written_explanation",
             "Explain the difference between authentication and "
             "authorisation, with an example of each.",
             "AuthN = proving identity; authZ = what you may "
             "do; example of both in one system."),
            ("scenario",
             "You discover a vulnerability in a third-party "
             "library used in production. What is your response "
             "process?",
             "Assess exposure, patch or mitigate, communicate, "
             "verify, monitor for exploit attempts."),
            ("short_answer",
             "What is the difference between a vulnerability, a "
             "threat and a risk?",
             "Vulnerability = weakness; threat = potential "
             "attacker/event; risk = likelihood x impact."),
            ("written_explanation",
             "Explain how encryption works at a high level: "
             "symmetric vs asymmetric, and when each is used.",
             "Symmetric (shared key, fast) vs asymmetric (key "
             "pairs, key exchange); use cases like TLS and "
             "data at rest."),
            ("design",
             "Design an access control model for a hospital "
             "system where staff need different data access.",
             "Role-based access, least privilege, "
             "separation of duties, audit logging, "
             "emergency access procedure."),
            ("scenario",
             "A ransomware note appears on a file server. "
             "Describe your incident response steps in order.",
             "Containment (disconnect), preserve evidence, "
             "notify, assess scope, recover from backups, "
             "investigate entry vector, communicate."),
            ("written_explanation",
             "Explain what a man-in-the-middle attack is and "
             "how TLS prevents it.",
             "Defines MITM; TLS provides authenticity "
             "(certificates) and confidentiality (encryption)."),
            ("short_answer",
             "What is the difference between a firewall and an "
             "intrusion detection system (IDS)?",
             "Firewall = prevent/allow traffic; IDS = "
             "detect suspicious activity; complementary."),
            ("design",
             "Design a secure password policy that balances "
             "security and usability.",
             "Modern guidance (length over complexity), MFA, "
             "breach monitoring, no forced rotation, "
             "education."),
            ("written_explanation",
             "Explain the OWASP Top Ten in your own words and "
             "why injection is still the top risk.",
             "Overview of the list; injection persists due to "
             "unsafe query construction."),
            ("scenario",
             "A developer wants to store customer credit card "
             "numbers in the database for convenience. How do "
             "you respond?",
             "Explains risk and compliance (PCI), proposes "
             "tokenisation or third-party processing, "
             "minimises data retention."),
            ("short_answer",
             "What is the difference between hashing and "
             "encryption?",
             "Hashing = one-way, for integrity/passwords; "
             "encryption = reversible, for confidentiality."),
            ("written_explanation",
             "Explain the principle of least privilege and give "
             "an example of applying it.",
             "Give minimum access needed; example like "
             "read-only roles for analysts."),
            ("design",
             "Design a security monitoring strategy for a "
             "medium company. What would you log, alert on "
             "and review?",
             "Log sources, alert rules (login anomalies, "
             "exfiltration), SIEM or aggregation, "
             "response playbooks."),
            ("scenario",
             "Your company is notified of a data breach at a "
             "vendor that held your customer data. What do "
             "you do?",
             "Assess data involved, legal/regulatory "
             "obligations, notify affected parties, "
             "review vendor risk."),
            ("written_explanation",
             "Explain the difference between a black-box and "
             "white-box security test.",
             "Black-box = no internal knowledge; white-box = "
             "full access; purpose of each in a testing "
             "program."),
            ("design",
             "Design a security awareness program for "
             "employees. What topics and cadence?",
             "Phishing, passwords/MFA, data handling, "
             "reporting, regular testing, leadership "
             "support."),
        ],
        "position": [
            ("written_explanation",
             "As a penetration tester, describe your methodology "
             "for testing a web application.",
             "Reconnaissance, enumeration, vulnerability "
             "identification, exploitation, reporting with "
             "remediation."),
            ("scenario",
             "You are a SOC analyst and an alert fires for "
             "possible data exfiltration at 3 AM. Describe "
             "your triage process.",
             "Validate the alert, scope the activity, "
             "contain, escalate, document, follow the "
             "playbook."),
            ("short_answer",
             "What is the difference between a vulnerability "
             "scan and a penetration test?",
             "Scan = automated identification; pentest = "
             "exploitation to prove impact; both needed."),
            ("design",
             "Design a secure SDLC (software development "
             "lifecycle) with security gates.",
             "Threat modelling, secure coding, SAST/DAST, "
             "dependency scanning, code review, pen tests "
             "before release."),
            ("written_explanation",
             "Explain how you would secure an API that is "
             "consumed by both mobile apps and third parties.",
             "Authentication (OAuth2/keys), rate limiting, "
             "input validation, logging, throttling, "
             "versioning."),
            ("scenario",
             "A developer wants to disable TLS verification "
             "in code to fix a certificate error. How do you "
             "respond?",
             "Explains the risk, finds the real fix "
             "(correct cert, proper config), never "
             "disables verification."),
            ("short_answer",
             "What is the difference between a virus and "
             "ransomware?",
             "Virus = self-replicating malware; ransomware = "
             "encrypts and demands payment; ransomware "
             "often spreads via other means."),
            ("design",
             "Design an incident response plan template for "
             "a company. What phases does it include?",
             "Preparation, detection, containment, "
             "eradication, recovery, lessons learned."),
            ("written_explanation",
             "Explain how you would investigate a suspected "
             "insider data leak.",
             "Preserve evidence, review access logs, "
             "interview, data movement analysis, DLP "
             "review, process improvements."),
            ("debugging",
             "Users report a certificate warning on an "
             "internal site. How do you diagnose?",
             "Check expiry, trust chain, hostname "
             "mismatch, time sync, deployment config."),
            ("short_answer",
             "What is the difference between a VPN and a "
             "proxy?",
             "VPN = encrypted tunnel for all traffic to a "
             "network; proxy = relay for specific "
             "traffic; different trust models."),
            ("scenario",
             "An employee's laptop is lost. Describe the "
             "security response.",
             "Remote wipe, credential rotation, assess data "
             "at risk, encryption check, report and "
             "learn."),
            ("design",
             "Design a DLP (data loss prevention) strategy "
             "for a company with sensitive documents.",
             "Classify data, control channels (email, USB), "
             "monitor, educate, incident process."),
            ("written_explanation",
             "Explain the difference between symmetric key "
             "management and public key infrastructure "
             "(PKI).",
             "Key exchange vs certificate chains; PKI "
             "solves trust distribution."),
            ("debugging",
             "A server is sending an unexpectedly high volume "
             "of outbound traffic. What is your first "
             "response?",
             "Contain, check for compromise indicators, "
             "analyse traffic, check for data "
             "exfiltration, notify."),
            ("short_answer",
             "What is the difference between a brute-force "
             "attack and a credential-stuffing attack?",
             "Brute force = try many passwords; stuffing = "
             "use breached credentials; both fought with "
             "MFA and rate limits."),
            ("design",
             "Design an identity and access management (IAM) "
             "plan for a company growing from 50 to 500 "
             "employees.",
             "SSO, lifecycle automation, role-based access, "
             "MFA, least privilege, audit."),
            ("written_explanation",
             "Explain how you would test the security of a "
             "mobile application.",
             "Static analysis, runtime analysis, insecure "
             "storage checks, network interception, "
             "jailbreak/root handling."),
            ("scenario",
             "You find that production credentials are stored "
             "in source code. How do you handle it?",
             "Rotate immediately, remove from history, "
             "implement secret management, scan for "
             "future leaks."),
            ("design",
             "Design a business continuity and disaster "
             "recovery plan for a company's IT systems.",
             "RTO/RPO, backup strategy, failover "
             "procedures, testing cadence, roles and "
             "communication."),
        ],
        "practical": [
            ("practical",
             "Write pseudo-code (or describe the SQL) for a "
             "query that lists user accounts with no activity "
             "in 90 days - a potential compromise or dormant "
             "account risk.",
             "Correct query and justification for the "
             "review."),
            ("design",
             "Design a secure file upload feature. Describe "
             "the validation, storage and serving decisions.",
             "Type/size validation, random filenames, "
             "non-executable storage, content validation, "
             "access control."),
            ("practical",
             "Describe how you would verify that a backup is "
             "free of ransomware before restoring.",
             "Isolate restore, scan, check file integrity, "
             "restore to staging first."),
            ("debugging",
             "A user reports receiving a suspicious "
             "email that looks like it is from your company. "
             "Walk through your investigation.",
             "Header analysis, domain/spf/dkim checks, "
             "malicious links, take-down, user "
             "guidance."),
            ("practical",
             "Write the checks you would run to assess the "
             "security of a newly discovered server on your "
             "network.",
             "Open ports, patch level, default "
             "credentials, service versions, ownership."),
            ("design",
             "Design a password reset flow that is secure "
             "against account takeover.",
             "Time-limited tokens, no user enumeration, "
             "notification, MFA step, rate limiting."),
            ("practical",
             "Given a log of failed login attempts, describe "
             "how you would identify a brute-force attack "
             "and the control you would implement.",
             "Thresholds per source, pattern "
             "recognition, rate limiting or lockout, "
             "alerting."),
            ("debugging",
             "An internal application is slow only for users "
             "on the VPN. How do you troubleshoot?",
             "Check path, MTU/fragmentation, VPN routing, "
             "DNS over VPN, server load."),
            ("practical",
             "Write pseudo-code for a function that safely "
             "queries a database with user input, preventing "
             "injection.",
             "Parameterised queries, no string "
             "concatenation, input validation."),
            ("design",
             "Design an email security posture: describe SPF, "
             "DKIM and DMARC and why all three matter.",
             "Correct roles of each; DMARC policy; "
             "monitoring and enforcement."),
            ("practical",
             "Describe how you would securely transfer a "
             "confidential file to a client.",
             "Encrypted channel, access control, "
             "expiry, verification of recipient."),
            ("debugging",
             "An antivirus quarantine is filling with "
             "false positives on a development machine. "
             "How do you handle it?",
             "Verify with analysis, add trusted "
             "exception scoped narrowly, review rules, "
             "document."),
            ("practical",
             "Write the steps to securely decommission a "
             "server that contained customer data.",
             "Backup decision, data wipe/degauss, "
             "certificate of destruction, hardware "
             "disposal, audit."),
            ("design",
             "Design a multi-factor authentication "
             "enforcement plan for a remote workforce.",
             "Choose factors, rollout, fallback "
             "(recovery codes), support, enforce "
             "policy."),
            ("practical",
             "Describe how you would check whether a "
             "company domain is in a breach database and "
             "what you would do next.",
             "Check breach sources, identify affected "
             "accounts, force resets, MFA, monitor."),
            ("debugging",
             "A firewall rule change broke remote "
             "desktop access. Describe how you "
             "diagnose and fix.",
             "Compare before/after rules, test "
             "connectivity layers, check logs, "
             "correct rule, verify."),
            ("practical",
             "Write a checklist for securing a new laptop "
             "before an employee uses it.",
             "Encryption, updates, AV/EDR, account "
             "setup, backups, policy."),
            ("design",
             "Design a data classification and handling "
             "policy for a company.",
             "Levels (public/internal/confidential), "
             "handling rules, storage, disposal, "
             "training."),
            ("practical",
             "Describe how you would respond to a "
             "phishing simulation failure rate that is "
             "too high.",
             "Analyse patterns, targeted training, "
             "technical controls, retest, measure "
             "improvement."),
            ("debugging",
             "A server's logs show logins from a foreign "
             "country at odd hours. Describe your "
             "verification process.",
             "Check legitimacy (VPN, travel), review "
             "activity, reset if suspicious, enable "
             "alerts, document."),
        ],
    },

    # ------------------------------------------------------------------ 9
    "Networking & Telecommunications": {
        "category": [
            ("written_explanation",
             "Explain the OSI model in your own words and give a "
             "real protocol at each of the seven layers.",
             "Accurate layer descriptions with correct "
             "protocol examples (HTTP, TCP, IP, Ethernet...)."),
            ("scenario",
             "A network that worked yesterday is slow today. "
             "Describe your troubleshooting methodology.",
             "Physical to logical or logical to physical; "
             "isolate the segment, check utilisation, errors, "
             "then fix."),
            ("design",
             "Design a network for a small office with 50 users, "
             "internet, Wi-Fi and a server room. Describe the "
             "topology and equipment.",
             "VLANs, routing, switching, APs, firewall, "
             "segmentation of sensitive traffic."),
            ("written_explanation",
             "Explain the difference between TCP and UDP, and "
             "give a use case for each.",
             "Reliability/ordering vs speed; HTTP, email (TCP) "
             "vs VoIP, video, gaming (UDP)."),
            ("short_answer",
             "What is the difference between a hub, a switch and "
             "a router?",
             "Hub = broadcast; switch = MAC learning; router = "
             "inter-network and routing."),
            ("design",
             "Design a Wi-Fi deployment for a warehouse with "
             "high metal racks. Describe access point placement "
             "and channel planning.",
             "Site survey, AP density, channel selection, "
             "roaming, interference management."),
            ("written_explanation",
             "Explain IP addressing: the difference between IPv4 "
             "and IPv6, and why IPv6 exists.",
             "Address exhaustion, header differences, "
             "notation; dual-stack transition."),
            ("scenario",
             "A user cannot reach the internet but can reach "
             "internal servers. Describe your diagnostic steps.",
             "Check default gateway, DNS, firewall, ISP "
             "status; layer-by-layer isolation."),
            ("short_answer",
             "What is the difference between a public IP and a "
             "private IP, and what is NAT?",
             "Public routable vs private (RFC1918); NAT maps "
             "private to public."),
            ("written_explanation",
             "Explain how DNS works end to end when you type a "
             "website address.",
             "Resolver, root, TLD, authoritative servers, "
             "caching - correct flow."),
            ("design",
             "Design a network monitoring system. What metrics "
             "would you track and what alerts would you set?",
             "Bandwidth, latency, packet loss, device health, "
             "link status; baselines and thresholds."),
            ("scenario",
             "A cable cut takes down a branch office. Describe "
             "the redundancy options that would have prevented "
             "it.",
             "Redundant links, WAN failover, SD-WAN, "
             "cellular backup; costs vs uptime."),
            ("written_explanation",
             "Explain what VLANs are and why network "
             "segmentation is a security control.",
             "Virtual LANs separate broadcast domains; "
             "containment and policy enforcement."),
            ("short_answer",
             "What is the difference between a static route and "
             "dynamic routing, and when is each used?",
             "Static = manual, predictable; dynamic (OSPF, "
             "BGP) = automatic, scalable."),
            ("design",
             "Design a guest Wi-Fi network that isolates guests "
             "from the corporate network.",
             "Separate VLAN, firewall rules, captive portal, "
             "bandwidth limits, no internal access."),
            ("written_explanation",
             "Explain what QoS is in networking and give an "
             "example of traffic you would prioritise.",
             "Quality of service classifies and prioritises "
             "traffic; VoIP/video over bulk downloads."),
            ("scenario",
             "Two offices need to connect securely over the "
             "internet. Compare site-to-site VPN options.",
             "IPsec vs SSL, dedicated circuits, SD-WAN; "
             "trade-offs in cost, security, performance."),
            ("short_answer",
             "What is the difference between a packet and a "
             "frame?",
             "Packet = network layer unit (IP); frame = data "
             "link layer unit (Ethernet)."),
            ("written_explanation",
             "Explain how you would troubleshoot an intermittent "
             "network issue that disappears when you test.",
             "Long-term monitoring, logs, cable testing, "
             "timing correlation, event correlation."),
            ("design",
             "Design the physical cabling plan for a new office "
             "floor including structured cabling standards.",
             "Cable types/categories, patch panels, "
             "labelling, pathway, testing, standards "
             "(TIA/EIA)."),
        ],
        "position": [
            ("written_explanation",
             "As a network administrator, describe your routine "
             "for managing network equipment changes safely.",
             "Change window, config backup, rollback plan, "
             "testing, documentation."),
            ("scenario",
             "A switch port is flapping (up/down). Describe how "
             "you diagnose and fix it.",
             "Check cable, NIC, duplex mismatch, errors, "
             "then replace/repair."),
            ("short_answer",
             "What is the difference between a routed protocol "
             "and a routing protocol?",
             "Routed = carries data (IP); routing = "
             "exchanges routes (OSPF, BGP)."),
            ("design",
             "Design a network segmentation plan for a company "
             "with finance, HR and public servers.",
             "VLANs per trust level, firewall between "
             "zones, least access, monitoring."),
            ("written_explanation",
             "Explain how you would set up a new branch office "
             "network from scratch.",
             "Requirements, ISP, design, cabling, "
             "equipment, configuration, testing, "
             "documentation."),
            ("debugging",
             "Users report VoIP calls cutting out. Describe "
             "your investigation.",
             "Check jitter/latency/loss, QoS, bandwidth, "
             "codec, network congestion."),
            ("short_answer",
             "What is the difference between a managed and an "
             "unmanaged switch?",
             "Managed = configurable (VLANs, monitoring); "
             "unmanaged = plug-and-play."),
            ("design",
             "Design a wireless network for a school with 1000 "
             "students and 60 classrooms.",
             "AP count and placement, controller, "
             "authentication, filtering, bandwidth per "
             "user, monitoring."),
            ("written_explanation",
             "Explain how you would test a newly installed "
             "network cable run.",
             "Cable tester, certification, link speed "
             "verification, documentation."),
            ("scenario",
             "A critical router fails. Describe your response "
             "and how redundancy would help.",
             "Failover to standby, isolate fault, vendor "
             "support, restore, post-incident review."),
            ("short_answer",
             "What is the difference between a subnet mask and "
             "a default gateway?",
             "Subnet = network size/boundary; gateway = "
             "route out of the network."),
            ("design",
             "Design a secure remote access solution for 20 "
             "employees working from home.",
             "VPN (IPsec/SSL), MFA, endpoint checks, "
             "least-privilege access, monitoring."),
            ("written_explanation",
             "Explain how you would upgrade the firmware on a "
             "network device safely.",
             "Backup config, check release notes, "
             "maintenance window, staged rollout, "
             "rollback."),
            ("debugging",
             "A network printer is unreachable from most "
             "computers but works from one. Describe your "
             "diagnosis.",
             "Check VLAN/IP, firewall, print server, "
             "driver, test from multiple points."),
            ("short_answer",
             "What is the difference between a firewall and an "
             "ACL?",
             "Firewall = stateful device/policy; ACL = "
             "packet filtering rules on a device."),
            ("design",
             "Design a network for a small data centre rack: "
             "switches, cabling, power and monitoring.",
             "Top-of-rack design, redundant power, cable "
             "management, environmental monitoring."),
            ("written_explanation",
             "Explain the process of commissioning a new "
             "switch: from unboxing to production.",
             "Firmware, baseline config, security "
             "hardening, VLANs, testing, documentation."),
            ("scenario",
             "A user's laptop gets a valid-looking IP but no "
             "internet. Describe your steps.",
             "Check DHCP, DNS, gateway, firewall, proxy "
             "settings, connectivity tests."),
            ("short_answer",
             "What is the difference between 2.4 GHz and 5 GHz "
             "Wi-Fi, and how do you choose?",
             "Range vs speed/interference; steer devices "
             "appropriately."),
            ("design",
             "Design a monitoring and alerting setup for "
             "network health that notifies the right people.",
             "Metrics, thresholds, severity, paging "
             "policy, dashboards, incident workflow."),
        ],
        "practical": [
            ("practical",
             "Write the CLI commands (or describe the steps) to "
             "trace a network path and identify where packets "
             "are lost.",
             "tracert/traceroute, ping tests hop by hop, "
             "interpret latency/loss per hop."),
            ("design",
             "Design an IP addressing scheme for an office with "
             "5 departments of 20 users each, using private "
             "addresses and VLANs.",
             "Sensible subnetting (e.g. /24 per VLAN), "
             "documented scheme, room to grow."),
            ("practical",
             "Describe how you would capture and analyse "
             "packets to diagnose a slow application.",
             "Wireshark capture, filter, look for "
             "retransmissions, latency, TCP window "
             "issues."),
            ("debugging",
             "A DHCP server is giving out duplicate addresses. "
             "Describe your investigation and fix.",
             "Check rogue DHCP, leases, static conflicts, "
             "DHCP snooping."),
            ("practical",
             "Write a checklist to test a new Wi-Fi deployment "
             "for coverage and performance.",
             "Signal strength map, throughput tests, "
             "roaming tests, interference check."),
            ("design",
             "Design a failover solution for an internet "
             "connection used by a critical business system.",
             "Second link, automatic failover, monitoring, "
             "load balancing optional, testing."),
            ("practical",
             "Describe how you would verify that a firewall "
             "rule change did what was intended.",
             "Test from source/destination, check logs, "
             "verify no collateral, document."),
            ("debugging",
             "A user cannot resolve internal hostnames. "
             "Describe your diagnostic steps.",
             "Check DNS servers, zones, forwarders, "
             "client config, test nslookup."),
            ("practical",
             "Write the steps to configure a new VLAN on a "
             "switch and verify it end to end.",
             "Create VLAN, assign ports, trunk, routing "
             "or gateway, test, document."),
            ("design",
             "Design a bandwidth management plan for an office "
             "where video calls compete with downloads.",
             "QoS policies, traffic shaping, "
             "prioritisation, monitoring, capacity "
             "planning."),
            ("practical",
             "Describe how you would migrate a server from one "
             "VLAN to another without downtime.",
             "Pre-configure, change IP, update DNS, "
             "switch port, verify, remove old."),
            ("debugging",
             "A network device shows high CPU usage but no "
             "obvious load. What are the likely causes?",
             "Broadcast storms, spanning-tree issues, "
             "monitoring overhead, faulty cable, "
             "malware."),
            ("practical",
             "Write the steps to secure a newly installed "
             "wireless access point.",
             "Change defaults, WPA2/3, disable WPS, "
             "firmware, separate SSIDs, monitoring."),
            ("design",
             "Design a structured cabling plan for a new "
             "office floor with 40 desks.",
             "Pathways, cable types, patch panels, "
             "labelling, testing, standards."),
            ("practical",
             "Describe how you would test internet speed "
             "accurately and interpret the result.",
             "Test methodology (wired, time of day), "
             "multiple tests, interpret vs contracted "
             "speed."),
            ("debugging",
             "A branch office VPN is unstable. Describe your "
             "diagnosis and fix.",
             "Check WAN stability, VPN logs, MTU, "
             "firewall, upgrade or reconfigure."),
            ("practical",
             "Write a plan to replace an old core switch with "
             "minimal downtime.",
             "Pre-stage, config backup, cutover plan, "
             "rollback, testing window."),
            ("design",
             "Design a network for a building with three "
             "floors and a shared server room.",
             "Hierarchical design, per-floor switches, "
             "core links, redundancy, cabling."),
            ("practical",
             "Describe how you would verify end-to-end "
             "connectivity between two servers across a "
             "firewall.",
             "Ping, port tests, packet capture, firewall "
             "logs, confirm policies."),
            ("debugging",
             "A wireless network is slow in one corner of the "
             "office. What are the likely causes and fixes?",
             "Coverage hole, interference, channel "
             "overlap, AP placement, roaming."),
        ],
    },
}
