# Databricks notebook source

# COMMAND ----------

dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

# COMMAND ----------


def main() -> None:
    """Databricksカタログからデータを取得する"""
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

    print("DB fetch completed successfully.")


# COMMAND ----------

main()
