import pytest

from analytics.domain.algorithms import FrenchMethodAlgorithm


class TestEffectiveRate:
    def test_constant_installment_is_correct_according_to_example(self):
        # Arrange
        constant_installment = 484.76596436935637

        vehicle_cost = 28500.00
        vehicle_type = "MEDIUM_RISK"
        down_payment_percentage = 0.25
        balloon_payment_percentage = 0.35
        tea = 0.1320
        initial_payment_date = "2024-01-01"
        total_number_of_years = 3
        grace_period_type = "NONE"
        grace_period_in_months = 6

        # Act
        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=vehicle_cost,
            vehicle_type=vehicle_type,
            down_payment_percentage=down_payment_percentage,
            balloon_payment_percentage=balloon_payment_percentage,
            tea=tea,
            initial_payment_date=initial_payment_date,
            total_number_of_years=total_number_of_years,
            grace_period_type=grace_period_type,
            grace_period_in_months=grace_period_in_months
        )

        algorithm.perform()

        # Assert
        print()
        print(algorithm.total_payments_for_periods)
        print()
        print(algorithm.payment_vehicular_insurance_values)
        print()
        print(algorithm.payment_mortgage_protection_values)
        assert algorithm.constant_installment == pytest.approx(constant_installment)
