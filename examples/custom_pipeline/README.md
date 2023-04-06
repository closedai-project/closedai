# Custom Pipeline

This example shows how to serve any model you want by using a custom pipeline.

## Running the Server

Get into this example's directory:

```
cd examples/custom_pipeline
```

Run the server:

```
uvicorn main:app --reload --port 8000
```

## Client

```python
from closedai import openai

completion = openai.Completion.create(model='asdf', prompt='hi there, my name is')
# >>> completion.choices[0].text
# ', and 0 (test), and 1 (test), and 2 (test), and 3 (test), and 4 (test)'
```