"""Application services for the Vehicles bounded context.

Orchestrates use-cases by coordinating domain services, infrastructure
adapters, and repositories.  Contains no domain logic of its own.

``on_application_started`` is the startup event handler registered in
``app.py``.  It is responsible for populating the initial car catalogue the
first time the application boots, uploading seed photos to Cloudinary and
persisting the resulting entities — all coordinated from the application layer
so that infrastructure components never drive their own lifecycle.
"""

import re
import urllib.request

from cloudinary_storage.service import CloudinaryCarPhotoService
from vehicles.domain.entities import Car
from vehicles.domain.services import CarService
from vehicles.infrastructure.repositories import CarRepository


_SEED_CARS: list[tuple[str, str, int, float, str]] = [
    (
        "Toyota", "Corolla", 2024, 22_000.00,
        "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb"
        "?w=640&q=80&auto=format&fit=crop",
    ),
    (
        "Honda", "Civic", 2023, 24_500.00,
        "https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5"
        "?w=640&q=80&auto=format&fit=crop",
    ),
    (
        "Ford", "Mustang", 2024, 32_000.00,
        "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd"
        "?w=640&q=80&auto=format&fit=crop",
    ),
]


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


class CreateCarCommand:
    """Value object that carries the raw input for the *create car* use-case.

    Grouping the parameters into a command object decouples the interface
    layer from the application service signature, making it easier to extend
    the command (e.g. adding optional fields) without changing call sites.

    Attributes:
        make (str): Manufacturer name.
        model (str): Model designation.
        year (int): Production year.
        price (float): Listed sale price.
        image_data (bytes | None): Raw image bytes from a multipart upload.
            ``None`` when no photo is attached to the request.
    """

    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        image_data: bytes | None = None,
    ) -> None:
        """Initialise a CreateCarCommand.

        Args:
            make (str): Manufacturer name.
            model (str): Model designation.
            year (int): Production year.
            price (float): Listed sale price.
            image_data (bytes | None): Raw image bytes from a multipart
                upload.  Defaults to ``None`` when no photo is provided.
        """
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.image_data = image_data


def on_application_started() -> None:
    """Handle the *application started* event for the Vehicles bounded context.

    Populates the ``cars`` table on first boot.  The operation is idempotent:
    if any car already exists in the database the function returns immediately
    without touching Cloudinary or the repository.

    Sequence for each seed entry:

    1. **Check** — skip entirely if the table is already populated.
    2. **Download** — fetch the public photo URL into memory (no temp files).
    3. **Upload** — push the bytes to Cloudinary via
       :class:`~vehicles.infrastructure.cloudinary_service.CloudinaryCarPhotoService`
       and obtain the managed ``secure_url``.
    4. **Create** — delegate to
       :class:`~vehicles.domain.services.CarService` to validate invariants
       and build a transient entity.
    5. **Persist** — save via
       :class:`~vehicles.infrastructure.repositories.CarRepository`.

    Any exception during seeding is caught and logged so that a Cloudinary
    outage or missing network during local development does not prevent the
    application from starting.
    """
    from vehicles.infrastructure.models import CarModel  # local import avoids circular deps

    if CarModel.select().count() > 0:
        print("[Vehicles] Catalogue already populated — skipping seed.")
        return

    print("[Vehicles] Seeding initial car catalogue …")
    repository = CarRepository()

    for make, model, year, price, photo_url in _SEED_CARS:
        try:
            req = urllib.request.Request(
                photo_url,
                headers={"User-Agent": "IntivaCarsSeeder/1.0 (university project)"}
            )
            with urllib.request.urlopen(req) as response:
                image_data: bytes = response.read()

            managed_url = CloudinaryCarPhotoService.upload(
                image_data, _slugify(f"{make}-{model}-{year}")
            )

            car = CarService.create_car(make, model, year, price, managed_url)

            repository.save(car)
            print(f"[Vehicles]   ✓ {year} {make} {model}")

        except Exception as exc:  # noqa: BLE001
            print(f"[Vehicles]   ✗ {year} {make} {model} — {exc}")

    print("[Vehicles] Seeding complete.")


class CarApplicationService:
    """Application service that orchestrates vehicle use-cases.

    Responsibilities:

    1. **Photo upload** — delegates to
       :class:`~vehicles.infrastructure.storage.cloudinary_storage.service.CloudinaryCarPhotoService`
       to persist the raw bytes and obtain a managed URL before entity
       creation.
    2. **Domain logic** — delegates to
       :class:`~vehicles.domain.services.CarService` to validate invariants
       and construct a transient :class:`~vehicles.domain.entities.Car` entity.
    3. **Persistence** — delegates to
       :class:`~vehicles.infrastructure.repositories.CarRepository` to save
       the entity and return the persisted aggregate with its assigned
       identity.
    """

    def __init__(self) -> None:
        """Initialise the service with its required collaborators."""
        self._repository = CarRepository()
        self._car_service = CarService()

    def create_car(self, command: CreateCarCommand) -> Car:
        """Execute the *create car* use-case.

        Uploads the photo to Cloudinary (when provided) before delegating
        entity creation to the domain service, so the entity is always
        constructed with a resolved ``photo_url``.

        Args:
            command (CreateCarCommand): Value object carrying the raw input
                for this use-case.

        Returns:
            Car: The persisted :class:`~vehicles.domain.entities.Car` entity
            with its assigned ``id``.

        Raises:
            ValueError: If domain invariants are violated (invalid make,
                model, year, or price).
            cloudinary_storage.exceptions.Error: If the photo upload fails.
        """
        photo_url: str | None = None

        if command.image_data:
            public_id = _slugify(f"{command.make}-{command.model}-{command.year}")
            photo_url = CloudinaryCarPhotoService.upload(command.image_data, public_id)

        car = self._car_service.create_car(
            command.make, command.model, command.year, command.price, photo_url
        )
        return self._repository.save(car)

    def list_cars(self) -> list[Car]:
        """Return all cars in the catalogue as domain entities.

        Returns:
            list[Car]: Every persisted :class:`~vehicles.domain.entities.Car`
            instance, in insertion order.
        """
        return self._repository.find_all()