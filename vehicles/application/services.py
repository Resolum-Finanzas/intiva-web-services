from __future__ import annotations

import re
import urllib.request

from vehicles.domain.entities import Car
from vehicles.domain.enums import InsuranceType
from vehicles.domain.services import CarService
from vehicles.infrastructure.repositories import CarRepository
from vehicles.infrastructure.seed.loader import load_car_fixtures
from vehicles.infrastructure.storage.cloudinary_storage.service import CloudinaryCarPhotoService


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def on_application_started() -> None:
    """Seed the car catalogue on first boot (idempotent).

    Downloads each fixture photo, uploads it to Cloudinary, builds a
    validated domain entity via the domain service, and persists it.
    The operation is a no-op if any car already exists in the database.
    """
    from vehicles.infrastructure.models import CarModel

    if CarModel.select().count() > 0:
        print("[Vehicles] Catalogue already populated — skipping seed.")
        return

    print("[Vehicles] Seeding initial car catalogue …")
    repository = CarRepository()
    fixtures = load_car_fixtures()

    for data in fixtures:
        try:
            req = urllib.request.Request(
                data["image_url"],
                headers={"User-Agent": "VeyraCarsSeeder/1.0"}
            )
            with urllib.request.urlopen(req) as response:
                image_bytes: bytes = response.read()

            slug = _slugify(f"{data['make']}-{data['model']}-{data['year']}")
            managed_url = CloudinaryCarPhotoService.upload(image_bytes, slug)

            car = CarService.create_car(
                make=data["make"],
                model=data["model"],
                year=data["year"],
                price=data["price"],
                version=data.get("version"),
                vehicle_type=data.get("vehicle_type"),
                risk_category=data.get("risk_category"),
                reference_price=data.get("reference_price"),
                residual_value=data.get("residual_value"),
                condition=data.get("condition"),
                fuel_type=data.get("fuel_type"),
                transmission=data.get("transmission"),
                mileage=data.get("mileage"),
                interest_rate=data.get("interest_rate"),
                drivetrain=data.get("drivetrain"),
                color_aesthetics=data.get("color_aesthetics"),
                engine_power=data.get("engine_power"),
                combined_consumption=data.get("combined_consumption"),
                safety=data.get("safety"),
                comfort=data.get("comfort"),
                photo_url=managed_url,
            )
            repository.save(car)
            print(f"[Vehicles]   ✓ {data['year']} {data['make']} {data['model']}")

        except Exception as exc:
            print(f"[Vehicles]   ✗ {data['year']} {data['make']} {data['model']} — {exc}")

    print("[Vehicles] Seeding complete.")


class AssignInsuranceCommand:
    """Value object for the assign-insurance use-case."""

    def __init__(self, car_id: int, insurance_type: str) -> None:
        self.car_id = car_id
        self.insurance_type = insurance_type


class CarApplicationService:
    """Application service that orchestrates vehicle use-cases.

    Responsibilities:

    1. Read access – delegates to
       :class:`~vehicles.infrastructure.repositories.CarRepository` to
       retrieve persisted entities.
    2. Insurance assignment – validates the raw insurance type string
       against the domain enum and delegates persistence to the repository.
    """

    def __init__(self):
        """Initialize the service with its required collaborators."""
        self.car_repository = CarRepository()

    def list_cars(self) -> list[Car]:
        """Return all cars in the catalogue as domain entities."""
        return self.car_repository.find_all()

    def get_car(self, car_id: int) -> Car | None:
        """Return a single car by id, or None if not found."""
        return self.car_repository.find_by_id(car_id)

    def assign_insurance(self, command: AssignInsuranceCommand) -> Car:
        """Execute the *assign insurance* use-case.

        Args:
            command (AssignInsuranceCommand): Value object carrying the
                target car id and the raw insurance type string.

        Returns:
            Car: The updated :class:`~vehicles.domain.entities.Car` entity.

        Raises:
            ValueError: If ``insurance_type`` is not a valid
                :class:`~vehicles.domain.enums.InsuranceType` value, or if
                no car matches ``car_id``.
        """
        try:
            insurance = InsuranceType(command.insurance_type)
        except ValueError:
            valid = [t.value for t in InsuranceType]
            raise ValueError(f"Invalid insurance_type. Valid options: {valid}")

        car = self.car_repository.update_insurance(command.car_id, insurance)
        if car is None:
            raise ValueError("Car not found")
        return car

    @staticmethod
    def car_to_dict(car: Car) -> dict:
        """Serialize a Car entity to a JSON-serializable dict.

        Args:
            car (Car): The entity to serialize.

        Returns:
            dict: A plain dict ready to be passed to ``flask.jsonify``.
        """
        return {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "price": car.price,
            "version": car.version,
            "vehicle_type": car.vehicle_type,
            "risk_category": car.risk_category,
            "reference_price": car.reference_price,
            "residual_value": car.residual_value,
            "condition": car.condition,
            "fuel_type": car.fuel_type,
            "transmission": car.transmission,
            "mileage": car.mileage,
            "interest_rate": car.interest_rate,
            "drivetrain": car.drivetrain,
            "color_aesthetics": car.color_aesthetics,
            "specs": {
                "engine_power": car.engine_power,
                "combined_consumption": car.combined_consumption,
                "safety": car.safety,
                "comfort": car.comfort,
            },
            "photo_url": car.photo_url,
            "vehicle_insurance": (
                {
                    "type": car.vehicle_insurance.value,
                    "display_name": car.vehicle_insurance.display_name,
                    "annual_rate": car.vehicle_insurance.annual_rate,
                }
                if car.vehicle_insurance else None
            ),
        }