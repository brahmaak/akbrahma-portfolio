from django.http import Http404
from django.shortcuts import render

# Temporary sample data: replaced by database queries in Phase 8
SAMPLE_PROJECTS = [
    {
        "title": "Developer Portfolio CMS",
        "slug": "developer-portfolio-cms",
        "icon": "bi-person-workspace",
        "summary": "This website: a portfolio with a secure dashboard to manage projects, skills and messages.",
        "technologies": ["Django", "PostgreSQL", "Bootstrap", "JavaScript"],
        "github_url": "#",
        "live_url": "#",
    },
    {
        "title": "E-commerce Store",
        "slug": "ecommerce-store",
        "icon": "bi-cart3",
        "summary": "Product catalogue, shopping cart and order management with user accounts.",
        "technologies": ["Python", "Django", "PostgreSQL", "JavaScript"],
        "github_url": "#",
        "live_url": "#",
    },
    {
        "title": "Task Manager App",
        "slug": "task-manager-app",
        "icon": "bi-kanban",
        "summary": "Create, organise and track tasks with deadlines, priorities and user login.",
        "technologies": ["Django", "PostgreSQL", "JavaScript"],
        "github_url": "#",
        "live_url": "#",
    },
    {
        "title": "Blog Platform",
        "slug": "blog-platform",
        "icon": "bi-journal-richtext",
        "summary": "Multi-author blog with categories, comments and an admin editor.",
        "technologies": ["Python", "Django", "Bootstrap"],
        "github_url": "#",
        "live_url": "#",
    },
    {
        "title": "Weather Dashboard",
        "slug": "weather-dashboard",
        "icon": "bi-cloud-sun",
        "summary": "Live weather search using a public API, with a 5-day forecast.",
        "technologies": ["JavaScript", "HTML5", "CSS3"],
        "github_url": "#",
        "live_url": "#",
    },
    {
        "title": "Restaurant Landing Page",
        "slug": "restaurant-landing-page",
        "icon": "bi-shop",
        "summary": "Responsive restaurant website with menu, gallery and reservation form.",
        "technologies": ["HTML5", "CSS3", "Bootstrap"],
        "github_url": "#",
        "live_url": "#",
    },
]


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


def projects(request):
    """Show all projects with technology filter buttons."""
    # Build a sorted list of every technology used, with no duplicates
    technologies = sorted(
        {tech for project in SAMPLE_PROJECTS for tech in project["technologies"]}
    )
    context = {
        "projects": SAMPLE_PROJECTS,
        "technologies": technologies,
    }
    return render(request, "portfolio/projects.html", context)


def project_detail(request, slug):
    """Show one project, found by its slug."""
    # Find the project whose slug matches the URL, or None if there isn't one
    project = next((p for p in SAMPLE_PROJECTS if p["slug"] == slug), None)
    if project is None:
        raise Http404("Project not found")

    other_projects = [p for p in SAMPLE_PROJECTS if p["slug"] != slug][:3]
    context = {
        "project": project,
        "other_projects": other_projects,
    }
    return render(request, "portfolio/project_detail.html", context)
