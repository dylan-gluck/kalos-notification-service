# App Module Documentation

## main.py

### `app`
FastAPI application instance with configured routes and middleware.

### Routes
- `GET /health` - Health check endpoint returning `{"status": "healthy"}`

## types.py

### `NotificationType`
Enum defining supported notification types:
- `CHANGE` - Actions completed on behalf of customer
- `LEARNING` - Insights and analytics discovered  
- `UPDATE` - Actions required from customer

### `NotificationRequest`
Pydantic model for API request validation:
```python
class NotificationRequest:
    type: NotificationType
    customer: str
    data: Union[str, List[str]]
    campaign: Optional[str] = None
    links: Optional[List[str]] = None
```

### `NotificationResponse`
Pydantic model for API response:
```python
class NotificationResponse:
    status: int
    success: bool
    message_id: Optional[str] = None
```

## exceptions.py

### `ValidationError`
Raised when input validation fails.

### `NotificationServiceError`
Base exception for general service errors.

### `SlackIntegrationError`
Raised for Slack API specific failures.