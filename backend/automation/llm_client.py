"""
LLM Client module.
Uses Google Gemini to convert workflow events into natural language task descriptions.
"""

import os
import json
from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from .config import config
from .workflow_loader import Workflow


SYSTEM_PROMPT = """You are a task description generator. Given a sequence of user actions recorded from a browser session, generate a clear, concise natural language description of what the user was trying to accomplish.

The description should be actionable and suitable for instructing an AI browser automation agent to perform the same task.

Guidelines:
- Focus on the high-level goal, not individual clicks
- Include specific details like URLs, form field values (if available), and button names
- Use imperative mood (e.g., "Go to...", "Fill in...", "Click...")
- Keep it concise but complete
- If the workflow seems incomplete, describe what was done so far

Output format:
Just the task description, nothing else. No explanations or preamble."""


WORKFLOW_STEPS_PROMPT = """You are a workflow analyzer. Given a sequence of user actions recorded from a browser session, generate a structured step-by-step plan that describes what the user was doing.

Your output MUST be valid JSON with this exact structure:
{
  "title": "A short, catchy 3-5 word title (e.g., 'Amazon Shoe Search', 'Hi.com Team Exploration')",
  "description": "A detailed, information-rich goal description that includes specific details like website names, pages visited, buttons clicked, and data entered",
  "steps": [
    {"id": 1, "label": "Step description with specific details"},
    {"id": 2, "label": "Step description with specific details"}
  ]
}

Guidelines for title:
- Keep it very short and memorable (3-5 words maximum)
- Capture the essence of what was done (e.g., "YouTube Video Search", "Twitter Profile Update")
- Use title case (capitalize main words)
- Be specific about the website/action (e.g., "Amazon Product Review" not "Website Visit")

Guidelines for description:
- Include specific website names and URLs visited (e.g., "Navigate to Amazon.com and search for running shoes")
- Mention specific buttons, links, or menu items clicked (e.g., "Click the 'About' menu and navigate to 'About hi' page")
- Include specific pages or sections visited (e.g., "Browse the team page on hi.com")
- Mention any forms filled, text entered, or important interactions
- Be detailed but concise - aim for 1-2 sentences that capture the essence with specifics
- If external sites were visited, mention them

Guidelines for steps:
- Each step should be a clear, actionable instruction with specific details
- Include exact names of links, buttons, or menu items (e.g., "Click on 'Open Banking' link")
- Combine trivial actions (like multiple clicks on the same element) into logical steps
- Use imperative mood (e.g., "Navigate to...", "Click on...", "Enter...")
- Include specific targets and destinations (e.g., "Navigate to the 'About hi' page on hi.com")
- Keep step labels descriptive but not overly long

Output ONLY the JSON object, no markdown code blocks, no explanations."""


class LLMClient:
    """Client for generating task descriptions using Gemini."""
    
    def __init__(
        self,
        model: Optional[str] = None,
        analysis_model: Optional[str] = None,
    ):
        self.model = model or config.llm_model
        self.analysis_model = analysis_model or "gemini-pro-latest"
        
        # Initialize Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required. Get one at https://aistudio.google.com/app/apikey")
        
        self.llm = ChatGoogleGenerativeAI(model=self.model, google_api_key=api_key)
        
        # Initialize a separate client for workflow step generation (uses the analysis model)
        self.llm_pro = ChatGoogleGenerativeAI(model=self.analysis_model, google_api_key=api_key)
    
    def generate_task_description(self, workflow: Workflow) -> str:
        """Generate a natural language task description from a workflow."""
        
        user_prompt = f"""Here is a recorded browser workflow:

Starting URL: {workflow.start_url}

Actions performed:
{workflow.summary}

Generate a task description for an AI browser agent to replicate this workflow."""
        
        return self._generate(user_prompt)

    def generate_from_summary(self, summary: str, start_url: str = "") -> str:
        """Generate a task description from a plain text summary."""
        
        user_prompt = f"""Here is a recorded browser workflow:

Starting URL: {start_url}

Actions performed:
{summary}

Generate a task description for an AI browser agent to replicate this workflow."""
        
        return self._generate(user_prompt)

    def _generate(self, prompt: str) -> str:
        """Internal generation logic using Gemini."""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ])
            content = response.content
            if isinstance(content, list):
                content = " ".join([str(c) for c in content])
            return str(content).strip()
        except Exception as e:
            # If generation fails, return a safe fallback
            print(f"Gemini generation failed: {e}")
            print(f"Falling back to raw workflow summary")
            # Extract a simple description from the prompt
            return f"Perform the task based on: {prompt[:200]}..."

    def generate_workflow_steps(self, events: list[dict], start_url: str = "") -> dict:
        """
        Generate a structured workflow description with steps from raw events.
        
        Uses gemini-pro for higher reasoning capability.
        
        Args:
            events: List of raw event dictionaries from the browser recording
            start_url: Optional starting URL
            
        Returns:
            dict with 'description' and 'steps' keys
        """
        # Format events for the prompt
        events_summary = []
        for i, event in enumerate(events, 1):
            event_type = event.get('event_type', event.get('event', 'unknown'))
            url = event.get('url', '')
            title = event.get('title', '')
            data = event.get('data', {})
            raw = event.get('raw', {})
            automation = event.get('automation', {})
            
            # Build a readable event description with all available details
            if event_type in ['navigation', 'page_visit']:
                events_summary.append(f"{i}. Navigated to: {url} (Page: {title})")
            elif event_type == 'click':
                # Try multiple places where click target text might be stored
                target_text = (
                    raw.get('text') or 
                    data.get('text') or 
                    data.get('target') or 
                    automation.get('tag', 'element')
                )
                xpath = automation.get('xpath', '')
                tag = automation.get('tag', '')
                events_summary.append(f"{i}. Clicked on: '{target_text}' ({tag} element) on page: {url}")
            elif event_type == 'input':
                field = data.get('field', data.get('target', raw.get('field', 'field')))
                value = data.get('value', raw.get('value', '[text entered]'))
                events_summary.append(f"{i}. Entered '{value}' in field: {field} on page: {url}")
            elif event_type == 'scroll':
                scroll_y = raw.get('y', data.get('y', 0))
                events_summary.append(f"{i}. Scrolled to position {scroll_y}px on page: {url} ({title})")
            elif event_type == 'keypress':
                key = raw.get('key', data.get('key', 'key'))
                events_summary.append(f"{i}. Pressed key: {key}")
            else:
                # Include all available data for unknown events
                all_data = {**data, **raw}
                events_summary.append(f"{i}. {event_type} on {url}: {all_data}")
        
        events_text = "\n".join(events_summary) if events_summary else "No events recorded"
        
        user_prompt = f"""Here is a recorded browser workflow:

Starting URL: {start_url}

Detailed events:
{events_text}

Analyze these events carefully. Note the specific text of buttons/links clicked, the URLs visited, and page titles. Generate a structured workflow plan with specific details."""

        try:
            response = self.llm_pro.invoke([
                SystemMessage(content=WORKFLOW_STEPS_PROMPT),
                HumanMessage(content=user_prompt)
            ])
            content = response.content
            if isinstance(content, list):
                content = " ".join([str(c) for c in content])
            
            # Parse the JSON response
            content = str(content).strip()
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            
            # Validate structure
            if "title" not in result:
                result["title"] = "Workflow"
            if "description" not in result:
                result["description"] = "Recorded workflow"
            if "steps" not in result:
                result["steps"] = []
            
            # Ensure step IDs are sequential
            for i, step in enumerate(result["steps"], 1):
                step["id"] = i
                if "label" not in step:
                    step["label"] = f"Step {i}"
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse workflow steps JSON: {e}")
            print(f"Raw response: {content}")
            # Return a fallback structure
            return {
                "title": "Workflow",
                "description": "Recorded workflow (AI analysis failed)",
                "steps": [{"id": i+1, "label": line} for i, line in enumerate(events_summary[:10])]
            }
        except Exception as e:
            print(f"Workflow steps generation failed: {e}")
            return {
                "title": "Workflow",
                "description": "Recorded workflow (AI analysis failed)",
                "steps": [{"id": i+1, "label": line} for i, line in enumerate(events_summary[:10])]
            }
