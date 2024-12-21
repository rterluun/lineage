from search.pipeline import filter_copy_activities


def test_filter_copy_activities(adf_copy_activity):

    assert (
        len(
            filter_copy_activities(
                copy_activities=adf_copy_activity,
                filter="outputs",
                filter_value="rawFolderPath",
            )
        )
        == 1
    )
