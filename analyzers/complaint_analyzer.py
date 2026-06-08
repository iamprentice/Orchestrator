import json
from typing import List, Dict, Optional
import anthropic
from rich.console import Console

from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, MAX_COMPLAINTS
from models.schemas import ComplaintAnalysis

console = Console()

SYSTEM_PROMPT = """You are an elite market researcher and business analyst specializing in
complaint mining and market opportunity identification. You have deep knowledge of SaaS markets,
consumer behavior, and startup opportunities.

Your role is to analyze user complaints about products and extract actionable market intelligence.
You synthesize data from Reddit, App Store reviews, Twitter/X, Discord, support forums, and
industry communities to identify patterns of frustration and market gaps.

Be specific, data-driven, and ruthlessly honest about market realities. Always quantify when possible."""

ANALYSIS_PROMPT = """Perform a comprehensive complaint mining analysis for: **{product_category}**

{complaint_context}

Analyze complaints across these dimensions:
1. Top frustrations users express (look for repeated themes, not one-offs)
2. Emotional intensity and frequency of each complaint
3. User segments most affected
4. Existing solutions and their critical limitations
5. Market gaps that remain genuinely unsolved
6. Total market opportunity size

Return a JSON object matching this exact schema:
{{
  "product_category": "{product_category}",
  "summary": "2-3 sentence executive summary of findings",
  "top_complaints": [
    {{
      "title": "Short complaint title",
      "description": "Detailed description of the pain point",
      "frequency": <estimated monthly mentions across all platforms as integer>,
      "emotional_intensity": "<low|medium|high|extreme>",
      "example_quotes": ["quote1", "quote2", "quote3"],
      "affected_user_segments": ["segment1", "segment2"]
    }}
  ],
  "existing_solutions": [
    {{
      "name": "Solution name",
      "description": "What it does",
      "limitations": ["limitation1", "limitation2", "limitation3"],
      "market_share": "approximate market share or revenue"
    }}
  ],
  "market_gaps": [
    {{
      "description": "The unsolved gap",
      "unsolved_complaints": ["complaint1", "complaint2"],
      "why_existing_solutions_fail": "Root cause analysis",
      "estimated_market_size": "$X billion"
    }}
  ],
  "market_opportunity": {{
    "total_addressable_market": "$X billion",
    "serviceable_addressable_market": "$X million",
    "growth_rate": "X% annually",
    "urgency": "Why this needs to be solved now"
  }},
  "data_sources_analyzed": ["Reddit", "App Store Reviews", "G2", "Twitter/X", "Discord", "Support Forums"]
}}

Include {max_complaints} complaints. Be specific with numbers and market sizes.
Return only valid JSON, no markdown."""


def analyze_complaints(
    product_category: str,
    scraped_data: Optional[List[Dict]] = None,
) -> ComplaintAnalysis:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    if scraped_data:
        top_posts = sorted(scraped_data, key=lambda x: x.get("upvotes", 0), reverse=True)[:20]
        complaint_context = "Additional complaint data from live sources:\n" + "\n".join(
            f'- [{c["source"]}] ({c.get("upvotes", 0)} upvotes): "{c["text"][:200]}"'
            for c in top_posts
        )
    else:
        complaint_context = (
            "Use your comprehensive knowledge of user complaints, forum discussions, "
            "reviews, and community feedback about this product category to identify "
            "the most common and painful frustrations."
        )

    prompt = ANALYSIS_PROMPT.format(
        product_category=product_category,
        complaint_context=complaint_context,
        max_complaints=MAX_COMPLAINTS,
    )

    console.print("[dim]Analyzing complaints with Claude...[/dim]")

    with client.messages.stream(
        model=DEFAULT_MODEL,
        max_tokens=8000,
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
    return ComplaintAnalysis(**data)
