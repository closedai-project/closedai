from ..runtime import is_transformers_available

# from .pipeline_base import ClosedAIPipeline
from .pipeline_dummy import DummyPipeline


# TODO - use strings here and load module
AVAILABLE_PIPELINES = {
    "dummy": DummyPipeline,
}


if is_transformers_available():
    from .pipeline_huggingface import HuggingFacePipeline

    AVAILABLE_PIPELINES["huggingface"] = HuggingFacePipeline


# TODO - load from custom pipeline file
def get_pipeline(name, **kwargs):
    if name in AVAILABLE_PIPELINES:
        return AVAILABLE_PIPELINES[name](**kwargs)
    else:
        # List available pipelines with newline and - at beginning, so like bulleted list
        raise RuntimeError(
            f"Pipeline {name} not found. Available pipelines: \n- " + "\n- ".join(AVAILABLE_PIPELINES) + "\n"
        )
