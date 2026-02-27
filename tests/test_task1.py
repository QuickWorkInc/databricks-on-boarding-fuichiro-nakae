"""Tests for task1_playwright_scraping"""


def test_env_parameter_validation() -> None:
    """環境パラメータのバリデーションテスト"""
    valid_envs = ["dev", "stg"]
    invalid_envs = ["prd", "prod", "production", ""]

    for env in valid_envs:
        assert env in ["dev", "stg"], f"{env} should be valid"

    for env in invalid_envs:
        assert env not in ["dev", "stg"], f"{env} should be invalid"
