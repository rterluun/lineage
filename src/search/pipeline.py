from json import dumps
from typing import List, Literal

from lineage.dataclasses.adf import CopyActivity, Pipeline


def find_copy_activities(
    pipeline: Pipeline,
    property_element: Literal["properties", "typeProperties"] = "properties",
):
    copy_activities: List[CopyActivity] = []
    json_data = pipeline.json_data

    if json_data:
        try:
            activities: list = json_data[property_element]["activities"]

            for activity in activities:
                if activity["type"] == "Until":
                    # Handle Until activity with nested activities

                    nested_activities = find_copy_activities(
                        pipeline=Pipeline(
                            file_path=pipeline.file_path,
                            json_data=activity,
                        ),
                        property_element="typeProperties",
                    )

                    for nested_activity in nested_activities:
                        copy_activities.append(nested_activity)

                if activity["type"] == "Copy":
                    copy_activities.append(
                        CopyActivity(
                            name=activity["name"],
                            inputs=activity["inputs"],
                            outputs=activity["outputs"],
                            inputs_dataset_name=activity["inputs"][0]["referenceName"],
                            outputs_dataset_name=activity["outputs"][0][
                                "referenceName"
                            ],
                        )
                    )

        except KeyError:
            pass
    return copy_activities


def filter_copy_activities(
    copy_activities: List[CopyActivity],
    filter: Literal["inputs", "outputs"],
    filter_value: str,
):

    filtered_copy_activities: List[CopyActivity] = []

    for activity in copy_activities:

        for filtered_activity in getattr(activity, filter):
            if filter_value in dumps(filtered_activity):
                filtered_copy_activities.append(activity)

    return filtered_copy_activities
