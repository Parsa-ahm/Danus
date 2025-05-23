import os
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model once globally
llm_model_name = "deepseek-ai/deepseek-coder-1.3b-base"
llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
llm_model = AutoModelForCausalLM.from_pretrained(
    llm_model_name,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True,
    use_safetensors=True
)

