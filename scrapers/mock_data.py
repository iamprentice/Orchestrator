from typing import List, Dict


_MOCK_COMPLAINTS: Dict[str, List[Dict]] = {
    "project management software": [
        {
            "source": "Reddit r/projectmanagement",
            "text": "Jira is so slow it makes me want to throw my laptop. Why does it take 3 seconds to load every ticket?",
            "upvotes": 2341,
        },
        {
            "source": "App Store",
            "text": "Another useless update that broke the mobile app. Can't even create tasks offline. 1 star.",
            "upvotes": 891,
        },
        {
            "source": "Reddit r/devops",
            "text": "The notification system is completely broken. I get 50 emails a day and still miss critical updates.",
            "upvotes": 1205,
        },
        {
            "source": "G2 Reviews",
            "text": "Pricing jumped 40% and they removed features from our plan without warning. Switching to something else.",
            "upvotes": 445,
        },
    ],
    "crm software": [
        {
            "source": "Reddit r/sales",
            "text": "Salesforce is a data entry nightmare. I spend more time logging calls than actually selling.",
            "upvotes": 3102,
        },
        {
            "source": "App Store",
            "text": "The mobile app is unusable. Can't pull up client history without WiFi. Lost a deal because of this.",
            "upvotes": 1567,
        },
        {
            "source": "Reddit r/entrepreneur",
            "text": "Implementation took 6 months and cost $50k. Still doesn't work the way we need it to.",
            "upvotes": 892,
        },
    ],
    "email marketing": [
        {
            "source": "Reddit r/marketing",
            "text": "Mailchimp's automations break constantly and support takes 3 days to respond. Unacceptable.",
            "upvotes": 1834,
        },
        {
            "source": "G2 Reviews",
            "text": "Deliverability tanked after their latest update. 40% open rate dropped to 12%. No explanation.",
            "upvotes": 2109,
        },
        {
            "source": "Reddit r/ecommerce",
            "text": "The segmentation tools are a joke. I need to export to Excel to do anything useful.",
            "upvotes": 987,
        },
    ],
}

_DEFAULT_COMPLAINTS = [
    {
        "source": "Reddit",
        "text": "This product is incredibly frustrating. Basic features don't work as advertised.",
        "upvotes": 500,
    },
    {
        "source": "App Store",
        "text": "Crashes constantly. The support team is unresponsive. Not worth the price.",
        "upvotes": 320,
    },
    {
        "source": "Google Reviews",
        "text": "Steep learning curve with no good documentation. Feels abandoned by the developers.",
        "upvotes": 210,
    },
]


def get_mock_complaints(product_category: str) -> List[Dict]:
    key = product_category.lower().strip()
    for k, complaints in _MOCK_COMPLAINTS.items():
        if k in key or any(word in key for word in k.split()):
            return complaints
    return _DEFAULT_COMPLAINTS
