from django.shortcuts import render


def skills(request):
    """Show skills grouped by category."""
    # Temporary sample data: replaced by a database query in Phase 8
    skill_groups = [
        {
            "category": "Frontend",
            "icon": "bi-window-sidebar",
            "skills": [
                {"name": "HTML5", "level": 90},
                {"name": "CSS3", "level": 85},
                {"name": "JavaScript", "level": 75},
                {"name": "Bootstrap", "level": 85},
            ],
        },
        {
            "category": "Backend",
            "icon": "bi-server",
            "skills": [
                {"name": "Python", "level": 80},
                {"name": "Django", "level": 75},
                {"name": "REST APIs", "level": 65},
            ],
        },
        {
            "category": "Database",
            "icon": "bi-database",
            "skills": [
                {"name": "PostgreSQL", "level": 70},
                {"name": "SQL", "level": 70},
            ],
        },
        {
            "category": "Tools",
            "icon": "bi-tools",
            "skills": [
                {"name": "Git", "level": 75},
                {"name": "GitHub", "level": 75},
                {"name": "VS Code", "level": 85},
            ],
        },
    ]
    context = {"skill_groups": skill_groups}
    return render(request, "portfolio/skills.html", context)
