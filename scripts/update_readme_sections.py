#!/usr/bin/env python3
"""Update README Techs and Contact sections from GitHub sources.

Techs source:
- Public repositories from the profile account (language stats).

Contact source:
- portfolio repository file: src/json/areas/contact.json
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

USERNAME = "JLBBARCO"
PORTFOLIO_CONTACT_JSON = (
    "https://raw.githubusercontent.com/JLBBARCO/portfolio/main/src/json/areas/contact.json"
)
README_PATH = Path("README.md")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "JLBBARCO-readme-updater",
}

LANGUAGE_BADGE_META: Dict[str, Tuple[str, str]] = {
    "Python": ("python", "3776AB"),
    "JavaScript": ("javascript", "F7DF1E"),
    "TypeScript": ("typescript", "3178C6"),
    "HTML": ("html5", "E34F26"),
    "CSS": ("css3", "1572B6"),
    "Java": ("openjdk", "ED8B00"),
    "C#": ("csharp", "512BD4"),
    "C++": ("cplusplus", "00599C"),
    "C": ("c", "A8B9CC"),
    "Go": ("go", "00ADD8"),
    "PHP": ("php", "777BB4"),
    "Ruby": ("ruby", "CC342D"),
    "Shell": ("gnubash", "4EAA25"),
    "Dockerfile": ("docker", "2496ED"),
    "Markdown": ("markdown", "000000"),
    "Kotlin": ("kotlin", "7F52FF"),
    "Swift": ("swift", "FA7343"),
    "Rust": ("rust", "000000"),
    "Vue": ("vuedotjs", "4FC08D"),
    "Dart": ("dart", "0175C2"),
    "SCSS": ("sass", "CC6699"),
}

CONTACT_ICON_TO_SHIELD = {
    "email": ("Gmail", "gmail", "EA4335"),
    "github": ("GitHub", "github", "181717"),
    "linkedin": ("LinkedIn", "linkedin", "0A66C2"),
    "instagram": ("Instagram", "instagram", "E4405F"),
    "youtube": ("YouTube", "youtube", "FF0000"),
    "discord": ("Discord", "discord", "5865F2"),
    "whatsapp": ("WhatsApp", "whatsapp", "25D366"),
    "fa-envelope": ("Gmail", "gmail", "EA4335"),
    "fa-github": ("GitHub", "github", "181717"),
    "fa-linkedin": ("LinkedIn", "linkedin", "0A66C2"),
    "fa-instagram": ("Instagram", "instagram", "E4405F"),
    "fa-youtube": ("YouTube", "youtube", "FF0000"),
    "fa-discord": ("Discord", "discord", "5865F2"),
    "fa-whatsapp": ("WhatsApp", "whatsapp", "25D366"),
}


def http_get_json(url: str) -> object:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_repositories(username: str) -> List[dict]:
    repos: List[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/users/{username}/repos"
            f"?per_page=100&page={page}&type=owner&sort=updated"
        )
        chunk = http_get_json(url)
        if not isinstance(chunk, list) or not chunk:
            break
        repos.extend(chunk)
        page += 1
    return repos


def fetch_repo_languages(languages_url: str) -> Dict[str, int]:
    data = http_get_json(languages_url)
    if not isinstance(data, dict):
        return {}
    result: Dict[str, int] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, int):
            result[key] = value
    return result


def aggregate_languages(repos: Iterable[dict]) -> Dict[str, int]:
    totals: Dict[str, int] = {}
    for repo in repos:
        if not isinstance(repo, dict):
            continue
        if repo.get("fork"):
            continue
        languages_url = repo.get("languages_url")
        repo_langs: Dict[str, int] = {}
        if isinstance(languages_url, str) and languages_url:
            try:
                repo_langs = fetch_repo_languages(languages_url)
            except urllib.error.URLError:
                repo_langs = {}
        if not repo_langs:
            main_lang = repo.get("language")
            if isinstance(main_lang, str) and main_lang:
                repo_langs = {main_lang: 1}

        for lang, weight in repo_langs.items():
            totals[lang] = totals.get(lang, 0) + int(weight)
    return totals


def shield_badge(label: str, logo: str, color: str) -> str:
    encoded_label = urllib.parse.quote(label)
    return (
        f"https://img.shields.io/badge/{encoded_label}-{color}"
        f"?logo={logo}&logoColor=white&style=for-the-badge"
    )


def generate_techs_markdown(language_totals: Dict[str, int], limit: int = 12) -> str:
    if not language_totals:
        return "_No language data available right now._"

    top_langs = sorted(language_totals.items(), key=lambda item: item[1], reverse=True)[:limit]
    ordered_langs = sorted((lang for lang, _ in top_langs), key=str.casefold)

    badges: List[str] = []
    for lang in ordered_langs:
        logo, color = LANGUAGE_BADGE_META.get(lang, (lang.lower().replace("#", "sharp"), "4B5563"))
        logo_color = "black" if lang == "JavaScript" else "white"
        encoded_label = urllib.parse.quote(lang)
        badge_url = (
            f"https://img.shields.io/badge/{encoded_label}-{color}"
            f"?logo={logo}&logoColor={logo_color}&style=for-the-badge"
        )
        badges.append(f"![{lang}]({badge_url})")
    return "\n".join(badges)


def read_contact_cards() -> List[dict]:
    data = http_get_json(PORTFOLIO_CONTACT_JSON)
    if not isinstance(data, dict):
        return []
    cards = data.get("cards")
    if not isinstance(cards, list):
        return []
    valid: List[dict] = []
    for card in cards:
        if not isinstance(card, dict):
            continue
        url = card.get("url")
        if isinstance(url, str) and url.strip():
            valid.append(card)
    return valid


def icon_meta_from_card(card: dict) -> Tuple[str, str, str]:
    """Extract icon metadata from a contact card.
    
    Tries multiple sources for icon information:
    1. Direct 'iconName' field (preferred)
    2. Legacy 'icon' field
    3. Fallback to name-based detection
    """
    # Try iconName first (from portfolio JSON)
    icon_name = card.get("iconName")
    if isinstance(icon_name, str) and icon_name in CONTACT_ICON_TO_SHIELD:
        return CONTACT_ICON_TO_SHIELD[icon_name]
    
    # Try legacy icon field
    icon = card.get("icon")
    if isinstance(icon, str) and icon in CONTACT_ICON_TO_SHIELD:
        return CONTACT_ICON_TO_SHIELD[icon]

    # Fallback to name-based detection
    name = str(card.get("name", "Contact"))
    lowered = name.lower()
    if "linkedin" in lowered:
        return ("LinkedIn", "linkedin", "0A66C2")
    if "instagram" in lowered:
        return ("Instagram", "instagram", "E4405F")
    if "github" in lowered:
        return ("GitHub", "github", "181717")
    if "mail" in lowered or "@" in lowered:
        return ("Gmail", "gmail", "EA4335")
    return ("Contact", "link", "4B5563")


def generate_contact_markdown(cards: List[dict]) -> str:
    if not cards:
        return "_No contact data available right now._"

    lines: List[str] = []
    for card in cards:
        url = str(card.get("url", "")).strip()
        if not url:
            continue
        label, logo, color = icon_meta_from_card(card)
        badge_url = shield_badge(label, logo, color)
        lines.append(f"[![{label}]({badge_url})]({url})")
    return "\n".join(lines) if lines else "_No contact data available right now._"


def replace_managed_block(readme: str, block_name: str, content: str) -> str:
    start = f"<!-- {block_name}:START -->"
    end = f"<!-- {block_name}:END -->"
    pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)
    replacement = f"{start}\n{content}\n{end}"
    if pattern.search(readme):
        return pattern.sub(replacement, readme, count=1)
    raise RuntimeError(f"Managed block not found: {block_name}")


def main() -> int:
    if not README_PATH.exists():
        print("README.md not found", file=sys.stderr)
        return 1

    readme = README_PATH.read_text(encoding="utf-8")

    repos = fetch_repositories(USERNAME)
    lang_totals = aggregate_languages(repos)
    techs_md = generate_techs_markdown(lang_totals)

    contact_cards = read_contact_cards()
    contact_md = generate_contact_markdown(contact_cards)

    updated = replace_managed_block(readme, "TECHS", techs_md)
    updated = replace_managed_block(updated, "CONTACT", contact_md)

    README_PATH.write_text(updated, encoding="utf-8")
    print("README managed sections updated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
