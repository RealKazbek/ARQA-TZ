from datetime import date
from typing import Literal

from pydantic import AwareDatetime, BaseModel, field_validator, model_validator


class Trip(BaseModel):
    id: str
    start: AwareDatetime
    end: AwareDatetime
    amount: int
    payment: Literal["cash", "card"]
    commission: int

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, amount: int) -> int:
        if amount <= 0:
            raise ValueError("amount must be greater than zero")
        return amount

    @model_validator(mode="after")
    def end_must_be_after_start(self) -> "Trip":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self


class DailySummary(BaseModel):
    trip_count: int
    revenue: int
    commission: int
    net_amount: int
    cash_amount: int
    card_amount: int


class DailyTrips(BaseModel):
    date: date
    trips: list[Trip]
    summary: DailySummary


def calculate_daily_summary(trips: list[Trip]) -> DailySummary:
    revenue = sum(trip.amount for trip in trips)
    commission = sum(trip.commission for trip in trips)

    return DailySummary(
        trip_count=len(trips),
        revenue=revenue,
        commission=commission,
        net_amount=revenue - commission,
        cash_amount=sum(trip.amount for trip in trips if trip.payment == "cash"),
        card_amount=sum(trip.amount for trip in trips if trip.payment == "card"),
    )
