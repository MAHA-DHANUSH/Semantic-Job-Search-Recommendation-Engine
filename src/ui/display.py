# pyrefly: ignore [missing-import]
from rich.console import Console
# pyrefly: ignore [missing-import]
from rich.panel import Panel

console = Console()

def show_results(results: list, query: str):
    console.print()
    console.print(Panel(
        f'[bold]Results for:[/bold] "{query}"',
        border_style="cyan",
        padding=(0, 1),
    ))

    for rank, row in enumerate(results, 1):
        pct = row["similarity"] * 100
        bar_len = int(pct / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)

        color = "green" if pct >= 85 else "yellow" if pct >= 70 else "red"
        tags = ", ".join(row["tags"]) if row["tags"] else "—"

        emb_preview = ""
        if "embedding" in row and row["embedding"] is not None:
            emb_list = list(row["embedding"])
            emb_preview = f"\n     🧠 [dim]Embedding: {str(emb_list[:3])[:-1]}... (384-dim)[/dim]"

        console.print(
            f"[bold cyan]#{rank}[/bold cyan]  "
            f"[bold]{row['title']}[/bold]  •  {row['company']}\n"
            f"     📍 {row['location']}  💰 {row['salary'] or '—'}\n"
            f"     🏷  {tags}"
            f"{emb_preview}\n"
            f"     [{color}]{bar}[/{color}]  [{color}]{pct:.1f}% match[/{color}]"
        )
        console.print()

def show_llm_summary(summary: str):
    console.print(Panel(
        summary,
        title="[bold magenta]Gemini Analysis[/bold magenta]",
        border_style="magenta",
        padding=(1, 1),
    ))
    console.print()

def show_tip():
    console.print(
        "[dim]Try queries like:\n"
        "  • remote python job high salary\n"
        "  • I want to work on AI models\n"
        "  • frontend design Figma\n"
        "  • cloud infra automation\n"
        "  • data pipelines big data\n"
        "Type [bold]quit[/bold] to exit.[/dim]\n"
    )
