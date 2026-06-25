class InsuranceAlgorithm:
    """
    This class implements the insurance algorithm for calculating the mortgage protection factor and vehicular insurance factor based on the provided parameters.

    Attributes:
        payment_frequency_in_days (int): The frequency of payments in days.
        mortgage_protection_monthly (float): The monthly amount for mortgage protection.
        vehicular_insurance_rate (float): The rate for vehicular insurance.
    """
    def __init__(self, payment_frequency_in_days: int, mortgage_protection_monthly: float, vehicular_insurance_rate: float):
        if payment_frequency_in_days <= 0:
            raise ValueError("Payment frequency in days must be greater than zero.")

        if mortgage_protection_monthly <= 0:
            raise ValueError("Mortgage protection amount must be greater than zero.")

        self.payment_frequency_in_days = payment_frequency_in_days
        self.mortgage_protection_monthly = mortgage_protection_monthly
        self.vehicular_insurance_rate = vehicular_insurance_rate

    def calculate_mortgage_protection_factor(self) -> float:
        """
        Calculate the mortgage protection factor based on the monthly mortgage protection amount and payment frequency.

        :return: The calculated mortgage protection factor.
        """
        # Convert monthly to annual amount
        tda = self.mortgage_protection_monthly * 12

        # Calculate the factor based on the payment frequency
        factor = (tda * self.payment_frequency_in_days) / 360

        # Return the factor
        return factor

    def calculate_vehicular_insurance_factor(self) -> float:
        """
        Calculate the vehicular insurance factor based on the vehicular insurance rate and payment frequency.

        :return: The calculated vehicular insurance factor.
        """
        # Calculate the factor based on the payment frequency
        factor = (self.vehicular_insurance_rate * self.payment_frequency_in_days) / 360

        # Return the factor
        return factor


class GracePeriodAlgorithm:
    """
    This class implements the algorithm to calculate the grace period for a loan based on the financed amount and the TEA (Effective Annual Rate).

    Attributes:
        financed_amount (float): The amount of money that has been financed.
        tem (float): The Monthly Effective Rate calculated from the TEA.
    """
    def __init__(self, financed_amount, tea):
        # Convert the TEA percentage to TEM (Monthly Effective Rate)
        factor = 1 + tea
        tem = (pow(factor, 12)) - 1

        self.financed_amount = financed_amount
        self.tem = tem

    def calculate_partial_grace_period_for_monthly_period(self) -> float:
        """
        Calculate the partial grace period for a monthly period.

        :return: The partial grace period for a monthly period.
        """
        # Calculate the partial grace period for the monthly period
        return self.financed_amount * self.tem

    def calculate_total_grace_period_amount(self, grace_period_in_months: int) -> float:
        """
        Calculate the total amount to be paid at the end of the grace period, including interest.

        :param grace_period_in_months: The duration of the grace period in months.
        :return: The new total value of the financed amount at the end of the grace period.
        """
        # Calculate the financed amount at the end of the grace period
        financed_amount_at_end_of_period = self.financed_amount * (pow(1 + self.tem, grace_period_in_months))

        # Return the financed amount at the end of the grace period
        return financed_amount_at_end_of_period


class FrenchMethodAlgorithm:
    def __init__(self, financed_amount: float, tea: float, total_number_of_periods: int):
        if financed_amount <= 0:
            raise ValueError("Financed amount must be greater than zero.")

        if tea < 0 or tea > 1:
            raise ValueError("TEA must be between 0 and 1.")

        if total_number_of_periods <= 0:
            raise ValueError("Total number of periods must be greater than zero.")

        self.financed_amount = financed_amount
        self.tea = tea
        self.total_number_of_periods = total_number_of_periods

    def calculate_period_fee(self) -> float:
        """
        Calculate the period fee using the French Method formula.

        :return: The calculated period fee.
        """
        # Calculate the period fee using the French Method formula
        period_fee = self.financed_amount * ((self.tea * pow(1 + self.tea, self.total_number_of_periods)) / (pow(1 + self.tea, self.total_number_of_periods) - 1))

        # Return the calculated period fee
        return period_fee

    def calculate_mortgage_protection_for_period(self, mortgage_factor: float) -> float:
        """
        Calculate the mortgage protection for a given period.

        :param mortgage_factor: The mortgage factor.
        :return: The calculated mortgage protection for the period.
        """
        mortgage_protection_for_period = mortgage_factor * self.financed_amount

        return mortgage_protection_for_period