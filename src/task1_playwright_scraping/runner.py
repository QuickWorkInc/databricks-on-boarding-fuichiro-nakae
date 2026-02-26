# Databricks notebook source

# COMMAND ----------

import subprocess

# Playwrightブラウザをインストール
print("Installing Playwright browsers...")
result = subprocess.run(["playwright", "install", "chromium"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
print("Playwright browsers installed.")

# COMMAND ----------

import nest_asyncio

nest_asyncio.apply()

# COMMAND ----------

from playwright.async_api import async_playwright

# COMMAND ----------

dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

# COMMAND ----------


async def main() -> None:
    """Playwrightを使用してWebスクレイピングを実行する"""
    print(f"Environment: {env}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        print(f"Page title: {title}")
        await browser.close()

    print("Playwright scraping completed successfully.")


# COMMAND ----------

await main()
