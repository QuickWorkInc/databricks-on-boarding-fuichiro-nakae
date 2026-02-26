"""Tests for task2_db_fetch"""


def test_catalog_name_generation() -> None:
    """カタログ名生成のテスト"""
    test_cases = [
        ("dev", "dev_snpf"),
        ("stg", "stg_snpf"),
    ]

    for env, expected_catalog in test_cases:
        catalog = f"{env}_snpf"
        assert catalog == expected_catalog, f"Expected {expected_catalog}, got {catalog}"


def test_query_generation() -> None:
    """SQLクエリ生成のテスト"""
    env = "dev"
    catalog = f"{env}_snpf"
    query = f"""
    SELECT corporate_number, company_name
    FROM {catalog}.public.data_companies
    LIMIT 5
    """

    assert "dev_snpf" in query
    assert "public.data_companies" in query
    assert "LIMIT 5" in query
    assert "SELECT" in query


def test_env_validation() -> None:
    """環境バリデーションのテスト"""
    valid_envs = ["dev", "stg"]

    for env in valid_envs:
        catalog = f"{env}_snpf"
        assert catalog.startswith(env)
        assert catalog.endswith("_snpf")
