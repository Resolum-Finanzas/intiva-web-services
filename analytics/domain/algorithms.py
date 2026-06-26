from datetime import datetime, timedelta


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


class FrenchMethodAlgorithm:
    """Implements the French method algorithm for calculating loan amortization schedules.

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
            grace_period_type: str, # NONE, PARTIAL, TOTAL
            grace_period_in_months: float = 1.0, # Only used if grace_period_type is PARTIAL or TOTAL
            period_type: str = "MONTHLY",  # MONTHLY, QUARTERLY, SEMI-ANNUALLY, ANNUALLY
    ):
        # Variables that will be calculated with the configuration
        self.periods_in_days: int = 0
        self.mortgage_protection_factor: float = 0.0
        self.financed_amount: float = 0.0
        self.balloon_payment_fee: float = 0.0
        self.number_of_periods: float = 0.0
        self.period_vehicular_insurance: float = 0.0
        self.period_effective_rate: float = 0.0
        self.constant_installment: float = 0.0

        self.partial_grace_period_payment_per_period: float = 0.0

        # Basic information needed to calculate the algorithm
        self.initial_payment_date = datetime.strptime(initial_payment_date, "%Y-%m-%d")
        self.balloon_payment_percentage = balloon_payment_percentage
        self.vehicle_cost = vehicle_cost
        self.vehicle_type = vehicle_type
        self.down_payment_percentage = down_payment_percentage
        self.tea = tea
        self.total_number_of_years = total_number_of_years
        self.period_type = period_type

        # Grace period information (optional)
        self.grace_period_type = grace_period_type
        self.grace_period_duration_by_period_type = grace_period_in_months

        self.calculate_number_of_periods()
        self.calculate_financed_amount()
        self.calculate_period_effective_rate()

        self.calculate_balloon_fee()
        self.calculate_period_vehicular_insurance()
        self.calculate_mortgage_protection_factor()

        if self.grace_period_type != "NONE":
            self.number_of_periods -= self.grace_period_duration_by_period_type

        self.calculate_constant_installment()

        # Lists for storing the results
        self.payment_dates = []
        self.current_balances_at_start = []
        self.current_balances_at_end = []
        self.payment_interest_amounts = []
        self.payment_amortization_amounts = []
        self.payment_mortgage_protection_values = []
        self.payment_vehicular_insurance_values = []
        self.total_payments_for_periods = []
        self.payment_dates = []

        self.grace_period_payment_amounts = [] # Can be 0 for a total grace period

    def calculate_number_of_periods(self) -> None:
        """ Calculate the number of periods based on the period type. """

        number_of_periods = 0

        match self.period_type:
            case "MONTHLY":
                number_of_periods = self.total_number_of_years * 12
                self.periods_in_days = 30
                self.grace_period_duration_by_period_type = self.grace_period_duration_by_period_type
            case "QUARTERLY":
                number_of_periods = self.total_number_of_years * 3
                self.periods_in_days = 120
                self.grace_period_duration_by_period_type = self.grace_period_duration_by_period_type / 4
            case "SEMI-ANNUALLY":
                number_of_periods = self.total_number_of_years * 2
                self.periods_in_days = 180
                self.grace_period_duration_by_period_type = self.grace_period_duration_by_period_type / 6
            case "ANNUALLY":
                number_of_periods = self.total_number_of_years
                self.periods_in_days = 360
                self.grace_period_duration_by_period_type = self.grace_period_duration_by_period_type / 12
            case _:
                raise ValueError("Invalid period type")

        if self.grace_period_type == "NONE":
            self.grace_period_duration_by_period_type = 0

        self.number_of_periods = number_of_periods

    def calculate_period_effective_rate(self) -> None:
        """ Calculate the effective rate for each period. """

        # Define a factor to calculate the effective rate
        factor = 1 + self.tea

        # Calculate the effective rate for the period
        period_effective_rate = (pow(factor, self.periods_in_days / 360)) - 1

        # Assign the effective rate to the instance variable
        self.period_effective_rate = period_effective_rate

    def calculate_period_vehicular_insurance(self) -> None:
        """ Calculate the annual vehicular insurance based on the vehicle type. """

        tua = 0

        match self.vehicle_type:
            case "LOW_RISK_1":
                tua = VehicleInsuranceConstants.LOW_RISK_1
            case "LOW_RISK_2":
                tua = VehicleInsuranceConstants.LOW_RISK_2
            case "MEDIUM_RISK":
                tua = VehicleInsuranceConstants.MEDIUM_RISK
            case "HIGH_RISK":
                tua = VehicleInsuranceConstants.HIGH_RISK
            case "PICK_UP":
                tua = VehicleInsuranceConstants.PICK_UP
            case "CHINESE_INDIANS":
                tua = VehicleInsuranceConstants.CHINESE_INDIANS
            case "L8":
                tua = VehicleInsuranceConstants.L8
            case "OTHERS":
                tua = VehicleInsuranceConstants.OTHERS

        # Depends on the period type (monthly, quarterly, semi-annually, annually)
        vehicular_insurance_factor = tua * (self.periods_in_days / 360)

        # Calculate the vehicular insurance for the period based on the vehicle type
        vehicular_insurance_for_period = self.vehicle_cost * vehicular_insurance_factor

        # Can be for monthly, quarterly, semi-annually, annually type of period
        self.period_vehicular_insurance = vehicular_insurance_for_period

    def calculate_mortgage_protection_factor(self) -> None:
        """ Calculate the mortgage protection factor based on the period type and assign it to the instance variable. """

        # Assigns the default mortgage protection factor
        mortgage_protection_monthly = MortgageInsuranceConstants.DEFAULT_VALUE

        # Calculates the mortgage protection annual percentage
        mortgage_protection_annual = mortgage_protection_monthly * 12

        # Calculates the mortgage protection factor based on the period type
        mortgage_protection_factor = (mortgage_protection_annual * self.periods_in_days) / 360

        # Returns the mortgage protection factor
        self.mortgage_protection_factor = mortgage_protection_factor

    def calculate_financed_amount(self) -> None:
        """ Calculate the financed amount based on the vehicle cost and down payment percentage. """

        if self.grace_period_type == "NONE":
            # Calculate the down payment based on the vehicle cost and down payment percentage
            down_payment = self.vehicle_cost * self.down_payment_percentage

            # Calculate the financed amount
            financed_amount = self.vehicle_cost - down_payment

            # Return the financed amount
            self.financed_amount = financed_amount

    def calculate_balloon_fee(self) -> None:
        """ Calculate the balloon fee based on the vehicle cost and balloon payment percentage. """

        # Calculate the balloon fee based on the vehicle cost and balloon payment percentage
        self.balloon_payment_fee = self.vehicle_cost * self.balloon_payment_percentage

    def calculate_constant_installment(self) -> None:
        """ Calculate the constant installment based on the financed amount, interest rate, and number of periods. """

        # Assign the financed amount, interest rate, and number of periods to variables
        financed_amount = self.financed_amount # P
        interest_rate = self.period_effective_rate # r
        number_of_periods = self.number_of_periods # n

        # Calculate the constant installment
        up = financed_amount * interest_rate
        down = 1 - pow(1 + interest_rate, -number_of_periods)
        constant_installment = up / down

        # Assign the constant installment to the instance variable
        self.constant_installment = constant_installment

    def calculate_period_mortgage_protection_value(self, current_balance: float, current_period: int) -> float:
        """ Calculate the mortgage protection value based on the financed amount and mortgage protection factor. """

        # Calculate the mortgage protection value based on the financed amount and mortgage protection factor
        if current_period == self.number_of_periods:
            mortgage_protection_value = self.financed_amount * self.mortgage_protection_factor
        else:
            mortgage_protection_value = current_balance * self.mortgage_protection_factor

        return mortgage_protection_value

    def calculate_interest_for_period(self, previous_period_current_balance: float, current_period: int) -> float:
        """ Calculate the interest for a period based on the effective rate and the previous period's current balance. """

        rate = self.period_effective_rate

        if current_period == self.number_of_periods:
            interest_for_period = self.financed_amount * rate
        else:
            interest_for_period = previous_period_current_balance * rate

        return interest_for_period

    def calculate_amortization_for_period(self, interest_for_period: float) -> float:
        """ Calculate the amortization for a period based on the constant installment and interest for the period. """

        # Calculate the amortization for the period
        amortization_for_period = self.constant_installment - interest_for_period

        # Return the amortization for the period
        return amortization_for_period

    @staticmethod
    def calculate_current_balance_for_period(previous_period_current_balance: float, amortization_for_period: float) -> float:
        """ Calculate the current balance for a period based on the previous period's current balance and amortization for the period. """

        # Calculate the current balance for the period
        current_balance_for_period = previous_period_current_balance - amortization_for_period

        # Return the current balance for the period
        return current_balance_for_period

    @staticmethod
    def calculate_amortized_capital_for_period(previous_period_amortized_capital: float, amortization_for_period: float) -> float:
        """ Calculate the amortized capital for a period based on the previous period's amortized capital and amortization for the period. """

        # Calculate the amortized capital for the period
        amortized_capital_for_period = previous_period_amortized_capital + amortization_for_period

        # Return the amortized capital for the period
        return amortized_capital_for_period

    def _append_payment(
            self,
            payment_date,
            current_balance_at_start,
            current_balance_at_end,
            interest,
            amortization,
            mortgage_protection,
            vehicular_insurance,
            total_payment,
    ) -> None:
        """ Append a payment to the payment schedule. """

        self.payment_dates.append(payment_date)
        self.current_balances_at_start.append(current_balance_at_start)
        self.current_balances_at_end.append(current_balance_at_end)
        self.payment_interest_amounts.append(interest)
        self.payment_amortization_amounts.append(amortization)
        self.payment_mortgage_protection_values.append(mortgage_protection)
        self.payment_vehicular_insurance_values.append(vehicular_insurance)
        self.total_payments_for_periods.append(total_payment)

    def perform(self) -> None:

        # Clear lists
        self.payment_dates.clear()
        self.current_balances_at_start.clear()
        self.current_balances_at_end.clear()
        self.payment_interest_amounts.clear()
        self.payment_amortization_amounts.clear()
        self.payment_mortgage_protection_values.clear()
        self.payment_vehicular_insurance_values.clear()
        self.total_payments_for_periods.clear()

        current_balance = self.financed_amount
        payment_date = self.initial_payment_date

        grace_periods = int(self.grace_period_duration_by_period_type)
        payment_periods = int(self.number_of_periods)

        ###########################################################################
        # GRACE PERIODS
        ###########################################################################

        for period in range(grace_periods):

            payment_date += timedelta(days=self.periods_in_days)

            balance_at_start = current_balance

            interest = self.calculate_interest_for_period(
                current_balance,
                period + 1
            )

            amortization = 0.0

            if self.grace_period_type == "PARTIAL":

                mortgage = self.calculate_period_mortgage_protection_value(
                    current_balance,
                    period + 1
                )

                vehicular = self.period_vehicular_insurance

                balance_at_end = current_balance

                total_payment = (
                        interest
                        + mortgage
                        + vehicular
                )

            else:  # TOTAL

                mortgage = 0.0
                vehicular = 0.0

                balance_at_end = current_balance + interest

                total_payment = 0.0

                current_balance = balance_at_end

            self._append_payment(
                payment_date=payment_date.strftime("%Y-%m-%d"),
                current_balance_at_start=balance_at_start,
                current_balance_at_end=balance_at_end,
                interest=interest,
                amortization=amortization,
                mortgage_protection=mortgage,
                vehicular_insurance=vehicular,
                total_payment=total_payment
            )

        ###########################################################################
        # FRENCH METHOD
        ###########################################################################

        for payment in range(payment_periods):

            payment_date += timedelta(days=self.periods_in_days)

            balance_at_start = current_balance

            interest = self.calculate_interest_for_period(
                current_balance,
                payment + 1
            )

            amortization = self.calculate_amortization_for_period(
                interest
            )

            balance_at_end = self.calculate_current_balance_for_period(
                current_balance,
                amortization
            )

            mortgage = self.calculate_period_mortgage_protection_value(
                current_balance,
                payment + 1
            )

            vehicular = self.period_vehicular_insurance

            total_payment = (
                    interest
                    + amortization
                    + mortgage
                    + vehicular
            )

            if payment == payment_periods - 1:
                total_payment += self.balloon_payment_fee

            self._append_payment(
                payment_date=payment_date.strftime("%Y-%m-%d"),
                current_balance_at_start=balance_at_start,
                current_balance_at_end=balance_at_end,
                interest=interest,
                amortization=amortization,
                mortgage_protection=mortgage,
                vehicular_insurance=vehicular,
                total_payment=total_payment
            )

            current_balance = balance_at_end