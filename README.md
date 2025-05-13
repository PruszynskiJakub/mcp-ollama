# Ollama MCP

A Model Context Protocol (MCP) server for the Ollama API, allowing you to use Ollama models with MCP-compatible clients like Claude Desktop, Continue, and others.

## Overview

This MCP server provides a standardized interface to Ollama's powerful local LLM capabilities, making it easy to integrate Ollama models into any MCP-compatible client application.

## Features

- **Text Generation**: Generate completions from Ollama models
- **Chat Completions**: Use Ollama models in conversational mode
- **Model Management**: List and pull models from the Ollama library
- **Model Information**: Access detailed information about available models

## Prerequisites

- Python 3.12 or newer
- Ollama installed and running locally (default: http://localhost:11434)

## Installation

### Using uv (recommended)

```bash
# Create a virtual environment and install dependencies
uv venv
uv pip install -e .
```

### Using pip

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### Running the Server

Start the MCP server:

```bash
python main.py
```

This will start the server on the default stdio transport, which can be used with MCP clients.

### Using with Claude Desktop

1. Install the [Claude Desktop App](https://claude.ai/download)
2. Use the MCP CLI to install this server:
   ```bash
   mcp install /path/to/ollama-mcp/main.py --name "Ollama"
   ```
3. The Ollama MCP server will now appear in the Claude Desktop app's sidebar

### Available Tools

The server provides these tools for MCP clients:

- `generate`: Generate text with an Ollama model
- `chat`: Generate chat completions with an Ollama model
- `list_models`: List all available models in your Ollama installation
- `pull_model`: Pull a new model from the Ollama library

### Available Resources

- `model://{model_name}`: Get detailed information about a specific model

## Configuration

By default, the server connects to Ollama at `http://localhost:11434`. If your Ollama instance is running elsewhere, modify the `OLLAMA_API_BASE_URL` in `main.py`.

## Examples

### Generating Text

```python
# Example of using the 'generate' tool from an MCP client
result = await mcp_client.call_tool("generate", {
    "model": "llama3", 
    "prompt": "Write a short poem about AI", 
    "temperature": 0.7
})
```

### Chat Completion

```python
# Example of using the 'chat' tool from an MCP client
result = await mcp_client.call_tool("chat", {
    "model": "llama3", 
    "messages": [
        {"role": "user", "content": "Hello, who are you?"}
    ],
    "temperature": 0.7
})
```

### Listing Models

```python
# Example of using the 'list_models' tool from an MCP client
models = await mcp_client.call_tool("list_models", {})
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is open source and available under the MIT License.