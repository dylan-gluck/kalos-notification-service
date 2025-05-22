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
   uv run fastapi dev
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## API Usage

### Send a Notification

Send a POST request to `/notify` with the following payload:

```bash
# Change notification example
curl -X POST "http://localhost:8000/notify" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "change",
    "customer": "hsbc",
    "campaign": "Investment Bankers, Thought-leadership",
    "data": ["Added 15 new prospects to targeting list", "Increased monthly spend from $25k to $40k"]
  }'

# Learning notification example
curl -X POST "http://localhost:8000/notify" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "learning",
    "customer": "goldman",
    "campaign": "Wealth Managers, Conversational",
    "data": ["Conversion rate up 18% month-over-month", "Cost per lead decreased by $45", "Video completion rate: 78%"]
  }'

# Update notification example
curl -X POST "http://localhost:8000/notify" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "update",
    "customer": "anthropic",
    "campaign": "AI Engineers, Video",
    "data": "Monthly spend limit reached - approval needed to continue campaign",
    "links": ["https://getkalos.com/account/approve-budget", "https://getkalos.com/campaigns/ai-engineers/settings"]
  }'
```

### Notification Types

- **`change`**: Changes made by the Blue agent on behalf of Kalos
  - Examples: Campaign modifications, new user additions, budget adjustments
  - Data: Single string or array of strings describing the changes made
  - Links: Not applicable for change notifications
  - LLM Format: Friendly acknowledgment of actions taken

- **`learning`**: Insights generated about active campaigns
  - Examples: Performance analytics, user behavior patterns, optimization recommendations
  - Data: Array of insights/data points discovered by analysis
  - Links: Not applicable for learning notifications
  - LLM Format: Structured presentation of insights and discoveries

- **`update`**: Action required notifications for users
  - Examples: Budget approval requests, campaign review needs, configuration confirmations
  - Data: Description of the action needed
  - Links: Required - URLs to take the specified action (e.g., https://getkalos.com/account/approve-budget)
  - LLM Format: Clear call-to-action with prominent action links

### Request Schema

```typescript
{
  "type": "change" | "learning" | "update",
  "customer": string,           // Customer identifier
  "campaign": string?,          // Optional campaign name
  "data": string | string[],    // Unstructured notification data (formatted by LLM)
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
├── routers/
│   ├── __init__.py
│   └── notifications.py    # Notification endpoint handlers
└── services/
    ├── __init__.py
    ├── message_formatter.py # OpenAI LLM message formatting service
    └── slack_client.py      # Slack SDK integration service
```

### Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **OpenAI API**: LLM integration for intelligent message formatting with Blue Bot persona
- **Slack SDK**: Official Slack API client for Python
- **UV**: Fast Python package installer and resolver
- **Ruff**: High-performance Python linter and formatter

### Key Components

1. **Request Validation**: Pydantic models ensure type safety and validation
2. **Message Formatting Service**: OpenAI LLM creates contextual, friendly messages with Blue Bot persona
3. **Slack Integration Service**: Automated posting to customer-specific channels with error handling
4. **Notification Router**: FastAPI endpoints handling different notification types
5. **Error Handling**: Comprehensive error responses, logging, and fallback to kalos-internal channel
6. **Health Monitoring**: Built-in connection validation and service health checks

## Development

### Code Quality

```bash
# Format code
uv run ruff format

# Run linting
uv run ruff check

# Run tests
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

### Channel Management

#### Channel Naming Convention

Customer names map to channels using a standardized format:
- **Client Format**: All lowercase, no spaces (e.g., `goldman`, `openai`)
- **Channel Format**: Always `${client-name}-private` (e.g., `openai-private`, `goldman-private`)
- **Request Assumption**: Client names in requests are pre-formatted correctly

#### Error Handling

If posting to a customer channel fails with `channel_not_found`:
- Automatically post error details to `kalos-internal` Slack channel
- Include information about the requested client and channel name
- Log the error for debugging purposes

## Development Status

### Completed (Phase 1)
- [x] FastAPI application structure
- [x] Pydantic request/response models
- [x] `/notify` endpoint with validation
- [x] Error handling and logging
- [x] Health check endpoints
- [x] Code formatting and linting setup

### Completed (Phase 2)
- [x] **Slack SDK integration**
  - [x] Slack WebClient integration with bot token authentication
  - [x] Channel discovery and mapping (`{customer}-private` format)
  - [x] Message posting functionality to customer channels
  - [x] Comprehensive Slack API error handling
  - [x] Automatic fallback to `kalos-internal` for channel not found errors
  - [x] Connection validation and health checks
  - [x] Basic message formatting as bridge to LLM integration

### Completed (Phase 3)
- [x] **LLM Message Formatting**
  - [x] OpenAI integration for intelligent message formatting
  - [x] Custom message formatting based on notification type and unstructured data
  - [x] Blue Bot persona implementation for consistent tone
  - [x] Support for single string or array of strings in data parameter
  - [x] Dynamic formatting with friendly, contextual messages
  - [x] Type-specific formatting (change, learning, update notifications)


## Documentation

- **API Documentation**: Available at `/docs` when running the server
- **Project Plan**: See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed specifications

---

**Built with ❤️ for the Kalos platform**
