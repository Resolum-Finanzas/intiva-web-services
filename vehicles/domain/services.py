"""Domain services for the Vehicles bounded context."""

from __future__ import annotations

from vehicles.domain.entities import Car


class CarService:
    """Domain service responsible for constructing valid Car entities."""

    @staticmethod
    def create_car(
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
    ) -> Car:
        """Validate raw input and produce a transient Car entity."""
        if not make or not isinstance(make, str):
            raise ValueError("'make' must be a non-empty string.")
        if not model or not isinstance(model, str):
            raise ValueError("'model' must be a non-empty string.")
        try:
            year = int(year)
            if not (1886 <= year <= 2100):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("'year' must be an integer between 1886 and 2100.")
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("'price' must be a positive number.")

        return Car(
            make=make,
            model=model,
            year=year,
            price=price,
            version=version,
            vehicle_type=vehicle_type,
            risk_category=risk_category,
            reference_price=float(reference_price) if reference_price is not None else None,
            residual_value=float(residual_value) if residual_value is not None else None,
            condition=condition,
            fuel_type=fuel_type,
            transmission=transmission,
            mileage=int(mileage) if mileage is not None else None,
            interest_rate=interest_rate,
            drivetrain=drivetrain,
            color_aesthetics=color_aesthetics,
            engine_power=engine_power,
            combined_consumption=combined_consumption,
            safety=safety,
            comfort=comfort,
            photo_url=photo_url,
            vehicle_insurance=None,
        )