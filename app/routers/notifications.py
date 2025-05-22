from fastapi import APIRouter, HTTPException
from app.types import NotificationRequest, NotificationResponse
from app.exceptions import (
    ValidationError,
    NotificationServiceError,
    SlackIntegrationError,
)
from app.services.slack_client import SlackService
from app.services.message_formatter import MessageFormatter
import logging
import os

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

        # Initialize services
        slack_service = SlackService()

        # Initialize message formatter (uses openai-agents which handles API key automatically)
        message_formatter = MessageFormatter()

        # Format message using LLM
        formatted_message = await message_formatter.format_message(
            notification_type=request.type,
            customer=request.customer,
            data=request.data,
            campaign=request.campaign,
            links=request.links,
        )

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
