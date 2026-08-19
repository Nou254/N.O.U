"""
Unique category / position / practical questions for the question banks.
"""

CATS = {
    # ----------------------------------------------------------------- 18
    "IoT & Embedded Systems": {
        "category": [
            ("written_explanation",
             "Explain what an IoT system is and describe the main "
             "components of a typical IoT architecture.",
             "Sensors/devices, connectivity, edge/gateway, "
             "cloud/platform, application; data flow."),
            ("scenario",
             "A smart device in the field stops reporting data. "
             "Describe how you would diagnose the problem "
             "remotely.",
             "Connectivity check, device power, firmware, "
             "gateway, server-side, network path; "
             "escalate with evidence."),
            ("design",
             "Design an IoT solution for monitoring "
             "temperature in a cold chain (food storage). "
             "Describe sensors, connectivity and alerts.",
             "Sensor selection, battery/power, "
             "connectivity (LoRa/Wi-Fi/cellular), "
             "threshold alerts, data storage, "
             "reliability."),
            ("written_explanation",
             "Explain the difference between edge computing and "
             "cloud computing in an IoT context.",
             "Edge = local processing near devices; cloud "
             "= centralised; latency, bandwidth, "
             "reliability trade-offs."),
            ("scenario",
             "An IoT device is hacked and used in a botnet. "
             "How do you respond and prevent recurrence?",
             "Containment, credential rotation, "
             "firmware updates, network isolation, "
             "security by design."),
            ("short_answer",
             "What is the difference between a sensor and an "
             "actuator?",
             "Sensor = measures environment; actuator = "
             "takes action; example of each."),
            ("written_explanation",
             "Explain how an IoT device communicates with a "
             "server using MQTT, and why MQTT is popular for "
             "IoT.",
             "Publish/subscribe, broker, topics, "
             "lightweight, works on unreliable "
             "networks."),
            ("design",
             "Design a battery-powered IoT sensor that must "
             "run for two years on two AA batteries.",
             "Low-power modes, duty cycling, "
             "efficient radio, energy budget "
             "calculation."),
            ("scenario",
             "A firmware update bricks some devices in the "
             "field. Describe your response.",
             "Assess scope, rollback path, safe "
             "recovery (bootloader), communicate, "
             "improve update process."),
            ("written_explanation",
             "Explain the concept of device provisioning and "
             "onboarding in an IoT platform.",
             "Identity, certificates/keys, secure "
             "registration, fleet management."),
            ("short_answer",
             "What is the difference between LoRaWAN, Wi-Fi "
             "and cellular IoT connectivity?",
             "Range/power/bandwidth trade-offs; "
             "selection by use case."),
            ("design",
             "Design the data pipeline for an IoT fleet "
             "sending readings every minute.",
             "Ingestion, validation, storage "
             "(time-series), analytics, alerting, "
             "retention."),
            ("scenario",
             "An IoT device behaves differently in "
             "production than in the lab. How do you "
             "investigate?",
             "Environmental factors, network, "
             "firmware version, configuration, "
             "telemetry."),
            ("written_explanation",
             "Explain the security challenges specific to "
             "IoT devices.",
             "Limited resources, long lifecycles, "
             "physical access, updates, default "
             "credentials."),
            ("design",
             "Design an over-the-air (OTA) update strategy "
             "for a fleet of devices.",
             "Signed images, staged rollout, "
             "rollback, verification, "
             "bandwidth management."),
            ("short_answer",
             "What is the difference between a microcontroller "
             "and a system-on-chip (SoC) in IoT?",
             "MCU = embedded control; SoC = "
             "integrated processor (often with "
             "OS); use cases."),
            ("written_explanation",
             "Explain how you would handle time synchronisation "
             "and local buffering when IoT devices lose "
             "connectivity.",
             "Store-and-forward, timestamps, "
             "reconciliation, ordering on "
             "reconnect."),
            ("design",
             "Design a smart lighting control system for a "
             "building, including sensors and a central "
             "controller.",
             "Occupancy/light sensors, control "
             "logic, network, energy savings, "
             "manual override."),
            ("scenario",
             "A customer complains their smart device "
             "collects data they did not consent to. How do "
             "you respond?",
             "Explain data handling, provide "
             "controls/opt-out, review compliance, "
             "improve transparency."),
            ("written_explanation",
             "Explain how you would test an IoT device "
             "before mass deployment.",
             "Functional, environmental, network, "
             "security, battery, soak testing."),
        ],
        "position": [
            ("written_explanation",
             "As an embedded developer, describe your process "
             "for writing firmware that reads a sensor and "
             "sends it over a network.",
             "Driver init, sampling, buffering, "
             "protocol, error handling, power "
             "management."),
            ("scenario",
             "A firmware bug causes intermittent crashes. "
             "How do you find it without a debugger in the "
             "field?",
             "Logging, watchdog, fault capture, "
             "reproduce in lab, static analysis, "
             "fix."),
            ("short_answer",
             "What is the difference between an interrupt "
             "and polling in embedded systems?",
             "Event-driven vs continuous check; "
             "latency and CPU trade-offs."),
            ("design",
             "Design the firmware architecture for a device "
             "with three sensors and a display.",
             "Task scheduling, drivers, shared "
             "resources, power states, "
             "updateability."),
            ("written_explanation",
             "Explain how you would manage memory in a "
             "constrained embedded system.",
             "Static allocation, stack budgeting, "
             "leak detection, watchdog, "
             "determinism."),
            ("debugging",
             "A device reboots when the motor starts. "
             "Describe your diagnosis.",
             "Power drop, inrush current, EMI, "
             "brownout reset, decoupling."),
            ("short_answer",
             "What is the difference between FreeRTOS-style "
             "tasks and a bare-metal main loop?",
             "Preemptive scheduling vs sequential "
             "loop; responsiveness vs "
             "simplicity."),
            ("design",
             "Design a communication protocol between two "
             "embedded devices over UART with error "
             "checking.",
             "Framing, checksum, retries, "
             "timeouts, state machine."),
            ("written_explanation",
             "Explain how you would calibrate an embedded "
             "sensor and store the calibration.",
             "Reference measurement, coefficients, "
             "persistent storage, factory vs "
             "field."),
            ("scenario",
             "A competitor's device drains batteries slower. "
             "How do you improve power efficiency?",
             "Measure currents, sleep modes, "
             "duty cycle, radio power, "
             "optimise."),
            ("short_answer",
             "What is the difference between flash memory "
             "and RAM in embedded design?",
             "Non-volatile storage vs volatile "
             "runtime memory; wear and "
             "speed."),
            ("design",
             "Design a bootloader that allows safe firmware "
             "updates.",
             "Dual-bank or A/B, signed "
             "images, recovery mode, "
             "failure handling."),
            ("written_explanation",
             "Explain how you would test real-time "
             "behaviour of an embedded system.",
             "Timing analysis, oscilloscope, "
             "logic analyzer, stress tests."),
            ("debugging",
             "A sensor reads zero after a firmware update. "
             "How do you diagnose?",
             "Check config, GPIO init, driver, "
             "power, hardware; bisect "
             "changes."),
            ("short_answer",
             "What is the difference between I2C and CAN "
             "bus for embedded networking?",
             "Short-distance board vs robust "
             "automotive/industrial bus; "
             "speed and reliability."),
            ("design",
             "Design a device state machine (boot, run, "
             "sleep, error) for an IoT product.",
             "States, transitions, recovery, "
             "safe fallback."),
            ("written_explanation",
             "Explain how you would secure credentials on "
             "an embedded device.",
             "Secure element/TPM, encrypted "
             "storage, minimal exposure, "
             "rotation."),
            ("scenario",
             "A device in the field has corrupted flash. "
             "How do you recover it?",
             "Bootloader recovery, factory "
             "reset, re-flash, diagnostics."),
            ("short_answer",
             "What is the difference between watchdog and "
             "brownout protection?",
             "Software hang vs power dip "
             "protection; both needed."),
            ("design",
             "Design a firmware testing strategy including "
             "hardware-in-the-loop.",
             "Unit tests, simulated inputs, "
             "HIL rig, soak tests, CI."),
        ],
        "practical": [
            ("practical",
             "Write pseudo-code for reading a temperature "
             "sensor and publishing it every 60 seconds "
             "with power efficiency.",
             "Correct sampling, sleep between "
             "reads, error handling."),
            ("design",
             "Design a low-power schedule for a sensor that "
             "must last 6 months on a coin cell.",
             "Duty cycle, sleep modes, "
             "transmission budget."),
            ("practical",
             "Describe how you would debug an I2C "
             "communication failure between two boards.",
             "Pull-ups, addresses, logic "
             "levels, timing, scope "
             "capture."),
            ("debugging",
             "An IoT device connects to Wi-Fi but cannot "
             "reach the server. Describe your diagnosis.",
             "Network path, DNS, firewall, "
             "server status, certificate, "
             "logs."),
            ("practical",
             "Write a state machine (pseudo-code) for a "
             "smart lock with open/close/error states.",
             "Correct transitions, safety, "
             "timeouts."),
            ("design",
             "Design the message schema for a fleet "
             "telemetry system.",
             "Device ID, timestamp, metrics, "
             "units, versioning."),
            ("practical",
             "Describe how you would calculate the battery "
             "life of a device given a current profile.",
             "Energy budget, duty cycle "
             "math, capacity, derating."),
            ("debugging",
             "A device's clock drifts and timestamps are "
             "wrong. How do you fix it?",
             "RTC calibration, NTP/time "
             "sync, crystal accuracy."),
            ("practical",
             "Write pseudo-code for debouncing a button "
             "input in firmware.",
             "Timing-based debounce, state "
             "tracking."),
            ("design",
             "Design a sensor fusion approach for a device "
             "with temperature and humidity sensors.",
             "Combined calibration, cross-"
             "checks, plausibility."),
            ("practical",
             "Describe how you would add OTA update "
             "support to an existing device.",
             "Bootloader, signed "
             "images, rollback, "
             "bandwidth."),
            ("debugging",
             "A device consumes 10x expected current in "
             "sleep mode. How do you find the cause?",
             "Peripheral states, pull-ups, "
             "regulator quiescent, measure "
             "per section."),
            ("practical",
             "Write a ring buffer implementation "
             "(pseudo-code) for streaming sensor data.",
             "Correct head/tail, "
             "overflow handling."),
            ("design",
             "Design a device onboarding flow that is "
             "secure and user-friendly.",
             "QR code, secure key "
             "exchange, verification."),
            ("practical",
             "Describe how you would set up a test to "
             "verify a device survives 1000 power cycles.",
             "Automation, failure "
             "capture, criteria."),
            ("debugging",
             "Two devices on the same network cannot see "
             "each other. Describe your diagnosis.",
             "IP config, subnet, "
             "broker/topic, firewall."),
            ("practical",
             "Write pseudo-code for a watchdog feed loop "
             "that cannot mask a real hang.",
             "Feed at correct points, "
             "timeout bounds."),
            ("design",
             "Design a data retention and privacy plan for "
             "a home IoT product.",
             "What data, where stored, "
             "consent, deletion."),
            ("practical",
             "Describe how you would measure the wireless "
             "range and reliability of a device.",
             "Range tests, RSSI logging, "
             "environmental factors."),
            ("debugging",
             "A device fails only at 3 AM. What are the "
             "likely causes?",
             "Nightly jobs, temperature, "
             "power, network maintenance; "
             "correlate logs."),
        ],
    },

    # ----------------------------------------------------------------- 19
    "CCTV & Physical Security Technology": {
        "category": [
            ("written_explanation",
             "Explain the difference between analog and IP "
             "cameras, and the advantages of each.",
             "Coax vs network; resolution, "
             "management, scalability, cost."),
            ("scenario",
             "A customer wants CCTV coverage of a large "
             "parking lot. Describe your design approach.",
             "Site survey, camera types and "
             "coverage, lighting, recording, "
             "storage, budget."),
            ("design",
             "Design a CCTV system for a small office: "
             "cameras, DVR/NVR, storage and viewing.",
             "Camera placement, NVR/DVR choice, "
             "resolution and fps, retention, "
             "remote access."),
            ("written_explanation",
             "Explain the difference between resolution and "
             "frame rate, and their impact on image quality "
             "and storage.",
             "Resolution = detail; fps = smoothness; "
             "both affect storage sizing."),
            ("scenario",
             "A recording is missing during a critical "
             "incident. Describe your investigation.",
             "Check device, schedule, storage, "
             "network, power, firmware; identify "
             "root cause."),
            ("short_answer",
             "What is the difference between a DVR and an "
             "NVR?",
             "DVR = analog input, encodes; NVR = "
             "IP cameras, records streams."),
            ("written_explanation",
             "Explain the concept of camera coverage and "
             "field of view, and how you determine camera "
             "count for an area.",
             "FOV, focal length, overlap, blind "
             "spots, detection vs identification "
             "distances."),
            ("design",
             "Design a night-time surveillance solution "
             "for an unlit area.",
             "IR illumination, low-light sensors, "
             "lighting integration, camera "
             "selection."),
            ("scenario",
             "A client wants facial recognition on their "
             "cameras. How do you advise on feasibility, "
             "privacy and law?",
             "Technical requirements, accuracy "
             "limits, privacy/consent, legal "
             "compliance, alternatives."),
            ("written_explanation",
             "Explain how you would calculate storage needs "
             "for a CCTV system.",
             "Cameras x resolution x fps x codec x "
             "hours x retention; correct "
             "calculation."),
            ("short_answer",
             "What is the difference between a fixed camera "
             "and a PTZ camera?",
             "Fixed FOV vs pan/tilt/zoom; when "
             "each is appropriate."),
            ("design",
             "Design remote monitoring access for a "
             "business owner, including security.",
             "VPN or secure app, user accounts, "
             "2FA, no public exposure of "
             "recorders."),
            ("scenario",
             "A camera feed is blurry at night. Describe "
             "the likely causes and fixes.",
             "IR issues, focus, lens, sensor "
             "sensitivity, cleaning, lighting."),
            ("written_explanation",
             "Explain the difference between motion "
             "detection and continuous recording, and when "
             "to use each.",
             "Event-based vs always-on; storage "
             "and coverage trade-offs."),
            ("design",
             "Design an access control system for a "
             "building with 100 employees (doors, badges, "
             "zones).",
             "Readers, controllers, credential "
             "management, zones, audit, "
             "integration with cameras."),
            ("scenario",
             "An employee badge stops working. Describe "
             "the troubleshooting process.",
             "Credential validity, reader, "
             "wiring, controller, software, "
             "replacement."),
            ("written_explanation",
             "Explain how CCTV and access control systems "
             "should be integrated for effective "
             "security.",
             "Event correlation, alarm "
             "verification, investigation "
             "efficiency."),
            ("design",
             "Design a visitor management system for a "
             "corporate office.",
             "Registration, temporary badges, "
             "escort rules, record keeping."),
            ("scenario",
             "A break-in occurs despite cameras. How do you "
             "audit the security system afterward?",
             "Review footage, test devices, "
             "coverage gaps, response times, "
             "improvements."),
            ("written_explanation",
             "Explain the legal considerations of "
             "installing surveillance in a workplace.",
             "Consent/notice, privacy laws, data "
             "protection, retention, access."),
        ],
        "position": [
            ("written_explanation",
             "As a CCTV installer, describe the steps of a "
             "typical site installation from survey to "
             "handover.",
             "Survey, design, cabling, mounting, "
             "configuration, testing, "
             "documentation, training."),
            ("scenario",
             "A customer cannot access their cameras "
             "remotely. Describe your support process.",
             "Network check, port/app config, "
             "credentials, firmware, firewall, "
             "escalation."),
            ("short_answer",
             "What is the difference between H.264 and "
             "H.265 codecs?",
             "Compression efficiency; H.265 "
             "halves bandwidth/storage."),
            ("design",
             "Design a camera layout for a retail store "
             "that reduces blind spots.",
             "Entry/exit, cash registers, "
             "high-value areas, aisle coverage, "
             "camera overlap."),
            ("written_explanation",
             "Explain how you would configure recording "
             "schedules for different areas (always vs "
             "motion).",
             "Risk-based schedules, motion "
             "zones, storage balancing."),
            ("debugging",
             "An IP camera shows offline intermittently. "
             "Describe your diagnosis.",
             "PoE/power, network, cabling, "
             "switch ports, camera load, "
             "firmware."),
            ("short_answer",
             "What is the difference between PoE and "
             "separate power for cameras?",
             "Power over Ethernet vs dedicated "
             "supply; cabling and reliability."),
            ("design",
             "Design a backup and retention policy for "
             "recorded footage.",
             "Retention period, archival, "
             "cloud/offsite, legal "
             "requirements."),
            ("written_explanation",
             "Explain how you would set up multi-site "
             "monitoring for a company with five "
             "branches.",
             "Central VMS, network links, "
             "unified accounts, monitoring "
             "roles."),
            ("scenario",
             "A camera's image is frozen but the feed "
             "shows as online. How do you diagnose?",
             "Check stream vs device, network "
             "health, device hang, reboot, "
             "replace."),
            ("short_answer",
             "What is the difference between a dome and a "
             "bullet camera?",
             "Housing/use; dome = discreet, "
             "indoor; bullet = long range, "
             "outdoor."),
            ("design",
             "Design an alarm system for a house "
             "(sensors, panel, monitoring).",
             "Zone design, sensor placement, "
             "arming modes, monitoring, "
             "integration."),
            ("written_explanation",
             "Explain how you would ensure a surveillance "
             "system remains available during a power "
             "outage.",
             "UPS, generator, battery backup, "
             "tested failover."),
            ("debugging",
             "A recording has no audio even though the "
             "mic is enabled. Describe your diagnosis.",
             "Mic hardware, camera config, "
             "codec, permissions, volume."),
            ("short_answer",
             "What is the difference between a camera's "
             "optical and digital zoom?",
             "Lens vs software zoom; quality "
             "difference."),
            ("design",
             "Design a secure password and access policy "
             "for a surveillance system.",
             "Unique credentials, 2FA, least "
             "privilege, rotation, audit."),
            ("written_explanation",
             "Explain how you would test a camera's night "
             "performance before acceptance.",
             "Dark test, IR range, image "
             "quality, threshold."),
            ("scenario",
             "A customer asks to view footage of an "
             "employee's behaviour. How do you handle "
             "privacy?",
             "Explain access rules, "
             "authorisation, legal limits, "
             "document."),
            ("short_answer",
             "What is the difference between a wired and a "
             "wireless camera?",
             "Reliability/bandwidth vs "
             "installation ease; when each "
             "works."),
            ("design",
             "Design a maintenance schedule for a CCTV "
             "system.",
             "Cleaning, firmware, storage "
             "checks, health reports, "
             "replacements."),
        ],
        "practical": [
            ("practical",
             "Calculate storage for 8 cameras at 1080p, 15 "
             "fps, H.264, retained 30 days.",
             "Per-camera bitrate x time x "
             "count; correct math."),
            ("design",
             "Design a camera placement plan for a "
             "warehouse entrance and loading dock.",
             "Coverage, lighting, choke "
             "points, overlap."),
            ("practical",
             "Describe the steps to install and configure "
             "an IP camera on a network.",
             "Mount, cable, IP config, "
             "stream, NVR add, test."),
            ("debugging",
             "A PoE camera drops offline when a second "
             "device powers on. Describe the cause.",
             "PoE budget, injector power, "
             "cable quality, switch."),
            ("practical",
             "Write a site survey checklist for a new CCTV "
             "installation.",
             "Power, network, coverage, "
             "lighting, mounting, "
             "constraints."),
            ("design",
             "Design an access control zone layout for a "
             "two-floor office.",
             "Entry points, zone "
             "hierarchy, restricted areas."),
            ("practical",
             "Describe how you would configure motion "
             "detection zones to reduce false alarms.",
             "Zone drawing, sensitivity, "
             "exclusions, testing."),
            ("debugging",
             "A recording is choppy. Describe the likely "
             "causes.",
             "Storage speed, bandwidth, "
             "camera load, NVR load, "
             "codec."),
            ("practical",
             "Write a camera test procedure (day and "
             "night) before handover.",
             "Image quality, focus, IR, "
             "coverage, recording."),
            ("design",
             "Design a remote video verification workflow "
             "for a monitoring center.",
             "Alarm receipt, camera "
             "lookup, verification, "
             "response."),
            ("practical",
             "Describe how you would export footage "
             "legally for an investigation.",
             "Proper export, chain of "
             "custody, format, time "
             "sync."),
            ("debugging",
             "A badge reader beeps but the door does not "
             "unlock. Describe your diagnosis.",
             "Lock power, wiring, "
             "controller, request-to-exit, "
             "timing."),
            ("practical",
             "Write a checklist for commissioning a new "
             "access control door.",
             "Hardware, wiring, "
             "config, test modes, "
             "handover."),
            ("design",
             "Design a camera health monitoring dashboard "
             "for a fleet of 200 cameras.",
             "Online status, storage, "
             "errors, bandwidth, "
             "alerts."),
            ("practical",
             "Describe how you would secure a DVR/NVR "
             "from internet attacks.",
             "No port forwarding, VPN, "
             "updates, strong "
             "passwords, monitoring."),
            ("debugging",
             "A camera's timestamp is wrong. How do you "
             "fix it?",
             "Time sync, NTP, timezone, "
             "verify."),
            ("practical",
             "Write the steps to replace a failed camera "
             "with minimal downtime.",
             "Prep, swap, config "
             "restore, test, verify "
             "recording."),
            ("design",
             "Design an incident response runbook for a "
             "security alarm event.",
             "Verification, response, "
             "escalation, evidence, "
             "review."),
            ("practical",
             "Describe how you would test battery backup "
             "of a security system.",
             "Simulate outage, measure "
             "runtime, restore, log."),
            ("debugging",
             "Two cameras show a mirrored image. What is "
             "wrong and how do you fix it?",
             "Dome orientation, image "
             "flip/mirror setting, "
             "mounting."),
        ],
    },

    # ----------------------------------------------------------------- 20
    "Research, Development & Innovation": {
        "category": [
            ("written_explanation",
             "Explain the difference between basic research and "
             "applied research, with an example of each.",
             "Knowledge for its own sake vs solving a "
             "practical problem; coherent examples."),
            ("scenario",
             "Your proposed project idea is rejected by "
             "management. How do you respond and adapt?",
             "Seek feedback, refine the proposal, "
             "align with business goals, find "
             "champions, iterate."),
            ("design",
             "Design a research plan for evaluating whether "
             "a new technology should be adopted.",
             "Hypothesis, method, metrics, "
             "timeline, success criteria, risks."),
            ("written_explanation",
             "Explain the difference between a prototype and "
             "a proof of concept.",
             "PoC = feasibility; prototype = "
             "working model for evaluation; "
             "purposes differ."),
            ("scenario",
             "Your experiment results contradict your "
             "hypothesis. How do you handle it?",
             "Verify methodology, accept the data, "
             "reframe, report honestly."),
            ("short_answer",
             "What is the difference between quantitative and "
             "qualitative research methods?",
             "Numbers/measurement vs "
             "meaning/understanding; when each "
             "applies."),
            ("written_explanation",
             "Explain the concept of a 'fail fast' culture "
             "and how you balance it with quality.",
             "Early cheap experiments; "
             "learning-focused; quality gates "
             "for production."),
            ("design",
             "Design an innovation funnel from idea to "
             "launch for a technology company.",
             "Idea capture, screening, "
             "validation, build, measure, "
             "scale."),
            ("scenario",
             "A competitor launches a similar product first. "
             "How does your R&D team respond?",
             "Assess their offering, differentiate, "
             "accelerate, learn from their "
             "mistakes."),
            ("written_explanation",
             "Explain the importance of literature review in "
             "research and how you would conduct one.",
             "Understand prior work, avoid "
             "duplication, identify gaps, "
             "methodology."),
            ("short_answer",
             "What is the difference between a hypothesis and "
             "a prediction?",
             "Hypothesis = testable statement; "
             "prediction = expected outcome if "
             "hypothesis true."),
            ("design",
             "Design an experimental setup to A/B test a "
             "new algorithm's performance.",
             "Controlled variables, metrics, "
             "sample size, significance, "
             "reproducibility."),
            ("scenario",
             "A promising project has no clear business "
             "case. How do you evaluate whether to "
             "continue?",
             "Potential value, cost, timing, "
             "strategic fit, opportunity "
             "cost."),
            ("written_explanation",
             "Explain how you would protect intellectual "
             "property from your research.",
             "Patents, trade secrets, "
             "publication strategy, "
             "agreements."),
            ("design",
             "Design a technology watch process to track "
             "emerging trends relevant to your company.",
             "Sources, curation, "
             "dissemination, assessment, "
             "action."),
            ("short_answer",
             "What is the difference between validation and "
             "verification in a research context?",
             "Building the right thing vs "
             "building it right; research "
             "analogy."),
            ("written_explanation",
             "Explain how you would measure the success of "
             "an innovation project.",
             "Adoption, business impact, "
             "learning, time to value, "
             "spillover."),
            ("design",
             "Design a process for running an internal "
             "hackathon that produces useful outcomes.",
             "Theme, constraints, teams, "
             "criteria, follow-through."),
            ("scenario",
             "A senior engineer is resistant to a new "
             "technology you propose. How do you win "
             "support?",
             "Evidence, small pilot, address "
             "concerns, involve them, "
             "demonstrate value."),
            ("written_explanation",
             "Explain the difference between incremental "
             "innovation and disruptive innovation, with "
             "examples.",
             "Small improvements vs fundamental "
             "change; examples and risks."),
        ],
        "position": [
            ("written_explanation",
             "As a researcher, describe how you would turn "
             "a vague idea from management into a concrete "
             "research project.",
             "Clarify goals, scope, method, "
             "success criteria, timeline, "
             "stakeholders."),
            ("scenario",
             "A research project is running out of budget "
             "with promising early results. What do you "
             "do?",
             "Prioritise the critical question, "
             "seek additional funding, "
             "communicate value."),
            ("short_answer",
             "What is the difference between a research "
             "proposal and a research report?",
             "Proposal = plan before; report = "
             "results after."),
            ("design",
             "Design a proof-of-concept plan for a new "
             "machine learning feature.",
             "Objective, data, method, "
             "success metric, timeline, "
             "exit criteria."),
            ("written_explanation",
             "Explain how you would evaluate a new "
             "technology with a hands-on experiment.",
             "Define criteria, build a small "
             "test, measure, compare to "
             "baseline, decide."),
            ("debugging",
             "Your experiment's results are not "
             "reproducible. How do you investigate?",
             "Environment, data, randomness, "
             "procedure, versioning; "
             "systematic check."),
            ("short_answer",
             "What is the difference between a control "
             "group and a treatment group?",
             "Baseline vs intervention; "
             "purpose in experiments."),
            ("design",
             "Design a stakeholder report for a research "
             "project with early-stage findings.",
             "Clear value, evidence, "
             "limitations, next steps."),
            ("written_explanation",
             "Explain how you would decide whether to "
             "publish, patent or keep a research finding "
             "secret.",
             "Strategic value, legal "
             "considerations, timing, "
             "competitive advantage."),
            ("scenario",
             "A colleague's research approach is flawed. "
             "How do you raise it?",
             "Constructive, evidence-based, "
             "focus on the method, offer "
             "help."),
            ("short_answer",
             "What is the difference between an experiment "
             "and an observational study?",
             "Manipulation vs observation; "
             "causation vs correlation."),
            ("design",
             "Design a technology evaluation matrix for "
             "comparing three vendor solutions.",
             "Criteria, weights, scoring, "
             "evidence, decision."),
            ("written_explanation",
             "Explain how you keep current in your field "
             "and how that informs your work.",
             "Sources, habits, application; "
             "concrete and honest."),
            ("debugging",
             "A prototype works in the lab but fails in a "
             "pilot deployment. How do you investigate?",
             "Environment differences, data, "
             "usage patterns, scale; "
             "compare."),
            ("short_answer",
             "What is the difference between a benchmark "
             "and a baseline?",
             "Benchmark = standard comparison; "
             "baseline = current state before "
             "change."),
            ("design",
             "Design a research repository and knowledge "
             "sharing process for a team.",
             "Storage, structure, "
             "discoverability, reuse, "
             "culture."),
            ("written_explanation",
             "Explain how you would prioritise research "
             "topics across a team.",
             "Business impact, feasibility, "
             "timing, capacity, "
             "alignment."),
            ("scenario",
             "A pilot shows weak results but the idea "
             "feels promising. How do you decide next "
             "steps?",
             "Analyse why, adjust "
             "hypothesis, run another "
             "pilot, or kill with "
             "learning."),
            ("short_answer",
             "What is the difference between a feasibility "
             "study and a pilot?",
             "Can it work vs does it work "
             "in practice; small scale."),
            ("design",
             "Design a metrics framework to track "
             "innovation portfolio health.",
             "Investment, stage, "
             "success rate, value "
             "realised."),
        ],
        "practical": [
            ("practical",
             "Write a one-page research brief for "
             "evaluating a new database technology.",
             "Question, method, "
             "criteria, timeline."),
            ("design",
             "Design an A/B experiment for a website "
             "change including metrics and sample size.",
             "Hypothesis, metric, "
             "significance, duration."),
            ("practical",
             "Describe how you would run a design "
             "sprint or rapid prototyping session.",
             "Structure, participants, "
             "output, testing."),
            ("debugging",
             "A benchmark shows your solution is "
             "slower than the current one. How do you "
             "proceed?",
             "Verify methodology, "
             "profile, optimise, or "
             "reassess."),
            ("practical",
             "Write a technology watch report on a "
             "trend you would track.",
             "Summary, relevance, "
             "implications, action."),
            ("design",
             "Design a proof-of-concept for a mobile "
             "payment feature (scope, data, success "
             "criteria).",
             "Minimal scope, clear "
             "success measure, "
             "risks."),
            ("practical",
             "Describe how you would measure the "
             "adoption of a new internal tool.",
             "Metrics, baseline, "
             "targets, feedback."),
            ("debugging",
             "A research dataset is missing values for "
             "a key variable. How do you handle it?",
             "Assess bias, "
             "imputation options, "
             "sensitivity, "
             "disclose."),
            ("practical",
             "Write a project brief for an internal "
             "innovation challenge.",
             "Problem, criteria, "
             "prizes, timeline, "
             "support."),
            ("design",
             "Design a competitor analysis framework for "
             "a new product idea.",
             "Dimensions, sources, "
             "scoring, insights."),
            ("practical",
             "Describe how you would run a small user "
             "study to validate an idea quickly.",
             "Recruit, tasks, "
             "capture, analyse, "
             "act."),
            ("debugging",
             "A pilot's metrics improved but the change "
             "was not the cause. How do you detect "
             "this?",
             "Control, time-series "
             "analysis, external "
             "factors."),
            ("practical",
             "Write a decision memo for leadership on "
             "whether to invest in a technology.",
             "Evidence, options, "
             "recommendation, "
             "risks."),
            ("design",
             "Design a sandbox environment for safely "
             "testing experimental code.",
             "Isolation, data, "
             "controls, review."),
            ("practical",
             "Describe how you would document a "
             "research finding for reuse by the team.",
             "Structure, context, "
             "method, results, "
             "lessons."),
            ("debugging",
             "An experiment uses a random seed and "
             "results vary between runs. How do you "
             "make it reliable?",
             "Fixed seed, multiple "
             "runs, statistical "
             "aggregation."),
            ("practical",
             "Write a kickoff checklist for a new "
             "research project.",
             "Goals, scope, "
             "team, data, "
             "timeline."),
            ("design",
             "Design a metrics dashboard for an "
             "innovation pipeline.",
             "Stages, counts, "
             "conversion, value."),
            ("practical",
             "Describe how you would present a failed "
             "experiment as a learning to the team.",
             "Honest, structured, "
             "actionable lessons."),
            ("debugging",
             "A new technology performs worse under "
             "real load than in tests. How do you "
             "investigate?",
             "Scale effects, "
             "resource limits, "
             "configuration, "
             "profiling."),
        ],
    },

    # ----------------------------------------------------------------- 21
    "Digital Marketing & Online Services": {
        "category": [
            ("written_explanation",
             "Explain the difference between organic and paid "
             "marketing channels, with examples of each.",
             "Unpaid visibility vs paid placement; "
             "goals, cost, sustainability."),
            ("scenario",
             "A campaign's click-through rate is high but "
             "conversions are low. How do you investigate?",
             "Check landing page, offer, audience "
             "match, tracking, funnel; identify "
             "the leak."),
            ("design",
             "Design a digital marketing campaign for "
             "launching a new product to a young audience.",
             "Channels, messaging, budget, "
             "timeline, metrics, creative "
             "strategy."),
            ("written_explanation",
             "Explain what SEO is and the difference between "
             "on-page and off-page SEO.",
             "Search optimisation; on-page = content/"
             "structure; off-page = links/authority."),
            ("scenario",
             "A client wants to buy fake followers to look "
             "popular. How do you respond?",
             "Explain the harm (engagement, "
             "trust, penalties), propose "
             "organic growth."),
            ("short_answer",
             "What is the difference between a KPI and a "
             "vanity metric?",
             "KPI = tied to business outcome; vanity "
             "= looks good but not meaningful."),
            ("written_explanation",
             "Explain the concept of a marketing funnel and "
             "how you would optimise each stage.",
             "Awareness, interest, decision, "
             "action; tactics per stage."),
            ("design",
             "Design a social media content calendar for a "
             "brand for one month.",
             "Content mix, cadence, platform "
             "fit, goals, measurement."),
            ("scenario",
             "A social media post goes viral but attracts "
             "negative attention. How do you handle the "
             "situation?",
             "Assess, respond appropriately, "
             "monitor, learn, align with "
             "values."),
            ("written_explanation",
             "Explain the difference between reach and "
             "impressions.",
             "Unique viewers vs total views; "
             "what each measures."),
            ("design",
             "Design an email marketing strategy including "
             "segmentation and automation.",
             "List building, segments, journeys, "
             "content, metrics, compliance."),
            ("scenario",
             "A customer complains about receiving too "
             "many marketing emails. How do you handle it?",
             "Honour preferences, audit frequency, "
             "improve targeting, apologise."),
            ("written_explanation",
             "Explain the difference between A/B testing "
             "and multivariate testing in marketing.",
             "Two variants vs many factors; "
             "complexity and use cases."),
            ("short_answer",
             "What is the difference between a landing page "
             "and a homepage?",
             "Focused conversion page vs general "
             "entry point; different goals."),
            ("design",
             "Design a content marketing plan that attracts "
             "organic traffic for a B2B company.",
             "Audience, topics, formats, "
             "distribution, measurement."),
            ("scenario",
             "Your ad spend is rising but sales are flat. "
             "How do you diagnose?",
             "Check attribution, audience "
             "quality, creative fatigue, "
             "competition, funnel."),
            ("written_explanation",
             "Explain how you would measure return on "
             "marketing investment (ROMI).",
             "Revenue attribution, cost, "
             "baseline, incremental impact."),
            ("design",
             "Design a customer referral program for an "
             "online service.",
             "Incentives, mechanics, "
             "tracking, fraud control, "
             "promotion."),
            ("scenario",
             "A brand gets a negative review online. How "
             "do you respond professionally?",
             "Acknowledge, investigate, offer "
             "resolution publicly, move "
             "privately."),
            ("written_explanation",
             "Explain the importance of a consistent brand "
             "voice across digital channels.",
             "Recognition, trust, expectations; "
             "adapting tone per channel without "
             "losing identity."),
        ],
        "position": [
            ("written_explanation",
             "As a digital marketer, describe how you would "
             "build a marketing plan from scratch for a "
             "new business.",
             "Audience, positioning, channels, "
             "budget, content, metrics."),
            ("scenario",
             "A campaign performs well on one platform but "
             "poorly on another. How do you adapt?",
             "Analyse audience and format fit, "
             "adjust creative, reallocate "
             "budget."),
            ("short_answer",
             "What is the difference between a campaign "
             "and an ad group?",
             "Campaign = goal/audience level; "
             "ad group = related ads and "
             "keywords."),
            ("design",
             "Design a paid search (PPC) account "
             "structure for a company selling three "
             "product lines.",
             "Campaigns, ad groups, keywords, "
             "negatives, budgets."),
            ("written_explanation",
             "Explain how you would use web analytics to "
             "improve a website's conversion rate.",
             "Funnel analysis, behaviour, "
             "hypotheses, tests, iterate."),
            ("debugging",
             "A tracking pixel shows zero conversions "
             "despite sales. How do you diagnose?",
             "Pixel installation, events, "
             "attribution window, test "
             "purchase."),
            ("short_answer",
             "What is the difference between CTR and "
             "conversion rate?",
             "Click ratio vs completed goal "
             "ratio; different funnel stages."),
            ("design",
             "Design an SEO plan for a local business "
             "website.",
             "Keywords, on-page, local "
             "listings, content, links."),
            ("written_explanation",
             "Explain how you would grow a brand's "
             "Instagram/TikTok following organically.",
             "Content strategy, engagement, "
             "trends, consistency, "
             "community."),
            ("scenario",
             "A competitor outbids you on every keyword. "
             "How do you compete?",
             "Differentiate, long-tail "
             "keywords, quality score, "
             "remarketing, value "
             "proposition."),
            ("short_answer",
             "What is the difference between remarketing "
             "and retargeting?",
             "Largely synonymous; re-engaging "
             "past visitors."),
            ("design",
             "Design an email nurture sequence for "
             "leads who downloaded a whitepaper.",
             "Triggers, content, cadence, "
             "goal, metrics."),
            ("written_explanation",
             "Explain how you would structure and read a "
             "weekly marketing report.",
             "Metrics vs goals, trends, "
             "insights, actions."),
            ("debugging",
             "Email open rates dropped sharply. List the "
             "likely causes.",
             "Deliverability, subject lines, "
             "list hygiene, time, "
             "competition."),
            ("short_answer",
             "What is the difference between a lead and a "
             "qualified lead?",
             "Interest vs fit/readiness; "
             "scoring."),
            ("design",
             "Design a social media crisis management "
             "plan.",
             "Monitoring, roles, response "
             "tiers, holding statements."),
            ("written_explanation",
             "Explain how you would choose between "
             "different marketing channels with a limited "
             "budget.",
             "Audience reach, cost per "
             "acquisition, experimentation, "
             "attribution."),
            ("scenario",
             "An influencer you partnered with is "
             "exposed for fraud. How do you respond?",
             "Remove content, communicate, "
             "vet influencers better."),
            ("short_answer",
             "What is the difference between a blog post "
             "and a landing page?",
             "Content vs conversion; "
             "different purposes."),
            ("design",
             "Design a referral and loyalty program for "
             "an online subscription service.",
             "Incentives, tracking, "
             "experience, retention."),
        ],
        "practical": [
            ("practical",
             "Write a Google Ads (or similar) ad copy for "
             "a product launch with a clear CTA.",
             "Compelling, clear, on-brand, "
             "action-oriented."),
            ("design",
             "Design an A/B test for a landing page "
             "headline (variants, metric, decision "
             "rule).",
             "Meaningful variants, clear "
             "metric, sample size."),
            ("practical",
             "Describe how you would build a 30-day "
             "social media plan for a product launch.",
             "Content types, cadence, "
             "platforms, goals."),
            ("debugging",
             "A website's organic traffic dropped 50% "
             "overnight. How do you diagnose?",
             "Search console, penalties, "
             "technical issues, content "
             "changes, competitors."),
            ("practical",
             "Write an email subject line and preview "
             "for a sale announcement (two options).",
             "Clear value, curiosity, "
             "appropriate length."),
            ("design",
             "Design a keyword research process for a "
             "new niche.",
             "Brainstorm, tools, intent "
             "analysis, selection."),
            ("practical",
             "Describe how you would set up conversion "
             "tracking for a website.",
             "Goals/events, pixels, "
             "verification, testing."),
            ("debugging",
             "Ad impressions are high but clicks are "
             "near zero. What is likely wrong?",
             "Ad relevance, creative, "
             "placement, audience, "
             "competition."),
            ("practical",
             "Write a social media post (copy) for a "
             "product benefit announcement.",
             "Clear benefit, tone, CTA."),
            ("design",
             "Design a quarterly content calendar for a "
             "blog targeting business readers.",
             "Topics, cadence, authors, "
             "promotion, metrics."),
            ("practical",
             "Describe how you would analyse a campaign's "
             "performance and present recommendations.",
             "Data, insight, "
             "recommendation, next "
             "steps."),
            ("debugging",
             "Cart abandonment is high. List the likely "
             "causes and fixes.",
             "Costs, friction, trust, "
             "checkout issues, "
             "alternatives."),
            ("practical",
             "Write a short welcome email for new "
             "subscribers.",
             "Value, expectations, "
             "first action."),
            ("design",
             "Design a customer persona for a new "
             "product's marketing.",
             "Demographics, goals, "
             "pain points, channels."),
            ("practical",
             "Describe how you would run a small "
             "influencer campaign on a budget.",
             "Selection, brief, "
             "tracking, compliance."),
            ("debugging",
             "A paid campaign converts well but at a "
             "loss. How do you fix profitability?",
             "Cost per acquisition, "
             "audience, offer, "
             "funnel."),
            ("practical",
             "Write an SEO title tag and meta "
             "description for a product page.",
             "Keyword, click appeal, "
             "length."),
            ("design",
             "Design a measurement plan (KPIs, tools, "
             "cadence) for a marketing team.",
             "Aligned to goals, "
             "actionable."),
            ("practical",
             "Describe how you would grow an email list "
             "ethically.",
             "Value exchange, "
             "opt-in, compliance, "
             "engagement."),
            ("debugging",
             "A viral post got great reach but no "
             "sales. How do you analyse why?",
             "Audience match, "
             "message, CTA, "
             "timing."),
        ],
    },
}
