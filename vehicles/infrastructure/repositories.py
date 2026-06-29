"""Repository implementation for the Vehicles bounded context."""

from __future__ import annotations

from peewee import DoesNotExist

from vehicles.domain.entities import Car
from vehicles.domain.enums import InsuranceType
from vehicles.infrastructure.models import CarModel


def _to_entity(r: CarModel) -> Car:
    """Map an ORM record to a domain entity."""
    return Car(
        car_id=r.id,
        make=r.make,
        model=r.model,
        year=r.year,
        price=r.price,
        version=r.version,
        vehicle_type=r.vehicle_type,
        risk_category=r.risk_category,
        reference_price=r.reference_price,
        residual_value=r.residual_value,
        condition=r.condition,
        fuel_type=r.fuel_type,
        transmission=r.transmission,
        mileage=r.mileage,
        interest_rate=r.interest_rate,
        drivetrain=r.drivetrain,
        color_aesthetics=r.color_aesthetics,
        engine_power=r.engine_power,
        combined_consumption=r.combined_consumption,
        safety=r.safety,
        comfort=r.comfort,
        photo_url=r.photo_url,
        vehicle_insurance=(
            InsuranceType(r.vehicle_insurance) if r.vehicle_insurance else None
        ),
    )


class CarRepository:
    """Repository that persists and reconstructs Car entities."""

    @staticmethod
    def save(car: Car) -> Car:
        """Insert a new car record and return the persisted entity."""
        record = CarModel.create(
            make=car.make,
            model=car.model,
            year=car.year,
            price=car.price,
            version=car.version,
            vehicle_type=car.vehicle_type,
            risk_category=car.risk_category,
            reference_price=car.reference_price,
            residual_value=car.residual_value,
            condition=car.condition,
            fuel_type=car.fuel_type,
            transmission=car.transmission,
            mileage=car.mileage,
            interest_rate=car.interest_rate,
            drivetrain=car.drivetrain,
            color_aesthetics=car.color_aesthetics,
            engine_power=car.engine_power,
            combined_consumption=car.combined_consumption,
            safety=car.safety,
            comfort=car.comfort,
            photo_url=car.photo_url,
            vehicle_insurance=(
                car.vehicle_insurance.value if car.vehicle_insurance else None
            ),
        )
        return _to_entity(record)

    @staticmethod
    def find_all() -> list[Car]:
        """Return all cars as domain entities."""
        return [_to_entity(r) for r in CarModel.select()]

    @staticmethod
    def find_by_id(car_id: int) -> Car | None:
        """Return a single car by primary key, or None if not found."""
        try:
            return _to_entity(CarModel.get_by_id(car_id))
        except DoesNotExist:
            return None

    @staticmethod
    def update_insurance(car_id: int, insurance: InsuranceType) -> Car | None:
        """Assign an insurance type to an existing car.

        Returns the updated entity, or None if the car does not exist.
        """
        try:
            record = CarModel.get_by_id(car_id)
        except DoesNotExist:
            return None

        record.vehicle_insurance = insurance.value
        record.save()
        return _to_entity(record)