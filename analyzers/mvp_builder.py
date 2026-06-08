import json
import anthropic
from rich.console import Console

from config import ANTHROPIC_API_KEY, DEFAULT_MODEL
from models.schemas import StartupOpportunity, ComplaintAnalysis, MVPSpec

console = Console()

SYSTEM_PROMPT = """You are a CTO and product strategist who has shipped dozens of successful SaaS products.
You specialize in ruthlessly scoping MVPs — cutting everything that isn't essential to prove
the core value proposition and get the first 10 paying customers.

Your framework:
- What is the ONE feature that makes someone pay immediately?
- What is the cheapest tech stack that can be shipped in weeks, not months?
- What is the exact GTM motion for the first 100 users?
- What does "this is working" look like in metrics?

You think in terms of: Ship → Learn → Iterate. Not: Plan → Build → Launch."""

MVP_PROMPT = """Build a complete MVP specification for this startup opportunity:

OPPORTUNITY:
Name: {name}
One-liner: {one_liner}
Problem: {problem}
Solution: {solution}
Target Users: {target_users}
Difficulty: {difficulty}
Time to Market: {time_to_market}
Revenue Potential: {revenue_potential}

MARKET CONTEXT:
Product Category: {product_category}
Top Complaints Being Solved: {complaints}
Key Differentiators: {differentiators}

Create a complete, actionable MVP specification. Return a JSON object:
{{
  "opportunity_name": "{name}",
  "problem_statement": "Clear 2-sentence problem statement for pitch decks",
  "core_features": [
    "Feature 1 — why it's essential (not nice-to-have)",
    "Feature 2 — why it's essential",
    "Feature 3 — why it's essential"
  ],
  "tech_stack_recommendation": "Specific stack with rationale (e.g., 'Next.js + Supabase + OpenAI — fastest path to demo-able product')",
  "timeline": "Week-by-week breakdown for the MVP",
  "pricing_model": [
    {{
      "name": "Tier name",
      "price": "$X/month or free",
      "features": ["feature1", "feature2", "feature3"],
      "target_user": "Who this tier is designed for"
    }}
  ],
  "go_to_market": [
    "Step 1: Specific channel and tactic",
    "Step 2: Specific channel and tactic",
    "Step 3: Specific channel and tactic",
    "Step 4: Specific channel and tactic"
  ],
  "key_metrics": [
    "Metric 1 with target (e.g., 'MRR: $10k in 90 days')",
    "Metric 2 with target",
    "Metric 3 with target"
  ],
  "competitor_analysis": [
    "Competitor 1: weakness and how you win",
    "Competitor 2: weakness and how you win",
    "Competitor 3: weakness and how you win"
  ],
  "marketing_angles": [
    "Angle 1 — specific messaging hook",
    "Angle 2 — specific messaging hook",
    "Angle 3 — specific messaging hook"
  ],
  "success_criteria": [
    "Criterion 1 — how you know it's working",
    "Criterion 2 — how you know it's working"
  ],
  "week_one_actions": [
    "Action 1 — concrete task you do on day 1",
    "Action 2 — concrete task you do on day 2",
    "Action 3 — concrete task you do on day 3",
    "Action 4 — concrete task you do on day 4",
    "Action 5 — concrete task you do on day 5"
  ]
}}

Be specific. Name real tools, real communities, real pricing numbers. No vague advice.
Return only valid JSON, no markdown."""


def build_mvp_spec(
    opportunity: StartupOpportunity,
    analysis: ComplaintAnalysis,
) -> MVPSpec:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    complaints_solved = [
        c.title for c in analysis.top_complaints
        if any(word in opportunity.problem.lower() for word in c.title.lower().split()[:3])
    ] or [c.title for c in analysis.top_complaints[:3]]

    prompt = MVP_PROMPT.format(
        name=opportunity.name,
        one_liner=opportunity.one_liner,
        problem=opportunity.problem,
        solution=opportunity.solution,
        target_users=", ".join(opportunity.target_users),
        difficulty=opportunity.difficulty_to_build,
        time_to_market=opportunity.time_to_market,
        revenue_potential=opportunity.estimated_revenue_potential,
        product_category=analysis.product_category,
        complaints=", ".join(complaints_solved),
        differentiators=", ".join(opportunity.key_differentiators),
    )

    console.print("[dim]Building MVP specification with Claude...[/dim]")

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
    return MVPSpec(**data)
