from typing import Dict, List, Literal

from lineage.dataclasses.adf import CopyActivity, Pipeline, PipelineParameter


def find_copy_activities(
    pipeline: Pipeline,
    property_element: Literal["properties", "typeProperties"] = "properties",
) -> List[CopyActivity]:
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


def replace_parameters_in_activity(
    activity_parameters: dict,
    parameters: List[PipelineParameter],
) -> Dict:
    replaced_activity_parameters: Dict = activity_parameters.copy()

    for param_name, param_properties in replaced_activity_parameters.items():
        for pipeline_parameter in parameters:
            placeholder = f"@parameters('{pipeline_parameter.name}')"

            if placeholder in param_properties.get("value", ""):
                param_properties["value"] = param_properties["value"].replace(
                    placeholder,
                    pipeline_parameter.default_value,
                )
        replaced_activity_parameters[param_name] = param_properties

    return replaced_activity_parameters


def replace_activity_parameters_with_values(
    activities: List[CopyActivity],
    parameters: List[PipelineParameter],
) -> List[CopyActivity]:

    replaced_activities = activities.copy()

    for activity in replaced_activities:
        if activity.inputs:
            replaced_activity_parameters = replace_parameters_in_activity(
                activity_parameters=activity.inputs[0].get("parameters", {}),
                parameters=parameters,
            )
            activity.inputs[0]["parameters"] = replaced_activity_parameters

        if activity.outputs:
            replaced_activity_parameters = replace_parameters_in_activity(
                activity_parameters=activity.outputs[0].get("parameters", {}),
                parameters=parameters,
            )
            activity.outputs[0]["parameters"] = replaced_activity_parameters

    return replaced_activities
