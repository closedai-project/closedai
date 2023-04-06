"""Check presence of installed packages at runtime."""
import sys

import packaging.version


_PY_VERSION: str = sys.version.split()[0].rstrip("+")

if packaging.version.Version(_PY_VERSION) < packaging.version.Version("3.8.0"):
    import importlib_metadata  # type: ignore
else:
    import importlib.metadata as importlib_metadata  # type: ignore


_package_versions = {}

_CANDIDATES = {
    "huggingface_hub": {"huggingface_hub"},
    "transformers": {"transformers"},
}

# Check once at runtime
for candidate_name, package_names in _CANDIDATES.items():
    _package_versions[candidate_name] = "N/A"
    for name in package_names:
        try:
            _package_versions[candidate_name] = importlib_metadata.version(name)
            break
        except importlib_metadata.PackageNotFoundError:
            pass


def _get_version(package_name: str) -> str:
    return _package_versions.get(package_name, "N/A")


def _is_available(package_name: str) -> bool:
    return _get_version(package_name) != "N/A"


# Python
def get_python_version() -> str:
    return _PY_VERSION


# Hf Hub
def is_huggingface_hub_available() -> bool:
    return _is_available("huggingface_hub")


def get_huggingface_hub_version() -> str:
    return _get_version("huggingface_hub")


# Transformers
def is_transformers_available() -> bool:
    return _is_available("transformers")


def get_transformers_version() -> str:
    return _get_version("transformers")
