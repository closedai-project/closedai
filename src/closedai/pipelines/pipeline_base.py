class ClosedAIPipeline:
    def __init__(self, *args, **kwargs):
        pass

    def generate_completion(self, text, **kwargs):
        raise NotImplementedError("Completions not implemented for this pipeline")

    def get_completion(self, text, **kwargs):
        return "".join(list(self.generate_completion(text, **kwargs)))

    def generate_chat_completion(self, text, **kwargs):
        raise NotImplementedError("Chat completions not implemented for this pipeline")

    def get_chat_completion(self, text, **kwargs):
        return "".join(list(self.generate_completion(text, **kwargs)))
