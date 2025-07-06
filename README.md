# HubSpotAutomation

Automate CRM operations using LangChain agents, HubSpot API, and Gmail API. This project provides an intelligent assistant for managing contacts, deals, and sending emails, leveraging LLMs and tool-based orchestration.

## Features
- **Contact Management:** Create and update HubSpot contacts.
- **Deal Management:** Create and update HubSpot deals.
- **Email Operations:** Send emails via Gmail API.
- **OOP-based Orchestration:** Modular, extensible agent orchestrator with robust error handling and logging.
- **LLM Integration:** Uses Groq LLM (via LangChain) for intelligent tool selection and prompt-based task execution.

### Architecture Overview
```
+-------------------+         +-------------------+         +-------------------+
|                   |         |                   |         |                   |
|   User Request    +-------->+  AgentOrchestrator+-------->+   AgentTools      |
|                   |         |                   |         |                   |
+-------------------+         +-------------------+         +-------------------+
                                                                |         |      
                                                                v         v      
                                                        +-----------+ +--------+
                                                        | HubSpot   | | Gmail  |
                                                        | Operations| | Client |
                                                        +-----------+ +--------+
                                                        

```
- **AgentOrchestrator:** Central class that initializes the LLM, loads tools, and routes user requests to the correct tool via prompt-based agent execution.

- **AgentTools:** Collection of tool methods for contact, deal, and email operations. Each tool wraps business logic and API calls.
- **HubSpotOperations:** Handles all HubSpot API interactions (contacts, deals).
- **GmailClient:** Handles Gmail API authentication and sending emails.
## Setup Instructions
1. Clone the Repository
```
git clone https://github.com/Drwaish/HubSpotAutomation
cd HubSpotAutomation
```
2. Create and Configure Environment
### a. Python Environment
Use Python 3.8+
```
(Optional) Create a virtual environment:
python3 -m venv venv
source venv/bin/activate
```
### b. Install Dependencies
```
pip install -r requirements.txt
```
### c. Environment Variables
Create a .env file in the root directory with the following structure:
```
HubSpotAPI=your_hubspot_private_app_token
GROQ_API_KEY=your_groq_api_key
```

### d. Google API Credentials
Download your credentials.json from Google Cloud Console (OAuth 2.0 Client IDs for Gmail API)
Place credentials.json in the agent directory
## File Structure
```
HubSpotAutomation/
├── config.json
├── requirements.txt
├── .env
├── README.md
└── agent/
    ├── agent_orchestrator.py
    ├── agent_tools.py
    ├── google_email.py
    ├── hubpot_ops.py
    └── utils.py
```
### Usage
1. Run the Agent Orchestrator
```
python agent/agent_orchestrator.py
```
- The orchestrator will prompt for user input and execute the appropriate tool (contact, deal, or email operation) using the LLM and available APIs.

2. Example Operations
- **Create Contact:** "Create a contact with email john@example.com and name John Doe."
- **Update Deal:** "Update the deal 'Big Opportunity' to stage 'appointmentscheduled' and amount 5000."
- **Send Email:** "Send an email to jane@example.com with subject 'Welcome' and body 'Hello Jane!'"
## Environment Variable Reference
`HubSpotAPI`: HubSpot Private App Token (required for API access)
`GROQ_API_KEY`: Groq LLM API Key (required for LLM operations)
## Google API Setup
1. Go to Google Cloud Console
2. Enable Gmail API for your project
3. Create OAuth 2.0 Client ID credentials
4. Download `json` and rename it `credential.json` and place it in agent
5. The first run will prompt for Gmail authentication and create token.json

## Extending & Customization
- Add new tools to AgentTools for more CRM or email operations.
- Update `hubpot_ops.py` for advanced HubSpot workflows.
- Modify prompts in `agent_orchestrator.py` for custom agent behavior.

## Troubleshooting
- **API Errors**: Check .env for correct API keys and tokens.
- **Gmail Auth Issues**: Delete token.json and re-run to re-authenticate.
- **Dependency Issues**: Ensure all packages in requirements.txt are installed.

## Authors
Zain Ali Nasir
Generative AI Engineer
mirzazainalinasir@gmail.com
