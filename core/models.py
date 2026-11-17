from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class Facility:
    """One bookable place on Discover. Maps 1:1 to your FastAPI response later."""

    id: str
    name: str
    category: str          # filter key: Fitness | Therapy | Recovery | Pop-ups
    subtitle: str
    distance: str
    credits: int
    percent_full: Optional[int] = None
    image_src: Optional[str] = None


# ---- Well E response contract -------------------------------------------
# Gemini returns JSON in this shape; parse_response() turns it into these objects.


@dataclass(frozen=True)
class FacilityRec:
    name: str
    subtitle: str
    distance: str
    credits: int
    image_src: Optional[str] = None


@dataclass(frozen=True)
class TipsCard:
    title: str
    tips: tuple[str, ...]


@dataclass(frozen=True)
class RoutineCard:
    title: str
    description: str
    minutes: int


@dataclass(frozen=True)
class PlanStep:
    title: str
    detail: str
    kind: str = "home"          # home | session | rest
    credits: int = 0            # 0 = free / at home
    recommended: bool = False


@dataclass(frozen=True)
class PlanDay:
    label: str
    steps: tuple[PlanStep, ...]


@dataclass(frozen=True)
class PlanCard:
    title: str
    subtitle: str
    days: tuple[PlanDay, ...]

    @property
    def total_credits(self) -> int:
        return sum(s.credits for d in self.days for s in d.steps)


WellECard = Union[FacilityRec, TipsCard, RoutineCard, PlanCard]


@dataclass(frozen=True)
class WellEResponse:
    message: str
    cards: tuple[WellECard, ...] = ()
    suggestions: tuple[str, ...] = ()


def parse_response(data: dict) -> WellEResponse:
    """Turn a Gemini JSON payload into typed objects. Unknown card types are skipped."""
    cards: list[WellECard] = []
    for raw in data.get("cards", []):
        kind = raw.get("type")
        if kind == "facility":
            cards.append(
                FacilityRec(
                    name=raw["name"],
                    subtitle=raw["subtitle"],
                    distance=raw["distance"],
                    credits=int(raw["credits"]),
                    image_src=raw.get("image_src"),
                )
            )
        elif kind == "tips":
            cards.append(TipsCard(title=raw["title"], tips=tuple(raw["tips"])))
        elif kind == "routine":
            cards.append(
                RoutineCard(
                    title=raw["title"],
                    description=raw["description"],
                    minutes=int(raw["minutes"]),
                )
            )
        elif kind == "plan":
            days = tuple(
                PlanDay(
                    label=d["label"],
                    steps=tuple(
                        PlanStep(
                            title=s["title"],
                            detail=s["detail"],
                            kind=s.get("kind", "home"),
                            credits=int(s.get("credits", 0)),
                            recommended=bool(s.get("recommended", False)),
                        )
                        for s in d["steps"]
                    ),
                )
                for d in raw["days"]
            )
            cards.append(PlanCard(title=raw["title"], subtitle=raw["subtitle"], days=days))
    return WellEResponse(
        message=data["message"],
        cards=tuple(cards),
        suggestions=tuple(data.get("suggestions", [])),
    )