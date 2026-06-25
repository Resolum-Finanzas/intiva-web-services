"""Domain services for the Vehicles bounded context.

Encapsulates the business invariants that must hold before a ``Car`` entity
can be created or updated.  No infrastructure dependency lives here.
"""

from vehicles.domain.entities import Car


class CarService:
    """Domain service responsible for constructing valid ``Car`` entities.

    Enforces the following invariants:

    - ``make`` and ``model`` must be non-empty strings.
    - ``year`` must be a four-digit integer in the range [1886, 2100].
    - ``price`` must be a positive number.
    """

    @staticmethod
    def create_car(
        make: str,
        model: str,
        year: int,
        price: float,
        photo_url: str | None = None,
    ) -> Car:
        """Validate raw input and produce a transient :class:`Car` entity.

        Args:
            make (str): Manufacturer name.
            model (str): Model designation.
            year (int): Production year.
            price (float): Sale price (must be > 0).
            photo_url (str | None): Optional Cloudinary URL already resolved
                by the application layer before calling this service.

        Returns:
            Car: A new, unsaved :class:`Car` domain entity.

        Raises:
            ValueError: If any invariant is violated.
        """
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

        return Car(make, model, year, price, photo_url)