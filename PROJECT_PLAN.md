# Kalos Slack Notification Service - Developer Specification

## Overview

A Python API service that formats and sends notifications to customer Slack channels through a Slack App integration. The service uses LLM to format messages and provides a simple interface for the Kalos platform to send notifications.

## Requirements

### Functional Requirements

1. **API Endpoint**: `/notify` POST endpoint accepting notification requests
2. **Message Formatting**: Use LLM (OpenAI) to format messages based on notification type and data
3. **Slack Integration**: Post formatted messages to customer-specific Slack channels
4. **Message Types**: Support "change", "learning", "update" notification types
5. **Tone**: Friendly "Blue Bot" persona matching company tone

### Non-Functional Requirements

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Package Manager**: UV
- **Dependencies**: OpenAI agents, Slack SDK, Pydantic
- **Environment**: Requires `OPENAI_API_KEY` & `SLACK_BOT_TOKEN`

## Architecture

### Technology Stack

- **API Framework**: FastAPI for HTTP server
- **Message Formatting**: OpenAI agents for LLM integration
- **Slack Integration**: Slack SDK for channel posting
- **Data Validation**: Pydantic models
- **Package Management**: UV for dependency management

### Service Flow

1. Receive notification request via `/notify` endpoint
2. Validate request data using Pydantic models
3. Format message using LLM based on notification type and data
4. Identify customer Slack channel
5. Post formatted message to channel via Slack SDK
6. Return success/error response

## API Specification

### POST `/notify`

**Request Body:**
```json
{
  "type": "change" | "learning" | "update",
  "customer": "string",
  "campaign": "string (optional)",
  "data": "string | string[]",
  "links": "string[]"
}
```

**Response:**
```json
{
  "status": 200,
  "success": true,
  "message_id": "string (optional)"
}
```

### Data Models

```python
from pydantic import BaseModel
from typing import Optional, Union, List
from enum import Enum

class NotificationType(str, Enum):
    CHANGE = "change"
    LEARNING = "learning"
    UPDATE = "update"

class NotificationRequest(BaseModel):
    type: NotificationType
    customer: str
    campaign: Optional[str] = None
    data: Union[str, List[str]]
    links: List[str] = []

class NotificationResponse(BaseModel):
    status: int
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
```

## Message Formatting

### Message Templates by Type

**Change Notifications:**
- "Hey there! I just `<change-made>` on `<campaign-name>`"
- Include links as action buttons or inline links

**Learning Notifications:**
- "New insights from your campaign: `<campaign-name>`"
- Format data as bullet points
- Include relevant links

**Update Notifications:**
- "Action Required: `<message>`"
- Include primary action link
- Clear call-to-action formatting

### LLM Integration

- Use OpenAI agents to format messages based on type, customer context, and data
- Maintain consistent "Blue Bot" friendly persona
- Ensure messages are concise and actionable
- Include campaign context when provided

## Error Handling Strategy

### HTTP Status Codes

- **200 OK**: Message successfully posted to Slack channel
- **400 Bad Request**: Invalid request data (validation errors)
- **500 Internal Server Error**: Server errors, LLM failures, or Slack API errors

### Error Response Format

```json
{
  "status": 400|500,
  "success": false,
  "error": "Descriptive error message"
}
```

### Error Scenarios

1. **Validation Errors (400)**:
   - Missing required fields
   - Invalid notification type
   - Invalid customer identifier

2. **Service Errors (500)**:
   - OpenAI API failures
   - Slack API failures
   - Customer channel not found
   - Authentication errors

### Error Recovery

- Log all errors for debugging
- Provide meaningful error messages to callers
- Consider retry mechanisms for transient Slack API failures
- Fallback message formatting if LLM fails

## Slack Integration

### Slack App Setup

1. Create Slack App in workspace
2. Configure bot permissions:
   - `chat:write` - Post messages
   - `channels:read` - Access channel information
3. Install app to workspace
4. Store bot token securely

### Channel Management

- Maintain customer-to-channel mapping
- Support both public and private channels
- Handle channel access permissions
- Validate channel existence before posting

## Testing Plan

### Unit Tests

```python
# Test notification request validation
def test_notification_request_validation():
    # Valid requests
    # Invalid type values
    # Missing required fields
    # Optional field handling

# Test message formatting
def test_message_formatting():
    # Each notification type
    # With/without campaign
    # Multiple data items
    # Link handling

# Test error handling
def test_error_scenarios():
    # Invalid requests
    # LLM failures
    # Slack API errors
```

### Integration Tests

```python
# Test full notification flow
def test_end_to_end_notification():
    # Mock Slack API
    # Mock OpenAI API
    # Verify message posted correctly

# Test Slack integration
def test_slack_integration():
    # Channel discovery
    # Message posting
    # Error handling

# Test LLM integration
def test_llm_formatting():
    # Message formatting quality
    # Persona consistency
    # Error handling
```

### Test Environment Setup

```bash
# Install test dependencies
uv add pytest pytest-asyncio httpx

# Run tests
uvx pytest

# Run with coverage
uvx pytest --cov=.
```

### Mock Strategy

- Mock Slack SDK calls for unit tests
- Mock OpenAI API responses
- Use test Slack workspace for integration tests
- Environment-specific configuration

## Implementation Checklist

### Phase 1: Core API
- [ ] Set up FastAPI application structure
- [ ] Implement Pydantic models
- [ ] Create `/notify` endpoint
- [ ] Add request validation
- [ ] Implement basic error handling

### Phase 2: Slack Integration
- [ ] Set up Slack App and permissions
- [ ] Integrate Slack SDK
- [ ] Implement channel discovery
- [ ] Add message posting functionality
- [ ] Handle Slack API errors

### Phase 3: LLM Integration
- [ ] Integrate OpenAI agents
- [ ] Implement message formatting logic
- [ ] Add persona and tone consistency
- [ ] Handle LLM API errors

### Phase 4: Testing & Polish
- [ ] Write comprehensive tests
- [ ] Add logging and monitoring
- [ ] Performance optimization
- [ ] Documentation updates

## Configuration

### Environment Variables

```bash
OPENAI_API_KEY=sk-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-... (if using socket mode)
```

### Development Setup

```bash
# Copy environment template
cp .env.example .env

# Set up virtual environment
uv venv

# Install dependencies
uv sync

# Start development server
uv run fastapi dev
```

## Deployment Considerations

- Secure storage of API keys
- Health check endpoints
- Logging and monitoring
- Rate limiting for Slack API
- Customer channel configuration management
