"""Domain entities for the Vehicles bounded context.

This module defines the core aggregate of the Vehicles bounded context.
Entities carry identity and encapsulate domain state; they should only be
created or mutated through domain services that enforce business invariants.
"""


class Car:
    """Aggregate root representing a car listing in the catalogue.

    A ``Car`` captures the essential commercial and photographic information
    for a vehicle offered through the platform.  Instances are created by
    :meth:`~vehicles.domain.services.CarService.create_car`, which validates
    the raw input before constructing this entity.

    Attributes:
        id (int | None): Surrogate identity assigned by the persistence layer
            after the record is saved.  ``None`` for transient (unsaved)
            instances.
        make (str): Manufacturer name (e.g. ``'Toyota'``).
        model (str): Model designation (e.g. ``'Corolla'``).
        year (int): Production year.
        price (float): Listed sale price.
        photo_url (str | None): Public Cloudinary URL for the cover photo.
            ``None`` when no photo has been uploaded yet.
    """

    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        photo_url: str | None = None,
        id: int | None = None,
    ) -> None:
        """Initialise a Car entity.

        Args:
            make (str): Manufacturer name.
            model (str): Model designation.
            year (int): Production year.
            price (float): Listed sale price.
            photo_url (str | None): Public Cloudinary URL for the cover photo.
                Defaults to ``None`` for entities created before a photo is
                uploaded.
            id (int | None): Persistence identity.  Defaults to ``None`` for
                transient entities that have not been saved yet.
        """
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.photo_url = photo_url