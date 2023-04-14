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
# >>> completion.choices[0].text
# ', and 0 (test), and 1 (test), and 2 (test), and 3 (test), and 4 (test)'
```

Or, if you want to use the hosted one:

```python
from closedai import openai

openai.api_base = 'https://nateraw-llama-huggingface.hf.space'
completion = openai.Completion.create(model='huggingface:zpn/llama-7b', prompt='hi there, my name is')
```