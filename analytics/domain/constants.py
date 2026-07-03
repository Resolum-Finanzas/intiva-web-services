class VehicleInsuranceConstants:
    """ Constants for vehicle insurance rates based on the vehicle type. """

    LOW_RISK_1 = 0.0486
    LOW_RISK_2 = 0.0585
    MEDIUM_RISK = 0.0611
    HIGH_RISK = 0.0611
    PICK_UP = 0.0723
    CHINESE_INDIANS = 0.0531
    L8 = 0.0389
    OTHERS = 0.0884


class MortgageInsuranceConstants:
    """ Constants for mortgage insurance rates. """

    DEFAULT_VALUE = 0.00077


class DiscountRateConstants:
    """ COK (Costo de Oportunidad del Capital) used to discount loan cashflows for the VAN.

    Distinct from the loan's own TEA: estimated from a risk-free rate plus a country
    risk premium, per the BCP "Compra Inteligente" reference model.
    """

    COK_ANNUAL = 0.1325