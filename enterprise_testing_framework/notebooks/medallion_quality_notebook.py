# Databricks notebook source
# MAGIC %md
# MAGIC # Medallion Quality Checks
# MAGIC
# MAGIC This notebook loads the testing config, builds SQL checks for each
# MAGIC medallion layer, and executes them with Spark SQL.

# COMMAND ----------
import json
import sys

repo_root = "/Workspace/Repos/your_user/your_repo/enterprise_testing_framework"
config_path = f"{repo_root}/config/sources.json"
sys.path.append(repo_root)

with open(config_path, "r", encoding="utf-8") as file:
    config = json.load(file)

# COMMAND ----------
from framework.sql_builder import render_quality_sql

medallion = config["medallion"]

for layer_name, layer_config in medallion.items():
    sql_text = render_quality_sql(layer_name, layer_config)
    print(f"Running {layer_name} checks")
    for statement in sql_text.split(";"):
        statement = statement.strip()
        if not statement or statement.startswith("--"):
            continue
        display(spark.sql(statement))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Next steps
# MAGIC - Add alerting for non-zero counts
# MAGIC - Store results in a quality metrics table
# MAGIC - Schedule this notebook after each pipeline run
