# Custom Pipeline

This example shows how to serve any Hugging Face `transformers` text generation pipeline (in this case, the llama model).

## Running the Server

Get into this example's directory:

```
cd examples/llama_huggingface
```

Run the server:

```
closedai --pipeline_name huggingface:zpn/llama-7b
```

## Client

```python
from closedai import openai

completion = openai.Completion.create(model='huggingface:zpn/llama-7b', prompt='hi there, my name is')
```

Or, if you want to use the [hosted one](https://nateraw-llama-huggingface-server.hf.space) (which is using a tiny model), you can do:

```python
from closedai import openai

openai.api_base = 'https://nateraw-llama-huggingface-server.hf.space'
completion = openai.Completion.create(model='huggingface:HuggingFaceM4/tiny-random-LlamaForCausalLM', prompt='hi there, my name is')
```