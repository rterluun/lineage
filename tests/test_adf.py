from lineage.adf import Pipeline


def test_pipeline_from_jsonfile():
    pipeline = Pipeline().from_jsonfile(file_path="tests/data/pipeline.json")
    print(pipeline.pipeline.file_path)
