# Routers Module Documentation

## notifications.py

### `router`
APIRouter instance handling notification endpoints.

### `send_notification(request: NotificationRequest) -> NotificationResponse`
**Endpoint:** `POST /notify`

Processes notification requests and posts formatted messages to customer Slack channels.

**Parameters:**
- `request`: NotificationRequest containing type, customer, data, campaign, and links

**Returns:**
- NotificationResponse with status, success flag, and optional message_id

**Raises:**
- `HTTPException(400)` - Validation errors
- `HTTPException(500)` - Service or Slack integration errors

**Flow:**
1. Initialize SlackService and MessageFormatter
2. Format message using LLM with Blue Bot persona
3. Post formatted message to customer's Slack channel
4. Return response with message ID on success

**Example Usage:**
```bash
curl -X POST "http://localhost:8000/notify" \
     -H "Content-Type: application/json" \
     -d '{
       "type": "change",
       "customer": "hsbc", 
       "data": ["Added 25 new prospects"],
       "campaign": "Private Equity Partners"
     }'
```