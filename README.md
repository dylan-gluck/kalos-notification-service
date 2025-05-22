## Kalos Slack Notification Service

Design a notification service / api that posts slack messages to client channels.

### Approach

Slack App to identify as "Blue" or Blue Bot. Could match tone, friendly etc. Example messages:
- "Hey there! I just `<change-made/>` on `<campaign-name/>`"
- "New insights from your campaign: `<campaign-name/>`"
	- List of insights as bullets
- "Action Required: `<message/>`"
	- Link

Notification service is a Python API that can be used to send notifications to Slack channels.
- Simple interface
- LLM to format message
- Slack integration to post to channels

**API design:**

- `/notify`
	- type: "change" | "learning" | "update"
	- customer: string
	- campaign?: string
	- data: string | string[]
	- links: string[]

### Questions

- How much intelligence in service vs on Kalos?
	- What if params/endpoint simplified, LLM decide how to structure message?
	- Eg: POST `/notify`
		- Req: {type: "change", customer: "abc", data: "Added user: dylan to account"}
		- (Format message, find customer channel, post message)
		- Res: {status: 200, success: true}
- How should errors be handled?
	- 400 --> Bad request, let requester know
	- 500 --> Server broken, let requester know
	- 200 --> Error posting to channel, but success posting error to slack?
	- 200 --> Success posting to channel

---

### Developing Locally:

Dependencies:
- Python 3.11
- UV ^0.7.2

1. Copy `.env.example` to `.env`. Add OPENAI_API_KEY.
```bash
cp .env.example .env
```

2. Set up virtual environment
```bash
uv venv
```

3. Install dependencies
```bash
uv sync
```

4. Start dev server
```bash
uv run fastapi dev
```

### TODO

- [x] Gather requirements
- [x] Slack API spec research
- [x] Define approach
- [x] Design API
- [ ] Create Slack App + Add to workspace
- [ ] Build API service (Python, UV, FastAPI)
- [ ] Simulation / testing script
- [ ] Review with team
