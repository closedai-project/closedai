import json
import os
import uuid
from datetime import datetime as dt
from typing import Generator

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import StreamingResponse

from . import ChatCompletionInput, CompletionInput, get_pipeline


app = FastAPI(docs_url="/")

_pipe_name = os.environ.get("CLOSEDAI_PIPELINE", "dummy")
_registry = {_pipe_name: get_pipeline(_pipe_name)}


def register_model(model_name: str, pipeline):
    _registry[model_name] = pipeline


def get_model(model_name: str):
    model = _registry.get(model_name)
    if model is None:
        raise ValueError(f"Model {model_name} not found")
    return model


def stream_completion_response(pipeline, completion_input: CompletionInput) -> Generator:
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
    if completion_input.model not in _registry:
        raise HTTPException(
            status_code=404, detail="Model not found. Available models: " + ", ".join(_registry.keys())
        )

    pipeline = get_model(completion_input.model)
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


def stream_chat_response(pipeline, completion_input: ChatCompletionInput):
    id = str(uuid.uuid4())
    current_timestamp = int(dt.now().timestamp())
    for text in pipeline.generate_chat_completion(completion_input.messages):
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
    if completion_input.model not in _registry:
        raise HTTPException(
            status_code=404, detail="Model not found. Available models: " + ", ".join(_registry.keys())
        )

    pipeline = get_model(completion_input.model)
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


@app.get("/models")
async def models():
    return {"models": list(_registry.keys())}
