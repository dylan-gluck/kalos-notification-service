# Services Module Documentation

## slack_client.py

### `SlackService`
Handles Slack API integration for posting messages to customer channels.

#### `__init__()`
Initializes Slack WebClient using `SLACK_BOT_TOKEN` environment variable.

#### `get_customer_channel_name(customer: str) -> str`
Generates Slack channel name for customer.
- **Returns:** `{customer}-private` format

#### `async post_message(customer: str, message: str) -> str`
Posts message to customer's Slack channel.
- **Parameters:**
  - `customer`: Customer identifier for channel targeting
  - `message`: Formatted message content to post
- **Returns:** Slack message timestamp ID
- **Raises:** `SlackIntegrationError` on API failures

#### `async _post_channel_not_found_error(customer: str)`
Internal method to post error notifications when customer channels don't exist.

## message_formatter.py

### `MessageFormatter`
Formats notification messages using OpenAI Agents with Blue Bot persona.

#### `__init__()`
Initializes OpenAI Agent with Blue Bot instructions and personality.

#### `async format_message(notification_type: NotificationType, customer: str, data: Union[str, List[str]], campaign: str = None, links: List[str] = None) -> str`
Formats notification data into engaging Slack message using LLM.

- **Parameters:**
  - `notification_type`: Type of notification (change/learning/update)
  - `customer`: Customer name for personalization
  - `data`: Notification content (string or list of strings)
  - `campaign`: Optional campaign context
  - `links`: Optional list of relevant URLs
- **Returns:** Formatted message text optimized for Slack
- **Fallback:** Returns simple formatted message if LLM fails

**LLM Instructions:**
- Blue Bot personality: warm, professional, enthusiastic
- Type-specific formatting (past tense for changes, data-focused for learnings, clear CTAs for updates)
- Sparse but effective emoji usage
- Slack-optimized formatting