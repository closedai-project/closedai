# Schema same as one in SimpleAI repo (MIT License)
# https://github.com/simpleai-team/simpleai
# TODO - determine if we need license from that repo pasted in this file?

from typing import List, Optional, Union

from pydantic import BaseModel


class CompletionInput(BaseModel):
    model: str
    prompt: str = "<|endoftext|>"
    suffix: str = ""
    max_tokens: int = 7
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    logprobs: int = 0
    echo: bool = False
    stop: Optional[Union[str, list]] = ""
    presence_penalty: float = 0.0
    frequence_penalty: float = 0.0
    best_of: int = 0
    logit_bias: dict = {}
    user: str = ""


class ChatCompletionInput(BaseModel):
    model: str
    messages: List[dict]
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[Union[str, list]] = ""
    max_tokens: int = 7
    presence_penalty: float = 0.0
    frequence_penalty: float = 0.0
    logit_bias: Optional[dict] = {}
    user: str = ""
