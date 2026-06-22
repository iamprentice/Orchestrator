import json
from typing import List
import anthropic
from rich.console import Console

from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, MAX_OPPORTUNITIES
from models.schemas import ComplaintAnalysis, StartupOpportunity

console = Console()

SYSTEM_PROMPT = """You are a serial entrepreneur and venture capitalist with a track record of
identifying billion-dollar opportunities hidden in user pain points. You have founded and exited
multiple companies and advised hundreds of startups.

Your superpower is translating raw complaints into viable businesses. You think about:
- What minimum product solves 80% of the pain?
- Who pays for it and why now?
- What unfair advantage can a new entrant have?
- What does the competitive moat look like?

Be ruthlessly honest about difficulty and market size. Don't sugarcoat challenges."""

OPPORTUNITY_PROMPT = """Based on this complaint mining analysis, identify the top {max_opportunities}
startup opportunities:

ANALYSIS:
Product Category: {product_category}
Summary: {summary}

TOP COMPLAINTS:
{complaints_text}

MARKET GAPS:
{gaps_text}

MARKET OPPORTUNITY:
TAM: {tam}
SAM: {sam}
Growth: {growth_rate}

Generate {max_opportunities} startup opportunities ordered by confidence score (highest first).
For each opportunity, focus on:
- Solving the MOST FREQUENT + MOST INTENSE complaint clusters
- Opportunities where existing solutions genuinely fail
- Businesses that can be bootstrapped or raise a small seed round

Return a JSON array matching this schema:
[
  {{
    "name": "Product/startup name",
    "one_liner": "One sentence that makes investors lean forward",
    "problem": "Specific problem being solved (cite the complaints)",
    "solution": "Specific solution approach",
    "target_users": ["primary user type", "secondary user type"],
    "key_differentiators": ["differentiator1", "differentiator2", "differentiator3"],
    "estimated_revenue_potential": "$X ARR at scale",
    "difficulty_to_build": "Easy|Medium|Hard|Very Hard",
    "time_to_market": "X weeks/months to MVP",
    "confidence_score": <integer 1-100>
  }}
]

Return only valid JSON array, no markdown."""


def generate_opportunities(analysis: ComplaintAnalysis) -> List[StartupOpportunity]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    complaints_text = "\n".join(
        f"- [{c.emotional_intensity.value.upper()}] {c.title}: {c.description} (~{c.frequency:,}/month)"
        for c in analysis.top_complaints
    )

    gaps_text = "\n".join(
        f"- {g.description}: {g.why_existing_solutions_fail}"
        for g in analysis.market_gaps
    )

    prompt = OPPORTUNITY_PROMPT.format(
        max_opportunities=MAX_OPPORTUNITIES,
        product_category=analysis.product_category,
        summary=analysis.summary,
        complaints_text=complaints_text,
        gaps_text=gaps_text,
        tam=analysis.market_opportunity.total_addressable_market,
        sam=analysis.market_opportunity.serviceable_addressable_market,
        growth_rate=analysis.market_opportunity.growth_rate,
    )

    console.print("[dim]Generating startup opportunities with Claude...[/dim]")

    with client.messages.stream(
        model=DEFAULT_MODEL,
        max_tokens=6000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        response = stream.get_final_message()

    raw = next(
        block.text for block in response.content
        if hasattr(block, "text")
    )

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0]

    data = json.loads(raw.strip())
    return [StartupOpportunity(**item) for item in data]
