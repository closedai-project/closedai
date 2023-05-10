import warnings

import torch

from ..runtime import is_transformers_available
from .pipeline_huggingface import HuggingFacePipeline


class MPTPipeline(HuggingFacePipeline):
    def __init__(
        self,
        repo_id,
        attn_impl="triton",
        trust_remote_code=False,
        use_auth_token=None,
        decode_kwargs=None,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    ):
        if is_transformers_available():
            from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
        else:
            raise RuntimeError(
                "HuggingFacePipeline requires transformers to be installed. Please install transformers with `pip install transformers`"
            )

        config = AutoConfig.from_pretrained(repo_id, trust_remote_code=trust_remote_code)
        if attn_impl:
            config.attn_config["attn_impl"] = attn_impl
        self.model = AutoModelForCausalLM.from_pretrained(
            repo_id,
            torch_dtype=torch_dtype,
            trust_remote_code=trust_remote_code,
            use_auth_token=use_auth_token,
            config=config,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            repo_id,
            trust_remote_code=trust_remote_code,
            use_auth_token=use_auth_token,
        )
        if tokenizer.pad_token_id is None:
            warnings.warn("pad_token_id is not set for the tokenizer. Using eos_token_id as pad_token_id.")
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"

        super().__init__(
            repo_id,
            model=self.model,
            tokenizer=self.tokenizer,
            decode_kwargs=decode_kwargs,
            torch_dtype=torch_dtype,
            device_map=device_map,
        )
