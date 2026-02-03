# Databricks notebook source
# MAGIC %md
# MAGIC # Medallion Quality Checks
# MAGIC
# MAGIC This notebook is a simple runner for the SQL checks. It loads the
# MAGIC config, builds SQL for each layer, and executes each statement.

# COMMAND ----------
import json
import sys

# Update this path to match your Databricks repo location.
repo_root = "/Workspace/Repos/your_user/your_repo/enterprise_testing_framework"
config_path = f"{repo_root}/config/sources.json"

# Allow imports from the framework package.
sys.path.append(repo_root)

# Load the JSON config that defines tables and checks.
with open(config_path, "r", encoding="utf-8") as file:
    config = json.load(file)

# COMMAND ----------
from framework.sql_builder import render_quality_sql

# Iterate through each layer and run its SQL checks.
medallion = config["medallion"]

for layer_name, layer_config in medallion.items():
    # Build the SQL script for this layer.
    sql_text = render_quality_sql(layer_name, layer_config)
    print(f"Running {layer_name} checks")
    for statement in sql_text.split(";"):
        # Skip empty lines and comments.
        statement = statement.strip()
        if not statement or statement.startswith("--"):
            continue
        # Execute the SQL and display the result.
        display(spark.sql(statement))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Next steps
# MAGIC - Add alerting for non-zero counts
# MAGIC - Store results in a quality metrics table
# MAGIC - Schedule this notebook after each pipeline run
