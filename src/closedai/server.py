import json
import os
import uuid
from datetime import datetime as dt
from typing import Generator

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import StreamingResponse

from . import ChatCompletionInput, CompletionInput, get_pipeline


app = FastAPI()

# This dict will be updated with the desired pipeline on the start of the server
# from within cli_main.py. The "pipeline" is a simple class that defines the model inference.
# NOTE - this means the "model" key in the CompletionInput schema is not used, as
# the pipeline (model) is already set. This differs from how OpenAI handles it, where
# you define the model on every call. We could do that too, but wanted to be careful not to load
# on each request, as for LLMs, this is time consuming.
# TODO - handle this more elegantly.
data = {"pipeline": get_pipeline(os.environ.get("CLOSEDAI_PIPELINE", "dummy"))}


async def stream_completion_response(pipeline, completion_input: CompletionInput) -> Generator:
    id = str(uuid.uuid4())
    current_timestamp = int(dt.now().timestamp())
    for text in pipeline.generate_completion(completion_input.prompt):
        print(text)
        yield "data: " + json.dumps(
            {
                "id": id,
                "object": "text_completion",
                "created": current_timestamp,
                "choices": [{"text": text, "index": 0, "logprobs": None, "finish_reason": ""}],
                "model": completion_input.model,
            }
        ) + "\n\n"


def get_completion_response(pipeline, completion_input: CompletionInput) -> str:
    response_id = str(uuid.uuid4())
    current_timestamp = int(dt.now().timestamp())

    text = ""
    for x in pipeline.generate_completion(completion_input.prompt):
        text += x

    return (
        json.dumps(
            {
                "id": response_id,
                "object": "text_completion",
                "created": current_timestamp,
                "model": completion_input.model,
                "choices": [{"text": text, "index": 0, "logprobs": None, "finish_reason": ""}],
            }
        )
        + "\n"
    )


@app.post("/completions")
async def completions(request: Request, completion_input: CompletionInput):
    global data
    pipeline = data["pipeline"]
    if completion_input.stream:
        return StreamingResponse(
            stream_completion_response(pipeline, completion_input),
            status_code=status.HTTP_200_OK,
            headers={
                "Content-Type": "text/event-stream",
            },
        )
    else:
        return Response(
            content=get_completion_response(pipeline, completion_input),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
            headers={
                "Content-Type": "application/json",
            },
        )


async def stream_chat_response(pipeline, completion_input: ChatCompletionInput):
    id = str(uuid.uuid4())
    current_timestamp = int(dt.now().timestamp())
    for text in pipeline.generate_chat_completion(completion_input.messages):
        print(text)
        yield "data: " + json.dumps(
            {
                "id": id,
                "object": "chat.completion",
                "created": current_timestamp,
                "choices": [{"finish_reason": "", "index": 0, "delta": {"content": text}}],
                "model": completion_input.model,
            }
        ) + "\n\n"


def get_chat_response(pipeline, completion_input: ChatCompletionInput):
    response_id = str(uuid.uuid4())
    current_timestamp = int(dt.now().timestamp())

    text = ""
    for x in pipeline.generate_chat_completion(completion_input.messages):
        text += x

    return (
        json.dumps(
            {
                "id": response_id,
                "object": "chat.completion",
                "created": current_timestamp,
                "model": completion_input.model,
                "choices": [{"finish_reason": "", "index": 0, "message": {"content": text, "role": "assistant"}}],
            }
        )
        + "\n"
    )


@app.post("/chat/completions")
async def chat_completions(request: Request, completion_input: ChatCompletionInput):
    global data
    pipeline = data["pipeline"]
    if completion_input.stream:
        return StreamingResponse(
            stream_chat_response(pipeline, completion_input),
            status_code=status.HTTP_200_OK,
            headers={
                "Content-Type": "text/event-stream",
            },
        )
    else:
        return Response(
            content=get_chat_response(pipeline, completion_input),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
            headers={
                "Content-Type": "application/json",
            },
        )
