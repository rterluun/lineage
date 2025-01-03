import lineage.dataclasses.adf as dataclasses
from writer.graph import diagram


def test_diagram(
    adf_pipeline: dataclasses.Pipeline,
    adf_copy_activity: list[dataclasses.CopyActivity],
):
    dot = diagram(
        pipeline=adf_pipeline,
        copy_activities=adf_copy_activity,
        datasets_dir_path="tests/data",
        linked_services_dir_path="tests/data",
    )

    assert (
        '// pipeline\ndigraph {\n\t"Copy 1" [label="Pipeline activity: Copy 1"]\n\tdataset [label="Dataset: dataset"]\n\tlinkedservice [label="Linked Service: linkedservice"]\n\tdataset -> linkedservice\n\t"Copy 1" -> dataset\n\t"Copy 2" [label="Pipeline activity: Copy 2"]\n\t"Copy 2" -> dataset\n}\n'  # noqa E501
        == dot.source
    )
