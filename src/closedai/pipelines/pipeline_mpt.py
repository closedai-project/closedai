import warnings

import torch

from ..runtime import is_transformers_available
from .pipeline_huggingface import HuggingFacePipeline


INSTRUCTION_KEY = "### Instruction:"
RESPONSE_KEY = "### Response:"
END_KEY = "### End"
INTRO_BLURB = "Below is an instruction that describes a task. Write a response that appropriately completes the request."
PROMPT_FOR_GENERATION_FORMAT = """{intro}
{instruction_key}
{instruction}
{response_key}
""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    response_key=RESPONSE_KEY,
)

class MPTPipeline(HuggingFacePipeline):
    def __init__(
        self,
        repo_id,
        attn_impl="triton",
        trust_remote_code=False,
        use_auth_token=None,
        decode_kwargs=None,
        torch_dtype=torch.bfloat16,
        device=0,
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
        self.tokenizer = AutoTokenizer.from_pretrained(
            repo_id,
            trust_remote_code=trust_remote_code,
            use_auth_token=use_auth_token,
        )
        if self.tokenizer.pad_token_id is None:
            warnings.warn("pad_token_id is not set for the tokenizer. Using eos_token_id as pad_token_id.")
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        super().__init__(
            repo_id,
            model=self.model,
            tokenizer=self.tokenizer,
            decode_kwargs=decode_kwargs,
            torch_dtype=torch_dtype,
            device=device,
        )

    def generate_completion(self, text, **generate_kwargs):
        yield from super().generate_completion(
            PROMPT_FOR_GENERATION_FORMAT.format(instruction=text),
            **{
                "temperature": 0.5,
                "top_p": 0.92,
                "top_k": 0,
                "max_new_tokens": 512,
                "use_cache": True,
                "do_sample": True,
                "eos_token_id": self.tokenizer.eos_token_id,
                "pad_token_id": self.tokenizer.pad_token_id,
                "repetition_penalty": 1.1,  # 1.0 means no penalty, > 1.0 means penalty, 1.2 from CTRL paper
                **generate_kwargs,
            }
        )
