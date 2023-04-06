import time

from .pipeline_base import ClosedAIPipeline


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
