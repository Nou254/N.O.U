        │                                                │
        ▼                                                │
 DOCUMENTATION                                           │
        │                                                │
        ▼                                                │
 PROJECT MANAGEMENT ◄────────────────────────────────────┘
        │
        ▼
 PERSONNEL SELECTION
        │
        ▼
 PROJECT TEAM
        │
        ├──────────────► DEVELOPMENT
        │                     │
        │                     ▼
        │                    QA
        │                     │
        │                     ▼
        │                 SECURITY
        │                     │
        │                     ▼
        │                  STAGING
        │                     │
        ▼                     ▼
 PROJECT PROGRESS       CUSTOMER ACCEPTANCE
                              │
                              ▼
                         DEPLOYMENT
                              │
                              ▼
                         SUPPORT PORTAL
```

## The key architectural principle

**Do not build 12 completely independent applications.**

Build **one N.O.U. platform with controlled portals/modules**.

The same user account can move between authorized modules according to their role.

For example, a Business Analyst might have:

> Customer Requests → Requirements Portal → Documentation Portal → Assigned Projects

while a Backend Developer might have:

> Employment Profile → Assigned Projects → Team Portal → Relevant Documentation

and a Customer might have:

> Customer Portal → My Requests → My Projects → Approvals → Support

This gives N.O.U. a much cleaner architecture and makes the system scalable as the company grows.

# N.O.U. DIGITAL SYSTEMS

## CUSTOMER PROJECT ASSESSMENT, APPROVAL AND DEVELOPMENT PROCESS

**Website:** nou.com
**Document Status:** Draft
**Version:** 1.0

---

# 1. PURPOSE

The N.O.U. Digital Systems project management process establishes the controlled procedure through which a customer project moves from the initial request to analysis, technical assessment, documentation, approval, team formation, development, testing, deployment, and eventual closure.

The purpose of this process is to ensure that:

* Customer requests are properly evaluated before development begins.
* Projects are technically and commercially feasible.
* Requirements are clearly documented before coding begins.
* Appropriate personnel are selected based on their qualifications and availability.
* Confidential customer information is protected.
* Developers do not receive access to projects before they are ready for development.
* Every project has clearly defined responsibilities, deadlines, documentation, and approval points.
* Project changes are controlled and documented.
* Management maintains appropriate oversight throughout the project lifecycle.

---

# 2. CORE PRINCIPLE

N.O.U. shall operate on the following principle:

> **A customer request is not automatically a development project.**

A request must pass through the appropriate evaluation, analysis, documentation, technical review, and approval stages before it becomes an active development project.

Similarly:

> **Personnel shall not receive access to a customer project merely because they are qualified developers.**

Project access shall be granted according to:

1. Professional classification;
2. Required skills;
3. Availability;
4. Project assignment;
5. Role within the project; and
6. Access permissions.

---

# 3. PROJECT LIFECYCLE

The official N.O.U. project lifecycle shall be:

```text
CUSTOMER
   │
   ▼
PROJECT REQUEST
   │
   ▼
ADMIN INITIAL ASSESSMENT
   │
   ▼
REQUIREMENTS & BUSINESS ANALYSIS
   │
   ▼
TECHNICAL FEASIBILITY
   │
   ▼
SYSTEM ARCHITECTURE
   │
   ▼
PROJECT DOCUMENTATION
   │
   ▼
INTERNAL REVIEW
   │
   ▼
PROJECT ESTIMATION & STAFFING PLAN
   │
   ▼
CUSTOMER PROPOSAL / APPROVAL
   │
   ▼
PROJECT STAFFING
   │
   ▼
TEAM FORMATION
   │
   ▼
DEVELOPMENT
   │
   ▼
QUALITY ASSURANCE
   │
   ▼
SECURITY REVIEW
   │
   ▼
STAGING
   │
   ▼
CUSTOMER ACCEPTANCE
   │
   ▼
DEPLOYMENT
   │
   ▼
SUPPORT & MAINTENANCE
   │
   ▼
PROJECT CLOSURE
```

---

# 4. STAGE ONE — CUSTOMER PROJECT REQUEST

A customer initiates a project through the N.O.U. Customer Portal.

The customer shall provide sufficient information to allow N.O.U. to understand the proposed project.

### Information may include:

* Customer name;
* Organization;
* Contact information;
* Project title;
* Description of the problem;
* Proposed solution;
* Target users;
* Desired platform;
* Required features;
* Expected integrations;
* Preferred completion period;
* Budget information, where applicable;
* Relevant attachments;
* Special requirements.

The customer is not required to understand the technical implementation of the proposed system.

For example, a customer may state:

> "I need a system to manage my employees, customers, stock and sales."

N.O.U. shall determine the appropriate technical solution through the analysis process.

---

# 5. STAGE TWO — ADMIN INITIAL ASSESSMENT

Once submitted, the request enters the **Admin Project Intake Portal**.

At this stage, the project is **confidential and restricted**.

### The project shall not yet be visible to general personnel or developers.

The administrator reviews:

* Completeness of the request;
* Customer information;
* Nature of the requested service;
* Business suitability;
* Initial technical indication;
* Potential legal or compliance concerns;
* Whether the project falls within N.O.U.'s services.

The administrator may request clarification from the customer.

### Possible outcomes

```text
NEW
   │
   ├── CLARIFICATION REQUIRED
   │
   ├── REJECTED
   │
   └── APPROVED FOR ANALYSIS
```

Only projects approved for analysis proceed to the next stage.

---

# 6. STAGE THREE — REQUIREMENTS AND BUSINESS ANALYSIS

An approved project is assigned to the **Requirements & Systems Analysis function**.

The purpose of this stage is to determine exactly what the customer requires.

The analyst shall establish:

### Functional Requirements

What the system must do.

### Non-Functional Requirements

How the system should operate.

### User Roles

Who will use the system.

### Business Rules

Rules governing how the customer's organization operates.

### Workflows

How information and activities move through the system.

### Acceptance Criteria

Conditions that must be satisfied before the customer can accept the completed system.

The analyst may communicate directly with the customer through the authorized project communication channel.

---

# 7. STAGE FOUR — TECHNICAL FEASIBILITY ASSESSMENT

Once the requirements are sufficiently understood, the project moves to technical assessment.

The technical function determines whether the proposed system can reasonably be developed by N.O.U.

The assessment may consider:

* Required technologies;
* Software architecture;
* Database requirements;
* APIs and external services;
* Infrastructure;
* Security;
* Scalability;
* Performance;
* Integration requirements;
* Development complexity;
* Technical risks;
* Availability of required skills.

The result shall be classified as:

```text
TECHNICALLY FEASIBLE
TECHNICALLY FEASIBLE WITH MODIFICATIONS
REQUIRES FURTHER ANALYSIS
NOT CURRENTLY FEASIBLE
```

A project that is not feasible should not proceed directly into development.

---

# 8. STAGE FIVE — SYSTEM ARCHITECTURE

If the project is technically feasible, the technical team prepares the proposed architecture.

Depending on the project, this may include:

* System architecture;
* Database architecture;
* API architecture;
* Frontend architecture;
* Backend architecture;
* Authentication architecture;
* Security architecture;
* Infrastructure architecture;
* Integration architecture;
* Backup and recovery strategy.

The architecture establishes **how the system is expected to work before developers begin implementing it.**

---

# 9. STAGE SIX — PROJECT DOCUMENTATION

The requirements and technical information are converted into the official project documentation.

The project documentation may contain:

### 9.1 Project Charter

Defines the project purpose, objectives, scope and stakeholders.

### 9.2 Software Requirements Specification

Defines what the software must do.

### 9.3 Technical Design Document

Defines how the software will be constructed.

### 9.4 Database Design

Defines the database structure and relationships.

### 9.5 UI/UX Specification

Defines the user interface and user experience requirements.

### 9.6 Security Specification

Defines security requirements and controls.

### 9.7 Testing Strategy

Defines how the system will be tested.

### 9.8 Deployment Plan

Defines how the completed system will be deployed.

### 9.9 Project Management Plan

Defines:

* Personnel;
* Tasks;
* Milestones;
* Deadlines;
* Dependencies;
* Risks;
* Resources.

---

# 10. PROJECT VISIBILITY DURING DOCUMENTATION

During requirements analysis, technical assessment, architecture and documentation:

> **The project remains restricted.**

General developers and other personnel shall not see the project in their normal project portals.

Only authorized individuals involved in preparing or reviewing the project may access it.

This protects:

* Customer confidentiality;
* Business information;
* Technical plans;
* Pricing;
* Internal discussions;
* Unapproved project concepts.

---

# 11. STAGE SEVEN — INTERNAL REVIEW

Completed documentation must undergo internal review before the project can become available for staffing.

The review may involve:

* Requirements review;
* Technical architecture review;
* Security review;
* Project management review;
* Management approval.

The documentation shall have a controlled status.

```text
DRAFT
   ↓
UNDER REVIEW
   ↓
REVISION REQUIRED
   ↓
RESUBMITTED
   ↓
APPROVED
```

Only the approved version becomes the project's official baseline.

---

# 12. STAGE EIGHT — PROJECT ESTIMATION

Once the project documentation has been approved, N.O.U. determines the resources required.

The estimation shall consider:

### Personnel

Example:

```text
Project Manager             1
Business Analyst            1
UI/UX Designer              1
Frontend Developers         2
Backend Developers          2
Database Engineer            1
QA Engineer                 1
DevOps Engineer              1
```

### Timeline

The project team shall estimate:

* Requirements period;
* Design period;
* Development period;
* Testing period;
* Deployment period.

### Infrastructure

This may include:

* Cloud hosting;
* Database hosting;
* Storage;
* APIs;
* Domains;
* Monitoring;
* Security services.

### Project Cost

The estimated internal resources and customer pricing shall be established before formal project commencement.

---

# 13. STAGE NINE — CUSTOMER PROPOSAL AND APPROVAL

After the project has been properly assessed, N.O.U. prepares the customer proposal.

The proposal should communicate:

* Project scope;
* Major features;
* Deliverables;
* Estimated timeline;
* Project cost;
* Payment schedule;
* Responsibilities;
* Assumptions;
* Exclusions;
* Support arrangements;
* Applicable terms.

The customer may:

```text
APPROVE
REQUEST CHANGES
DECLINE
```

If the customer requests significant changes, the project may return to requirements analysis.

---

# 14. STAGE TEN — PROJECT STAFFING

Once the project has been authorized to proceed, it enters the **Project Staffing Portal**.

This is the point at which the project may become visible to **eligible N.O.U. personnel**.

The system identifies personnel based on:

* Professional classification;
* Skills;
* Assessment results;
* Experience;
* Current workload;
* Availability;
* Previous project performance.

For example:

```text
PROJECT REQUIRES:

Backend Developer × 2
Frontend Developer × 2
Database Engineer × 1
UI/UX Designer × 1
QA Engineer × 1
DevOps Engineer × 1
```

The system can identify qualified personnel in the N.O.U. Talent Pool.

---

# 15. PERSONNEL PROJECT VISIBILITY

Project visibility shall be controlled.

Before staffing:

> **Project is invisible to general personnel.**

During staffing:

> **Eligible personnel may see a limited project opportunity.**

After assignment:

> **Assigned personnel receive project-specific access.**

For example, a backend developer may see:

```text
PROJECT ID: NOU-PRJ-2026-001

Category:
Business Management Software

Position:
Backend Developer

Required Skills:
Python
FastAPI
PostgreSQL
REST APIs

Duration:
5 Months

Status:
Recruiting
```

The developer should not automatically see confidential customer information.

---

# 16. STAGE ELEVEN — TEAM FORMATION

After suitable personnel have been identified, the project team is formally formed.

The first person to express interest in a project shall **not automatically become Team Leader**.

Team leadership shall be determined using factors such as:

* Relevant experience;
* Technical competence;
* Leadership ability;
* Previous N.O.U. performance;
* Availability;
* Project requirements.

The final appointment shall be approved by the appropriate Project Manager or Administrator.

---

# 17. PROJECT ACCESS AFTER TEAM FORMATION

Once a person is assigned to the project, the system grants project-specific permissions.

For example:

### Backend Developer

May access:

* Backend requirements;
* Relevant architecture;
* API specifications;
* Assigned database information;
* Development tasks;
* Project communications.

### UI/UX Designer

May access:

* UI/UX requirements;
* User workflows;
* Design specifications;
* Design tasks.

### QA Engineer

May access:

* Testing requirements;
* Acceptance criteria;
* Test environment;
* Testing documentation.

Personnel shall only receive information necessary for their role.

---

# 18. STAGE TWELVE — DEVELOPMENT

Development begins only after:

* Project approval;
* Documentation approval;
* Team formation;
* Personnel assignment;
* Development environment preparation.

Developers work through the Project Team Portal.

The portal should manage:

* Tasks;
* Milestones;
* Assignments;
* Progress;
* Project communication;
* Documentation;
* Repository references;
* Development submissions.

---

# 19. PROJECT TEAM LEADER

The Team Leader shall coordinate the development team within the approved project structure.

The Team Leader is responsible for:

* Monitoring assigned work;
* Coordinating team members;
* Reporting project progress;
* Identifying risks;
* Escalating blockers;
* Preparing weekly reports;
* Monitoring project deadlines.

The Team Leader shall submit a **weekly project progress report**.

The report should include:

* Work completed;
* Work in progress;
* Outstanding work;
* Problems encountered;
* Risks;
* Percentage completion;
* Team status;
* Next week's objectives.

---

# 20. PROJECT DEADLINES AND EXTENSIONS

Projects must be submitted through the N.O.U. Project Portal before the approved deadline.

If the team determines that the project cannot reasonably be completed on time, an extension request must be submitted before the deadline.

The request shall state:

* Reason for delay;
* Work remaining;
* Impact;
* Revised completion date;
* Resources required.

An extension may be granted for a maximum period of **four weeks**, subject to management approval.

Extensions shall not be automatic.

---

# 21. MAXIMUM ACTIVE PROJECTS

An N.O.U. personnel member shall not normally be assigned to more than **three active projects simultaneously**.

The system should automatically monitor:

```text
ACTIVE PROJECTS: 2 / 3
```

When a person reaches the maximum:

> The system should prevent them from being assigned to another active project unless an authorized administrator overrides the restriction.

---

# 22. QUALITY ASSURANCE

When development reaches the appropriate milestone, the project moves to QA.

The QA team performs:

* Functional testing;
* Integration testing;
* Usability testing;
* Performance testing;
* Regression testing;
* Compatibility testing;
* Security-related testing where applicable.

A failed test returns the relevant work to the development team.

```text
DEVELOPMENT
     ↓
QA
     ↓
FAILED ─────────► DEVELOPMENT
     │
     ▼
PASSED
```

---

# 23. SECURITY REVIEW

Projects requiring security assessment shall undergo security review before production deployment.

The review may cover:

* Authentication;
* Authorization;
* Data protection;
* API security;
* Input validation;
* Access controls;
* Secrets management;
* Vulnerability testing;
* Logging;
* Backup and recovery.

---

# 24. STAGING

After successful development and testing, the system is deployed to a staging environment.

The staging environment should represent the production environment as closely as practical.

Final testing and customer acceptance take place from this stage.

---

# 25. CUSTOMER ACCEPTANCE

The customer is given access to the appropriate acceptance environment.

The customer may:

* Test the system;
* Review functionality;
* Report defects;
* Request clarification;
* Confirm that agreed requirements have been met.

The customer should not be able to introduce unlimited new requirements under the original project scope.

New requirements should enter the **Change Request Process**.

---

# 26. CHANGE REQUEST PROCESS

A change request shall follow:

```text
CUSTOMER REQUEST
       ↓
IMPACT ANALYSIS
       ↓
TECHNICAL REVIEW
       ↓
COST / TIME ASSESSMENT
       ↓
CUSTOMER APPROVAL
       ↓
DOCUMENTATION UPDATE
       ↓
DEVELOPMENT
```

This prevents uncontrolled scope expansion.

---

# 27. DEPLOYMENT

After customer acceptance and required internal approvals, the project may be deployed to production.

Deployment shall be performed by authorized technical personnel.

The deployment process should be documented.

---

# 28. PROJECT CLOSURE

Once delivery has been completed:

* Final documentation is archived;
* Source code is securely stored;
* Customer deliverables are recorded;
* Deployment information is documented;
* Support arrangements become active;
* Project performance is recorded;
* Personnel project records are updated;
* Project-specific access is reviewed and removed where appropriate.

The project status becomes:

> **COMPLETED**

or:

> **ACTIVE SUPPORT**

depending on the agreement.

---

# 29. PERSONNEL RECORD UPDATE

Project completion should contribute to each participating employee's professional record.

For example:

```text
PERSONNEL PROFILE

Developer:
Backend Developer

Projects Completed:
7

Current Active Projects:
1 / 3

Skills Demonstrated:
Python
FastAPI
PostgreSQL
API Development

Project Performance:
Excellent

Latest Project:
NOU-PRJ-2026-001
```

This allows N.O.U. to make better personnel decisions in future projects.

---

# 30. INVESTOR VISIBILITY

Investors shall only receive information specifically authorized for investor access.

Investors may view:

* Approved project status;
* General project progress;
* Milestones;
* Approved progress reports;
* High-level project information.

Investors shall not:

* Assign personnel;
* Modify requirements;
* Approve technical decisions;
* Access source code;
* Access customer confidential information;
* Direct developers;
* Modify project deadlines.

Investor access shall remain **read-only** unless a separate lawful agreement provides otherwise.

---

# 31. ADMINISTRATOR ACCESS

During the current stage of N.O.U.'s development, the Founder/Super Administrator shall have access to all operational portals.

The Super Administrator may access:

* Customer Management;
* Project Intake;
* Requirements;
* Architecture;
* Documentation;
* Project Management;
* Employment;
* Talent Management;
* Development Projects;
* QA;
* Security;
* Investor Management;
* Finance;
* Support;
* Reports;
* Audit Logs;
* System Configuration.

However, the system shall still maintain separate roles and permissions internally.

This allows N.O.U. to delegate responsibilities as employees are hired without redesigning the platform.

---

# 32. PROJECT VISIBILITY RULE

The following rule shall govern project visibility:

> **A project shall remain restricted to authorized administrative and professional functions until its requirements, technical feasibility, architecture, documentation, internal review, estimation, and authorization have been completed.**

After the project reaches the staffing stage:

> **Only eligible personnel may view the limited project opportunity.**

After personnel are assigned:

> **Only assigned team members receive project-specific access according to their roles.**

---

# 33. FINAL PROJECT FLOW

The official N.O.U. workflow can therefore be summarized as:

```text
CUSTOMER
   ↓
PROJECT REQUEST
   ↓
ADMIN ASSESSMENT
   ↓
APPROVED?
 ┌─┴───────────────┐
NO                 YES
│                   │
▼                   ▼
CLOSED        REQUIREMENTS ANALYSIS
                    │
                    ▼
             TECHNICAL FEASIBILITY
                    │
                    ▼
                ARCHITECTURE
                    │
                    ▼
              DOCUMENTATION
                    │
                    ▼
             INTERNAL REVIEW
                    │
                    ▼
             ESTIMATION
                    │
                    ▼
          CUSTOMER APPROVAL
                    │
                    ▼
            PROJECT STAFFING
                    │
                    ▼
       ELIGIBLE PERSONNEL VIEW
                    │
                    ▼
             TEAM FORMATION
                    │
                    ▼
              DEVELOPMENT
                    │
                    ▼
                    QA
                    │
                    ▼
             SECURITY REVIEW
                    │
                    ▼
                 STAGING
                    │
                    ▼
          CUSTOMER ACCEPTANCE
                    │
                    ▼
               DEPLOYMENT
                    │
                    ▼
            SUPPORT / MAINTENANCE
                    │
                    ▼
             PROJECT CLOSURE
```

## 34. GOVERNING RULE

The N.O.U. project system shall follow one fundamental rule:

> **No coding begins from a customer request alone. A project must first pass through requirements analysis, technical feasibility assessment, architecture, documentation, review, estimation, authorization and team formation before development begins.**

This creates a controlled separation between **what the customer requested**, **what N.O.U. approved**, **what the technical team designed**, and **what developers are authorized to build**.

It also ensures that as N.O.U. grows from a one-person operation into a larger technology company, the same project governance structure can continue operating without fundamentally redesigning the platform.

# N.O.U. DIGITAL SYSTEMS

## PROJECT STAFFING AND TEAM FORMATION POLICY

**Website:** nou.com
**Document Status:** Draft
**Version:** 1.0

---

## 1. PURPOSE

The N.O.U. Project Staffing and Team Formation Policy establishes the procedures through which qualified personnel are identified, evaluated, selected, assigned, and organized into teams for approved company projects.

The purpose of this policy is to ensure that every project receives personnel whose skills, experience, availability, and professional classification correspond to the requirements of the project.

Team formation shall be based on the needs of the project and the qualifications of personnel rather than on personal preference, first-come-first-served selection, or arbitrary assignment.

---

# 2. CORE PRINCIPLE

N.O.U. shall operate under the following principle:

> **The project determines the personnel required, and the qualifications of personnel determine who is eligible to participate.**

Personnel shall not be assigned to projects solely because they express interest.

Similarly, being a qualified N.O.U. developer does not automatically give an individual access to every project.

Project participation shall be determined by:

* Professional classification;
* Assessment results;
* Technical skills;
* Experience;
* Availability;
* Current project workload;
* Previous performance;
* Project requirements;
* Leadership capability where applicable.

---

# 3. RESPONSIBILITY FOR TEAM FORMATION

Team formation shall primarily be a management function supported by the N.O.U. Talent Management system.

The principal responsibilities shall be divided as follows: