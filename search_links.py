"""Generate human-reviewed search links for business and contact discovery."""

from __future__ import annotations

from urllib.parse import quote_plus, urlsplit


PLATFORM_SITES = (
    ("Instagram", "site:instagram.com"),
    ("Facebook", "site:facebook.com"),
    ("LinkedIn companies", "site:linkedin.com/company"),
    ("LinkedIn decision-makers", "site:linkedin.com/in"),
    ("TikTok", "site:tiktok.com"),
    ("YouTube", "site:youtube.com"),
    ("X", "site:x.com"),
)


def build_search_links(
    *,
    industry_english: str,
    industry_arabic: str,
    location_english: str,
    location_arabic: str,
) -> list[dict[str, str]]:
    industries = [
        (language, value.strip())
        for language, value in (("English", industry_english), ("Arabic", industry_arabic))
        if value.strip()
    ]
    locations = [
        (language, value.strip())
        for language, value in (("English", location_english), ("Arabic", location_arabic))
        if value.strip()
    ]
    if not industries:
        raise ValueError("Enter an industry or business keyword in English or Arabic.")

    links: list[dict[str, str]] = []
    for platform, site in PLATFORM_SITES:
        for language, industry in industries:
            matching_locations = [value for lang, value in locations if lang == language]
            if not matching_locations:
                matching_locations = [value for _, value in locations] or ["Egypt"]
            for location in matching_locations:
                location_terms = f'"{location}"' if location != "Egypt" else '"Egypt"'
                if platform == "LinkedIn decision-makers":
                    title_terms = (
                        '"مدير تسويق" OR "مدير التسويق" OR "الرئيس التنفيذي" OR مؤسس'
                        if language == "Arabic"
                        else '"marketing manager" OR "marketing director" OR CEO OR founder'
                    )
                    query = f'{site} {title_terms} "{industry}" {location_terms} Egypt'
                else:
                    query = f'{site} "{industry}" {location_terms} Egypt'
                links.append(
                    {
                        "platform": platform,
                        "language": language,
                        "query": query,
                        "google_url": f"https://www.google.com/search?q={quote_plus(query)}",
                        "bing_url": f"https://www.bing.com/search?q={quote_plus(query)}",
                    }
                )
    return links


def build_manual_decision_maker_search_links(
    *,
    business_name: str,
    industry: str = "",
    location: str = "Egypt",
    include_company_page: bool = False,
) -> list[dict[str, str]]:
    business = business_name.strip()
    if not business:
        raise ValueError("Enter a business name to build manual search links.")

    industry_term = f' "{industry.strip()}"' if industry.strip() else ""
    place = location.strip() or "Egypt"
    queries = (
        (
            "LinkedIn decision-makers",
            "English",
            f'site:linkedin.com/in ("CEO" OR founder OR "marketing director" OR '
            f'"business development manager") "{business}"{industry_term} "{place}"',
        ),
        (
            "LinkedIn decision-makers",
            "Arabic",
            f'site:linkedin.com/in ("الرئيس التنفيذي" OR مؤسس OR "مدير التسويق" OR '
            f'"مدير تطوير الأعمال") "{business}"{industry_term} "{place}"',
        ),
        (
            "Facebook business-page candidates",
            "English",
            f'site:facebook.com "{business}"{industry_term} "{place}" Egypt',
        ),
        (
            "Instagram business-profile candidates",
            "English",
            f'site:instagram.com "{business}"{industry_term} "{place}" Egypt',
        ),
    )
    if include_company_page:
        queries = (
            (
                "LinkedIn company-page candidates",
                "English",
                f'site:linkedin.com/company "{business}"{industry_term} "{place}"',
            ),
            *queries,
        )
    return [
        {
            "topic": topic,
            "language": language,
            "query": query,
            "google_url": f"https://www.google.com/search?q={quote_plus(query)}",
            "bing_url": f"https://www.bing.com/search?q={quote_plus(query)}",
        }
        for topic, language, query in queries
    ]


def build_manual_phone_search_links(
    *,
    business_name: str,
    person_name: str,
    alternate_person_name: str = "",
    job_title: str = "",
    location: str = "Egypt",
) -> list[dict[str, str]]:
    business = business_name.strip().replace('"', "")
    person = person_name.strip().replace('"', "")
    alternate_person = alternate_person_name.strip().replace('"', "") or person
    if not business or not person:
        raise ValueError("Business and decision-maker names are required for phone searches.")
    title_term = f' "{job_title.strip()}"' if job_title.strip() else ""
    place = location.strip() or "Egypt"
    queries = (
        (
            "English",
            f'"{person}" "{business}"{title_term} (phone OR mobile OR contact) "{place}" Egypt',
        ),
        (
            "Arabic",
            f'"{alternate_person}" "{business}"{title_term} '
            f'("رقم هاتف" OR هاتف OR تواصل OR موبايل) "{place}" Egypt',
        ),
    )
    return [
        {
            "language": language,
            "query": query,
            "google_url": f"https://www.google.com/search?q={quote_plus(query)}",
            "bing_url": f"https://www.bing.com/search?q={quote_plus(query)}",
        }
        for language, query in queries
    ]


def build_manual_email_search_links(
    *,
    business_name: str,
    person_name: str,
    alternate_person_name: str = "",
    job_title: str = "",
    location: str = "Egypt",
) -> list[dict[str, str]]:
    business = business_name.strip().replace('"', "")
    person = person_name.strip().replace('"', "")
    alternate_person = alternate_person_name.strip().replace('"', "") or person
    if not business or not person:
        raise ValueError("Business and decision-maker names are required for email searches.")
    title_term = f' "{job_title.strip()}"' if job_title.strip() else ""
    place = location.strip() or "Egypt"
    queries = (
        (
            "English",
            f'"{person}" "{business}"{title_term} '
            f'("work email" OR "business email" OR contact) "{place}" Egypt',
        ),
        (
            "Arabic",
            f'"{alternate_person}" "{business}"{title_term} '
            f'("بريد العمل" OR "بريد إلكتروني" OR تواصل) "{place}" Egypt',
        ),
    )
    return [
        {
            "language": language,
            "query": query,
            "google_url": f"https://www.google.com/search?q={quote_plus(query)}",
            "bing_url": f"https://www.bing.com/search?q={quote_plus(query)}",
        }
        for language, query in queries
    ]


def is_business_social_profile_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").casefold()
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    segments = [part.casefold() for part in parsed.path.split("/") if part]
    if host == "instagram.com" or host.endswith(".instagram.com"):
        reserved = {
            "about",
            "accounts",
            "developer",
            "direct",
            "explore",
            "legal",
            "p",
            "reel",
            "reels",
            "stories",
        }
        return len(segments) == 1 and segments[0] not in reserved
    if host == "facebook.com" or host.endswith(".facebook.com"):
        reserved = {
            "events",
            "groups",
            "marketplace",
            "photo",
            "photos",
            "posts",
            "reel",
            "share",
            "stories",
            "watch",
        }
        if len(segments) == 1:
            return segments[0] not in reserved and segments[0] != "profile.php"
        return (
            len(segments) >= 3
            and segments[0] == "pages"
            and segments[-1].isdigit()
        )
    return False
