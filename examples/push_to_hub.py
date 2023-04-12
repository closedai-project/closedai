"""Use this script to push your model pipeline example to the Hugging Face Hub."""

from pathlib import Path

from huggingface_hub import create_repo, upload_folder


def main(name="custom_pipeline"):
    repo_name = name.replace("_", "-")
    repo_url = create_repo(repo_id=repo_name, exist_ok=True, repo_type="space", space_sdk="docker")
    print(f"Repo URL: {repo_url}")
    repo_id = repo_url.repo_id

    project_dir = Path(__file__).parent / name
    if not project_dir.exists():
        raise RuntimeError(f"Project directory {project_dir} does not exist.")

    upload_folder(
        repo_id=repo_id,
        folder_path=str(project_dir),
        path_in_repo=".",
        commit_message="🍻 cheers",
        repo_type="space",
        ignore_patterns=["*.git*", "*README.md*", "*__pycache__*"],
    )


if __name__ == "__main__":
    import fire

    fire.Fire(main)
