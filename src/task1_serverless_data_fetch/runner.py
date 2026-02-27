# Databricks notebook source

# COMMAND ----------

dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

# COMMAND ----------


def main() -> None:
    """gold_intent_dataテーブルからデータを取得する"""
    print(f"Environment: {env}")

    query = """
    SELECT *
    FROM dev_salesnow.intent_data.gold_intent_data
    LIMIT 5
    """

    print("Executing query on dev_salesnow.intent_data.gold_intent_data")
    df = spark.sql(query)  # noqa: F821
    df.show()

    print("Data fetch completed successfully.")


# COMMAND ----------

main()
