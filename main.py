import sys
import os

# Add the project root to sys.path so that 'src' is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# pyrefly: ignore [missing-import]
from rich.console import Console
# pyrefly: ignore [missing-import]
from rich.panel import Panel

from src.config.db import connect
from src.models.embedding import get_model
from src.services.job_service import seed_jobs, semantic_search
from src.services.llm_service import summarize_results
from src.ui.display import show_results, show_llm_summary, show_tip

console = Console()

def main():
    console.print(Panel(
        "[bold cyan]Job Board — Semantic Search[/bold cyan]\n"
        "[dim]Powered by pgvector · sentence-transformers · Gemini 2.0 Flash[/dim]",
        border_style="cyan",
    ))

    console.print(f"[dim]Connecting to PostgreSQL…[/dim]")
    try:
        conn = connect()
        console.print(f"[green]✓[/green] Connected to database: [cyan]{conn.info.dbname}[/cyan]\n")
    except Exception as e:
        console.print(f"[red]PostgreSQL connection failed:[/red] {e}")
        console.print("[yellow]Start PostgreSQL and run setup.sql first.[/yellow]")
        return

    console.print(f"[dim]Loading embedding model (all-MiniLM-L6-v2)…[/dim]")
    get_model()  # Preload the model
    console.print("[green]✓[/green] Model ready\n")

    seed_jobs(conn)
    console.print()
    show_tip()

    while True:
        try:
            query = console.input("[bold cyan]Search:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            console.print("[dim]Bye![/dim]")
            break

        results = semantic_search(conn, query, top_k=5)
        show_results(results, query)

        # LLM reasoning & summarization via Gemini
        console.print("[dim]🤖 Asking Gemini to reason over results…[/dim]")
        try:
            summary = summarize_results(query, results)
            show_llm_summary(summary)
        except EnvironmentError as e:
            console.print(f"[yellow]⚠ LLM summary skipped:[/yellow] {e}")
        except Exception as e:
            console.print(f"[red]LLM error:[/red] {e}")

    conn.close()

if __name__ == "__main__":
    main()
