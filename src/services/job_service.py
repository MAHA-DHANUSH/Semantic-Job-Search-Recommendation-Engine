from psycopg2.extras import RealDictCursor
# pyrefly: ignore [missing-import]
from rich.console import Console
from src.models.embedding import embed

console = Console()

# Define the 5 sample job designations directly inline
SAMPLE_JOBS = [
    {
        "title": "Senior Backend Engineer",
        "company": "DataFlow Inc",
        "location": "Remote",
        "salary": "₹30-45 LPA",
        "tags": ["Python", "FastAPI", "PostgreSQL", "AWS"],
        "description": (
            "We are looking for an experienced backend developer skilled in Python "
            "and REST APIs. Work fully remotely with a globally distributed team. "
            "Competitive compensation, stock options, flexible hours. "
            "You will design scalable microservices and own the data pipeline."
        ),
    },
    {
        "title": "ML Engineer",
        "company": "NeuralMind",
        "location": "Bangalore (Hybrid)",
        "salary": "₹25–40 LPA",
        "tags": ["PyTorch", "Python", "LLMs", "MLOps"],
        "description": (
            "Build and deploy large language models in production. "
            "Strong Python skills required. Work on cutting-edge AI research "
            "alongside a world-class team. Great pay and annual bonus. "
            "Hybrid office in Bangalore."
        ),
    },
    {
        "title": "Frontend Developer",
        "company": "PixelCraft",
        "location": "Chennai",
        "salary": "₹12–18 LPA",
        "tags": ["React", "TypeScript", "Figma", "CSS"],
        "description": (
            "Create beautiful, responsive web interfaces using React and TypeScript. "
            "Collaborate with designers. Office-based in Chennai. "
            "Great work culture and growth opportunities."
        ),
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudNine",
        "location": "Remote",
        "salary": "₹20–35 LPA",
        "tags": ["Kubernetes", "Terraform", "AWS", "CI/CD"],
        "description": (
            "Manage cloud infrastructure on AWS, automate deployments with Terraform "
            "and Kubernetes. Remote-first company. Good pay and strong work-life balance. "
            "You will build and maintain CI/CD pipelines."
        ),
    },
    {
        "title": "Data Analyst",
        "company": "Insightful Co",
        "location": "Mumbai",
        "salary": "₹8–14 LPA",
        "tags": ["SQL", "Tableau", "Excel", "Python"],
        "description": (
            "Analyse business data, build dashboards, and present insights to stakeholders. "
            "SQL and Tableau expertise needed. Entry-level friendly. "
            "Mumbai office, good work culture."
        ),
    }
]

def seed_jobs(conn):
    """Ensure vector extension, create table, and seed 5 sample jobs."""
    with conn.cursor() as cur:
        # Enable vector extension
        console.print("[bold yellow]1. Database Setup[/bold yellow]")
        console.print("[dim]   Enabling pgvector extension if not exists…[/dim]")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Recreate table to ensure fresh setup of 5 designations
        console.print("[dim]   Creating table 'jobs'…[/dim]")
        cur.execute("DROP TABLE IF EXISTS jobs;")
        cur.execute("""
            CREATE TABLE jobs (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                salary TEXT,
                tags TEXT[],
                description TEXT NOT NULL,
                embedding vector(384)
            );
        """)
        conn.commit()
        console.print("[green]   ✓[/green] Table 'jobs' created successfully.")

        # Seed exactly 5 sample jobs
        console.print(f"\n[bold yellow]2. Seeding Embeddings[/bold yellow]")
        console.print(f"[dim]   Generating 384-dim embeddings and inserting {len(SAMPLE_JOBS)} designations…[/dim]")
        for j in SAMPLE_JOBS:
            vec = embed(j["description"])
            cur.execute(
                """INSERT INTO jobs (title, company, location, salary, tags, description, embedding)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (j["title"], j["company"], j["location"],
                 j["salary"], j["tags"], j["description"], vec),
            )
        conn.commit()
        console.print(f"[green]   ✓[/green] Successfully stored {len(SAMPLE_JOBS)} designations with embeddings in PostgreSQL.")

def semantic_search(conn, query: str, top_k: int = 5) -> list:
    """
    Core of the whole app:
      1. Embed the user's free-text query
      2. Ask pgvector for the top_k closest job vectors (cosine distance)
      3. Return ranked results with similarity score
    """
    query_vec = embed(query)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT
                title, company, location, salary, tags, embedding,
                1 - (embedding <=> %s::vector)  AS similarity
            FROM jobs
            ORDER BY embedding <=> %s::vector    -- nearest neighbours first
            LIMIT %s
            """,
            (query_vec, query_vec, top_k),
        )
        return cur.fetchall()
