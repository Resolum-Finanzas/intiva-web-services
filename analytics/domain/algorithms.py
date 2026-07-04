from datetime import datetime, timedelta
from math import pow

from analytics.domain.constants import VehicleInsuranceConstants, MortgageInsuranceConstants, DiscountRateConstants


class FrenchMethodAlgorithm:
    """French method algorithm for calculating loan amortization schedules.

    This class provides methods to calculate the financed amount, number of periods, effective rate, balloon fee, period vehicular insurance, mortgage protection factor, constant installment, and period mortgage protection value.
    """

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

        self.net_flows = []

        self.irr = 0.0 # TIR
        self.tcea = 0.0 # TCEA
        self.npv = 0.0 # VAN

        self._calculate_all()

    def _calculate_all(self):
        """ Calculate all the values that are needed for the algorithm. """

        self._calculate_periods()
        self._calculate_financed_amount()
        self._calculate_effective_rate()
        self._calculate_balloon_fee()
        self._calculate_insurance()
        self._calculate_mortgage_factor()
        self._calculate_grace_periods()
        self._calculate_constant_installment()

    def _calculate_periods(self):
        """ Calculate the number of periods and the periods in days based on the period type. """

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
        """ Calculate the financed amount based on the vehicle cost and down payment percentage. """

        down = self.vehicle_cost * self.down_payment_percentage
        self.financed_amount = self.vehicle_cost - down

    def _calculate_effective_rate(self):
        """ Calculate the effective rate based on the TEA and the number of periods in days. """

        self.period_effective_rate = (pow(1 + self.tea, self.periods_in_days / 360)) - 1

    def _calculate_balloon_fee(self):
        """ Calculate the balloon fee based on the vehicle cost and balloon payment percentage. """

        self.balloon_payment_fee = self.vehicle_cost * self.balloon_payment_percentage

    def _calculate_insurance(self):
        """ Calculate the period vehicular insurance based on the vehicle type and the number of periods in days. """

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
        """ Calculate the mortgage protection factor based on the number of periods by the number of days. """

        annual = MortgageInsuranceConstants.DEFAULT_VALUE * 12
        self.mortgage_protection_factor = annual * (self.periods_in_days / 360)

    def _calculate_grace_periods(self):
        """ Calculate the number of grace periods based on the grace period type and grace period in months. """

        if self.grace_period_type == "NONE":
            self.grace_period_in_periods = 0
        else:
            self.grace_period_in_periods = int(self.grace_period_in_months)

    def _calculate_constant_installment(self):
        """ Calculate the constant installment based on the financed amount, effective rate, balloon fee, and number of periods.

        The grace periods are part of number_of_periods (the total term), not extra
        periods on top of it, so the installment is spread over the remaining periods.
        """

        n = self.number_of_periods - self.grace_period_in_periods
        r = self.period_effective_rate

        factor = (1 + r) ** n
        balloon_pv = self.balloon_payment_fee / factor

        base = self.financed_amount - balloon_pv

        self.constant_installment = base * (r * factor) / (factor - 1)

    # -------------------------
    # FINANCIAL FUNCTIONS
    # -------------------------

    def interest(self, balance):
        """ Calculate the interest for a period. """

        return balance * self.period_effective_rate

    def amortization(self, interest):
        """ Calculate the amortization for a period. """

        return self.constant_installment - interest

    def mortgage(self):
        """ Calculate the mortgage insurance for a period.

        Charged on the original financed amount (like the vehicular insurance),
        not on the declining balance, so it stays constant across periods.
        """

        return self.financed_amount * self.mortgage_protection_factor

    # -------------------------
    # FINANCIAL INDICATORS
    # -------------------------

    def _build_cashflows(self):
        """Build the cashflows for the periods.

        t=0 -> + financed amount
        t>0 -> - payments
        """

        self.net_flows = [self.financed_amount]

        self.net_flows.extend(
            payment["net_flow"]
            for payment in self.payment_periods
        )

    def _calculate_irr(self, tolerance=1e-10, max_iterations=100):
        """ Calculate the Internal Rate of Return (IRR) using Newton's method. """

        cashflows = self.net_flows
        guess = self.period_effective_rate
        rate = guess

        for _ in range(max_iterations):
            npv = 0.0
            derivative = 0.0

            for t, cf in enumerate(cashflows):
                npv += cf / ((1 + rate) ** t)
                if t > 0:
                    derivative -= (
                            t * cf /
                            ((1 + rate) ** (t + 1))
                    )

            if abs(npv) < tolerance:
                self.irr = rate
                return

            if abs(derivative) < tolerance:
                break

            rate -= npv / derivative

        self.irr = rate

    def _calculate_tcea(self):
        """ Calculate the Effective Annual Cost Rate (TCEA or EACR) using the IRR."""

        self.tcea = (
            (1 + self.irr)
            ** (360 / self.periods_in_days)
        ) - 1

    def _calculate_npv(self):
        """ Calculate the Net Present Value (NPV) discounting the cashflows at the COK. """

        period_cok = (pow(1 + DiscountRateConstants.COK_ANNUAL, self.periods_in_days / 360)) - 1

        self.npv = sum(
            cf / ((1 + period_cok) ** t)
            for t, cf in enumerate(self.net_flows)
        )

    # -------------------------
    # EXECUTION
    # -------------------------

    def perform(self):
        """Perform the French method algorithm and calculate the payment periods."""

        self.payment_periods.clear()

        balance = self.financed_amount
        date = self.initial_payment_date
        period = 1

        # ---------------- GRACE ----------------

        for _ in range(self.grace_period_in_periods):

            date += timedelta(days=self.periods_in_days)

            interest = self.interest(balance)

            if self.grace_period_type == "PARTIAL":

                mortgage = self.mortgage()
                vehicular = self.period_vehicular_insurance

                amort = 0.0
                balloon_fee = 0.0
                french_installment = interest

                total = interest + mortgage + vehicular + balloon_fee
                end = balance
                grace_type = "PARTIAL"

            else:  # TOTAL

                mortgage = 0.0
                vehicular = 0.0

                amort = 0.0
                balloon_fee = 0.0
                french_installment = 0.0

                total = 0.0
                end = balance + interest  # unpaid interest capitalizes into the balance
                grace_type = "TOTAL"

            net_flow = -total

            self.payment_periods.append(
                {
                    "period": period,
                    "date": date.strftime("%Y-%m-%d"),
                    "start": balance,
                    "end": end,
                    "interest": interest,
                    "amortization": amort,
                    "french_installment": french_installment,
                    "mortgage": mortgage,
                    "vehicular": vehicular,
                    "balloon_fee": balloon_fee,
                    "total": total,
                    "net_flow": net_flow,
                    "grace": grace_type,
                }
            )

            balance = end
            period += 1

        # ---------------- FRENCH ----------------

        number_of_french_periods = self.number_of_periods - self.grace_period_in_periods

        for i in range(number_of_french_periods):

            date += timedelta(days=self.periods_in_days)

            interest = self.interest(balance)
            amort = self.amortization(interest)

            balloon_fee = 0.0

            # Último período
            if i == number_of_french_periods - 1:

                amort = balance - self.balloon_payment_fee
                balloon_fee = self.balloon_payment_fee
                end = 0.0

            else:

                end = balance - amort

            french_installment = interest + amort
            mortgage = self.mortgage()
            vehicular = self.period_vehicular_insurance

            total = (
                    interest
                    + amort
                    + mortgage
                    + vehicular
                    + balloon_fee
            )

            net_flow = -total

            self.payment_periods.append(
                {
                    "period": period,
                    "date": date.strftime("%Y-%m-%d"),
                    "start": balance,
                    "end": end,
                    "interest": interest,
                    "amortization": amort,
                    "french_installment": french_installment,
                    "mortgage": mortgage,
                    "vehicular": vehicular,
                    "balloon_fee": balloon_fee,
                    "total": total,
                    "net_flow": net_flow,
                    "grace": "NONE",
                }
            )

            balance = end
            period += 1

        # ---------------- FINANCIAL INDICATORS ----------------

        self._build_cashflows()
        self._calculate_irr()
        self._calculate_tcea()
        self._calculate_npv()