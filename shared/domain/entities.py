class GraceStrategy:
    """
    Base class for grace strategies.
    Used for calculating partial and total grace periods.
    """

    def apply(self, balance: float, interest: float) -> tuple[float, float]:
        raise NotImplementedError