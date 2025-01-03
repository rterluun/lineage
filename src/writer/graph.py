from os import path
from typing import Union

from graphviz import Digraph

import lineage.adf as lineage
import lineage.dataclasses.adf as dataclasses


def retrieve_dataclass(
    cls: Union[lineage.Dataset, lineage.LinkedService],
    dir_path: str,
    base_file_name: str,
):

    return cls.from_jsonfile(
        file_path=path.join(
            dir_path,
            ".".join((base_file_name, "json")),
        )
    ).data


def diagram(
    pipeline: dataclasses.Pipeline,
    copy_activities: list[dataclasses.CopyActivity],
    datasets_dir_path: str,
    linked_services_dir_path: str,
):
    dot = Digraph(comment=pipeline.name)
    added_nodes = set()

    for copy_activity in copy_activities:
        dot.node(copy_activity.name, "Pipeline activity: " + copy_activity.name)

        if copy_activity.outputs_dataset_name not in added_nodes:

            dataset: dataclasses.Dataset = retrieve_dataclass(
                cls=lineage.Dataset(),
                dir_path=datasets_dir_path,
                base_file_name=copy_activity.outputs_dataset_name,
            )

            if dataset.linked_service_name:
                linked_service: dataclasses.LinkedService = retrieve_dataclass(
                    cls=lineage.LinkedService(),
                    dir_path=linked_services_dir_path,
                    base_file_name=dataset.linked_service_name,
                )

                dot.node(dataset.name, f"Dataset: {dataset.name}")
                dot.node(linked_service.name, f"Linked Service: {linked_service.name}")

                dot.edge(dataset.name, linked_service.name)

                added_nodes.add(dataset.name)
                added_nodes.add(linked_service.name)

        dot.edge(copy_activity.name, copy_activity.outputs_dataset_name)

    return dot
