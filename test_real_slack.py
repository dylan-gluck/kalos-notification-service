#!/usr/bin/env python3
"""
Real Slack integration test with actual API calls.
This will post messages to actual Slack channels.
"""

import asyncio
import os
from dotenv import load_dotenv
from app.services.slack_client import SlackService
from app.types import NotificationRequest, NotificationType
from app.routers.notifications import send_notification

# Load environment variables from .env file
load_dotenv()


async def test_slack_connection():
    """Test if we can connect to Slack"""
    print("Testing Slack connection...")

    service = SlackService()
    is_connected = service.validate_connection()

    if is_connected:
        print("   PASS: Successfully connected to Slack API")
        return True
    else:
        print("   FAIL: Could not connect to Slack API")
        print("   Check SLACK_BOT_TOKEN environment variable")
        return False


async def test_real_slack_messages():
    """Test posting real messages to Slack channels"""
    print("\nTesting real Slack message posting...")

    # Test cases for different notification types
    test_cases = [
        {
            "name": "Change Notification",
            "type": NotificationType.CHANGE,
            "customer": "hsbc",
            "campaign": "Investment Bankers, Thought-leadership",
            "data": [
                "Added 15 new prospects to targeting list",
                "Increased monthly spend from $25k to $40k",
                "Updated creative for Q4 messaging",
            ],
            "links": [],
        },
        {
            "name": "Learning Notification",
            "type": NotificationType.LEARNING,
            "customer": "goldman",
            "campaign": "Wealth Managers, Conversational",
            "data": [
                "Conversion rate up 18% month-over-month",
                "Cost per lead decreased by $45",
                "Video completion rate: 78%",
                "Peak engagement: Tuesday 10-11 AM EST",
            ],
            "links": [],
        },
        {
            "name": "Update Notification",
            "type": NotificationType.UPDATE,
            "customer": "anthropic",
            "campaign": "AI Engineers, Video",
            "data": "Monthly spend limit reached - approval needed to continue campaign",
            "links": [
                "https://getkalos.com/account/approve-budget",
                "https://getkalos.com/campaigns/ai-engineers/settings",
            ],
        },
    ]

    for test_case in test_cases:
        print(f"\n   Testing {test_case['name']}...")

        try:
            request = NotificationRequest(
                type=test_case["type"],
                customer=test_case["customer"],
                campaign=test_case["campaign"],
                data=test_case["data"],
                links=test_case["links"],
            )

            response = await send_notification(request)

            if response.success:
                print(f"   PASS: Posted to #{test_case['customer']}-private")
                print(f"   Message ID: {response.message_id}")
            else:
                print("   FAIL: Failed to post message")

        except Exception as e:
            print(f"   ERROR: {str(e)}")
            # This might trigger kalos-internal notification for channel not found


async def test_channel_not_found():
    """Test error handling when channel doesn't exist"""
    print("\nTesting channel not found error handling...")

    try:
        request = NotificationRequest(
            type=NotificationType.CHANGE,
            customer="openai",
            campaign="Error Test",
            data="This should trigger kalos-internal notification",
            links=[],
        )

        await send_notification(request)
        print(
            "   UNEXPECTED: Message posted successfully when channel should not exist"
        )

    except Exception as e:
        print(f"   EXPECTED: Error occurred - {str(e)}")
        print("   Check #kalos-internal channel for error notification")


async def main():
    """Run real Slack tests"""
    print("Starting Real Slack Integration Tests")
    print("=" * 50)

    # Check if we have a token
    if not os.getenv("SLACK_BOT_TOKEN"):
        print("ERROR: SLACK_BOT_TOKEN not found in environment")
        print("Please set your Slack bot token before running real tests")
        return

    # Test connection first
    if not await test_slack_connection():
        return

    # Run actual message tests
    await test_real_slack_messages()

    # Test error handling
    await test_channel_not_found()

    print("\n" + "=" * 50)
    print("Real Slack integration tests completed!")
    print("Check your Slack workspace for posted messages")


if __name__ == "__main__":
    asyncio.run(main())
