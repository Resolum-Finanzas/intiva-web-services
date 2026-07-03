"""Domain enumerations for the Vehicles bounded context."""

from enum import Enum


class InsuranceType(str, Enum):
    LOW_RISK_1 = "LOW_RISK_1"
    LOW_RISK_2 = "LOW_RISK_2"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"
    PICK_UP = "PICK_UP"
    CHINESE_AND_INDIAN = "CHINESE_AND_INDIAN"
    L8 = "L8"
    OTHERS = "OTHERS"

    @property
    def annual_rate(self) -> float:
        _rates = {
            "LOW_RISK_1":        0.0486,
            "LOW_RISK_2":        0.0585,
            "MEDIUM_RISK":       0.0611,
            "HIGH_RISK":         0.0611,
            "PICK_UP":           0.0723,
            "CHINESE_AND_INDIAN":0.0531,
            "L8":                0.0389,
            "OTHERS":            0.0884,
        }
        return _rates[self.value]

    @property
    def display_name(self) -> str:
        """Human-readable Spanish label for API responses."""
        _labels = {
            "LOW_RISK_1":        "Bajo Riesgo 1",
            "LOW_RISK_2":        "Bajo Riesgo 2",
            "MEDIUM_RISK":       "Mediano Riesgo",
            "HIGH_RISK":         "Alto Riesgo",
            "PICK_UP":           "Pick Up",
            "CHINESE_AND_INDIAN":"Chinos e Indios",
            "L8":                "L8",
            "OTHERS":            "Otros",
        }
        return _labels[self.value]

    @classmethod
    def from_risk_category(cls, risk_category: str) -> "InsuranceType":
        """Map a car's Spanish risk_category label (seed data) to its InsuranceType.

        Falls back to OTHERS when the label doesn't match any known category.
        """
        for insurance_type in cls:
            if insurance_type.display_name == risk_category:
                return insurance_type
        return cls.OTHERS