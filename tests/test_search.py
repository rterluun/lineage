from search.pipeline import filter_copy_activities


def test_filter_copy_activities(adf_copy_activity):

    filtered_copy_activities = filter_copy_activities(
        copy_activities=adf_copy_activity,
        filter="outputs",
        filter_value="rawFolderPath",
    )

    assert len(filtered_copy_activities) == 1
    assert (
        filtered_copy_activities[0].outputs[0]["parameters"]["pFolder"][
            "value"
        ]  # noqa: E501
        == "@parameters('rawFolderPath')"
    )
