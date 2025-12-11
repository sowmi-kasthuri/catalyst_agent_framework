# CAF configuration defaults

LLM_PROVIDER = LLM_PROVIDER = "gemini"        # gemini | llama | openai
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
DEFAULT_LLAMA_MODEL = "llama-3.1-8b"
DEFAULT_OPENAI_MODEL = "gpt-4.1"

ENABLE_METRICS = True
ENABLE_LOGGING = True
MAX_STEPS = 5

def get_default_model(provider: str) -> str:
    if provider == "gemini":
        return DEFAULT_GEMINI_MODEL
    if provider == "llama":
        return DEFAULT_LLAMA_MODEL
    if provider == "openai":
        return DEFAULT_OPENAI_MODEL
    raise ValueError(f"Unknown provider: {provider}")