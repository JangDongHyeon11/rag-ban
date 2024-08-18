import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_index.llms.huggingface import HuggingFaceLLM

class LLMCPULoader():
    def __init__(self,BASE_MODEL):
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        self.stopping_ids = [self.tokenizer.eos_token_id,self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),self.tokenizer.convert_tokens_to_ids(".")]
        self.base_model = BASE_MODEL
    def load_llm(self):
        print("Loading LLM...")
        print(f"EOS Token ID: {self.tokenizer.eos_token_id}")
        max_len= self.tokenizer.model_max_length
        if max_len > 20000:
            max_len=8192
        return HuggingFaceLLM(
                context_window=max_len,
                max_new_tokens=256,
                generate_kwargs={"temperature": 0, "do_sample": False},
                tokenizer_name=self.base_model,
                model_name=self.base_model,
                device_map="cpu",  # CPU에서 실행되도록 설정 (필요시 'auto'로 변경)
                stopping_ids=self.stopping_ids,
                
                #model_kwargs={"torch_dtype": torch.float32}  # CPU에서 float32를 사용
                )
        
class LLMGPULoader():
    def __init__(self,BASE_MODEL):
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        self.stopping_ids = [self.tokenizer.eos_token_id,self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),self.tokenizer.convert_tokens_to_ids(".")]
        self.base_model = BASE_MODEL
    def load_llm(self):
        print("Loading LLM...")
        print(f"EOS Token ID: {self.tokenizer.eos_token_id}")
        max_len= self.tokenizer.model_max_length
        if max_len > 20000:
            max_len=8192
        return HuggingFaceLLM(
                context_window=max_len,
                max_new_tokens=256,
                generate_kwargs={"temperature": 0, "do_sample": False},
                tokenizer_name=self.base_model,
                model_name=self.base_model,
                device_map="auto",  # CPU에서 실행되도록 설정 (필요시 'auto'로 변경)
                stopping_ids=self.stopping_ids,
                
                model_kwargs={"torch_dtype": torch.float16}  # CPU에서 float32를 사용
                )