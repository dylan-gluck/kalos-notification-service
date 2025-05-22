class NotificationServiceError(Exception):
    """Base exception for notification service"""

    pass


class ValidationError(NotificationServiceError):
    """Raised when request validation fails"""

    pass


class SlackAPIError(NotificationServiceError):
    """Raised when Slack API calls fail"""

    pass


class SlackIntegrationError(NotificationServiceError):
    """Raised when Slack integration fails"""

    pass


class LLMError(NotificationServiceError):
    """Raised when LLM formatting fails"""

    pass


class CustomerNotFoundError(NotificationServiceError):
    """Raised when customer channel cannot be found"""

    pass
