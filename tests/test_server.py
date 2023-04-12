from fastapi.testclient import TestClient

from closedai.pipelines import DummyPipeline
from closedai.server import _registry, app, register_model


client = TestClient(app)


def test_completions():
    # make post request to /completions
    response = client.post(
        "/completions/",
        json={
            "model": "dummy",
            "prompt": "This is a test",
            "stream": False,
        },
    )
    # assert response is 200
    assert response.status_code == 200


def test_completions_streaming():
    # make post request to /completions
    response = client.post(
        "/completions/",
        json={
            "model": "dummy",
            "prompt": "This is a test",
            "stream": True,
        },
    )
    # assert response is 200
    assert response.status_code == 200
    assert response.text.startswith("data:")
    # check that response is streaming
    assert response.headers["Content-Type"] == "text/event-stream"


def test_chat_completions():
    # make post request to /completions
    response = client.post(
        "/chat/completions/",
        json={
            "model": "dummy",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"},
            ],
            "stream": True,
        },
    )
    # assert response is 200
    assert response.status_code == 200


def test_chat_completions_streaming():
    # make post request to /completions
    response = client.post(
        "/chat/completions/",
        json={
            "model": "dummy",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"},
            ],
            "stream": True,
        },
    )
    # assert response is 200
    assert response.status_code == 200
    assert response.text.startswith("data:")
    # check that response is streaming
    assert response.headers["Content-Type"] == "text/event-stream"


def test_model_not_available():
    # make post request to /completions
    response = client.post(
        "/completions/",
        json={
            "model": "davinci",
            "prompt": "This is a test",
            "stream": False,
        },
    )
    # assert response is 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found. Available models: dummy"


def test_custom_model():
    register_model("dummy_v2", DummyPipeline())
    _client = TestClient(app)
    # make post request to /completions
    response = _client.get("/models/")
    # assert response is 200
    assert response.status_code == 200
    assert response.json() == {"models": ["dummy", "dummy_v2"]}

    # make post request to /completions

    response = _client.post(
        "/completions/",
        json={
            "model": "dummy_v2",
            "prompt": "This is a test",
            "stream": False,
        },
    )
    # assert response is 200
    assert response.status_code == 200

    # cleanup
    _registry.pop("dummy_v2")
