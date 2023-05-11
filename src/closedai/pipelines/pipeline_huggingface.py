from threading import Thread

from ..runtime import is_transformers_available
from .pipeline_base import ClosedAIPipeline


class HuggingFacePipeline(ClosedAIPipeline):
    def __init__(
        self,
        repo_id="gpt2",
        model=None,
        tokenizer=None,
        streamer=None,
        use_auth_token=None,
        decode_kwargs=None,
        torch_dtype=None,
        device_map=None,
        device=None,
    ):
        if is_transformers_available():
            from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline
        else:
            raise RuntimeError(
                "HuggingFacePipeline requires transformers to be installed. Please install transformers with `pip install transformers`"
            )

        tokenizer = tokenizer or AutoTokenizer.from_pretrained(repo_id, use_auth_token=use_auth_token)
        model = model or AutoModelForCausalLM.from_pretrained(repo_id, use_auth_token=use_auth_token)
        self.streamer = streamer or TextIteratorStreamer(tokenizer, skip_prompt=True, **(decode_kwargs or {}))
        self.pipe = pipeline(
            "text-generation",
            streamer=self.streamer,
            model=model,
            tokenizer=tokenizer,
            use_auth_token=use_auth_token,
            device_map=device_map,
            torch_dtype=torch_dtype,
            device=device,
        )

    def generate_completion(self, text, **generate_kwargs):
        thread = Thread(target=self.pipe.__call__, kwargs=dict(text_inputs=text, **generate_kwargs))
        thread.start()
        for new_text in self.streamer:
            yield new_text
