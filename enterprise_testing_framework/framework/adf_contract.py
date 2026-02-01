import json
from pathlib import Path


def load_pipeline(path):
    """Load the ADF pipeline JSON from disk."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_pipeline_name(pipeline):
    """Read the pipeline name field."""
    return pipeline.get("name")


def get_parameters(pipeline):
    """Return the declared pipeline parameter names."""
    return list(pipeline.get("properties", {}).get("parameters", {}).keys())


def get_activities(pipeline):
    """Return all activities defined in the pipeline."""
    return pipeline.get("properties", {}).get("activities", [])


def get_copy_activities(pipeline):
    """Filter activities to Copy activities only."""
    return [activity for activity in get_activities(pipeline) if activity.get("type") == "Copy"]


def get_activity_names(pipeline):
    """Return a list of activity names."""
    return [activity.get("name") for activity in get_activities(pipeline)]


def get_copy_activity_inputs(pipeline):
    """Map Copy activity name -> list of input dataset names."""
    inputs = {}
    for activity in get_copy_activities(pipeline):
        datasets = []
        # Each Copy activity can have one or more dataset references.
        for input_ref in activity.get("inputs", []):
            if input_ref.get("type") == "DatasetReference":
                datasets.append(input_ref.get("referenceName"))
        inputs[activity.get("name")] = datasets
    return inputs


def find_failure_handler(pipeline):
    """Find the first activity that depends on a failed step."""
    for activity in get_activities(pipeline):
        for dependency in activity.get("dependsOn", []):
            if "Failed" in dependency.get("dependencyConditions", []):
                return activity.get("name")
    return None
