
**UI/UX Designer**

> Design the interface for a supplied business scenario.

**Network Engineer**

> Design and troubleshoot a network.

**Cybersecurity Applicant**

> Analyze a controlled security scenario.

**QA Engineer**

> Test a supplied application.

**Project Manager**

> Develop a project plan.

**Business Analyst**

> Convert a customer interview into system requirements.

---

# 38. ASSESSMENT QUESTION BANK

The N.O.U. platform should not permanently expose the same examination to every applicant.

Each module should have a **question bank**.

For example:

```text
CATEGORY
Software Development

POSITION
Backend Developer

MODULE
Database

QUESTION BANK
├── Question 001
├── Question 002
├── Question 003
├── Question 004
├── Question 005
├── Practical Task 001
├── Practical Task 002
└── Scenario 001
```

The system can select different questions from the bank.

This reduces applicants sharing the exact examination questions with future applicants.

---

# 39. Assessment Types

Each question should have a classification.

N:B NO MULTIPLE CHOICE QUESTIONS AND ANSWERS

### Short Answer

Tests understanding.

### Written Explanation

Tests reasoning.

### Scenario

Tests real-world decision-making.

### Practical

Tests actual ability.

### Debugging

Tests troubleshooting.

### Design

Tests solution architecture/design.

### Project

Tests the ability to produce a complete solution.

---

# 40. Recommended Applicant Assessment Flow

```text
APPLICANT
   │
   ▼
CREATE ACCOUNT
   │
   ▼
SELECT PROFESSIONAL CATEGORY
   │
   ▼
SELECT POSITION
   │
   ▼
COMMON ASSESSMENT
   │
   ▼
CATEGORY ASSESSMENT
   │
   ▼
POSITION ASSESSMENT
   │
   ▼
PRACTICAL ASSESSMENT
   │
   ▼
ASSESSMENT REVIEW
   │
   ▼
COMPETENCY SCORE
   │
   ▼
TALENT CLASSIFICATION
   │
   ▼
N.O.U. TALENT POOL
   │
   ▼
PROJECT/VACANCY MATCHING
```

---

# 41. Important Rule for N.O.U.

The assessment system should **not be designed merely to eliminate people**.

Its more important purpose is to answer:

> **"What can this person actually do, and where can N.O.U. use their abilities?"**

Therefore, an applicant who does not qualify for Backend Development might demonstrate excellent UI/UX, networking, database, technical support, or analytical abilities.

The system should be capable of recommending an alternative category where the assessment evidence supports it.

---

# 42. Final Assessment Principle

N.O.U. Digital Systems shall apply the following principle:

> **Knowledge gets an applicant into consideration; practical ability demonstrates competence; critical thinking demonstrates problem-solving capacity; professional conduct demonstrates reliability; and project performance demonstrates sustained capability.**

The assessment system should therefore become a **talent classification engine**, not simply an employment examination.

**Next logical document:** *Position-by-Position Assessment Structure* — where we take each category above and define the actual positions under it, the required educational modules, number/type of questions, practical examination, pass marks, and how the system determines whether an applicant qualifies for that particular position.

# N.O.U. DIGITAL SYSTEMS

# PROJECT FLOW AND PORTAL ACCESS STRUCTURE

**Website:** nou.com
**Document Status:** Draft
**Purpose:** Define the complete lifecycle of a customer project and establish the portals through which customers, administrators, analysts, developers, investors, and management interact with the project.

---

# 1. INTRODUCTION

The N.O.U. platform should not treat a customer project as a single transaction between a customer and a developer.

A project should move through a controlled lifecycle in which each stage has:

* A defined purpose;
* Responsible personnel;
* Required documentation;
* Approval requirements;
* Access restrictions;
* Status tracking; and
* A clear transition to the next stage.

The central N.O.U. platform shall therefore consist of several interconnected portals rather than one dashboard where everyone can see and modify everything.

---

# 2. MASTER PROJECT FLOW

The proposed project lifecycle is:

```text
CUSTOMER
   │
   ▼
CUSTOMER PORTAL
   │
   │  Submit Project Request
   ▼
PROJECT INTAKE
   │
   ▼
ADMIN PORTAL
   │
   │ Initial Screening
   ▼
BUSINESS / COMPLIANCE REVIEW
   │
   ▼
REQUIREMENTS & ANALYSIS PORTAL
   │
   │ Requirements Gathering
   ▼
TECHNICAL FEASIBILITY
   │
   ▼
TECHNICAL ARCHITECTURE
   │
   ▼
PROJECT DOCUMENTATION
   │
   ▼
TECHNICAL / MANAGEMENT REVIEW
   │
   ▼
PROJECT ESTIMATION
   │
   ├── Cost
   ├── Personnel
   ├── Timeline
   ├── Infrastructure
   └── Risk
   │
   ▼
CUSTOMER PROPOSAL
   │
   ▼
CUSTOMER APPROVAL
   │
   ▼
PROJECT MANAGEMENT PORTAL
   │
   ▼
PERSONNEL SELECTION
   │
   ▼
PROJECT TEAM PORTAL
   │
   ▼
DEVELOPMENT
   │
   ▼
CODE REVIEW
   │
   ▼
QA / TESTING
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
PROJECT CLOSURE
   │
   ▼
SUPPORT / MAINTENANCE
```

---

# 3. N.O.U. PORTAL STRUCTURE

I recommend the following major portals.

| Portal                         | Main Purpose                     |
| ------------------------------ | -------------------------------- |
| Customer Portal                | Customer interaction             |
| Admin Portal                   | Company-wide administration      |
| Project Intake Portal          | Manage incoming requests         |
| Requirements & Analysis Portal | Gather and define requirements   |
| Architecture Portal            | Technical solution design        |
| Documentation Portal           | Manage project documentation     |
| Project Management Portal      | Manage approved projects         |
| Talent/Employment Portal       | Recruit and classify personnel   |
| Project Team Portal            | Developers' working environment  |
| QA Portal                      | Testing and quality assurance    |
| Security Portal                | Security assessment              |
| Investor Portal                | Project visibility for investors |
| Support Portal                 | Post-delivery customer support   |
| Management Portal              | Executive oversight              |

These do **not necessarily need to be separate websites**.

They can be separate modules within the same N.O.U. platform.

---

# 4. CUSTOMER PORTAL

## Purpose

The Customer Portal is the customer's primary interface with N.O.U.

### Customer can:

* Create an account;
* Manage profile;
* Submit project requests;
* View submitted requests;
* Communicate with N.O.U.;
* Review proposals;
* Approve/reject proposals;
* View project status;
* View milestones;
* Submit feedback;
* Participate in acceptance testing;
* Access delivered software;
* Download authorized deliverables;
* Submit support requests;
* View invoices/payment information where integrated.

### Customer cannot:

* Access developer workspaces;
* View internal technical discussions;
* Assign N.O.U. employees;
* Change architecture;
* Modify project documentation directly;
* Access internal financial information;
* View other customers' projects.

---

# 5. PROJECT INTAKE PORTAL

This handles the transition between customer submission and internal review.

## Access

**Primary:**

* Admin
* Project Intake Officer

**Limited:**

* Management

### Functions

The portal displays:

* New project requests;
* Request status;
* Customer information;
* Requested services;
* Attachments;
* Initial requirements;
* Submission date;
* Priority;
* Assigned analyst.

### Possible statuses

```text
NEW
   ↓
UNDER INITIAL REVIEW
   ↓
CLARIFICATION REQUIRED
   ↓
ACCEPTED FOR ANALYSIS
   ↓
REJECTED
```

---

# 6. ADMIN PORTAL

The Admin Portal is the central operational control area.

## Access

**Full access:**

* System Administrator
* Authorized Company Management

**Restricted access:**

* Department Heads

### Admin functions

The administrator can:

* Manage users;
* Manage roles;
* Review project requests;
* Assign analysts;
* Approve workflow transitions;
* Manage personnel;
* Manage projects;
* Manage company documents;
* Monitor system activity;
* Manage permissions;
* View audit logs;
* Manage portal configuration.

### Important restriction

Admin should **not automatically be able to modify technical documentation simply because they are an administrator**.

Technical content should remain under the responsible technical teams.

---

# 7. REQUIREMENTS & ANALYSIS PORTAL

This is one of the most important new portals.

## Primary users

* Business Analysts
* Systems Analysts
* Requirements Analysts

## Secondary access

* Project Managers
* Technical Architects
* Authorized Admin
* Customer — selected portions

### Responsibilities

The analyst uses this portal to determine:

> What does the customer actually need?

The portal should contain:

* Customer interviews;
* Requirements;
* User stories;
* Use cases;
* Business rules;
* Workflows;
* User roles;
* Functional requirements;
* Non-functional requirements;
* Acceptance criteria;
* Questions requiring customer clarification.

### Customer interaction

Customers should be able to review and approve **customer-facing requirements**, but should not modify N.O.U.'s internal analysis.

---

# 8. TECHNICAL ARCHITECTURE PORTAL

This portal is used after requirements are sufficiently understood.

## Primary users

* Software Architects
* Senior Engineers
* Database Engineers
* DevOps Engineers
* Security Engineers

## Secondary access

* Project Manager
* Business Analyst
* Authorized Management

### Functions

The portal manages:

* System architecture;
* Technology stack;
* Database architecture;
* API architecture;
* Infrastructure;
* Authentication;
* Security architecture;
* Integration requirements;
* Scalability;
* Backup;
* Disaster recovery.

### Example

```text
Frontend:
React

Backend:
FastAPI

Database:
PostgreSQL

Authentication:
OAuth2 / JWT

Infrastructure:
Cloud

External Services:
SMS
Payments
Email
```

---

# 9. DOCUMENTATION PORTAL

The Documentation Portal becomes the official project knowledge base.

## Access

### Full/Authoring

* Business Analysts
* Systems Analysts
* Technical Architects
* Project Managers
* Technical Writers

### Review

* Department Heads
* Senior Engineers
* Management

### Read-only

* Developers
* QA
* Security Team
* Customer — approved sections

### Documents

The portal should contain:

1. Project Charter
2. Requirements Specification
3. Technical Design
4. Database Design
5. UI/UX Specification
6. Security Requirements
7. Project Plan
8. Testing Strategy
9. Deployment Plan
10. User Documentation

Every document should have:

* Version;
* Author;
* Reviewer;
* Date;
* Approval status;
* Change history.

---

# 10. PROJECT MANAGEMENT PORTAL

This becomes the central operational area once a project is approved.

## Primary users

* Project Manager
* Project Coordinator

## Access

### Management

Read/oversight.

### Developers

Project-specific access.

### Customer

Limited progress visibility.

### Investors

Read-only project progress where authorized.

### Functions

The Project Management Portal manages:

* Project status;
* Milestones;
* Tasks;
* Deadlines;
* Dependencies;
* Team;
* Risks;
* Issues;
* Resources;
* Progress;
* Weekly reports;
* Approvals;
* Project communications.

---

# 11. TALENT / EMPLOYMENT PORTAL

This portal connects N.O.U.'s employment system to project staffing.

## Users

### Applicants

* Apply for positions;
* Take assessments;
* Upload portfolios;
* View results where appropriate;
* Manage professional profiles.

### HR/Talent Management

* Review applicants;
* Classify personnel;
* Manage talent pool;
* Manage employment status.

### Project Managers

* Search eligible personnel;
* View approved skills;
* Check availability;
* Request personnel.

### Department Heads

* Approve personnel assignments.

### Admin/Management

* Oversight.

---

# 12. PROJECT TEAM PORTAL

This is where the actual development team works.

## Users

Only assigned project personnel should have access.

For example:

```text
Project Manager
Business Analyst
UI/UX Designer
Frontend Developers
Backend Developers
Database Engineer
DevOps Engineer
QA Engineer
Security Engineer
```

### Functions

* Assigned tasks;
* Project documentation;
* Team communication;
* Code repository links;
* Task progress;
* Development milestones;
* Technical discussions;
* File sharing;
* Weekly progress information;
* Project notices.

---

# 13. PROJECT TEAM LEADER ACCESS

The Team Leader should have additional project permissions.

They can:

* View all team tasks;
* Assign tasks within the approved project structure;
* Monitor progress;
* Review team submissions;
* Submit weekly reports;
* Escalate issues;
* Request extensions;
* Request additional resources.

They should **not** be able to:

* Change project scope independently;
* Increase project budget;
* Add unauthorized personnel;
* Remove personnel without authorization;
* Change technical architecture without approval.

---

# 14. QA PORTAL

Quality Assurance should have a separate controlled environment.

## Users

* QA Engineers
* QA Lead
* Project Manager
* Developers — limited defect information
* Management — read-only

### Functions

* Test cases;
* Test plans;
* Test execution;
* Bug reporting;
* Defect severity;
* Regression testing;
* Acceptance testing;
* Test results;
* Release approval.

### Basic workflow

```text
DEVELOPMENT COMPLETE
        ↓
QA TEST
        ↓
FAILED ──────► DEVELOPMENT
        │
        ▼
      PASSED
        ↓
SECURITY REVIEW
        ↓
STAGING
```

---

# 15. SECURITY PORTAL

Not every project necessarily needs a separate security team, but N.O.U. should have a security review capability.

## Users

* Security Engineers
* Cybersecurity Lead
* Authorized Architects
* Management — oversight

### Functions

* Security requirements;
* Vulnerability findings;
* Security testing;
* Access review;
* Risk assessment;
* Security approval;
* Incident tracking.

Developers should see the findings relevant to fixing their work, but highly sensitive security information should be appropriately restricted.

---

# 16. INVESTOR PORTAL

Investors should have **visibility without operational authority**.

## Investor can view:

* Approved project list;
* Project status;
* Milestones;
* General progress;
* Approved progress reports;
* High-level financial/project information where authorized;
* Project completion status.

## Investor cannot:

* Assign employees;
* Modify requirements;
* Approve code;
* Change project deadlines;
* Access customer confidential information;
* Access source code;
* Access credentials;
* Direct developers.

---

# 17. SUPPORT PORTAL

After delivery, the customer moves into the support lifecycle.

## Users

### Customer

* Report problems;
* Request support;
* Track tickets;
* View responses.

### Support Team

* Receive tickets;
* Diagnose issues;
* Escalate technical problems.

### Developers

Access only when technical intervention is required.

### Project Manager

Can oversee unresolved issues.

---

# 18. MANAGEMENT PORTAL

Management requires a higher-level view than administrators.

The Management Portal should show:

### Company

* Active projects;
* Completed projects;
* Pending projects;
* Revenue;
* Expenses;
* Personnel;
* Capacity;
* Project risks.

### Personnel

* Available developers;
* Active developers;
* Project workload;
* Performance;
* Skills.

### Projects

* On schedule;
* Delayed;
* At risk;
* Completed;
* Over budget;
* Awaiting customer.

### Important

Management should see **aggregated information** without necessarily having access to every private conversation or technical credential.

---

# 19. ACCESS CONTROL MODEL

N.O.U. should use **Role-Based Access Control (RBAC)**.

A person's login should determine:

> Who they are → What department they belong to → What project they belong to → What they are allowed to see/do.

For example:

```text
USER
 │
 ├── ROLE
 │     └── Developer
 │
 ├── DEPARTMENT
 │     └── Software Engineering
 │
 └── PROJECT
       └── NOU-PRJ-0047
```

The developer should therefore only receive the permissions necessary for that project.

---

# 20. ACCESS LEVELS

N.O.U. should not simply use:

> Admin / User

Instead, use permission levels such as:

### Level 1 — Public

No authentication required.

### Level 2 — Customer

Customer-specific information.

### Level 3 — Applicant

Employment and assessment information.

### Level 4 — Employee

Internal company information.

### Level 5 — Project Member

Specific project information.

### Level 6 — Team Leader

Additional project management permissions.

### Level 7 — Department Head

Department oversight.

### Level 8 — Administrator

System administration.

### Level 9 — Management

Company-wide oversight.

### Level 10 — Super Administrator

Highly restricted system-level control.

---

# 21. PROJECT STATUS FLOW

Every project should have a controlled status.

```text
REQUESTED
   ↓
INITIAL REVIEW
   ↓
CLARIFICATION
   ↓
ANALYSIS
   ↓
TECHNICAL FEASIBILITY
   ↓
DOCUMENTATION
   ↓
INTERNAL REVIEW
   ↓
ESTIMATION
   ↓
CUSTOMER PROPOSAL
   ↓
CUSTOMER APPROVAL
   ↓
TEAM FORMATION
   ↓
PLANNING
   ↓
DEVELOPMENT
   ↓
QA
   ↓
SECURITY REVIEW
   ↓
STAGING
   ↓
CUSTOMER ACCEPTANCE
   ↓
DEPLOYMENT
   ↓
SUPPORT
   ↓
CLOSED
```

At any stage, the project can also enter:

```text
ON HOLD
BLOCKED
CANCELLED
REJECTED
```

---

# 22. PROJECT DOCUMENT APPROVAL FLOW

Documents should also have their own workflow.

```text
DRAFT
 ↓
UNDER REVIEW
 ↓
REVISION REQUIRED
 ↓
RE-SUBMITTED
 ↓
APPROVED
 ↓
LOCKED VERSION
```

Once a document is approved, developers should work against the **approved version**.

If requirements change later, the system should create a **change request** rather than silently modifying the original requirements.

---

# 23. CHANGE REQUEST PORTAL/FUNCTION

I recommend adding this from V1.0.

A customer may later say:

> "I also want mobile payments."

That should **not simply be added to the developer's task list**.

Instead:

```text
CHANGE REQUEST
      ↓
Impact Analysis
      ↓
Technical Review
      ↓
Cost/Timeline Impact
      ↓
Customer Approval
      ↓
Documentation Updated
      ↓
Development Task Created
```

This protects N.O.U. from uncontrolled **scope creep**.

---

# 24. FINAL PORTAL RELATIONSHIP

The overall N.O.U. system can therefore be visualized as:

```text
                         N.O.U. PLATFORM
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
 CUSTOMER PORTAL          EMPLOYMENT PORTAL        INVESTOR PORTAL
        │                       │                        │
        ▼                       ▼                        │
 PROJECT REQUEST          TALENT DATABASE                │
        │                       │                        │
        ▼                       │                        │
 ADMIN / INTAKE                │                        │
        │                       │                        │
        ▼                       │                        │
 REQUIREMENTS & ANALYSIS ◄──────┘                        │
        │                                                │
        ▼                                                │
 TECHNICAL ARCHITECTURE                                  │