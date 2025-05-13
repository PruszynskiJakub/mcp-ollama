from mcp.server.fastmcp import FastMCP, Context
import httpx
import asyncio
from typing import Dict, List, Any, Optional

# Create the MCP server
mcp = FastMCP(name="Ollama", 
              description="MCP server for Ollama API integration")

# Base URL for Ollama API
OLLAMA_API_BASE_URL = "http://localhost:11434/api"
TIMEOUT = 300.0  # 5 minutes timeout for model operations


@mcp.tool()
async def generate(model: str, prompt: str, temperature: float = 0.7) -> str:
    """Generate a completion using an Ollama model.
    
    Args:
        model: The name of the model to use (e.g., "llama3")
        prompt: The prompt text to generate from
        temperature: Controls randomness (0.0 to 1.0, lower is more deterministic)
    
    Returns:
        The generated text response
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        response = await client.post(f"{OLLAMA_API_BASE_URL}/generate", json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")


@mcp.tool()
async def chat(model: str, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """Generate a chat completion using an Ollama model.
    
    Args:
        model: The name of the model to use (e.g., "llama3")
        messages: List of message objects with role and content
        temperature: Controls randomness (0.0 to 1.0, lower is more deterministic)
    
    Returns:
        The assistant's response text
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        response = await client.post(f"{OLLAMA_API_BASE_URL}/chat", json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "")


@mcp.tool()
async def list_models() -> List[Dict[str, Any]]:
    """List all available models in the Ollama server.
    
    Returns:
        List of model information dictionaries
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(f"{OLLAMA_API_BASE_URL}/tags")
        response.raise_for_status()
        return response.json().get("models", [])


@mcp.tool()
async def pull_model(model: str) -> str:
    """Pull a model from the Ollama library.
    
    Args:
        model: The name of the model to pull (e.g., "llama3")
    
    Returns:
        Status message about the pull operation
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        data = {
            "model": model,
            "stream": False
        }
        
        response = await client.post(f"{OLLAMA_API_BASE_URL}/pull", json=data)
        response.raise_for_status()
        return f"Successfully pulled model: {model}"


@mcp.resource("model://{model_name}")
async def get_model_info(model_name: str) -> str:
    """Get information about a specific model.
    
    Args:
        model_name: The name of the model to get information for
    
    Returns:
        Formatted model information
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        data = {
            "model": model_name
        }
        
        response = await client.post(f"{OLLAMA_API_BASE_URL}/show", json=data)
        response.raise_for_status()
        info = response.json()
        
        # Format model info in a readable way
        output = [f"# Model: {model_name}"]
        
        if "modelfile" in info:
            output.append("\n## Modelfile")
            output.append(f"```\n{info['modelfile']}\n```")
            
        if "parameters" in info:
            output.append("\n## Parameters")
            output.append(f"```\n{info['parameters']}\n```")
            
        if "template" in info:
            output.append("\n## Template")
            output.append(f"```\n{info['template']}\n```")
            
        if "details" in info:
            output.append("\n## Details")
            for key, value in info["details"].items():
                output.append(f"- {key}: {value}")
                
        return "\n".join(output)


def main():
    """Run the Ollama MCP server"""
    print("Starting Ollama MCP server...")
    mcp.run()


if __name__ == "__main__":
    main()