import os
from abc import ABC

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

load_dotenv(override=True)

class OpenAIClient(ABC):

    def __init__(self):
        self.name =  os.getenv("AGENT_PROVIDER", "github").lower()
        self.model = os.getenv(f"{self.name.upper()}_MODEL", "gpt-4o").lower()
        self.client = self._get_client()

    def _get_client(self):
        providers = {
            "azure": self._get_azure_client,
            "openai": self._get_openai_client,
            "anthropic": self._get_anthropic_client,
            "github": self._get_github_client,
        }
        try:
            return providers[self.name]()
        except KeyError:
            raise ValueError(f"Unsupported agent provider: {self.name}")
       
    def _get_openai_client(self):
        return OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    def _get_anthropic_client(self):
        from anthropic import Anthropic
        return Anthropic()
    
    def _get_github_client(self):
        return OpenAI(
            base_url=os.getenv("GITHUB_API_URL", "https://models.github.ai/inference"),
            api_key=os.environ["GITHUB_TOKEN"]
        )

    def _get_azure_client(self):
        import azure.identity
        token_provider = azure.identity.get_bearer_token_provider(
            azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        return OpenAI(
            base_url=os.environ["AZURE_ENDPOINT"],
            api_key=token_provider
        )
    
    def _get_ollama_client(self):
        # from ollama import AsyncClient
        # return AsyncClient(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        return OpenAI(base_url=os.environ["OLLAMA_HOST"], api_key="nokeyneeded")
    
    def __del__(self):
        if self.client is not None:
            try:
                self.client.close()
            except Exception:
                pass

class AsyncOpenAIClient(ABC):

    def __init__(self):
        self.name =  os.getenv("AGENT_PROVIDER", "github").lower()
        self.model = os.getenv(f"{self.name.upper()}_MODEL", "gpt-4o").lower()
        self.client = self._get_client()

    def _get_client(self):
        providers = {
            "azure": self._get_azure_client,
            "openai": self._get_openai_client,
            "anthropic": self._get_anthropic_client,
            "github": self._get_github_client,
        }
        try:
            return providers[self.name]()
        except KeyError:
            raise ValueError(f"Unsupported agent provider: {self.name}")
       
    def _get_openai_client(self):
        return AsyncOpenAI(api_key=os.environ["OPENAI_KEY"])
    
    def _get_anthropic_client(self):
        from anthropic import Anthropic
        return Anthropic()
    
    def _get_github_client(self):
        return AsyncOpenAI(
            base_url=os.getenv("GITHUB_API_URL", "https://models.github.ai/inference"),
            api_key=os.environ["GITHUB_TOKEN"]
        )

    def _get_azure_client(self):
        import azure.identity.aio
        azure_credential = azure.identity.aio.DefaultAzureCredential()
        token_provider = azure.identity.aio.get_bearer_token_provider(
            azure_credential, "https://cognitiveservices.azure.com/.default"
        )
        return AsyncOpenAI(
            base_url=os.environ["AZURE_ENDPOINT"],
            api_key=token_provider
        )
    
    def _get_ollama_client(self):
        # from ollama import AsyncClient
        # return AsyncClient(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        return AsyncOpenAI(base_url=os.environ["OLLAMA_HOST"], api_key="nokeyneeded")
    
    def __del__(self):
        if self.client is not None:
            try:
                self.client.close()
            except Exception:
                pass