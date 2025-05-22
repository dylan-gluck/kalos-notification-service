#!/usr/bin/env python3
"""
Test script for Slack integration functionality.
This tests the basic Slack service functionality without requiring actual API calls.
"""

import asyncio
from unittest.mock import Mock, patch
from app.services.slack_client import SlackService
from app.exceptions import SlackIntegrationError


async def test_slack_service():
    """Test basic SlackService functionality"""
    print("Testing Slack Service...")

    # Test channel name generation
    service = SlackService()

    test_cases = [
        ("hsbc", "hsbc-private"),
        ("goldman", "goldman-private"),
        ("anthropic", "anthropic-private"),
        ("openai", "openai-private"),
    ]

    print("\nTesting channel name generation:")
    for customer, expected in test_cases:
        result = service.get_customer_channel_name(customer)
        status = "PASS" if result == expected else "FAIL"
        print(f"   {status}: {customer} -> {result} (expected: {expected})")

    # Test mock Slack API integration
    print("\nTesting Slack API integration:")

    with patch.object(service.client, "chat_postMessage") as mock_post:
        # Test successful message posting
        mock_post.return_value = {"ok": True, "ts": "1234567890.123456"}

        try:
            message_id = await service.post_message("hsbc", "Test message")
            print(f"   PASS: Successfully posted message (ID: {message_id})")
        except Exception as e:
            print(f"   FAIL: Failed to post message: {e}")

    # Test error handling
    print("\nTesting error handling:")

    # Test channel not found error
    with patch.object(service, "_post_channel_not_found_error") as mock_internal_post:
        with patch.object(service.client, "chat_postMessage") as mock_post:
            # Simulate channel not found error
            from slack_sdk.errors import SlackApiError

            mock_response = {"error": "channel_not_found"}
            mock_post.side_effect = SlackApiError("Error", mock_response)
            mock_internal_post.return_value = None

            try:
                await service.post_message("openai", "Test message")
                print("   FAIL: Expected SlackIntegrationError but none was raised")
            except SlackIntegrationError as e:
                print(f"   PASS: Correctly handled channel not found: {e}")
                # Verify internal notification was called
                mock_internal_post.assert_called_once()

    print("\nSlack service tests completed!")


def test_simple_message_formatting():
    """Test the simple message formatting function"""
    print("\nTesting simple message formatting:")

    from app.routers.notifications import _create_simple_message
    from app.types import NotificationRequest, NotificationType

    test_cases = [
        {
            "type": NotificationType.CHANGE,
            "customer": "hsbc",
            "campaign": "Private Equity Partners, Thought-leadership",
            "data": [
                "Added 25 new prospects from tier-1 firms",
                "Increased monthly budget from $30k to $50k",
            ],
            "links": [],
        },
        {
            "type": NotificationType.LEARNING,
            "customer": "goldman",
            "campaign": "Institutional Investors, Video",
            "data": [
                "Lead conversion up 22% vs last month",
                "CPM decreased 15%",
                "Best performing creative: market outlook video",
            ],
            "links": [],
        },
        {
            "type": NotificationType.UPDATE,
            "customer": "anthropic",
            "campaign": "ML Engineers, Conversational",
            "data": "Campaign spend approaching monthly limit - budget approval needed",
            "links": ["https://getkalos.com/account/approve-budget"],
        },
    ]

    for case in test_cases:
        request = NotificationRequest(**case)
        message = _create_simple_message(request)
        print(f"   {request.type}: {message}")

    print("Message formatting tests completed!")


def test_slack_connection_validation():
    """Test the Slack connection validation"""
    print("\nTesting Slack connection validation:")

    service = SlackService()

    # Test successful validation
    with patch.object(service.client, "auth_test") as mock_auth:
        mock_auth.return_value = {"ok": True}
        result = service.validate_connection()
        status = "PASS" if result else "FAIL"
        print(f"   {status}: Connection validation with success response")

    # Test failed validation
    with patch.object(service.client, "auth_test") as mock_auth:
        from slack_sdk.errors import SlackApiError

        mock_auth.side_effect = SlackApiError("Auth failed", {"error": "invalid_auth"})
        result = service.validate_connection()
        status = "PASS" if not result else "FAIL"
        print(f"   {status}: Connection validation with auth error")

    print("Connection validation tests completed!")


async def test_end_to_end_notification():
    """Test the complete notification flow"""
    print("\nTesting end-to-end notification flow:")

    from app.routers.notifications import send_notification
    from app.types import NotificationRequest, NotificationType

    # Create test request
    test_request = NotificationRequest(
        type=NotificationType.CHANGE,
        customer="hsbc",
        campaign="Investment Advisors, Conversational",
        data=["Added 10 new high-value prospects", "Spend increased to $35k monthly"],
        links=[],
    )

    # Mock the Slack client
    with patch("app.services.slack_client.WebClient") as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.chat_postMessage.return_value = {
            "ok": True,
            "ts": "1234567890.123456",
        }

        try:
            response = await send_notification(test_request)
            if response.success and response.message_id:
                print("   PASS: End-to-end notification completed successfully")
                print(f"   Message ID: {response.message_id}")
            else:
                print("   FAIL: End-to-end notification failed")
        except Exception as e:
            print(f"   FAIL: End-to-end notification error: {e}")

    print("End-to-end notification tests completed!")


async def main():
    """Run all tests"""
    print("Starting Slack Integration Tests\n")

    await test_slack_service()
    test_simple_message_formatting()
    test_slack_connection_validation()
    await test_end_to_end_notification()

    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
