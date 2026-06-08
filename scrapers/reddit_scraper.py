from typing import List, Dict, Optional


def scrape_reddit(product_category: str, limit: int = 50) -> Optional[List[Dict]]:
    """
    Scrapes Reddit for complaints about a product category using PRAW.
    Returns None if Reddit credentials are not configured.
    """
    try:
        import praw
        from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_ENABLED

        if not REDDIT_ENABLED:
            return None

        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )

        subreddits = [
            "productivity", "software", "SaaS", "entrepreneur",
            "smallbusiness", "startups", "webdev", "programming",
        ]

        search_terms = [
            f"{product_category} problem",
            f"{product_category} frustrating",
            f"{product_category} broken",
            f"{product_category} alternative",
            f"hate {product_category}",
            f"{product_category} sucks",
        ]

        complaints = []
        seen_ids = set()

        for subreddit_name in subreddits[:3]:
            subreddit = reddit.subreddit(subreddit_name)
            for term in search_terms[:2]:
                try:
                    results = subreddit.search(term, limit=limit // 6, sort="top", time_filter="year")
                    for post in results:
                        if post.id not in seen_ids and post.score > 10:
                            seen_ids.add(post.id)
                            complaints.append({
                                "source": f"Reddit r/{subreddit_name}",
                                "text": f"{post.title}. {post.selftext[:300]}".strip(),
                                "upvotes": post.score,
                                "url": f"https://reddit.com{post.permalink}",
                            })
                except Exception:
                    continue

        return complaints if complaints else None

    except ImportError:
        return None
    except Exception:
        return None
