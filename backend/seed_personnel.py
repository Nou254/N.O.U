"""
Seed the N.O.U. personnel categories and positions (today.md - PERSONNEL
CATEGORIES). Idempotent: existing categories are left untouched, missing ones
are inserted with their default assessment weights and positions.

Usage (from backend/):
    python seed_personnel.py
"""

import asyncio
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Register the full model set so SQLAlchemy can resolve string-based
# relationships (e.g. CompanyProject -> ProjectRelease) when mappers are
# configured in standalone scripts.
import app.models.project_release  # noqa: F401

from app.core.database import async_session_factory, engine
from app.models.personnel import PersonnelCategory, PersonnelPosition

# (category, description, {weight overrides}, [positions])
# Default weights: logic 15, general 5, category 25, position 25,
# practical 25, professional 5.
SEED = [
    (
        "Software Development & Engineering",
        "Designing, developing, maintaining and improving software applications and systems.",
        {},
        [
            "Web Development", "Backend Development", "Frontend Development",
            "Full-Stack Development", "Mobile Application Development",
            "Desktop Application Development", "API Development",
            "Embedded Software Development", "Software Engineering",
            "Software Architecture", "Systems Engineering",
        ],
    ),
    (
        "UI/UX & Product Design",
        "Designing how applications, websites and digital products look, feel and operate.",
        {"practical": 35, "category": 20, "position": 20},
        [
            "UI Design", "UX Design", "UI/UX Design", "Product Design",
            "Interaction Design", "UX Research", "Design Systems",
            "Prototyping", "Usability Design", "Accessibility Design",
        ],
    ),
    (
        "Graphic Design & Digital Media",
        "Visual communication, branding, digital content, graphics, animation and digital media.",
        {"practical": 35, "category": 20, "position": 20},
        [
            "Graphic Design", "Brand Design", "Digital Illustration",
            "Motion Graphics", "2D Design", "3D Design", "Animation",
            "Video Production", "Video Editing", "Digital Content Creation",
        ],
    ),
    (
        "Game Development",
        "Creation and development of digital games for mobile, desktop, web and console.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Game Programming", "Game Design", "Game Development", "Game Art",
            "2D Game Development", "3D Game Development", "Level Design",
            "Game Animation", "Game UI/UX", "Game Testing",
        ],
    ),
    (
        "Database & Data Engineering",
        "Designing, managing, securing, processing and maintaining organizational data systems.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Database Development", "Database Administration",
            "Database Architecture", "Data Engineering", "Data Migration",
            "Data Integration", "Database Security", "Data Infrastructure",
        ],
    ),
    (
        "Data Analytics & Business Intelligence",
        "Analyzing data and transforming it into useful information for decision-making.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Data Analysis", "Business Intelligence", "Data Visualization",
            "Statistical Analysis", "Reporting", "Business Reporting",
            "Data Modelling", "Business Intelligence Development",
        ],
    ),
    (
        "Artificial Intelligence & Machine Learning",
        "Developing, implementing and researching artificial intelligence systems.",
        {"practical": 25, "category": 25, "position": 25},
        [
            "Artificial Intelligence Engineering", "Machine Learning",
            "Deep Learning", "Data Science", "Natural Language Processing",
            "Computer Vision", "Generative AI", "AI Application Development",
            "AI Research", "Intelligent Systems",
        ],
    ),
    (
        "Cybersecurity",
        "Protecting systems, networks, applications, infrastructure and information.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Cybersecurity", "Network Security", "Application Security",
            "Cloud Security", "Security Engineering", "Security Operations",
            "Penetration Testing", "Vulnerability Assessment",
            "Incident Response", "Digital Forensics", "Security Architecture",
        ],
    ),
    (
        "Networking & Telecommunications",
        "Designing, installing, configuring, maintaining and troubleshooting communication networks.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Network Engineering", "Network Administration",
            "Wireless Networking", "Wi-Fi Installation", "Network Security",
            "Network Infrastructure", "Structured Cabling",
            "Telecommunications", "Network Monitoring", "Network Support",
        ],
    ),
    (
        "Cloud Computing & Infrastructure",
        "Cloud platforms, computing infrastructure, deployment and infrastructure operations.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Cloud Engineering", "Cloud Architecture", "Cloud Administration",
            "Cloud Security", "Infrastructure Engineering", "Virtualization",
            "Infrastructure Automation", "Cloud Solutions",
        ],
    ),
    (
        "DevOps & Platform Engineering",
        "Connecting software development with deployment, infrastructure, automation and reliability.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "DevOps Engineering", "DevSecOps", "Site Reliability Engineering",
            "Platform Engineering", "CI/CD", "Containerization",
            "Infrastructure as Code", "Deployment Automation", "System Monitoring",
        ],
    ),
    (
        "Quality Assurance & Software Testing",
        "Ensuring software meets its requirements and maintains acceptable quality standards.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Quality Assurance", "Manual Testing", "Automated Testing",
            "Software Testing", "API Testing", "Performance Testing",
            "Security Testing", "Integration Testing", "Regression Testing",
            "Test Engineering",
        ],
    ),
    (
        "Business & Systems Analysis",
        "Understanding customer and organizational problems and translating them into requirements.",
        {"category": 20, "position": 20, "practical": 20, "logic": 25, "professional": 10},
        [
            "Business Analysis", "Systems Analysis", "Requirements Analysis",
            "Business Process Analysis", "Process Modelling",
            "Systems Requirements", "Stakeholder Analysis",
            "Business Process Improvement",
        ],
    ),
    (
        "Project & Product Management",
        "Planning, coordinating, managing and delivering N.O.U. projects and products.",
        {"category": 20, "position": 20, "practical": 20, "logic": 25, "professional": 10},
        [
            "Project Management", "Project Coordination", "Product Management",
            "Product Ownership", "Scrum Management", "Program Management",
            "Project Planning", "Project Operations",
        ],
    ),
    (
        "Technical Documentation & Knowledge Management",
        "Creating and maintaining technical and operational documentation.",
        {"practical": 25, "position": 25, "category": 20, "professional": 10},
        [
            "Technical Writing", "Software Documentation",
            "API Documentation", "User Documentation",
            "Developer Documentation", "Knowledge Management",
            "Documentation Administration", "Technical Editing",
        ],
    ),
    (
        "IT Support & Technical Operations",
        "Supporting users, systems, devices, software and day-to-day technical operations.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "IT Support", "Technical Support", "Help Desk", "Systems Support",
            "Computer Support", "Field Technical Support",
            "Remote Technical Support", "IT Operations",
        ],
    ),
    (
        "Hardware & Electronics",
        "Computer hardware, electronic systems, embedded hardware and related physical technology.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Hardware Engineering", "Electronics Engineering",
            "Computer Hardware", "Electronics Technology",
            "Hardware Maintenance", "Embedded Hardware", "Circuit Design",
            "PCB Design", "Hardware Troubleshooting",
        ],
    ),
    (
        "IoT & Embedded Systems",
        "Systems that connect physical devices, sensors, machines and software.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Internet of Things (IoT)", "Embedded Systems", "Firmware Development",
            "Smart Devices", "Sensor Systems", "Device Integration",
            "IoT Networking", "IoT Security", "Automation Systems",
        ],
    ),
    (
        "CCTV & Physical Security Technology",
        "Installation, configuration, maintenance and support of electronic security systems.",
        {"practical": 35, "category": 15, "position": 25},
        [
            "CCTV Installation", "CCTV Configuration", "IP Camera Systems",
            "DVR/NVR Systems", "Access Control", "Alarm Systems",
            "Surveillance Systems", "Security System Maintenance",
        ],
    ),
    (
        "Research, Development & Innovation",
        "Investigating emerging technologies and developing experimental solutions.",
        {"practical": 30, "category": 20, "position": 25},
        [
            "Technology Research", "Software Research", "AI Research",
            "Research & Development", "Prototyping",
            "Proof-of-Concept Development", "Emerging Technology Research",
            "Innovation",
        ],
    ),
    (
        "Digital Marketing & Online Services",
        "Promoting N.O.U. products, services, applications and customer solutions.",
        {"practical": 20, "position": 30, "category": 15, "logic": 20, "professional": 10},
        [
            "Digital Marketing", "Search Engine Optimization",
            "Social Media Management", "Digital Advertising",
            "Content Strategy", "Web Analytics", "Online Campaign Management",
            "Digital Communications",
        ],
    ),
    (
        "Sales & Business Development",
        "Identifying business opportunities, acquiring customers and expanding N.O.U.'s market.",
        {"professional": 15, "logic": 25, "position": 20, "category": 15, "practical": 20},
        [
            "Sales", "Business Development", "Account Management",
            "Customer Acquisition", "Partnership Development",
            "Technical Sales", "Client Relationship Management",
            "Corporate Sales",
        ],
    ),
    (
        "Customer Success & Client Services",
        "Maintaining customer relationships after acquisition and providing support.",
        {"professional": 15, "logic": 25, "position": 20, "category": 15, "practical": 20},
        [
            "Customer Success", "Client Support",
            "Customer Relationship Management", "Client Onboarding",
            "Customer Training", "Service Coordination", "Account Support",
        ],
    ),
    (
        "Finance & Accounting",
        "Financial management and financial administration.",
        {"category": 20, "position": 30, "practical": 20, "logic": 20},
        [
            "Accounting", "Finance", "Financial Analysis", "Bookkeeping",
            "Financial Reporting", "Budget Management", "Procurement",
            "Financial Administration",
        ],
    ),
    (
        "Human Resources & Talent Management",
        "Recruitment, employee management, training, performance and the N.O.U. talent pool.",
        {"professional": 10, "category": 20, "position": 25, "logic": 20, "practical": 20},
        [
            "Human Resources", "Recruitment", "Talent Acquisition",
            "Talent Management", "Employee Relations",
            "Training & Development", "Performance Management",
            "Workforce Planning",
        ],
    ),
    (
        "Legal, Compliance & Governance",
        "Legal, regulatory, contractual, risk, privacy and governance matters.",
        {"category": 20, "position": 30, "logic": 25, "practical": 15},
        [
            "Legal Services", "Legal Administration", "Compliance",
            "Data Protection & Privacy", "Contract Administration",
            "Risk Management", "Corporate Governance", "Regulatory Affairs",
        ],
    ),
    (
        "Administration & Operations",
        "General administration and operational management of N.O.U.",
        {"professional": 10, "category": 20, "position": 20, "logic": 25, "practical": 20},
        [
            "Administration", "Office Operations", "Operations Management",
            "Procurement", "Records Management", "Logistics",
            "Facilities Management",
        ],
    ),
    (
        "Internship, Training & Entry-Level Technology",
        "Entry-level category for individuals developing their professional capabilities.",
        {"logic": 25, "general": 15, "category": 20, "position": 15, "practical": 15, "professional": 10},
        [
            "Technology Intern", "Software Development Trainee",
            "IT Trainee", "Junior Technology Assistant", "Graduate Trainee",
            "Technical Apprentice",
        ],
    ),
    (
        "General Technology Personnel",
        "General technology classification for applicants without a defined specialization.",
        {"logic": 20, "general": 15, "category": 20, "position": 15, "practical": 20, "professional": 10},
        [
            "Computer Technician", "IT Assistant", "Digital Technology Assistant",
            "General IT Specialist", "Technology Support Assistant",
        ],
    ),
]


async def seed():
    async with async_session_factory() as db:
        added_categories = 0
        added_positions = 0
        updated_weights = 0
        for name, description, weights, positions in SEED:
            existing = await db.scalar(
                select(PersonnelCategory).where(PersonnelCategory.name == name)
            )
            if existing:
                # Correct any pre-seeded categories whose weights don't total 100.
                existing.weight_logic = weights.get("logic", 15)
                existing.weight_general = weights.get("general", 5)
                existing.weight_category = weights.get("category", 25)
                existing.weight_position = weights.get("position", 25)
                existing.weight_practical = weights.get("practical", 25)
                existing.weight_professional = weights.get("professional", 5)
                updated_weights += 1
                continue
            category = PersonnelCategory(
                name=name,
                description=description,
                weight_logic=weights.get("logic", 15),
                weight_general=weights.get("general", 5),
                weight_category=weights.get("category", 25),
                weight_position=weights.get("position", 25),
                weight_practical=weights.get("practical", 25),
                weight_professional=weights.get("professional", 5),
            )
            db.add(category)
            await db.flush()
            added_categories += 1
            for pos in positions:
                db.add(PersonnelPosition(
                    category_id=category.id,
                    name=pos,
                    modules=json.dumps([pos]),
                    is_active="active",
                ))
                added_positions += 1
        await db.commit()
        print(f"Seeded {added_categories} categories and {added_positions} positions; corrected {updated_weights} existing")


if __name__ == "__main__":
    asyncio.run(seed())
