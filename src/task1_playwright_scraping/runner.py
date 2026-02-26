# Databricks notebook source

# COMMAND ----------

from playwright.sync_api import sync_playwright

# COMMAND ----------

dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

# COMMAND ----------


def main() -> None:
    """Playwrightを使用してWebスクレイピングを実行する"""
    print(f"Environment: {env}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        title = page.title()
        print(f"Page title: {title}")
        browser.close()

    print("Playwright scraping completed successfully.")


# COMMAND ----------

main()
