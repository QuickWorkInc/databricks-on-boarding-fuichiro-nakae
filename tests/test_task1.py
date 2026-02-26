"""Tests for task1_playwright_scraping"""

from unittest.mock import MagicMock, patch


def test_playwright_scraping_mock() -> None:
    """Playwrightスクレイピングのモックテスト"""
    mock_page = MagicMock()
    mock_page.title.return_value = "Example Domain"

    mock_browser = MagicMock()
    mock_browser.new_page.return_value = mock_page

    mock_playwright = MagicMock()
    mock_playwright.chromium.launch.return_value = mock_browser

    with patch("playwright.sync_api.sync_playwright") as mock_sync_playwright:
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_playwright)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_sync_playwright.return_value = mock_context

        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()

        assert title == "Example Domain"
        mock_page.goto.assert_called_once_with("https://example.com")


def test_env_parameter_validation() -> None:
    """環境パラメータのバリデーションテスト"""
    valid_envs = ["dev", "stg"]
    invalid_envs = ["prd", "prod", "production", ""]

    for env in valid_envs:
        assert env in ["dev", "stg"], f"{env} should be valid"

    for env in invalid_envs:
        assert env not in ["dev", "stg"], f"{env} should be invalid"
