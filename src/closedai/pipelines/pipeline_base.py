from typing import List


class ClosedAIPipeline:
    def __init__(self, *args, **kwargs):
        pass

    def generate_completion(self, text: str, **kwargs):
        raise NotImplementedError("Completions not implemented for this pipeline")

    def get_completion(self, text: str, **kwargs):
        return "".join(list(self.generate_completion(text, **kwargs)))

    def generate_chat_completion(self, messages: List[str], **kwargs):
        raise NotImplementedError("Chat completions not implemented for this pipeline")

    def get_chat_completion(self, messages: List[str], **kwargs):
        return "".join(list(self.generate_chat_completion(messages, **kwargs)))
