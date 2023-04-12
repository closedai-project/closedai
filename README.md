# Closed AI

`closedai` is a drop-in replacement for `openai`, but only with open models.

⚠️ **This project is in early development and is a work in progress.** ⚠️

## Installation

```
pip install closedai
```

## Local Development
For now, install locally, as this project is a WIP and PyPi may be out of date.

```
git clone https://github.com/nateraw/closedai.git
cd closedai
pip install -e .
```

## Usage

The idea is that you will run your own OpenAI-like server with whatever model you want. Once the server is running, you can hit it with `openai` python library (or any other SDK of your choosing) by overriding the api base endpoint with the URL to your running server.

To add your own models, check out [this example](https://github.com/closedai-project/closedai/tree/main/examples/custom_pipeline).

### Server

In your terminal, run:

```
closedai
```

You can see the available configuration flags with `closedai --help`.

#### Docker

```
docker build -t closedai .
docker run -p 7860:7860
```

### Client

If using localhost, you can `from closedai import openai`. If running remotely, for now you can just `import openai` and override `openai.api_base` with your endpoint and openai.api_key with a dummy value.

Then, use it as you normally would...

#### Completions

```python
from closedai import openai

completion = openai.Completion.create(model='dummy', prompt='hi there, my name is', stream=False)
print(completion)
```

#### Completions streaming

```python
from closedai import openai

completion = openai.Completion.create(model='dummy', prompt='hi there, my name is', stream=True)
for new_text in completion:
    print(new_text)
```

#### Chat Completions

```python
from closedai import openai

completion = openai.ChatCompletion.create(
    model="dummy",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"},
    ],
    stream=False,
)
print(completion)
```

#### Chat Completions streaming

```python
from closedai import openai

completion = openai.ChatCompletion.create(
    model="dummy",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"},
    ],
    stream=True,
)

for x in completion:
    print(x)
```
