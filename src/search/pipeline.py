from logging import Logger, getLogger
from typing import List, Literal

from lineage.dataclasses.adf import CopyActivity, Pipeline

LOGGER = getLogger(__name__)


def find_copy_activities(
    pipeline: Pipeline,
    property_element: Literal["properties", "typeProperties"] = "properties",
    logger: Logger = LOGGER,
):
    copy_activities: List[CopyActivity] = []
    json_data = pipeline.json_data

    if json_data:
        try:
            activities: list = json_data[property_element]["activities"]

            for activity in activities:
                if activity["type"] == "Until":
                    # Handle Until activity with nested activities
                    copy_activities.append(
                        find_copy_activities(
                            pipeline=Pipeline(
                                file_path=pipeline.file_path,
                                json_data=activity,
                            ),
                            property_element="typeProperties",
                            logger=logger,
                        )
                    )

                if activity["type"] == "Copy":
                    copy_activities.append(
                        CopyActivity(
                            name=activity["name"],
                            inputs=activity["inputs"],
                            outputs=activity["outputs"],
                        )
                    )

        except KeyError:
            logger.warning("No activities found in pipeline")
    return copy_activities
