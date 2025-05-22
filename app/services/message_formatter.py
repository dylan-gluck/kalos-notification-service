"""
Message formatting service using OpenAI Agents for intelligent Slack notifications.
"""

import logging
from typing import List, Union
from agents import Agent, Runner
from ..types import NotificationType

logger = logging.getLogger(__name__)


class MessageFormatter:
    """Formats notification messages using OpenAI Agents with Blue Bot persona."""

    def __init__(self):
        """Initialize the message formatter with OpenAI Agents."""
        self.agent = Agent(
            name="Blue",
            instructions="""You are Blue, a friendly AI assistant representing Kalos. You format notifications for customers through Slack.

Your personality:
- Warm and professional tone
- Enthusiastic about helping customers succeed  
- Clear and concise communication
- Use emojis sparingly but effectively

Notification types:
- "change": Actions you completed on behalf of the customer (past tense, positive)
- "learning": Insights and analytics discovered about campaigns (exciting, data-focused)
- "update": Actions required from customer (clear call-to-action, include links prominently)

Format the notification data into a friendly Slack message. Return ONLY the formatted message text.""",
        )

    async def format_message(
        self,
        notification_type: NotificationType,
        customer: str,
        data: Union[str, List[str]],
        campaign: str = None,
        links: List[str] = None,
    ) -> str:
        """Format a notification message based on type and data."""
        try:
            # Build notification data object
            notification_data = {
                "type": notification_type.value,
                "customer": customer,
                "data": data,
                "campaign": campaign,
                "links": links or [],
            }

            user_prompt = f"Format this notification: {notification_data}"

            result = await Runner.run(self.agent, user_prompt)
            formatted_message = result.final_output.strip()

            logger.info(
                f"Successfully formatted {notification_type} message for {customer}"
            )

            return formatted_message

        except Exception as e:
            logger.error(f"Failed to format message: {str(e)}")
            # Simple fallback
            data_text = ", ".join(data) if isinstance(data, list) else data
            return f"Update from Blue: {data_text}"
