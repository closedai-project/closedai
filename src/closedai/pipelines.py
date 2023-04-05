# Helpful links:
# https://huggingface.co/docs/transformers/main/en/main_classes/pipelines#transformers.TextGenerationPipeline


import time
from threading import Thread

from transformers import TextIteratorStreamer, pipeline


class ClosedAIPipeline:
    def __init__(self, *args, **kwargs):
        pass

    def generate_completion(self, text, **kwargs):
        pass

    def get_completion(self, text, **kwargs):
        return "".join(list(self.generate_completion(text, **kwargs)))


class DummyPipeline(ClosedAIPipeline):
    def __init__(self, duration=5):
        self.duration = duration

    def generate_completion(self, text, **kwargs):
        for i in range(1, self.duration + 1):
            yield f", and {i}"
            time.sleep(0.5)

    def generate_chat_completion(self, messages, **kwargs):
        for i in range(1, self.duration + 1):
            yield f", and {i}"
            time.sleep(0.5)


class HuggingFacePipeline(ClosedAIPipeline):
    def __init__(self, pipe=None, model=None, tokenizer=None, streamer=None, decode_kwargs=None):
        if pipe is None and model is None and tokenizer is None:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            tokenizer = AutoTokenizer.from_pretrained("gpt2")
            model = AutoModelForCausalLM.from_pretrained("gpt2")

        if not pipe:
            self.streamer = streamer or TextIteratorStreamer(tokenizer, skip_prompt=True, **(decode_kwargs or {}))
            pipe = pipeline("text-generation", streamer=self.streamer, model=model, tokenizer=tokenizer)
        elif streamer is None:
            raise RuntimeError("Must pass pipe and streamer together, or exclude pipe and pass model directly")
        self.pipe = pipe

    def generate_completion(self, text, **generate_kwargs):
        thread = Thread(target=self.pipe.__call__, kwargs=dict(text_inputs=text, **generate_kwargs))
        thread.start()
        for new_text in self.streamer:
            yield new_text


# TODO - load from custom pipeline file
def get_pipeline(name, **kwargs):
    if name == "dummy":
        return DummyPipeline(**kwargs)
    elif name == "huggingface":
        return HuggingFacePipeline(**kwargs)
    else:
        raise RuntimeError(f"Pipeline {name} not found")
