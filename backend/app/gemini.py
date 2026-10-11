from google import genai
from app.config import settings
import json
from typing import Optional


class GeminiClient:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        self.client = genai.Client(api_key=settings.gemini_api_key)
        # Use gemini-3.8-flash (latest available model)
        self.model_id = "gemini-3.8-flash"

    def chat_with_recommendations(
        self,
        user_message: str,
        user_name: str,
        menu: list[dict],
        order_history: list[str],
        preferences: list[str],
    ) -> dict:
        """Generate a chat response with optional order intent and recommendations."""

        menu_text = "\n".join(
            [f"- {item['name']}: ${item['price']} ({item['description']})" for item in menu]
        )

        history_text = ", ".join(order_history[-5:]) if order_history else "None"
        preferences_text = ", ".join(preferences) if preferences else "None"

        prompt = f"""You are a friendly café assistant helping a customer.

Customer Name: {user_name}
Previous Orders: {history_text}
Known Preferences: {preferences_text}

Current Menu:
{menu_text}

Customer Message: {user_message}

Respond conversationally and helpfully. If the customer is ordering, include a JSON block at the end like:
{{"order_intent": {{"items": ["item_name1", "item_name2"], "instructions": "any special notes"}}}}

Always provide personalized recommendations based on their preferences and history."""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            response_text = response.text

            # Try to extract order intent from response
            order_intent = None
            if "order_intent" in response_text:
                try:
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    if json_start != -1 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        data = json.loads(json_str)
                        order_intent = data.get("order_intent")
                except json.JSONDecodeError:
                    pass

            return {
                "reply": response_text,
                "order_intent": order_intent,
                "recommendation": self._extract_recommendation(response_text),
            }
        except Exception as e:
            return {
                "reply": f"Sorry, I encountered an error: {str(e)}",
                "order_intent": None,
                "recommendation": None,
            }

    def _extract_recommendation(self, response_text: str) -> Optional[str]:
        """Extract recommendation from response if present."""
        if "recommend" in response_text.lower() or "suggest" in response_text.lower():
            lines = response_text.split("\n")
            for line in lines:
                if any(
                    keyword in line.lower()
                    for keyword in ["recommend", "suggest", "try", "perfect"]
                ):
                    return line.strip()
        return None


gemini_client: Optional[GeminiClient] = None


def get_gemini_client():
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiClient()
    return gemini_client
