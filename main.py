#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import ANTHROPIC_API_KEY, REDDIT_ENABLED, OUTPUT_DIR
from models.schemas import ComplaintAnalysis, StartupOpportunity
from scrapers.mock_data import get_mock_complaints
from scrapers.reddit_scraper import scrape_reddit
from analyzers.complaint_analyzer import analyze_complaints
from analyzers.opportunity_generator import generate_opportunities
from analyzers.mvp_builder import build_mvp_spec
from utils.formatters import (
    print_complaint_analysis,
    print_opportunities,
    print_mvp_spec,
    print_header,
    print_error,
    print_success,
)

app = typer.Typer(
    name="complaint-miner",
    help="Convert user complaints into business opportunities using AI.",
    add_completion=False,
)
console = Console()


def _check_api_key() -> None:
    if not ANTHROPIC_API_KEY:
        print_error("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")
        raise typer.Exit(1)


def _save_json(data: dict, filename: str) -> None:
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / filename
    filepath.write_text(json.dumps(data, indent=2, default=str))
    console.print(f"[dim]Saved to {filepath}[/dim]")


@app.command()
def analyze(
    query: Optional[str] = typer.Argument(None, help="Product category to analyze"),
    use_reddit: bool = typer.Option(False, "--reddit", help="Enable live Reddit scraping"),
    save: bool = typer.Option(False, "--save", help="Save results to JSON"),
) -> None:
    """Analyze complaints for a product category and surface market gaps."""
    _check_api_key()

    if not query:
        query = Prompt.ask("[bold cyan]What product/niche should I analyze?[/bold cyan]")

    print_header(
        "Complaint Mining Analysis",
        f"Analyzing: {query}",
    )

    scraped_data = None
    if use_reddit and REDDIT_ENABLED:
        with Progress(SpinnerColumn(), TextColumn("[cyan]Scraping Reddit..."), console=console) as p:
            p.add_task("scrape")
            scraped_data = scrape_reddit(query)
        if scraped_data:
            print_success(f"Found {len(scraped_data)} posts from Reddit")
        else:
            console.print("[dim]Reddit scraping returned no results, using AI knowledge[/dim]")
    elif use_reddit and not REDDIT_ENABLED:
        console.print("[yellow]Reddit credentials not configured. Using AI knowledge instead.[/yellow]")
    else:
        mock = get_mock_complaints(query)
        if mock and mock[0]["text"] != "This product is incredibly frustrating. Basic features don't work as advertised.":
            scraped_data = mock
            console.print(f"[dim]Using {len(scraped_data)} sample complaint data points[/dim]")

    with Progress(SpinnerColumn(), TextColumn("[cyan]Mining complaints with Claude AI..."), console=console) as p:
        p.add_task("analyze")
        analysis = analyze_complaints(query, scraped_data)

    print_complaint_analysis(analysis)

    if save:
        _save_json(analysis.model_dump(), f"analysis_{query.replace(' ', '_')}.json")

    console.print()
    console.print("[dim]Run [bold]complaint-miner opportunities[/bold] to generate startup opportunities.[/dim]")


@app.command()
def opportunities(
    query: Optional[str] = typer.Argument(None, help="Product category to analyze"),
    use_reddit: bool = typer.Option(False, "--reddit", help="Enable live Reddit scraping"),
    save: bool = typer.Option(False, "--save", help="Save results to JSON"),
) -> None:
    """Generate startup opportunities from complaint analysis."""
    _check_api_key()

    if not query:
        query = Prompt.ask("[bold cyan]What product/niche should I analyze?[/bold cyan]")

    print_header(
        "Startup Opportunity Generator",
        f"Finding opportunities in: {query}",
    )

    scraped_data = None
    if use_reddit and REDDIT_ENABLED:
        with Progress(SpinnerColumn(), TextColumn("[cyan]Scraping Reddit..."), console=console) as p:
            p.add_task("scrape")
            scraped_data = scrape_reddit(query)
    else:
        mock = get_mock_complaints(query)
        if mock and mock[0]["text"] != "This product is incredibly frustrating. Basic features don't work as advertised.":
            scraped_data = mock

    with Progress(SpinnerColumn(), TextColumn("[cyan]Analyzing complaints..."), console=console) as p:
        p.add_task("analyze")
        analysis = analyze_complaints(query, scraped_data)

    with Progress(SpinnerColumn(), TextColumn("[cyan]Generating opportunities..."), console=console) as p:
        p.add_task("opportunities")
        opps = generate_opportunities(analysis)

    print_opportunities(opps)

    if save:
        _save_json(
            {"analysis": analysis.model_dump(), "opportunities": [o.model_dump() for o in opps]},
            f"opportunities_{query.replace(' ', '_')}.json",
        )

    console.print()
    if opps:
        console.print(
            f"[dim]Run [bold]complaint-miner mvp \"{query}\"[/bold] to build an MVP spec "
            f"for the top opportunity: [bold]{opps[0].name}[/bold][/dim]"
        )


@app.command()
def mvp(
    query: Optional[str] = typer.Argument(None, help="Product category to analyze"),
    opportunity_index: int = typer.Option(0, "--index", "-i", help="Which opportunity to build MVP for (0=top)"),
    use_reddit: bool = typer.Option(False, "--reddit", help="Enable live Reddit scraping"),
    save: bool = typer.Option(False, "--save", help="Save results to JSON"),
) -> None:
    """Generate a complete MVP specification for the top startup opportunity."""
    _check_api_key()

    if not query:
        query = Prompt.ask("[bold cyan]What product/niche should I analyze?[/bold cyan]")

    print_header(
        "MVP Builder",
        f"Building MVP spec for: {query}",
    )

    scraped_data = None
    if use_reddit and REDDIT_ENABLED:
        with Progress(SpinnerColumn(), TextColumn("[cyan]Scraping Reddit..."), console=console) as p:
            p.add_task("scrape")
            scraped_data = scrape_reddit(query)
    else:
        mock = get_mock_complaints(query)
        if mock and mock[0]["text"] != "This product is incredibly frustrating. Basic features don't work as advertised.":
            scraped_data = mock

    with Progress(SpinnerColumn(), TextColumn("[cyan]Analyzing complaints..."), console=console) as p:
        p.add_task("analyze")
        analysis = analyze_complaints(query, scraped_data)

    with Progress(SpinnerColumn(), TextColumn("[cyan]Generating opportunities..."), console=console) as p:
        p.add_task("opportunities")
        opps = generate_opportunities(analysis)

    if not opps:
        print_error("No opportunities found.")
        raise typer.Exit(1)

    idx = min(opportunity_index, len(opps) - 1)
    selected = opps[idx]

    console.print(f"\n[cyan]Building MVP for:[/cyan] [bold]{selected.name}[/bold] — {selected.one_liner}\n")

    with Progress(SpinnerColumn(), TextColumn("[cyan]Building MVP specification..."), console=console) as p:
        p.add_task("mvp")
        spec = build_mvp_spec(selected, analysis)

    print_mvp_spec(spec)

    if save:
        _save_json(
            {
                "analysis": analysis.model_dump(),
                "opportunity": selected.model_dump(),
                "mvp_spec": spec.model_dump(),
            },
            f"mvp_{query.replace(' ', '_')}.json",
        )


@app.command()
def full(
    query: Optional[str] = typer.Argument(None, help="Product category to analyze"),
    use_reddit: bool = typer.Option(False, "--reddit", help="Enable live Reddit scraping"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save results to JSON"),
) -> None:
    """Run the complete pipeline: analyze → opportunities → MVP spec."""
    _check_api_key()

    if not query:
        query = Prompt.ask("[bold cyan]What product/niche should I analyze?[/bold cyan]")

    print_header(
        "Complaint-Mining Product Builder",
        f"Full pipeline for: {query}",
    )

    scraped_data = None
    if use_reddit and REDDIT_ENABLED:
        with Progress(SpinnerColumn(), TextColumn("[cyan]Scraping Reddit..."), console=console) as p:
            p.add_task("scrape")
            scraped_data = scrape_reddit(query)
        if scraped_data:
            print_success(f"Found {len(scraped_data)} posts from Reddit")
    else:
        mock = get_mock_complaints(query)
        if mock and mock[0]["text"] != "This product is incredibly frustrating. Basic features don't work as advertised.":
            scraped_data = mock

    with Progress(SpinnerColumn(), TextColumn("[cyan]Step 1/3: Mining complaints..."), console=console) as p:
        p.add_task("analyze")
        analysis = analyze_complaints(query, scraped_data)

    print_complaint_analysis(analysis)

    with Progress(SpinnerColumn(), TextColumn("[cyan]Step 2/3: Generating opportunities..."), console=console) as p:
        p.add_task("opportunities")
        opps = generate_opportunities(analysis)

    print_opportunities(opps)

    if not opps:
        print_error("No opportunities generated.")
        raise typer.Exit(1)

    console.print(f"\n[cyan]Building MVP for top opportunity:[/cyan] [bold]{opps[0].name}[/bold]\n")

    with Progress(SpinnerColumn(), TextColumn("[cyan]Step 3/3: Building MVP spec..."), console=console) as p:
        p.add_task("mvp")
        spec = build_mvp_spec(opps[0], analysis)

    print_mvp_spec(spec)

    if save:
        slug = query.replace(" ", "_").lower()
        _save_json(
            {
                "query": query,
                "analysis": analysis.model_dump(),
                "opportunities": [o.model_dump() for o in opps],
                "top_mvp_spec": spec.model_dump(),
            },
            f"full_report_{slug}.json",
        )
        print_success(f"Full report saved to {OUTPUT_DIR}/full_report_{slug}.json")


if __name__ == "__main__":
    app()
