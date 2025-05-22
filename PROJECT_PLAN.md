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

### Notification Type Specifications

**Change Notifications:**
- **Purpose**: Actions taken by Blue agent on behalf of Kalos
- **Data Input**: Single string or array of strings describing changes made
- **Links**: Not applicable (change notifications don't include action links)
- **LLM Formatting**: Friendly acknowledgment of completed actions
- **Example**: "Hey there! I just added 15 new prospects to targeting list and increased your monthly spend from $25k to $40k for Investment Bankers, Thought-leadership campaign"

**Learning Notifications:**
- **Purpose**: Insights and analytics discovered about active campaigns
- **Data Input**: Array of insights/data points from campaign analysis
- **Links**: Not applicable (learning notifications are informational)
- **LLM Formatting**: Structured presentation of discoveries and insights
- **Example**: "New insights from your Wealth Managers, Conversational campaign: Conversion rate up 18% month-over-month, Cost per lead decreased by $45, Video completion rate: 78%"

**Update Notifications:**
- **Purpose**: Action required from the user
- **Data Input**: Description of the action needed
- **Links**: Required - URLs for taking the specified action (e.g., https://getkalos.com/account/approve-budget)
- **LLM Formatting**: Clear call-to-action with prominent action links
- **Example**: "Action Required: Monthly spend limit reached for AI Engineers, Video campaign - approval needed to continue. [Approve Budget] [Review Settings]"

### LLM Integration Requirements

- Use OpenAI agents to format unstructured data into contextual messages
- Maintain consistent "Blue Bot" friendly persona across all notification types
- Support both single string and array of strings for data parameter
- Include campaign context when provided
- Format links appropriately for update notifications only
- Ensure messages are concise, actionable, and type-appropriate

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

3. **Channel Not Found (Special Handling)**:
   - When target customer channel `${client-name}-private` doesn't exist
   - Post error notification to `kalos-internal` channel
   - Include client name and attempted channel in error message

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

#### Channel Access

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

### Phase 1: Core API (COMPLETED)
- [x] Set up FastAPI application structure
- [x] Implement Pydantic models
- [x] Create `/notify` endpoint
- [x] Add request validation
- [x] Implement basic error handling

### Phase 2: Slack Integration (COMPLETED)
- [x] Set up Slack App and permissions
- [x] Integrate Slack SDK
- [x] Implement channel discovery (`{customer}-private` format)
- [x] Add message posting functionality
- [x] Handle Slack API errors with fallback to kalos-internal
- [x] Connection validation and health checks
- [x] Comprehensive testing with real Slack integration

### Phase 3: LLM Integration (IN PROGRESS)
- [ ] Integrate OpenAI agents for intelligent message formatting
- [ ] Implement notification type-specific formatting:
  - [ ] **Change**: Friendly acknowledgment of Blue agent actions
  - [ ] **Learning**: Structured presentation of campaign insights
  - [ ] **Update**: Clear call-to-action with prominent links
- [ ] Support unstructured data input (string or array of strings)
- [ ] Add Blue Bot persona and tone consistency
- [ ] Handle LLM API errors with graceful fallbacks

### Phase 4: Testing & Polish
- [x] Write comprehensive Slack integration tests
- [ ] Add LLM integration tests
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
