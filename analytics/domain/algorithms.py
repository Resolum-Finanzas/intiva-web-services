from datetime import datetime, timedelta
from math import pow

from analytics.domain.constants import VehicleInsuranceConstants, MortgageInsuranceConstants


class FrenchMethodAlgorithm:

    def __init__(
        self,
        vehicle_cost: float,
        vehicle_type: str,
        down_payment_percentage: float,
        balloon_payment_percentage: float,
        tea: float,
        initial_payment_date: str,
        total_number_of_years: float,
        grace_period_type: str,
        grace_period_in_months: float = 1.0,
        period_type: str = "MONTHLY",
    ):
        if grace_period_type not in ["NONE", "PARTIAL", "TOTAL"]:
            raise ValueError("Invalid grace period type")

        self.vehicle_cost = vehicle_cost
        self.vehicle_type = vehicle_type
        self.down_payment_percentage = down_payment_percentage
        self.balloon_payment_percentage = balloon_payment_percentage
        self.tea = tea
        self.total_number_of_years = total_number_of_years
        self.period_type = period_type

        self.initial_payment_date = datetime.strptime(initial_payment_date, "%Y-%m-%d")

        self.grace_period_type = grace_period_type
        self.grace_period_in_months = grace_period_in_months

        self.periods_in_days = 0
        self.number_of_periods = 0
        self.grace_period_in_periods = 0

        self.financed_amount = 0.0
        self.balloon_payment_fee = 0.0
        self.period_effective_rate = 0.0
        self.period_vehicular_insurance = 0.0
        self.mortgage_protection_factor = 0.0
        self.constant_installment = 0.0

        self.payment_periods = []

        self._calculate_all()

    # -------------------------
    # CONFIG CALCULATIONS
    # -------------------------

    def _calculate_all(self):
        self._calculate_periods()
        self._calculate_financed_amount()
        self._calculate_effective_rate()
        self._calculate_balloon_fee()
        self._calculate_insurance()
        self._calculate_mortgage_factor()
        self._calculate_grace_periods()
        self._calculate_constant_installment()

    def _calculate_periods(self):
        match self.period_type:
            case "MONTHLY":
                self.number_of_periods = int(self.total_number_of_years * 12)
                self.periods_in_days = 30
            case "QUARTERLY":
                self.number_of_periods = int(self.total_number_of_years * 3)
                self.periods_in_days = 120
            case "SEMI-ANNUALLY":
                self.number_of_periods = int(self.total_number_of_years * 2)
                self.periods_in_days = 180
            case "ANNUALLY":
                self.number_of_periods = int(self.total_number_of_years)
                self.periods_in_days = 360
            case _:
                raise ValueError("Invalid period type")

    def _calculate_financed_amount(self):
        down = self.vehicle_cost * self.down_payment_percentage
        self.financed_amount = self.vehicle_cost - down

    def _calculate_effective_rate(self):
        self.period_effective_rate = (pow(1 + self.tea, self.periods_in_days / 360)) - 1

    def _calculate_balloon_fee(self):
        self.balloon_payment_fee = self.vehicle_cost * self.balloon_payment_percentage

    def _calculate_insurance(self):
        match self.vehicle_type:
            case "LOW_RISK_1":
                rate = VehicleInsuranceConstants.LOW_RISK_1
            case "LOW_RISK_2":
                rate = VehicleInsuranceConstants.LOW_RISK_2
            case "MEDIUM_RISK":
                rate = VehicleInsuranceConstants.MEDIUM_RISK
            case "HIGH_RISK":
                rate = VehicleInsuranceConstants.HIGH_RISK
            case "PICK_UP":
                rate = VehicleInsuranceConstants.PICK_UP
            case "CHINESE_INDIANS":
                rate = VehicleInsuranceConstants.CHINESE_INDIANS
            case "L8":
                rate = VehicleInsuranceConstants.L8
            case _:
                rate = VehicleInsuranceConstants.OTHERS

        self.period_vehicular_insurance = self.vehicle_cost * rate * (self.periods_in_days / 360)

    def _calculate_mortgage_factor(self):
        annual = MortgageInsuranceConstants.DEFAULT_VALUE * 12
        self.mortgage_protection_factor = annual * (self.periods_in_days / 360)

    def _calculate_grace_periods(self):
        if self.grace_period_type == "NONE":
            self.grace_period_in_periods = 0
        else:
            self.grace_period_in_periods = int(self.grace_period_in_months)

    def _calculate_constant_installment(self):
        n = self.number_of_periods
        r = self.period_effective_rate

        factor = (1 + r) ** n
        balloon_pv = self.balloon_payment_fee / factor

        base = self.financed_amount - balloon_pv

        self.constant_installment = base * (r * factor) / (factor - 1)

    # -------------------------
    # FINANCIAL FUNCTIONS
    # -------------------------

    def interest(self, balance):
        return balance * self.period_effective_rate

    def amortization(self, interest):
        return self.constant_installment - interest

    def mortgage(self, balance):
        return balance * self.mortgage_protection_factor

    # -------------------------
    # EXECUTION
    # -------------------------

    def perform(self):
        self.payment_periods.clear()

        balance = self.financed_amount
        date = self.initial_payment_date

        # ---------------- GRACE ----------------
        for _ in range(self.grace_period_in_periods):

            date += timedelta(days=self.periods_in_days)

            interest = self.interest(balance)

            if self.grace_period_type == "PARTIAL":
                mortgage = self.mortgage(balance)
                vehicular = self.period_vehicular_insurance
                total = interest + mortgage + vehicular
                amort = 0.0
                end = balance

            else:  # TOTAL
                mortgage = 0.0
                vehicular = 0.0
                amort = 0.0
                total = 0.0
                end = balance

            self.payment_periods.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "start": balance,
                    "end": end,
                    "interest": interest,
                    "amortization": amort,
                    "mortgage": mortgage,
                    "vehicular": vehicular,
                    "total": total,
                    "grace": True,
                }
            )

        # ---------------- FRENCH ----------------
        for i in range(self.number_of_periods):

            date += timedelta(days=self.periods_in_days)

            interest = self.interest(balance)
            amort = self.amortization(interest)

            if i == self.number_of_periods - 1:
                amort = balance

            end = balance - amort

            mortgage = self.mortgage(balance)
            vehicular = self.period_vehicular_insurance

            total = interest + amort + mortgage + vehicular

            self.payment_periods.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "start": balance,
                    "end": end,
                    "interest": interest,
                    "amortization": amort,
                    "mortgage": mortgage,
                    "vehicular": vehicular,
                    "total": total,
                    "grace": False,
                }
            )

            balance = end