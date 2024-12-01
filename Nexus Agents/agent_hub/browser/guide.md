

```markdown
## Browser Agent Setup

The browser agent requires several dependencies to function properly. Follow these steps to set up your environment:

### 1. Install Required Packages
```bash
# Install the main packages
pip install browser-use langchain-mistralai

# Install Playwright
pip install playwright

# Install Playwright browsers
playwright install
```

### 2. Configure API Keys
Create a `.env` file in your project root or set environment variables:

```bash
# Mistral AI API key (required)
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional: Other supported LLM API keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

You can get your API keys from:
- Mistral AI: https://console.mistral.ai/
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/

### Example Usage

```python
from agent_hub.browser.browser_agent import BrowserUse
from agent_hub.graph import State

# Initialize the agent
browser_agent = BrowserUse()
await browser_agent.setup()

# Synchronous usage
result = browser_agent({
    "next_agent_input": {
        "query": "Find flights from New York to London"
    }
})

# Asynchronous usage
result = await browser_agent.__acall__({
    "next_agent_input": {
        "query": "Find flights from New York to London"
    }
})
```

### Supported LLM Models

The browser agent works with various LangChain models. Here are some examples:

```python
# Mistral AI (default)
from langchain_mistralai import ChatMistralAI
llm = ChatMistralAI(model="pixtral-large-latest")

# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-opus-20240229")

# OpenAI GPT-4
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4-turbo-preview")

# Initialize browser agent with your chosen LLM
browser_agent = BrowserUse(llm=llm)
```

### Troubleshooting

If you encounter any issues with Playwright:
- Make sure you ran `playwright install` after installing the playwright package
- On Windows, you might need to run PowerShell as administrator
- If browsers fail to start, try reinstalling with `playwright install --force`
```
