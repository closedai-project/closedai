# Lazy loader vendored from https://github.com/scientific-python/lazy_loader
import importlib
import os
import sys
from typing import TYPE_CHECKING


__version__ = "0.0.2"


_SUBMOD_ATTRS = {
    "cli_main": [
        "main",
        "launch_app",
    ],
    "client": [
        "openai",
    ],
    "runtime": [
        "is_transformers_available",
        "get_transformers_version",
        "is_huggingface_hub_available",
        "get_huggingface_hub_version",
        "get_python_version",
    ],
    "schema": [
        "ChatCompletionInput",
        "CompletionInput",
    ],
    "server": [
        "app",
    ],
    "pipelines": [
        "AVAILABLE_PIPELINES",
        "get_pipeline",
    ],
    "pipelines.pipeline_base": [
        "ClosedAIPipeline",
    ],
    "pipelines.pipeline_dummy": [
        "DummyPipeline",
    ],
    "pipelines.pipeline_huggingface": [
        "HuggingFacePipeline",
    ],
}


def _attach(package_name, submodules=None, submod_attrs=None):
    """Attach lazily loaded submodules, functions, or other attributes.

    Typically, modules import submodules and attributes as follows:

    ```py
    import mysubmodule
    import anothersubmodule

    from .foo import someattr
    ```

    The idea is to replace a package's `__getattr__`, `__dir__`, and
    `__all__`, such that all imports work exactly the way they would
    with normal imports, except that the import occurs upon first use.

    The typical way to call this function, replacing the above imports, is:

    ```python
    __getattr__, __dir__, __all__ = lazy.attach(
        __name__,
        ['mysubmodule', 'anothersubmodule'],
        {'foo': ['someattr']}
    )
    ```
    This functionality requires Python 3.7 or higher.

    Args:
        package_name (`str`):
            Typically use `__name__`.
        submodules (`set`):
            List of submodules to attach.
        submod_attrs (`dict`):
            Dictionary of submodule -> list of attributes / functions.
            These attributes are imported as they are used.

    Returns:
        __getattr__, __dir__, __all__

    """
    if submod_attrs is None:
        submod_attrs = {}

    if submodules is None:
        submodules = set()
    else:
        submodules = set(submodules)

    attr_to_modules = {attr: mod for mod, attrs in submod_attrs.items() for attr in attrs}

    __all__ = list(submodules | attr_to_modules.keys())

    def __getattr__(name):
        if name in submodules:
            return importlib.import_module(f"{package_name}.{name}")
        elif name in attr_to_modules:
            submod_path = f"{package_name}.{attr_to_modules[name]}"
            submod = importlib.import_module(submod_path)
            attr = getattr(submod, name)

            # If the attribute lives in a file (module) with the same
            # name as the attribute, ensure that the attribute and *not*
            # the module is accessible on the package.
            if name == attr_to_modules[name]:
                pkg = sys.modules[package_name]
                pkg.__dict__[name] = attr

            return attr
        else:
            raise AttributeError(f"No {package_name} attribute {name}")

    def __dir__():
        return __all__

    if os.environ.get("EAGER_IMPORT", ""):
        for attr in set(attr_to_modules.keys()) | submodules:
            __getattr__(attr)

    return __getattr__, __dir__, list(__all__)


__getattr__, __dir__, __all__ = _attach(__name__, submodules=[], submod_attrs=_SUBMOD_ATTRS)

# TODO - type checking?
