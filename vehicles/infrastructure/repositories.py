"""Repository implementation for the Vehicles bounded context.

Provides the persistence adapter that maps between the
:class:`~vehicles.domain.entities.Car` domain entity and the
:class:`~vehicles.infrastructure.models.CarModel` Peewee ORM model.
Following the Repository pattern, callers in the application layer interact
only with domain entities and are shielded from ORM/database details.
"""

from peewee import DoesNotExist

from vehicles.domain.entities import Car
from vehicles.infrastructure.models import CarModel


class CarRepository:
    """Repository that persists and reconstructs :class:`~vehicles.domain.entities.Car` entities.

    Acts as an in-process collection of domain entities backed by the SQLite
    database.  The mapping between the ORM model and the domain entity is
    handled entirely within this class, keeping the domain layer free of
    infrastructure concerns.
    """

    @staticmethod
    def save(car: Car) -> Car:
        """Persist a transient :class:`~vehicles.domain.entities.Car` entity.

        Inserts a new row into the ``cars`` table using Peewee's ``create``
        helper and returns a new domain entity instance populated with the
        database-assigned ``id``.

        Args:
            car (Car): The transient entity to persist.  Its ``id`` attribute
                is expected to be ``None`` at this point.

        Returns:
            Car: A new :class:`~vehicles.domain.entities.Car` instance that is
            a copy of the input enriched with the auto-assigned ``id`` from
            the database.
        """
        record = CarModel.create(
            make=car.make,
            model=car.model,
            year=car.year,
            price=car.price,
            photo_url=car.photo_url,
        )
        return Car(car.make, car.model, car.year, car.price, car.photo_url, record.id)

    @staticmethod
    def find_all() -> list[Car]:
        """Retrieve every car in the catalogue as domain entities.

        Returns:
            list[Car]: All persisted :class:`~vehicles.domain.entities.Car`
            instances, in insertion order.
        """
        return [
            Car(r.make, r.model, r.year, r.price, r.photo_url, r.id)
            for r in CarModel.select()
        ]

    @staticmethod
    def find_by_id(car_id: int) -> Car | None:
        """Look up a single car by its surrogate identity.

        Args:
            car_id (int): The database-assigned primary key of the record.

        Returns:
            Car | None: The matching :class:`~vehicles.domain.entities.Car`
            entity, or ``None`` if no record with that ``id`` exists.
        """
        try:
            r = CarModel.get_by_id(car_id)
            return Car(r.make, r.model, r.year, r.price, r.photo_url, r.id)
        except DoesNotExist:
            return None