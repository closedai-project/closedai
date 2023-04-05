import os

import uvicorn


def launch_app(host="127.0.0.1", port=8000, reload=True, pipeline_name="dummy", **kwargs):
    os.environ["CLOSEDAI_PIPELINE"] = pipeline_name
    uvicorn.run(
        "closedai.server:app",
        host="127.0.0.1",
        port=8000,
        reload=reload,
    )


def main():
    from fire import Fire

    Fire(launch_app)
