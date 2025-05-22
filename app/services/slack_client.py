import os
import logging
from typing import Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.exceptions import SlackIntegrationError

logger = logging.getLogger(__name__)


class SlackService:
    """Service for handling Slack API interactions"""

    def __init__(self):
        self.client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        self.internal_channel = "kalos-internal"

    def get_customer_channel_name(self, customer: str) -> str:
        """Convert customer name to Slack channel name format"""
        return f"{customer.lower()}-private"

    async def post_message(self, customer: str, message: str) -> Optional[str]:
        """
        Post a message to the customer's Slack channel.

        Args:
            customer: Customer identifier
            message: Formatted message to send

        Returns:
            Message ID if successful, None if failed

        Raises:
            SlackIntegrationError: If posting fails
        """
        channel_name = self.get_customer_channel_name(customer)

        try:
            response = self.client.chat_postMessage(
                channel=channel_name, text=message, username="Blue Bot"
            )

            if response["ok"]:
                logger.info(f"Successfully posted message to {channel_name}")
                return response["ts"]  # Message timestamp ID
            else:
                logger.error(
                    f"Failed to post message to {channel_name}: {response['error']}"
                )
                raise SlackIntegrationError(f"Slack API error: {response['error']}")

        except SlackApiError as e:
            logger.error(
                f"Slack API error posting to {channel_name}: {e.response['error']}"
            )

            # Handle channel not found specifically
            if e.response["error"] == "channel_not_found":
                await self._post_channel_not_found_error(customer, channel_name)
                raise SlackIntegrationError(
                    f"Customer channel '{channel_name}' not found"
                )

            raise SlackIntegrationError(f"Slack API error: {e.response['error']}")

        except Exception as e:
            logger.error(f"Unexpected error posting to Slack: {str(e)}")
            raise SlackIntegrationError(f"Unexpected Slack error: {str(e)}")

    async def _post_channel_not_found_error(self, customer: str, channel_name: str):
        """Post error notification to internal channel when customer channel not found"""
        error_message = (
            f"Channel Not Found Error\n"
            f"Failed to post notification for customer: `{customer}`\n"
            f"Attempted channel: `{channel_name}`\n"
            f"Please verify the channel exists and the bot has access."
        )

        try:
            self.client.chat_postMessage(
                channel=self.internal_channel, text=error_message, username="Blue Bot"
            )
            logger.info(f"Posted channel not found error to {self.internal_channel}")
        except SlackApiError as e:
            logger.error(
                f"Failed to post error to internal channel: {e.response['error']}"
            )
        except Exception as e:
            logger.error(f"Unexpected error posting to internal channel: {str(e)}")

    def validate_connection(self) -> bool:
        """Test if the Slack client can connect and authenticate"""
        try:
            response = self.client.auth_test()
            return response["ok"]
        except SlackApiError:
            return False
        except Exception:
            return False
