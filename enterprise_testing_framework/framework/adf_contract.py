import json
from pathlib import Path


def load_pipeline(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_pipeline_name(pipeline):
    return pipeline.get("name")


def get_parameters(pipeline):
    return list(pipeline.get("properties", {}).get("parameters", {}).keys())


def get_activities(pipeline):
    return pipeline.get("properties", {}).get("activities", [])


def get_copy_activities(pipeline):
    return [activity for activity in get_activities(pipeline) if activity.get("type") == "Copy"]


def get_activity_names(pipeline):
    return [activity.get("name") for activity in get_activities(pipeline)]


def get_copy_activity_inputs(pipeline):
    inputs = {}
    for activity in get_copy_activities(pipeline):
        datasets = []
        for input_ref in activity.get("inputs", []):
            if input_ref.get("type") == "DatasetReference":
                datasets.append(input_ref.get("referenceName"))
        inputs[activity.get("name")] = datasets
    return inputs


def find_failure_handler(pipeline):
    for activity in get_activities(pipeline):
        for dependency in activity.get("dependsOn", []):
            if "Failed" in dependency.get("dependencyConditions", []):
                return activity.get("name")
    return None
