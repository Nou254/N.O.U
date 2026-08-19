"""
Unique category / position / practical questions for the question banks.
"""

CATS = {
    # ----------------------------------------------------------------- 10
    "Cloud Computing & Infrastructure": {
        "category": [
            ("written_explanation",
             "Explain the three main cloud service models (IaaS, PaaS, "
             "SaaS) and give a real example of each.",
             "Correct definitions and examples (VM/IaaS, app platform/"
             "PaaS, web app/SaaS)."),
            ("scenario",
             "A company wants to move its on-premise systems to the "
             "cloud. Describe your migration assessment approach.",
             "Inventory, dependency mapping, cost analysis, "
             "security/compliance review, migration strategy "
             "(rehost/refactor/relocate/replace)."),
            ("design",
             "Design a highly available architecture for a web "
             "application in the cloud. Describe the components.",
             "Load balancer, multi-AZ deployment, auto-scaling, "
             "managed database with failover, health checks, "
             "backups."),
            ("written_explanation",
             "Explain the difference between vertical and horizontal "
             "scaling, and when you would choose each.",
             "Vertical = bigger machine; horizontal = more machines; "
             "limits and use cases."),
            ("scenario",
             "Your cloud bill doubled unexpectedly. Describe how you "
             "would investigate and control it.",
             "Cost analysis by service, resource utilisation review, "
             "find idle resources, rightsizing, budget alerts."),
            ("short_answer",
             "What is the difference between a virtual machine and a "
             "container?",
             "VM = full OS virtualisation; container = shared kernel "
             "isolation; trade-offs in density and isolation."),
            ("written_explanation",
             "Explain the shared responsibility model in cloud "
             "security.",
             "Provider secures the infrastructure; customer secures "
             "their data, access and configurations; differs by "
             "service model."),
            ("design",
             "Design a disaster recovery strategy for a critical "
             "application with an RPO of 15 minutes.",
             "Continuous replication, automated failover, "
             "tested runbooks, cross-region strategy."),
            ("scenario",
             "An application in the cloud suddenly fails after a "
             "deployment. Describe your diagnosis process.",
             "Check deployment history, logs, metrics, config "
             "changes; rollback; verify."),
            ("short_answer",
             "What is the difference between a region and an "
             "availability zone?",
             "Region = geographic area; AZ = isolated data centre "
             "within a region; used for redundancy."),
            ("written_explanation",
             "Explain what serverless computing is, its advantages "
             "and its limitations.",
             "No server management, pay-per-invocation; "
             "limitations: cold starts, vendor lock-in, "
             "execution limits."),
            ("design",
             "Design a secure cloud network with public and private "
             "subnets.",
             "VPC design, subnets, security groups, internet "
             "gateway, NAT, least-privilege rules."),
            ("scenario",
             "A developer created a cloud resource with a default "
             "password. What risks exist and what do you do?",
             "Explain exposure, rotate credentials, audit for "
             "similar issues, add guardrails/policy."),
            ("written_explanation",
             "Explain the difference between block storage, object "
             "storage and file storage, with use cases.",
             "Block = VM disks; object = unstructured (S3-like); "
             "file = shared filesystems; correct usage."),
            ("short_answer",
             "What is the difference between cloud cost optimisation "
             "and cost cutting?",
             "Optimisation = right-size and eliminate waste while "
             "maintaining performance; cutting can harm "
             "reliability."),
            ("design",
             "Design an identity and access strategy for a cloud "
             "environment with 100 employees.",
             "SSO, role-based access, least privilege, MFA, "
             "audit logging, lifecycle management."),
            ("written_explanation",
             "Explain what infrastructure as code is and why it "
             "improves cloud management.",
             "Define infrastructure in versioned code; "
             "repeatability, review, audit, rollback."),
            ("scenario",
             "A compliance auditor asks how you secure data at rest "
             "and in transit. How do you answer?",
             "Encryption mechanisms, key management, TLS "
             "policies, evidence and documentation."),
            ("short_answer",
             "What is the difference between a load balancer and a "
             "reverse proxy?",
             "Load balancer distributes traffic; reverse proxy "
             "fronts and forwards; often combined."),
            ("design",
             "Design a multi-cloud or hybrid cloud strategy for a "
             "company. What are the trade-offs?",
             "Flexibility and resilience vs complexity and cost; "
             "clear use cases for each workload."),
        ],
        "position": [
            ("written_explanation",
             "As a cloud architect, explain how you would size and "
             "right-size a workload before deployment.",
             "Understand requirements, benchmark, pick "
             "appropriate instance types, plan for scaling."),
            ("scenario",
             "A cloud administrator receives an alert that a "
             "database is at 90% storage. Describe your response.",
             "Assess growth rate, add storage safely, archive or "
             "clean, set alerts, plan capacity."),
            ("short_answer",
             "What is the difference between a security group and a "
             "network ACL?",
             "Security group = instance-level stateful; NACL = "
             "subnet-level stateless."),
            ("design",
             "Design an auto-scaling policy for a web application "
             "that handles traffic spikes.",
             "Metrics (CPU, requests), min/max, cooldowns, "
             "predictive or reactive, health checks."),
            ("written_explanation",
             "Explain how you would migrate a monolithic "
             "application to the cloud with minimal risk.",
             "Lift-and-shift first, then incremental "
             "modernisation, parallel runs, rollback plan."),
            ("debugging",
             "An application cannot reach the internet from a "
             "private subnet. Describe your diagnosis.",
             "Check NAT gateway/instance, routes, security "
             "groups, IAM roles."),
            ("short_answer",
             "What is the difference between a snapshot and an AMI "
             "(or machine image)?",
             "Snapshot = volume backup; image = template for "
             "instances; images can include snapshots."),
            ("design",
             "Design a cloud monitoring and alerting setup for a "
             "production environment.",
             "Metrics, logs, dashboards, alert thresholds, "
             "on-call rotation, runbooks."),
            ("written_explanation",
             "Explain how you would handle secrets (API keys, "
             "passwords) in a cloud application.",
             "Secret manager, rotation, no hard-coding, "
             "least-privilege access."),
            ("scenario",
             "A contractor left with access to cloud resources. "
             "Describe the offboarding process.",
             "Revoke access, rotate shared credentials, audit "
             "activity, review roles."),
            ("short_answer",
             "What is the difference between a VPC peering "
             "connection and a transit gateway?",
             "Peering = direct point-to-point; transit gateway = "
             "hub for many VPCs."),
            ("design",
             "Design a backup strategy for a cloud database with "
             "daily backups and point-in-time recovery.",
             "Automated snapshots, transaction log "
             "continuous backup, retention, restore "
             "testing."),
            ("written_explanation",
             "Explain how you would deploy a new version of an "
             "application in the cloud with zero downtime.",
             "Blue-green or rolling deployment, health checks, "
             "automatic rollback, traffic shift."),
            ("debugging",
             "A cloud function times out at a specific workload. "
             "How do you diagnose?",
             "Check logs, memory/CPU limits, cold starts, "
             "external dependencies, optimise."),
            ("short_answer",
             "What is the difference between horizontal and vertical "
             "auto-scaling?",
             "Add instances vs resize instances; typical usage "
             "for each."),
            ("design",
             "Design a landing zone for a new cloud account "
             "(organisation structure, security baseline).",
             "Account structure, guardrails, identity, "
             "logging, budgets, compliance baseline."),
            ("written_explanation",
             "Explain how you would estimate and report cloud costs "
             "to stakeholders.",
             "Forecast models, tagging, usage attribution, "
             "regular reviews, cost per business unit."),
            ("scenario",
             "A critical cloud service goes down. Describe your "
             "incident response.",
             "Status check, communicate, failover or rollback, "
             "vendor support, post-incident review."),
            ("short_answer",
             "What is the difference between a managed and an "
             "unmanaged cloud service?",
             "Managed = provider handles ops (RDS); unmanaged = "
             "you operate it (EC2)."),
            ("design",
             "Design a cloud environment that meets a "
             "data-residency requirement (data must stay in "
             "country X).",
             "Region selection, replication boundaries, "
             "encryption keys location, documentation."),
        ],
        "practical": [
            ("practical",
             "Describe (or write commands for) how you would "
             "provision a virtual machine with a web server "
             "using infrastructure as code.",
             "IaC definition, bootstrapping, security group, "
             "verify reachable, document."),
            ("design",
             "Design a cost-tagging strategy for cloud resources "
             "so costs can be attributed to projects.",
             "Tag schema, enforcement, reporting, ownership."),
            ("practical",
             "Write a checklist to audit a cloud account for "
             "security misconfigurations.",
             "Public storage, open security groups, "
             "unused credentials, logging enabled, MFA."),
            ("debugging",
             "A load balancer health check fails intermittently. "
             "Describe your diagnosis.",
             "Check endpoint, dependencies, logs, "
             "timeout/thresholds, resource exhaustion."),
            ("practical",
             "Describe how you would move 2 TB of data to the "
             "cloud efficiently.",
             "Direct transfer, transfer appliance, "
             "parallelism, verification, bandwidth "
             "considerations."),
            ("design",
             "Design a backup retention policy for a company "
             "that must keep records for 7 years.",
             "Tiers (daily/weekly/yearly), archival to "
             "cold storage, compliance, restore tests."),
            ("practical",
             "Write the steps to set up a VPN connection "
             "between an office and a cloud VPC.",
             "Gateway config, tunnel, routes, testing, "
             "monitoring."),
            ("debugging",
             "A server in the cloud runs out of memory every "
             "few days. How do you diagnose?",
             "Monitor memory trends, check processes, logs, "
             "leaks, resize or fix app."),
            ("practical",
             "Describe how you would set up a cloud billing "
             "alert before spending exceeds budget.",
             "Budgets, thresholds, notifications, "
             "enforcement policies."),
            ("design",
             "Design a serverless architecture for a photo "
             "upload and processing feature.",
             "Upload endpoint, object storage, event-driven "
             "function, processing, results."),
            ("practical",
             "Write a runbook for responding to a cloud "
             "database failover event.",
             "Detection, verification, failover steps, "
             "rollback, communication, post-review."),
            ("debugging",
             "A container in the cloud restarts in a loop. "
             "Describe your investigation.",
             "Check logs, exit codes, health checks, "
             "resource limits, config."),
            ("practical",
             "Describe how you would verify that a cloud "
             "deployment meets compliance requirements.",
             "Evidence collection, automated checks, "
             "policy-as-code, audit logs, reports."),
            ("design",
             "Design a multi-region deployment for a "
             "global application.",
             "Replication, DNS routing, failover, data "
             "consistency, latency."),
            ("practical",
             "Write the steps to rotate a compromised cloud "
             "access key.",
             "Revoke key, assess usage, issue new key, "
             "update consumers, monitor."),
            ("debugging",
             "An application is slow only during business "
             "hours. What are the likely causes?",
             "Load, scaling lag, batch jobs, contention; "
             "correlate metrics with time."),
            ("practical",
             "Describe how you would test a disaster recovery "
             "plan without disrupting production.",
             "Test in staging, partial failover, "
             "simulations, verify RPO/RTO."),
            ("design",
             "Design a secure three-tier architecture "
             "(web, app, database) in the cloud.",
             "Separate tiers, network controls, "
             "least privilege, monitoring."),
            ("practical",
             "Write a plan to decommission an old cloud "
             "environment safely.",
             "Inventory, backup decisions, shutdown "
             "order, verify dependencies, cost stop."),
            ("debugging",
             "A scheduled cloud job fails only on weekends. "
             "What are the likely causes?",
             "Maintenance windows, data freshness, "
             "timezone, capacity; reproduce with "
             "simulated conditions."),
        ],
    },

    # ----------------------------------------------------------------- 11
    "DevOps & Platform Engineering": {
        "category": [
            ("written_explanation",
             "Explain what DevOps is and how it changes the way "
             "development and operations teams work.",
             "Culture + practices (CI/CD, automation, "
             "observability, shared ownership); not just a tool."),
            ("scenario",
             "A deployment pipeline is frequently failing late at "
             "night. Describe how you would improve reliability.",
             "Analyse failures, add tests, stabilise "
             "environments, improve feedback, reduce batch "
             "size."),
            ("design",
             "Design a CI/CD pipeline for a web application from "
             "commit to production.",
             "Build, test, security scan, staging deploy, "
             "approval gate, production deploy, rollback."),
            ("written_explanation",
             "Explain the difference between continuous delivery "
             "and continuous deployment.",
             "Delivery = ready to release automatically; "
             "deployment = released automatically; gate "
             "difference."),
            ("scenario",
             "A critical bug is found in production minutes after "
             "a deploy. Describe your response.",
             "Assess severity, rollback or hotfix, "
             "communicate, post-incident review, improve "
             "gates."),
            ("short_answer",
             "What is the difference between Docker and a "
             "container orchestrator like Kubernetes?",
             "Docker builds/runs containers; orchestrator "
             "manages them at scale (scheduling, "
             "networking, scaling)."),
            ("written_explanation",
             "Explain the concept of immutable infrastructure and "
             "its advantages.",
             "Servers/images never changed after creation; "
             "replace instead of patch; consistency and "
             "rollback."),
            ("design",
             "Design a Kubernetes deployment for a stateless web "
             "service with auto-scaling.",
             "Deployment, service, ingress, HPA, "
             "readiness probes, resource limits."),
            ("scenario",
             "A monitoring alert shows the release pipeline is "
             "blocked by a flaky test. How do you handle it?",
             "Investigate flakiness, quarantine or fix, "
             "prevent masking real failures, track."),
            ("short_answer",
             "What is the difference between a container image "
             "and a container?",
             "Image = immutable template; container = running "
             "instance of the image."),
            ("written_explanation",
             "Explain what infrastructure as code is and name the "
             "benefits over manual configuration.",
             "Versioned, reviewable, reproducible, "
             "auditable; tools like Terraform/Ansible."),
            ("design",
             "Design a secrets management approach for a "
             "CI/CD pipeline.",
             "Secret store, injection at runtime, no "
             "secrets in code or logs, rotation, "
             "least privilege."),
            ("scenario",
             "Developers complain that the pipeline takes 40 "
             "minutes. How do you reduce feedback time?",
             "Parallelise stages, cache dependencies, "
             "split test suites, faster machines, "
             "fail-fast."),
            ("written_explanation",
             "Explain the difference between blue-green and "
             "canary deployments.",
             "Blue-green = full switch between versions; "
             "canary = gradual percentage rollout with "
             "monitoring."),
            ("short_answer",
             "What is a service mesh and what problems does it "
             "solve?",
             "Sidecar proxies for traffic, observability, "
             "security between services; mTLS, tracing."),
            ("design",
             "Design a monitoring and alerting strategy for a "
             "microservices platform.",
             "Metrics, logs, traces (observability), "
             "SLOs, alerting with meaningful thresholds."),
            ("scenario",
             "A team wants to skip the staging environment to "
             "ship faster. How do you respond?",
             "Understand their pain, propose alternatives "
             "(ephemeral environments, better tests), "
             "protect quality gates."),
            ("written_explanation",
             "Explain the concept of 'shift left' in DevOps and "
             "give examples.",
             "Move quality/security/performance checks "
             "earlier in the pipeline; testing, linting, "
             "security at commit time."),
            ("short_answer",
             "What is the difference between a Dockerfile and "
             "docker-compose?",
             "Dockerfile = image build recipe; compose = "
             "multi-container orchestration definition."),
            ("design",
             "Design an on-call and incident response process for "
             "a platform team.",
             "Alert routing, severity levels, escalation, "
             "runbooks, blameless post-mortems."),
        ],
        "position": [
            ("written_explanation",
             "As a DevOps engineer, explain how you would onboard "
             "a new service into the existing CI/CD platform.",
             "Repository setup, pipeline template, "
             "environments, monitoring, documentation."),
            ("scenario",
             "A build is failing due to an outdated dependency. "
             "Describe how you handle dependency management.",
             "Renovate/dependabot, pinning strategy, "
             "update cadence, security scanning."),
            ("short_answer",
             "What is the difference between a Docker volume and "
             "a bind mount?",
             "Volume = managed by Docker; bind = host "
             "directory; persistence and portability."),
            ("design",
             "Design a deployment strategy for a database schema "
             "change in a continuous delivery world.",
             "Expand-contract migrations, backwards "
             "compatibility, rollback plan, dual-write "
             "phases."),
            ("written_explanation",
             "Explain how you would debug a container that "
             "starts then immediately exits.",
             "Check logs, entrypoint, exit codes, resource "
             "limits, health checks, run interactively."),
            ("debugging",
             "A Kubernetes pod is stuck in CrashLoopBackOff. "
             "Describe your diagnosis.",
             "Describe pod, logs, events, resource "
             "limits, image issues, config."),
            ("short_answer",
             "What is the difference between a ReplicaSet and a "
             "Deployment in Kubernetes?",
             "ReplicaSet = desired pod count; Deployment = "
             "manages ReplicaSets and rolling updates."),
            ("design",
             "Design a backup strategy for stateful workloads in "
             "Kubernetes.",
             "Volume snapshots, database backups, "
             "restore testing, disaster recovery."),
            ("written_explanation",
             "Explain how you would implement feature flags in a "
             "deployment pipeline.",
             "Flag service, gradual rollout, kill switch, "
             "flag lifecycle cleanup."),
            ("scenario",
             "A developer deployed directly to production "
             "bypassing the pipeline. How do you respond?",
             "Assess what happened, restore control "
             "(permissions, branch protection), "
             "communicate, improve guardrails."),
            ("short_answer",
             "What is the difference between observability and "
             "monitoring?",
             "Monitoring = known indicators; observability = "
             "explore unknown failure modes via logs, "
             "metrics, traces."),
            ("design",
             "Design a CI pipeline matrix for a project that "
             "must support three operating systems and two "
             "language versions.",
             "Matrix strategy, caching, parallel jobs, "
             "coverage of all combinations."),
            ("written_explanation",
             "Explain how you would secure a CI/CD pipeline "
             "from supply-chain attacks.",
             "Signed images, lock dependencies, scan "
             "artifacts, least-privilege secrets, "
             "review permissions."),
            ("debugging",
             "Deployments succeed but traffic goes to the old "
             "version. What might be wrong?",
             "Ingress/service selector mismatch, image "
             "tag issue, cache, rollout state."),
            ("short_answer",
             "What is the difference between a service and an "
             "ingress in Kubernetes?",
             "Service = internal load balancing; ingress = "
             "external HTTP routing rules."),
            ("design",
             "Design a self-service platform where developers "
             "can deploy their own services safely.",
             "Templates, guardrails, automated checks, "
             "permissions, audit."),
            ("written_explanation",
             "Explain how you would handle log management for a "
             "microservices platform.",
             "Centralised logging, structured logs, "
             "retention, correlation IDs, access."),
            ("scenario",
             "A vendor library in your pipeline has a known "
             "vulnerability but upgrading breaks the build. "
             "How do you proceed?",
             "Assess exposure, plan upgrade with fixes, "
             "interim mitigation, track deadline."),
            ("short_answer",
             "What is the difference between a linter, a formatter "
             "and a type checker?",
             "Lint = potential issues; format = style; "
             "type check = type correctness; all shift "
             "left."),
            ("design",
             "Design a release management calendar and "
             "communication plan for a team shipping weekly.",
             "Freeze windows, release notes, "
             "communication channels, rollback "
             "procedures."),
        ],
        "practical": [
            ("practical",
             "Write a Dockerfile (or describe it) for a small "
             "Node.js application optimised for size and "
             "security.",
             "Multi-stage build, non-root user, pinned "
             "base image, minimal layers."),
            ("design",
             "Design a Kubernetes namespace strategy for "
             "environments (dev, staging, prod) with resource "
             "limits.",
             "Namespace per env, quotas, limits, labels, "
             "network policies."),
            ("practical",
             "Describe the commands you would run to inspect a "
             "failing container and its logs.",
             "docker ps, logs, inspect, exec; correlate "
             "with events."),
            ("debugging",
             "A Kubernetes service returns connection refused. "
             "Describe your diagnosis.",
             "Check pods running, labels/selectors, "
             "ports, endpoints, network policies."),
            ("practical",
             "Write a CI pipeline stage (YAML/pseudo) that "
             "builds, tests and caches dependencies.",
             "Correct order, caching for speed, "
             "fail-fast, artifact output."),
            ("design",
             "Design a Terraform (or similar IaC) layout for a "
             "small project with environments.",
             "Module structure, state management, "
             "workspaces, variable handling."),
            ("practical",
             "Describe how you would roll back a bad Kubernetes "
             "deployment.",
             "Rollout undo, verify, decide fix forward "
             "vs rollback."),
            ("debugging",
             "A pod cannot pull its image. List the likely "
             "causes and checks.",
             "Image name/tag, registry access, "
             "credentials, network, quota."),
            ("practical",
             "Write a script (pseudo-code) that checks "
             "container health and restarts unhealthy ones.",
             "Health check logic, restart policy, "
             "alerting, avoid flapping."),
            ("design",
             "Design a canary release pipeline with automated "
             "analysis of the canary's health.",
             "Percentage shifts, metric comparison, "
             "auto-rollback, logging."),
            ("practical",
             "Describe how you would back up and restore an "
             "etcd (or similar) cluster.",
             "Snapshot, restore procedure, testing, "
             "disaster recovery."),
            ("debugging",
             "A deployment is slow to scale during a traffic "
             "spike. What are the bottlenecks?",
             "Image pull, resource limits, quota, "
             "scheduler, registry; fix accordingly."),
            ("practical",
             "Write a checklist for a new environment setup "
             "(namespaces, secrets, monitoring).",
             "Complete and ordered setup steps, "
             "verification, documentation."),
            ("design",
             "Design a strategy for zero-downtime database "
             "schema migrations in production.",
             "Expand/contract, feature flags, "
             "backward-compatible releases."),
            ("practical",
             "Describe how you would add an alert that fires "
             "when error rate exceeds 1% for 5 minutes.",
             "Metric definition, threshold, window, "
             "severity, runbook link."),
            ("debugging",
             "A container is using far more memory than "
             "expected. How do you investigate?",
             "Profiling, logs, leak checks, limits, "
             "compare versions."),
            ("practical",
             "Write a runbook for a failed production deploy "
             "rollback.",
             "Detection, decision, rollback steps, "
             "verification, communication."),
            ("design",
             "Design a Git branching and release strategy "
             "for a team of 10.",
             "Trunk-based or GitFlow choice, protected "
             "branches, release process."),
            ("practical",
             "Describe how you would set up cross-environment "
             "configuration (dev/staging/prod) safely.",
             "Config management, environment variables, "
             "secrets, validation."),
            ("debugging",
             "A nightly pipeline job fails intermittently "
             "with a network error. How do you make it "
             "reliable?",
             "Retries with backoff, idempotency, "
             "dependency checks, better error "
             "handling."),
        ],
    },

    # ----------------------------------------------------------------- 12
    "Quality Assurance & Software Testing": {
        "category": [
            ("written_explanation",
             "Explain the difference between verification and "
             "validation in software testing.",
             "Verification = building the product right; "
             "validation = building the right product."),
            ("scenario",
             "A developer says a bug is 'not a bug, it's a "
             "feature request'. How do you determine the truth?",
             "Refer to requirements/acceptance criteria, "
             "reproduce, discuss with stakeholders, "
             "document the decision."),
            ("design",
             "Design a test strategy for a new e-commerce "
             "website. Describe the levels and types of "
             "testing you would include.",
             "Unit, integration, system, UAT; functional, "
             "performance, security, usability, "
             "accessibility."),
            ("written_explanation",
             "Explain the difference between black-box and "
             "white-box testing.",
             "Black-box = without code knowledge; white-box = "
             "with code/structure knowledge; when each is "
             "used."),
            ("scenario",
             "A critical bug is found on the day of release. "
             "How do you decide whether to block the release?",
             "Assess severity and impact, options "
             "(fix/hotfix/defer), risk-based decision "
             "with stakeholders, document."),
            ("short_answer",
             "What is the difference between a bug, a defect "
             "and a failure?",
             "Bug = error in code; defect = deviation from "
             "requirement; failure = observable wrong "
             "behaviour."),
            ("written_explanation",
             "Explain what regression testing is and why it "
             "matters.",
             "Re-testing after changes to catch "
             "unintended breakage; prioritised and "
             "automated where possible."),
            ("design",
             "Design a test case for a login page, listing the "
             "key scenarios including negative ones.",
             "Valid login, wrong password, locked account, "
             "empty fields, injection attempts, "
             "remember-me."),
            ("scenario",
             "Automated tests pass locally but fail in the "
             "pipeline. How do you investigate?",
             "Compare environments, data, timing, "
             "flakiness; reproduce; fix root cause."),
            ("short_answer",
             "What is the difference between a test plan and a "
             "test case?",
             "Plan = strategy/scope/resources; case = "
             "specific inputs, steps, expected results."),
            ("written_explanation",
             "Explain the concept of test coverage and its "
             "limitations.",
             "Measures what was exercised (lines, branches, "
             "requirements); high coverage does not mean "
             "good tests."),
            ("design",
             "Design a performance test plan for a web "
             "application expected to handle 10,000 concurrent "
             "users.",
             "Load, stress, endurance, spike tests; "
             "metrics (response, throughput, errors); "
             "baselines."),
            ("scenario",
             "A developer argues unit tests are enough and "
             "integration tests are a waste. How do you "
             "respond?",
             "Explain what each catches, the test "
             "pyramid, risk of gaps between "
             "components."),
            ("written_explanation",
             "Explain the difference between a smoke test and "
             "a sanity test.",
             "Smoke = quick check of core functions "
             "after build; sanity = focused check after "
             "specific changes."),
            ("short_answer",
             "What is the difference between error handling and "
             "exception testing?",
             "Error handling = code behaviour on errors; "
             "exception testing = verifying that "
             "behaviour via test cases."),
            ("design",
             "Design an accessibility test checklist for a "
             "public website.",
             "Keyboard navigation, screen reader, "
             "contrast, labels, focus states, "
             "WCAG criteria."),
            ("scenario",
             "A stakeholder wants to skip testing to meet a "
             "deadline. How do you communicate the risk?",
             "Quantify risk (defect leakage, cost of "
             "fixing later), propose a risk-based "
             "reduced scope, document acceptance."),
            ("written_explanation",
             "Explain the test pyramid and how it guides "
             "test automation investment.",
             "Many unit tests, fewer integration, fewest "
             "E2E; speed and cost rationale."),
            ("short_answer",
             "What is the difference between a defect report "
             "and a bug report?",
             "Same concept; defect report includes "
             "severity, steps, environment, evidence "
             "and priority."),
            ("design",
             "Design a test data management strategy for a "
             "team testing a customer-facing app.",
             "Masked production data, synthetic "
             "datasets, environment-specific data, "
             "refresh processes."),
        ],
        "position": [
            ("written_explanation",
             "As a QA engineer, describe your process for "
             "testing a new feature from handoff to sign-off.",
             "Understand requirements, test planning, "
             "test case design, execution, defect "
             "reporting, sign-off."),
            ("scenario",
             "You find a bug that only occurs with a specific "
             "browser version. How do you report and handle "
             "it?",
             "Document environment specifics, "
             "reproduce, assess impact, prioritise, "
             "verify fix across browsers."),
            ("short_answer",
             "What is the difference between a test case and a "
             "test script?",
             "Case = manual steps/expected results; "
             "script = automated code executing the "
             "test."),
            ("design",
             "Design an automation framework structure for a "
             "web application (page objects, utilities).",
             "Layers (page objects, helpers, tests), "
             "configuration, reporting, CI "
             "integration."),
            ("written_explanation",
             "Explain how you would test a mobile application "
             "across devices and OS versions.",
             "Device matrix, emulators vs real devices, "
             "cloud device farms, prioritisation by "
             "usage."),
            ("debugging",
             "An automated test is flaky - passes sometimes, "
             "fails sometimes. Describe your approach.",
             "Identify the variable (timing, state, "
             "order), stabilise with waits/cleanup, "
             "isolate and fix root cause."),
            ("short_answer",
             "What is the difference between a bug's severity "
             "and its priority?",
             "Severity = impact; priority = urgency of "
             "fix; a cosmetic bug can be high "
             "priority."),
            ("design",
             "Design a release gate checklist for a mobile "
             "app store submission.",
             "Functionality, crash-free rate, privacy, "
             "store guidelines, metadata, rollback."),
            ("written_explanation",
             "Explain how you would test an API, including "
             "what you validate.",
             "Status codes, payloads, schema, error "
             "handling, security, performance, "
             "contracts."),
            ("scenario",
             "A developer fixes a bug but the fix breaks "
             "another feature. How do you handle the "
             "regression?",
             "Report regression with evidence, "
             "coordinate, add regression tests, "
             "verify both."),
            ("short_answer",
             "What is the difference between exploratory "
             "testing and scripted testing?",
             "Exploratory = simultaneous learning and "
             "testing; scripted = pre-defined steps; "
             "both valuable."),
            ("design",
             "Design a test environment strategy for a team "
             "with dev, staging and production.",
             "Environment purpose, parity, data "
             "handling, deployment triggers, "
             "isolation."),
            ("written_explanation",
             "Explain how you would prioritise which "
             "regression tests to automate first.",
             "Risk, frequency of use, business "
             "criticality, flakiness, cost."),
            ("debugging",
             "A defect cannot be reproduced in the test "
             "environment. What do you do?",
             "Gather more detail from production, "
             "check environment differences, "
             "instrument, collaborate with "
             "developers."),
            ("short_answer",
             "What is the difference between a stubbed test "
             "and a mocked test?",
             "Stub = fixed responses; mock = verifies "
             "interactions; when each is "
             "appropriate."),
            ("design",
             "Design a UAT (user acceptance testing) plan "
             "for a new system.",
             "User scenarios, acceptance criteria, "
             "participant selection, sign-off "
             "process."),
            ("written_explanation",
             "Explain how you would test a system's security "
             "from a QA perspective.",
             "Security test cases (auth, authorisation, "
             "input validation, session handling), "
             "coordinate with security team."),
            ("scenario",
             "You disagree with a developer who says a bug "
             "is acceptable behaviour. How do you resolve "
             "it?",
             "Refer to the requirement, reproduce with "
             "evidence, escalate to product owner, "
             "document."),
            ("short_answer",
             "What is the difference between compatibility "
             "testing and interoperability testing?",
             "Compatibility = works with intended "
             "environments; interoperability = works "
             "with other systems."),
            ("design",
             "Design a QA process for a continuous delivery "
             "team shipping multiple times a day.",
             "Automation coverage, risk-based "
             "selection, fast feedback, smoke tests "
             "in pipeline."),
        ],
        "practical": [
            ("practical",
             "Write a test case for a shopping cart 'add to "
             "cart' feature including expected results for "
             "five scenarios.",
             "Valid, duplicate, out of stock, "
             "guest, quantity limits."),
            ("design",
             "Design a smoke test suite for a web app's core "
             "journey (login -> browse -> purchase).",
             "Core journey covered, quick, reliable, "
             "pipeline-integrated."),
            ("practical",
             "Describe how you would write a bug report that "
             "a developer can act on immediately.",
             "Title, steps, expected/actual, "
             "environment, evidence, severity."),
            ("debugging",
             "A test suite takes 45 minutes and slows the "
             "pipeline. Describe your optimisation.",
             "Parallelise, drop flaky/duplicate, "
             "shorter scenarios, faster waits, "
             "prioritise."),
            ("practical",
             "Write pseudo-code for a data-driven test that "
             "runs the same login flow with multiple input "
             "sets.",
             "Parameterised test, readable data, "
             "clear failure messages."),
            ("design",
             "Design a performance test scenario for a "
             "checkout flow (load profile, metrics, pass "
             "criteria).",
             "Realistic load profile, metrics "
             "(response, error, throughput), pass "
             "criteria."),
            ("practical",
             "Describe how you would verify a fix for a "
             "date-related bug that only occurs on 29 "
             "February.",
             "Test with simulated dates, boundary "
             "analysis, timezone handling."),
            ("debugging",
             "Tests pass with one dataset but fail with "
             "another. What is the likely cause and how "
             "do you fix it?",
             "Test data assumptions, hidden "
             "dependencies, ordering; fix data "
             "fixtures."),
            ("practical",
             "Write a checklist for testing a password "
             "reset flow end to end.",
             "Request, email delivery, link "
             "expiry, reuse, new login."),
            ("design",
             "Design an API test suite for a user "
             "registration endpoint (valid, invalid, "
             "duplicate, security).",
             "Coverage of positive/negative/security "
             "cases with assertions."),
            ("practical",
             "Describe how you would test file upload "
             "functionality comprehensively.",
             "Types, sizes, invalid files, "
             "permissions, virus/scan, large "
             "files, concurrent."),
            ("debugging",
             "A UI automation test clicks a button that is "
             "sometimes not ready. Describe the fix.",
             "Explicit waits, condition checks, "
             "avoid sleeps, stable selectors."),
            ("practical",
             "Write the steps to perform a smoke test of a "
             "new build in five minutes.",
             "Prioritised quick checks of core "
             "functions, scripted, repeatable."),
            ("design",
             "Design a test matrix for a form with three "
             "fields (required, format, length).",
             "Coverage of combinations, boundary "
             "values, validation messages."),
            ("practical",
             "Describe how you would measure and report test "
             "progress to management.",
             "Metrics (executed, passed, failed, "
             "blocked, defects), trend, "
             "risk."),
            ("debugging",
             "A defect appears only on the first run of the "
             "day. What might cause it and how do you "
             "confirm?",
             "State pollution, scheduled jobs, "
             "time-dependent logic; reproduce "
             "under same conditions."),
            ("practical",
             "Write a test plan outline for a one-week "
             "release cycle.",
             "Scope, schedule, resources, risks, "
             "exit criteria."),
            ("design",
             "Design a regression suite that runs in under "
             "10 minutes for a medium web app.",
             "Prioritised critical paths, parallel "
             "execution, mocked external "
             "dependencies."),
            ("practical",
             "Describe how you would test pagination "
             "behaviour including edge cases.",
             "First/last page, page size changes, "
             "empty results, rapid "
             "navigation."),
            ("debugging",
             "A test environment is unreliable and tests "
             "fail randomly. Describe how you restore "
             "trust in the environment.",
             "Stabilise environment, isolate "
             "failures, fix root causes, "
             "document, monitor."),
        ],
    },

    # ----------------------------------------------------------------- 13
    "Business & Systems Analysis": {
        "category": [
            ("written_explanation",
             "Explain the role of a business analyst in a "
             "technology project and how they add value.",
             "Bridges business and technical teams; "
             "elicits requirements, analyses processes, "
             "validates solutions."),
            ("scenario",
             "Stakeholders disagree on the requirements for a "
             "new system. How do you facilitate a decision?",
             "Understands each position, finds "
             "underlying needs, facilitates a "
             "workshop, prioritises, documents the "
             "decision."),
            ("design",
             "Design a requirements elicitation plan for a new "
             "customer portal. What techniques and "
             "stakeholders?",
             "Interviews, workshops, document "
             "analysis, surveys, observation; "
             "right stakeholders identified."),
            ("written_explanation",
             "Explain the difference between functional and "
             "non-functional requirements, with examples of "
             "each.",
             "Functional = what system does; "
             "non-functional = how (performance, "
             "security, usability)."),
            ("scenario",
             "A requirement is feasible but very expensive. "
             "How do you communicate the trade-off to "
             "stakeholders?",
             "Presents options with cost/benefit, "
             "proposes alternatives, lets business "
             "decide, documents."),
            ("short_answer",
             "What is the difference between a stakeholder and "
             "a user?",
             "Stakeholder = anyone affected/with "
             "interest; user = someone who uses the "
             "system; overlap."),
            ("written_explanation",
             "Explain the difference between a BRD (business "
             "requirements document) and an FRD (functional "
             "requirements document).",
             "BRD = business needs/objectives; FRD = "
             "detailed functional behaviour."),
            ("design",
             "Design a business process for handling customer "
             "refunds, including decision points.",
             "Clear swimlanes, decision criteria, "
             "escalation, SLA, system touchpoints."),
            ("scenario",
             "A project is over budget and behind schedule. As "
             "the analyst, how do you help?",
             "Revisit scope, identify waste and "
             "rework, clarify requirements, "
             "reprioritise, communicate."),
            ("written_explanation",
             "Explain what a use case is and its key "
             "components.",
             "Actor, goal, preconditions, main flow, "
             "alternate flows; describes "
             "interaction."),
            ("short_answer",
             "What is the difference between an 'as-is' and a "
             "'to-be' process model?",
             "Current state vs future state; "
             "gap analysis between them."),
            ("design",
             "Design a user story with acceptance criteria for "
             "a 'change password' feature.",
             "Well-formed story, clear acceptance "
             "criteria, edge cases covered."),
            ("scenario",
             "A developer implements a feature differently "
             "from the documented requirement. How do you "
             "handle the discrepancy?",
             "Compare against requirement, discuss "
             "with both sides, update either "
             "implementation or requirement with "
             "approval, document."),
            ("written_explanation",
             "Explain the difference between a functional "
             "specification and a design document.",
             "Spec = what to build; design = how to "
             "build it; separate audiences."),
            ("design",
             "Design a data flow diagram for an order "
             "processing system.",
             "External entities, processes, data "
             "stores, data flows - correct and "
             "readable."),
            ("scenario",
             "A stakeholder requests a change after "
             "requirements are signed off. How do you manage "
             "it?",
             "Impact analysis, change request "
             "process, cost/timeline update, "
             "approval, update documentation."),
            ("written_explanation",
             "Explain the difference between a requirement and "
             "a constraint.",
             "Requirement = what is needed; "
             "constraint = limitation (budget, "
             "time, tech, regulation)."),
            ("short_answer",
             "What is the difference between a swimlane "
             "diagram and a flow chart?",
             "Flow chart = process steps; swimlane = "
             "steps assigned to actors/departments."),
            ("design",
             "Design a requirements traceability approach so "
             "every requirement is linked to tests and "
             "deliverables.",
             "Traceability matrix, tooling, "
             "review points, coverage."),
            ("written_explanation",
             "Explain how you validate that a delivered "
             "solution meets the business need.",
             "Acceptance testing, UAT, benefit "
             "measurement, feedback loop, "
             "lessons learned."),
        ],
        "position": [
            ("written_explanation",
             "As a business analyst, describe how you run a "
             "requirements workshop from preparation to "
             "follow-up.",
             "Agenda, participants, facilitation "
             "techniques, outputs, actions, "
             "validation."),
            ("scenario",
             "You are asked to analyse why a sales process is "
             "inefficient. Describe your approach.",
             "Map the current process, gather data, "
             "interview stakeholders, identify "
             "bottlenecks, recommend changes with "
             "benefits."),
            ("short_answer",
             "What is the difference between a business "
             "process model and a process map?",
             "Model = formal representation; map = "
             "visual summary; similar but different "
             "depth."),
            ("design",
             "Design a requirements document template for a "
             "software project.",
             "Sections: background, scope, "
             "functional/non-functional, "
             "assumptions, acceptance criteria."),
            ("written_explanation",
             "Explain how you would elicit requirements from "
             "users who do not know what they want.",
             "Show prototypes, walk through "
             "scenarios, ask about goals not "
             "features, iterate."),
            ("debugging",
             "A process change caused a drop in customer "
             "satisfaction. How do you investigate?",
             "Gather data (surveys, tickets), "
             "compare before/after, find the "
             "change's impact, recommend "
             "adjustments."),
            ("short_answer",
             "What is the difference between a user story and "
             "a use case?",
             "Story = short goal-oriented; use case "
             "= detailed interaction steps; "
             "different levels of detail."),
            ("design",
             "Design a gap analysis for a company moving "
             "from spreadsheets to a CRM.",
             "As-is/to-be comparison, missing "
             "capabilities, data migration, "
             "training needs."),
            ("written_explanation",
             "Explain how you would write acceptance criteria "
             "that developers and testers can both use.",
             "Testable, unambiguous, complete, "
             "with boundaries."),
            ("scenario",
             "Two departments want the same system built "
             "differently. How do you find common ground?",
             "Identify shared underlying goals, "
             "design reusable core with "
             "configurable differences, "
             "prioritise."),
            ("short_answer",
             "What is the difference between a data flow "
             "diagram and a process flow diagram?",
             "DFD = data movement and stores; PFD = "
             "process steps and sequence."),
            ("design",
             "Design an approach for estimating the effort of "
             "a new feature at the requirements stage.",
             "Decomposition, historical "
             "benchmarks, assumptions, "
             "contingency, review."),
            ("written_explanation",
             "Explain the difference between qualitative and "
             "quantitative requirements evidence.",
             "Qualitative = interviews/opinions; "
             "quantitative = metrics/data; both "
             "support decisions."),
            ("debugging",
             "A new system meets all requirements but users "
             "will not adopt it. How do you analyse why?",
             "Usability, training, change "
             "management, workflow fit; "
             "investigate and address."),
            ("short_answer",
             "What is the difference between a backlog item "
             "and a requirement?",
             "Requirement = need; backlog item = "
             "sized, prioritised unit of work "
             "derived from requirements."),
            ("design",
             "Design a stakeholder analysis and communication "
             "plan for a system rollout.",
             "Identify stakeholders, their "
             "interest/influence, communication "
             "cadence and channels."),
            ("written_explanation",
             "Explain how you would document a complex "
             "business rule so it is unambiguous.",
             "Decision tables, precise language, "
             "examples, validation with "
             "business."),
            ("scenario",
             "A vendor solution covers 80% of requirements. "
             "How do you analyse buy vs build?",
             "Compare total cost, fit, "
             "customisation, maintenance, "
             "risk; structured decision."),
            ("short_answer",
             "What is the difference between a feasibility "
             "study and a business case?",
             "Feasibility = can we do it; business "
             "case = should we, with costs and "
             "benefits."),
            ("design",
             "Design a benefits realisation plan for a new "
             "system.",
             "Baseline, target benefits, "
             "measurement method, owners, "
             "review dates."),
        ],
        "practical": [
            ("practical",
             "Write a user story and three acceptance criteria "
             "for a 'search by location' feature.",
             "Story format, testable criteria, "
             "edge cases."),
            ("design",
             "Draw (describe) a swimlane diagram for an "
             "invoice approval process involving employee, "
             "manager and finance.",
             "Correct lanes, steps, decision "
             "points, handoffs."),
            ("practical",
             "Write the questions you would ask in a "
             "stakeholder interview for a reporting system "
             "upgrade.",
             "Goal-focused, open-ended, "
             "prioritisation and constraint "
             "questions."),
            ("debugging",
             "A process takes 4 days but the target is 2. "
             "Describe how you would find where the time "
             "goes.",
             "Time-mapping, waiting times, "
             "bottlenecks, rework; data-driven."),
            ("practical",
             "Create a decision table for a discount policy "
             "(member status x order value x season).",
             "Complete conditions, no gaps, "
             "unambiguous rules."),
            ("design",
             "Design a requirements traceability matrix "
             "template.",
             "Requirement, source, design, test, "
             "status links."),
            ("practical",
             "Write a change request template for a "
             "mid-project change.",
             "Description, reason, impact, "
             "cost/timeline, approval."),
            ("debugging",
             "Two systems report different customer counts. "
             "How do you investigate as an analyst?",
             "Definitions, timing, data sources, "
             "filters; reconcile and "
             "document."),
            ("practical",
             "Describe how you would run a requirements "
             "prioritisation session (MoSCoW or similar).",
             "Method, criteria, facilitation, "
             "output, follow-up."),
            ("design",
             "Design an 'as-is' to 'to-be' comparison for "
             "a manual timesheet process being automated.",
             "Both flows, pain points, "
             "automation benefits, migration "
             "steps."),
            ("practical",
             "Write acceptance criteria for a search feature "
             "that must handle accents and partial words.",
             "Specific, testable, covers "
             "matching rules."),
            ("debugging",
             "A requirement was misunderstood and the system "
             "was built wrong. How do you prevent recurrence?",
             "Root-cause the gap, improve "
             "validation (walkthroughs, "
             "prototypes), traceability."),
            ("practical",
             "Describe how you would measure the business "
             "impact of a process improvement you "
             "recommended.",
             "Baseline vs after, key metrics, "
             "owners, review."),
            ("design",
             "Design a data dictionary template for a "
             "system's key data elements.",
             "Name, definition, type, source, "
             "owner, rules."),
            ("practical",
             "Write a one-page requirements summary for a "
             "mobile app that non-technical executives "
             "will read.",
             "Clear, concise, goal-focused, "
             "no jargon."),
            ("debugging",
             "A report shows sales are down but the sales "
             "team disagrees. How do you validate?",
             "Check data pipeline, definitions, "
             "timing, filters; reconcile with "
             "source."),
            ("practical",
             "Describe how you would facilitate a "
             "brainstorming session that produces "
             "prioritised ideas.",
             "Divergence then convergence, "
             "voting, criteria, actions."),
            ("design",
             "Design a process for handling requirement "
             "changes during development.",
             "Change intake, impact analysis, "
             "approval, communication, "
             "traceability update."),
            ("practical",
             "Write a stakeholder communication plan for "
             "a weekly project status.",
             "Audience, content, cadence, "
             "channel, owner."),
            ("debugging",
             "A process works in one branch but not "
             "another. As an analyst, how do you find the "
             "difference?",
             "Compare processes step by step, "
             "find variations, standardise or "
             "accommodate."),
        ],
    },
}
