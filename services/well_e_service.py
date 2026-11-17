import asyncio

from core.models import WellEResponse, parse_response

TRIAGE_PROMPTS = (
    "I pulled a muscle",
    "I need a mental reset",
    "I have high energy today",
)


class WellEService:
    """Mock Well E backend. Replace ask() with a FastAPI call that returns the same JSON shape.

    The prompt for Gemini should force JSON output matching core.models.parse_response.
    """

    async def ask(self, prompt: str) -> WellEResponse:
        await asyncio.sleep(0.8)  # simulated latency
        try:
            return parse_response(self._mock_payload(prompt))
        except (KeyError, TypeError, ValueError):
            return WellEResponse(
                message="Sorry, something went wrong on my side. Want to try again?",
                suggestions=TRIAGE_PROMPTS,
            )

    # ---- mock data ------------------------------------------------------

    def _mock_payload(self, prompt: str) -> dict:
        text = prompt.lower()

        if "plan" in text:
            return self._plan()
        if any(k in text for k in ("at home", "before", "stretch", "routine")):
            return self._home_help()
        if any(k in text for k in ("muscle", "pain", "pulled", "sore", "hurt")):
            return self._physical()
        if any(k in text for k in ("mental", "stress", "burn", "anxious", "reset", "tired")):
            return self._mental()
        if any(k in text for k in ("energy", "workout", "gym", "active")):
            return self._energy()
        return {
            "message": "I can help with aches, stress, or extra energy. What's going on today?",
            "suggestions": list(TRIAGE_PROMPTS),
        }

    @staticmethod
    def _physical() -> dict:
        return {
            "message": "Got it. Here are two places that can help you recover and get moving again.",
            "cards": [
                {"type": "facility", "name": "Balance Recovery", "subtitle": "Physiotherapy · Recovery plan",
                 "distance": "0.8 km", "credits": 24},
                {"type": "facility", "name": "Cold Plunge Studio", "subtitle": "Cold therapy · Recovery",
                 "distance": "1.4 km", "credits": 15},
            ],
            "suggestions": ["What can I do at home?", "Plan my recovery week"],
        }

    @staticmethod
    def _mental() -> dict:
        return {
            "message": "Take it easy today. Here are two calm options nearby.",
            "cards": [
                {"type": "facility", "name": "Aura Mental Health", "subtitle": "Counseling · Stress relief",
                 "distance": "0.9 km", "credits": 20},
                {"type": "facility", "name": "Zen Garden Pop-up", "subtitle": "Breathwork · Walk-ins open",
                 "distance": "1.2 km", "credits": 12},
            ],
            "suggestions": ["What can I do at home?"],
        }

    @staticmethod
    def _energy() -> dict:
        return {
            "message": "Let's use that energy. These spots have room right now.",
            "cards": [
                {"type": "facility", "name": "Forma Fitness", "subtitle": "Gym · Strength · Mobility",
                 "distance": "0.4 km", "credits": 8},
                {"type": "facility", "name": "Roundhouse Boxing", "subtitle": "Boxing · High intensity",
                 "distance": "1.0 km", "credits": 14},
            ],
            "suggestions": ["Plan my week"],
        }

    @staticmethod
    def _home_help() -> dict:
        return {
            "message": "Yes. Here are a few gentle things you can do at home.",
            "cards": [
                {"type": "tips", "title": "At-Home Recovery Tips",
                 "tips": ["Use a cold pack for 10-15 minutes",
                          "Do gentle, pain-free stretches",
                          "Keep the area supported and rested"]},
                {"type": "routine", "title": "Quick Stretch Routine",
                 "description": "A 7-minute, low-impact routine to ease muscle tension.", "minutes": 7},
            ],
            "suggestions": ["Plan my recovery week"],
        }

    @staticmethod
    def _plan() -> dict:
        return {
            "message": "Here's a 3-day plan to help you recover. Book it all at once, or one step at a time.",
            "cards": [
                {
                    "type": "plan",
                    "title": "Your Recovery Plan",
                    "subtitle": "A simple 3-day plan to help you recover and feel your best.",
                    "days": [
                        {"label": "Day 1", "steps": [
                            {"title": "Gentle Mobility", "detail": "10 min · At home", "kind": "home"},
                            {"title": "Physiotherapy Session", "detail": "Meet a certified therapist.",
                             "kind": "session", "credits": 24, "recommended": True},
                            {"title": "Rest", "detail": "Sleep well, drink water, move lightly.", "kind": "rest"},
                        ]},
                        {"label": "Day 2", "steps": [
                            {"title": "Cold Plunge Recovery", "detail": "Ease soreness and swelling.",
                             "kind": "session", "credits": 15},
                            {"title": "Easy Walk", "detail": "20 min · Outside, no rush", "kind": "home"},
                        ]},
                        {"label": "Day 3", "steps": [
                            {"title": "Mobility Class", "detail": "Forma Fitness · Low impact.",
                             "kind": "session", "credits": 6},
                            {"title": "Light Stretching", "detail": "10 min · At home", "kind": "home"},
                        ]},
                    ],
                }
            ],
            "suggestions": [],
        }