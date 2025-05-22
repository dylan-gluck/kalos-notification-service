from fastapi import APIRouter, HTTPException
from app.types import NotificationRequest, NotificationResponse
from app.exceptions import (
    ValidationError,
    NotificationServiceError,
    SlackIntegrationError,
)
from app.services.slack_client import SlackService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/notify", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest) -> NotificationResponse:
    """
    Send a notification to a customer's Slack channel.

    Args:
        request: The notification request containing type, customer, and data

    Returns:
        NotificationResponse with success status and optional message_id

    Raises:
        HTTPException: For validation errors (400) or service errors (500)
    """
    try:
        logger.info(
            f"Received notification request for customer {request.customer}, type {request.type}"
        )

        # Initialize Slack service
        slack_service = SlackService()

        # TODO: Phase 3 - Add LLM message formatting
        # For now, create a simple formatted message
        formatted_message = _create_simple_message(request)

        # Post message to Slack
        message_id = await slack_service.post_message(
            request.customer, formatted_message
        )

        return NotificationResponse(status=200, success=True, message_id=message_id)

    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except SlackIntegrationError as e:
        logger.error(f"Slack integration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    except NotificationServiceError as e:
        logger.error(f"Service error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def _create_simple_message(request: NotificationRequest) -> str:
    """
    Create a simple formatted message for the notification.
    This is a temporary implementation until LLM formatting is added.
    """
    campaign_text = f" on {request.campaign}" if request.campaign else ""

    if request.type == "change":
        return f"Hey there! Change notification for {request.customer}{campaign_text}: {request.data}"
    elif request.type == "learning":
        return f"New insights for {request.customer}{campaign_text}: {request.data}"
    elif request.type == "update":
        return f"Action Required for {request.customer}{campaign_text}: {request.data}"
    else:
        return f"Notification for {request.customer}{campaign_text}: {request.data}"
