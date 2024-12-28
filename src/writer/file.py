from logging import Logger, getLogger
from os import path

import lineage.adf as adf
import lineage.dataclasses.adf as dataclasses

LOGGER = getLogger(__name__)


def log(
    pipeline_name: str,
    copy_activities: list[dataclasses.CopyActivity],
    datasets_dir_path: str,
    linked_services_dir_path: str,
    logger: Logger = LOGGER,
):

    for copy_activity in copy_activities:
        dataset = (
            adf.Dataset()
            .from_jsonfile(
                file_path=path.join(
                    datasets_dir_path,
                    ".".join((copy_activity.outputs_dataset_name, "json")),
                )
            )
            .dataset
        )
        linked_service = (
            adf.LinkedService()
            .from_jsonfile(
                file_path=path.join(
                    linked_services_dir_path,
                    ".".join((dataset.linked_service_name, "json")),
                )
            )
            .linkedservice
        )

        if linked_service.json_data:

            logger.info(
                f"Pipeline '{pipeline_name}' activity '{copy_activity.name}' writes to dataset '{dataset.name}' "
                f"using linked service '{linked_service.name}' to "
                f"'{linked_service.json_data.get('properties', {}).get('typeProperties', {}).get('url', None)}'"
            )
