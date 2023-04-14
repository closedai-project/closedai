from threading import Thread

from ..runtime import is_transformers_available
from .pipeline_base import ClosedAIPipeline


class HuggingFacePipeline(ClosedAIPipeline):
    def __init__(
        self, repo_id="gpt2", model=None, tokenizer=None, streamer=None, decode_kwargs=None, device_map="auto"
    ):
        if is_transformers_available():
            from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline
        else:
            raise RuntimeError(
                "HuggingFacePipeline requires transformers to be installed. Please install transformers with `pip install transformers`"
            )

        tokenizer = tokenizer or AutoTokenizer.from_pretrained(repo_id)
        model = model or AutoModelForCausalLM.from_pretrained(repo_id)
        self.streamer = streamer or TextIteratorStreamer(tokenizer, skip_prompt=True, **(decode_kwargs or {}))
        self.pipe = pipeline(
            "text-generation", streamer=self.streamer, model=model, tokenizer=tokenizer, device_map=device_map
        )

    def generate_completion(self, text, **generate_kwargs):
        thread = Thread(target=self.pipe.__call__, kwargs=dict(text_inputs=text, **generate_kwargs))
        thread.start()
        for new_text in self.streamer:
            yield new_text
