# Databricks notebook source

# COMMAND ----------

import subprocess

# Playwrightのシステム依存関係をインストール
print("Installing Playwright system dependencies...")
result = subprocess.run(
    ["playwright", "install-deps", "chromium"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print(f"install-deps stderr: {result.stderr}")

# Playwrightブラウザをインストール
print("Installing Playwright browsers...")
result = subprocess.run(
    ["playwright", "install", "chromium"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print(f"install stderr: {result.stderr}")
print("Playwright installation completed.")

# COMMAND ----------

import nest_asyncio

nest_asyncio.apply()

# COMMAND ----------

from playwright.async_api import async_playwright

# COMMAND ----------

dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

# COMMAND ----------


async def scrape_example() -> None:
    """Playwrightを使用してexample.comから情報を収集する"""
    print("=== Playwright Scraping ===")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://example.com/")
        title = await page.title()
        print(f"Page title: {title}")

        # ページの本文を取得
        body_text = await page.locator("p").first.text_content()
        print(f"Body text: {body_text}")

        await browser.close()

    print("Playwright scraping completed.")


# COMMAND ----------


def fetch_db_records() -> None:
    """SNPF DBのdata_companiesテーブルからレコードを取得する"""
    print("=== DB Fetch ===")
    print(f"Environment: {env}")

    catalog = f"{env}_snpf"
    query = f"""
    SELECT corporate_number, company_name
    FROM {catalog}.public.data_companies
    LIMIT 5
    """

    print(f"Executing query on catalog: {catalog}")
    df = spark.sql(query)  # noqa: F821
    df.show()

    print("DB fetch completed.")


# COMMAND ----------

# Playwrightでスクレイピング
await scrape_example()

# COMMAND ----------

# DBからレコード取得
fetch_db_records()

# COMMAND ----------

print("All tasks completed successfully.")
