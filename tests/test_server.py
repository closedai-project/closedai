from fastapi.testclient import TestClient

from closedai.server import app


client = TestClient(app)


def test_completions():
    # make post request to /completions
    response = client.post(
        "/completions/",
        json={
            "model": "davinci",
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
            "model": "davinci",
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
            "model": "gpt-3.5-turbo",
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
            "model": "gpt-3.5-turbo",
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
