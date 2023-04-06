import time

from closedai import ClosedAIPipeline
from closedai.server import app, data  # noqa


class MyPipeline(ClosedAIPipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_completion(self, text, **kwargs):
        for i in range(5):
            yield f", and {i} (test)"
            time.sleep(1)

    def generate_chat_completion(self, messages, **kwargs):
        for i in range(5):
            yield f", and {i} (test)"
            time.sleep(1)


pipeline = MyPipeline()
data["pipeline"] = pipeline
