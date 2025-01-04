from typing import List, Literal

from lineage.dataclasses.adf import CopyActivity, Pipeline, PipelineParameter


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
                            name=pipeline.name,
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


def find_pipeline_parameters(pipeline: Pipeline) -> List[PipelineParameter]:

    pipeline_parameters: List[PipelineParameter] = []

    if pipeline.json_data:
        parameters = pipeline.json_data.get("properties", {}).get("parameters", {})
        for param_name, param_properties in parameters.items():
            pipeline_parameters.append(
                PipelineParameter(
                    name=param_name,
                    type=str(param_properties.get("type", None)),
                    default_value=str(param_properties.get("defaultValue", None)),
                )
            )

    return pipeline_parameters
