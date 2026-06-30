"""Domain entities for the Vehicles bounded context."""

from __future__ import annotations

from vehicles.domain.enums import InsuranceType


class Car:
    """Aggregate root representing a car listing in the catalogue."""

    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        version: str | None = None,
        vehicle_type: str | None = None,
        risk_category: str | None = None,
        reference_price: float | None = None,
        residual_value: float | None = None,
        condition: str | None = None,
        fuel_type: str | None = None,
        transmission: str | None = None,
        mileage: int | None = None,
        interest_rate: str | None = None,
        drivetrain: str | None = None,
        color_aesthetics: str | None = None,
        engine_power: str | None = None,
        combined_consumption: str | None = None,
        safety: str | None = None,
        comfort: str | None = None,
        photo_url: str | None = None,
        vehicle_insurance: InsuranceType | None = None,
        car_id: int | None = None,  # renamed from id
    ) -> None:
        self.id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.version = version
        self.vehicle_type = vehicle_type
        self.risk_category = risk_category
        self.reference_price = reference_price
        self.residual_value = residual_value
        self.condition = condition
        self.fuel_type = fuel_type
        self.transmission = transmission
        self.mileage = mileage
        self.interest_rate = interest_rate
        self.drivetrain = drivetrain
        self.color_aesthetics = color_aesthetics
        self.engine_power = engine_power
        self.combined_consumption = combined_consumption
        self.safety = safety
        self.comfort = comfort
        self.photo_url = photo_url
        self.vehicle_insurance = vehicle_insurance