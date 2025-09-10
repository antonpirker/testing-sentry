#!/usr/bin/env python3
"""
Local text generation server that mimics the Hugging Face Inference API.
This allows you to use InferenceClient with a local model.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import uvicorn
from typing import Dict, Any, Optional


class TextGenerationRequest(BaseModel):
    inputs: str
    parameters: Optional[Dict[str, Any]] = {}


class TextGenerationResponse(BaseModel):
    generated_text: str


class LocalTextGenerationServer:
    def __init__(self, model_name: str = "gpt2"):
        print(f"🔄 Loading model: {model_name}")
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        print("✅ Model loaded successfully!")

    def generate_text(self, prompt: str, parameters: Dict[str, Any] = None) -> str:
        if parameters is None:
            parameters = {}

        # Default parameters
        max_new_tokens = parameters.get("max_new_tokens", 50)
        temperature = parameters.get("temperature", 0.7)
        do_sample = parameters.get("do_sample", True)

        # Tokenize
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )

        # Decode
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return full text (like HF API does)
        print("--------------------------------")
        print(generated_text)
        print("--------------------------------")
        return generated_text


# Initialize the model server
print("🚀 Starting Local Text Generation Server...")
text_gen_server = LocalTextGenerationServer()

# Create FastAPI app
app = FastAPI(title="Local Text Generation API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Local Text Generation Server", "status": "running"}


@app.post("/")
async def generate_text_endpoint(request: TextGenerationRequest):
    """
    Main text generation endpoint that mimics HuggingFace Inference API format.
    """
    try:
        generated_text = text_gen_server.generate_text(
            request.inputs,
            request.parameters
        )
        import ipdb; ipdb.set_trace()

        out = {"generated_text": generated_text}

        if request.parameters.get("details"):
            out["details"] = {
                "finish_reason": "length",
                "generated_tokens": 10,
                "prefill": [],
                "tokens": [],
            }

        return out

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("🌐 Server will be available at: http://localhost:8000")
    print("📝 Test endpoint: POST http://localhost:8000/")
    print("📚 API docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")

    uvicorn.run(
        "local_server:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
