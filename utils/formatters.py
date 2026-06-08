from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns

from models.schemas import ComplaintAnalysis, StartupOpportunity, MVPSpec, EmotionalIntensity

console = Console()

INTENSITY_COLORS = {
    EmotionalIntensity.LOW: "green",
    EmotionalIntensity.MEDIUM: "yellow",
    EmotionalIntensity.HIGH: "orange1",
    EmotionalIntensity.EXTREME: "red",
}

INTENSITY_EMOJI = {
    EmotionalIntensity.LOW: "😐",
    EmotionalIntensity.MEDIUM: "😤",
    EmotionalIntensity.HIGH: "😠",
    EmotionalIntensity.EXTREME: "🤬",
}


def print_header(title: str, subtitle: str = "") -> None:
    text = Text(title, style="bold white")
    if subtitle:
        text.append(f"\n{subtitle}", style="dim white")
    console.print(Panel(text, style="bold blue", padding=(1, 4)))


def print_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    console.print(f"[bold green]✓[/bold green] {message}")


def print_complaint_analysis(analysis: ComplaintAnalysis) -> None:
    console.print()
    console.print(Panel(
        f"[bold white]{analysis.product_category}[/bold white]\n\n"
        f"[dim]{analysis.summary}[/dim]",
        title="[bold blue]Complaint Mining Analysis[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    ))

    console.print()
    console.print("[bold cyan]TOP COMPLAINTS[/bold cyan]")
    console.print()

    for i, complaint in enumerate(analysis.top_complaints, 1):
        color = INTENSITY_COLORS[complaint.emotional_intensity]
        emoji = INTENSITY_EMOJI[complaint.emotional_intensity]

        table = Table(box=box.ROUNDED, border_style=color, show_header=False, padding=(0, 1))
        table.add_column("Key", style="dim", width=20)
        table.add_column("Value", style="white")

        table.add_row("Frequency", f"~{complaint.frequency:,} mentions/month")
        table.add_row(
            "Intensity",
            f"[{color}]{emoji} {complaint.emotional_intensity.value.upper()}[/{color}]"
        )
        table.add_row("Affects", ", ".join(complaint.affected_user_segments))

        quote_text = "\n".join(f'  "[italic]{q}[/italic]"' for q in complaint.example_quotes[:2])

        console.print(Panel(
            f"[bold white]{i}. {complaint.title}[/bold white]\n\n"
            f"{complaint.description}\n\n"
            f"[dim]Example voices:[/dim]\n{quote_text}",
            subtitle_align="left",
            border_style=color,
            padding=(0, 1),
        ))
        console.print(table)
        console.print()

    console.print("[bold cyan]EXISTING SOLUTIONS[/bold cyan]")
    console.print()

    sol_table = Table(box=box.ROUNDED, border_style="dim", show_header=True)
    sol_table.add_column("Solution", style="bold white", width=20)
    sol_table.add_column("Description", width=35)
    sol_table.add_column("Key Limitations", style="red", width=40)

    for sol in analysis.existing_solutions:
        limitations = "\n".join(f"• {l}" for l in sol.limitations[:3])
        sol_table.add_row(sol.name, sol.description, limitations)

    console.print(sol_table)

    console.print()
    console.print("[bold cyan]MARKET GAPS[/bold cyan]")
    console.print()

    for gap in analysis.market_gaps:
        gap_text = (
            f"[bold yellow]{gap.description}[/bold yellow]\n\n"
            f"[dim]Why existing solutions fail:[/dim] {gap.why_existing_solutions_fail}\n"
            f"[dim]Estimated market size:[/dim] [green]{gap.estimated_market_size}[/green]"
        )
        console.print(Panel(gap_text, border_style="yellow", padding=(0, 1)))
        console.print()

    console.print(Panel(
        f"[bold green]TAM:[/bold green] {analysis.market_opportunity.total_addressable_market}\n"
        f"[bold green]SAM:[/bold green] {analysis.market_opportunity.serviceable_addressable_market}\n"
        f"[bold green]Growth:[/bold green] {analysis.market_opportunity.growth_rate}\n"
        f"[bold green]Urgency:[/bold green] {analysis.market_opportunity.urgency}",
        title="[bold green]Market Opportunity[/bold green]",
        border_style="green",
        padding=(0, 1),
    ))

    console.print()
    console.print(f"[dim]Sources analyzed: {', '.join(analysis.data_sources_analyzed)}[/dim]")


def print_opportunities(opportunities: List[StartupOpportunity]) -> None:
    console.print()
    console.print("[bold cyan]STARTUP OPPORTUNITIES[/bold cyan]")
    console.print()

    for i, opp in enumerate(opportunities, 1):
        score_color = "green" if opp.confidence_score >= 70 else "yellow" if opp.confidence_score >= 40 else "red"

        header = (
            f"[bold white]{i}. {opp.name}[/bold white]  "
            f"[{score_color}]Confidence: {opp.confidence_score}/100[/{score_color}]\n"
            f"[italic dim]{opp.one_liner}[/italic dim]"
        )

        details = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        details.add_column("Key", style="dim", width=22)
        details.add_column("Value", style="white")

        details.add_row("Target Users", ", ".join(opp.target_users))
        details.add_row("Revenue Potential", f"[green]{opp.estimated_revenue_potential}[/green]")
        details.add_row("Difficulty", opp.difficulty_to_build)
        details.add_row("Time to Market", opp.time_to_market)
        details.add_row("Differentiators", "\n".join(f"• {d}" for d in opp.key_differentiators[:3]))

        console.print(Panel(
            f"{header}\n\n"
            f"[dim]Problem:[/dim] {opp.problem}\n"
            f"[dim]Solution:[/dim] {opp.solution}",
            border_style="cyan",
            padding=(0, 1),
        ))
        console.print(details)
        console.print()


def print_mvp_spec(spec: MVPSpec) -> None:
    console.print()
    console.print(Panel(
        f"[bold white]{spec.opportunity_name}[/bold white]\n\n"
        f"[dim]{spec.problem_statement}[/dim]",
        title="[bold magenta]MVP Specification[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
    ))

    console.print()
    console.print("[bold magenta]CORE FEATURES[/bold magenta]")
    for f in spec.core_features:
        console.print(f"  [cyan]▸[/cyan] {f}")

    console.print()
    console.print(Panel(
        f"[bold]Stack:[/bold] {spec.tech_stack_recommendation}\n"
        f"[bold]Timeline:[/bold] {spec.timeline}",
        title="[bold]Technical[/bold]",
        border_style="dim",
        padding=(0, 1),
    ))

    console.print()
    console.print("[bold magenta]PRICING MODEL[/bold magenta]")
    price_table = Table(box=box.ROUNDED, border_style="magenta")
    price_table.add_column("Tier", style="bold white", width=15)
    price_table.add_column("Price", style="green", width=15)
    price_table.add_column("Target User", width=25)
    price_table.add_column("Features", width=50)

    for tier in spec.pricing_model:
        price_table.add_row(
            tier.name,
            tier.price,
            tier.target_user,
            "\n".join(f"• {f}" for f in tier.features[:4]),
        )
    console.print(price_table)

    console.print()
    console.print("[bold magenta]GO-TO-MARKET[/bold magenta]")
    for step in spec.go_to_market:
        console.print(f"  [magenta]→[/magenta] {step}")

    console.print()
    console.print("[bold magenta]COMPETITOR ANALYSIS[/bold magenta]")
    for comp in spec.competitor_analysis:
        console.print(f"  [yellow]⚡[/yellow] {comp}")

    console.print()
    console.print("[bold magenta]MARKETING ANGLES[/bold magenta]")
    for angle in spec.marketing_angles:
        console.print(f"  [cyan]✦[/cyan] {angle}")

    console.print()
    console.print("[bold magenta]WEEK ONE ACTIONS[/bold magenta]")
    for j, action in enumerate(spec.week_one_actions, 1):
        console.print(f"  [bold white]{j}.[/bold white] {action}")

    console.print()
    console.print("[bold magenta]SUCCESS CRITERIA[/bold magenta]")
    for criterion in spec.success_criteria:
        console.print(f"  [green]✓[/green] {criterion}")

    console.print()
    console.print("[bold magenta]KEY METRICS TO TRACK[/bold magenta]")
    for metric in spec.key_metrics:
        console.print(f"  [dim]📊[/dim] {metric}")
