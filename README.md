# Kalos Slack Notification Service

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![UV](https://img.shields.io/badge/UV-package%20manager-orange.svg)](https://github.com/astral-sh/uv)

A Python API service that intelligently formats and sends notifications to customer Slack channels. Built with FastAPI, the service uses LLM technology to create friendly, contextual messages and delivers them through Slack's Bot API.

## Features

- **Smart Message Formatting**: Uses OpenAI LLM to create contextual, friendly messages
- **Multiple Notification Types**: Supports "change", "learning", and "update" notifications
- **Customer-Specific Channels**: Routes notifications to appropriate customer Slack channels
- **FastAPI Backend**: High-performance async API with automatic OpenAPI documentation
- **Type Safety**: Full Pydantic validation for request/response models
- **Comprehensive Logging**: Structured logging for monitoring and debugging
- **Blue Bot Persona**: Consistent friendly tone matching company branding

## Quick Start

### Prerequisites

- Python 3.11+
- [UV package manager](https://github.com/astral-sh/uv) ^0.7.2
- OpenAI API key
- Slack Bot token

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kalos-notification-service
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=sk-...
   # SLACK_BOT_TOKEN=xoxb-...
   ```

3. **Install dependencies**
   ```bash
   uv venv
   uv sync
   ```

4. **Start the development server**
   ```bash
   uv run fastapi dev app/main.py
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## API Usage

### Send a Notification

Send a POST request to `/notify` with the following payload:

```bash
curl -X POST "http://localhost:8000/notify" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "change",
    "customer": "acme-corp",
    "campaign": "Q4 Launch Campaign",
    "data": "Added new user: john.doe@acme.com to the account"
  }'
```

### Notification Types

- **`change`**: System changes, user additions, configuration updates
  - Example: "Hey there! I just added new user: john.doe@acme.com on Q4 Launch Campaign"

- **`learning`**: Insights, analytics, and discoveries
  - Example: "New insights from your campaign: Q4 Launch Campaign"
  - Formats data as bullet points

- **`update`**: Action required notifications
  - Example: "Action Required: Review pending campaign settings"
  - Includes prominent call-to-action

### Request Schema

```typescript
{
  "type": "change" | "learning" | "update",
  "customer": string,           // Customer identifier
  "campaign": string?,          // Optional campaign name
  "data": string | string[],    // Notification content
  "links": string[]             // Related URLs
}
```

### Response Schema

```typescript
{
  "status": 200,
  "success": true,
  "message_id": string?       // Slack message ID if successful
}
```

## Architecture

### Project Structure

```
app/
├── __init__.py              # Package initialization
├── main.py                  # FastAPI application entry point
├── types.py                 # Pydantic models and type definitions
├── exceptions.py            # Custom exception classes
└── routers/
    ├── __init__.py
    └── notifications.py     # Notification endpoint handlers
```

### Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **OpenAI Agents**: LLM integration for intelligent message formatting
- **Slack SDK**: Official Slack API client for Python
- **UV**: Fast Python package installer and resolver
- **Ruff**: High-performance Python linter and formatter

### Key Components

1. **Request Validation**: Pydantic models ensure type safety and validation
2. **Message Formatting**: OpenAI LLM creates contextual, friendly messages
3. **Slack Integration**: Automated posting to customer-specific channels
4. **Error Handling**: Comprehensive error responses and logging
5. **Health Monitoring**: Built-in health check endpoints

## Development

### Code Quality

```bash
# Format code
uv run ruff format

# Run linting
uv run ruff check

# Run tests (when implemented)
uvx pytest
```

### Adding Dependencies

```bash
# Add a new package
uv add package-name

# Add development dependency
uv add --dev package-name
```

### Development Commands

- **Start server**: `uv run fastapi dev app/main.py`
- **Format code**: `uv run ruff format`
- **Sync dependencies**: `uv sync`
- **Run tools**: `uvx <tool-name>`

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM formatting | Yes |
| `SLACK_BOT_TOKEN` | Slack Bot token for posting messages | Yes |

### Slack App Setup

1. Create a Slack App in your workspace
2. Configure bot permissions:
   - `chat:write` - Post messages
   - `channels:read` - Access channel information
3. Install app to workspace
4. Copy Bot User OAuth Token to `SLACK_BOT_TOKEN`

## Development Status

### Completed (Phase 1)
- [x] FastAPI application structure
- [x] Pydantic request/response models
- [x] `/notify` endpoint with validation
- [x] Error handling and logging
- [x] Health check endpoints
- [x] Code formatting and linting setup

### In Progress
- [ ] **Phase 2**: Slack SDK integration
  - [ ] Channel discovery and mapping
  - [ ] Message posting functionality
  - [ ] Slack API error handling

- [ ] **Phase 3**: LLM Message Formatting
  - [ ] OpenAI agents integration
  - [ ] Message template system
  - [ ] Blue Bot persona implementation

## Documentation

- **API Documentation**: Available at `/docs` when running the server
- **Project Plan**: See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed specifications

---

**Built with ❤️ for the Kalos platform**
