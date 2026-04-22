#!/usr/bin/env python3
"""Validate the auto-update system is working correctly."""

import urllib.request
import json
import sys


def test_github_api():
    """Test if GitHub API is accessible."""
    print("=== TEST 1: GitHub API Access ===")
    try:
        req = urllib.request.Request(
            "https://api.github.com/users/JLBBARCO",
            headers={"User-Agent": "test"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("✓ GitHub API accessible")
            print(f"  Public repos: {data.get('public_repos')}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_portfolio_json():
    """Test if Portfolio JSON is accessible."""
    print("\n=== TEST 2: Portfolio JSON Access ===")
    try:
        url = "https://raw.githubusercontent.com/JLBBARCO/portfolio/main/src/json/areas/contact.json"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            cards = data.get("cards", [])
            print("✓ Portfolio JSON accessible")
            print(f"  Contacts: {len(cards)}")
            for card in cards:
                print(f"    - {card.get('iconName')}: {card.get('name')}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_readme():
    """Test README sections."""
    print("\n=== TEST 3: README Sections ===")
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            techs_count = content.count("![") - 2  # -2 for Snake and Stats
            contact_count = content.count("[![")
            print("✓ README.md read successfully")
            print(f"  Tech badges: {techs_count}")
            print(f"  Contact badges: {contact_count}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    results = [
        test_github_api(),
        test_portfolio_json(),
        test_readme(),
    ]
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
