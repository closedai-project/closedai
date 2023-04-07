import os
import sys

import llamacpp
from closedai import ClosedAIPipeline
from closedai.server import app, data  # noqa


class LlamaCPP(ClosedAIPipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def progress_callback(progress):
            print("Progress: {:.2f}%".format(progress * 100))
            sys.stdout.flush()

        params = llamacpp.InferenceParams.default_with_callback(progress_callback)
        if "LLAMA_PATH" in os.environ:
            params.path_model = os.environ["LLAMA_PATH"]
        else:
            raise RuntimeError(
                "Must export LLAMA_PATH to ggml quantize weights. See https://github.com/thomasantony/llamacpp-python#get-the-model-weights"
            )
        self.model = llamacpp.LlamaInference(params)

    def generate_completion(self, text, **kwargs):
        prompt_tokens = self.model.tokenize(text, True)
        self.model.update_input(prompt_tokens)
        self.model.ingest_all_pending_input()
        # TODO stop on end character
        for i in range(20):
            self.model.eval()
            token = self.model.sample()
            text = self.model.token_to_str(token)
            yield text


pipeline = LlamaCPP()
data["pipeline"] = pipeline
