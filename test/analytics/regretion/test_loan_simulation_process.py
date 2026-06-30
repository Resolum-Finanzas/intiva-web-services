import pytest

from analytics.domain.algorithms import FrenchMethodAlgorithm


class TestLoanSimulationProcess:

    def test_final_balance_must_be_zero(self):
        expected = 0.0

        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=28500.00,
            vehicle_type="MEDIUM_RISK",
            down_payment_percentage=0.25,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="NONE",
            grace_period_in_months=6
        )

        algorithm.perform()

        schedule = algorithm.payment_periods

        # último periodo
        assert schedule[-1]["end"] == pytest.approx(expected)

    def test_partial_grace_period_must_calculate_only_interests(self):
        vehicle_cost = 28500.00
        down_payment_percentage = 0.25

        expected = vehicle_cost * (1 - down_payment_percentage)

        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=vehicle_cost,
            vehicle_type="MEDIUM_RISK",
            down_payment_percentage=down_payment_percentage,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="PARTIAL",
            grace_period_in_months=6
        )

        algorithm.perform()

        schedule = algorithm.payment_periods

        first_grace_period = next(p for p in schedule if p["grace"] is "PARTIAL")

        assert first_grace_period["start"] == pytest.approx(expected)
        assert first_grace_period["end"] == pytest.approx(expected)
        assert first_grace_period["amortization"] == 0.0

    def test_total_grace_period_must_not_calculate_anything(self):
        vehicle_cost = 28500.00
        down_payment_percentage = 0.25

        expected = vehicle_cost * (1 - down_payment_percentage)

        algorithm = FrenchMethodAlgorithm(
            vehicle_cost=vehicle_cost,
            vehicle_type="MEDIUM_RISK",
            down_payment_percentage=down_payment_percentage,
            balloon_payment_percentage=0.35,
            tea=0.1320,
            initial_payment_date="2024-01-01",
            total_number_of_years=3,
            grace_period_type="TOTAL",
            grace_period_in_months=6
        )

        algorithm.perform()

        schedule = algorithm.payment_periods

        first = schedule[0]

        assert first["start"] == pytest.approx(expected)

        assert first["amortization"] == 0.0
        assert first["total"] == 0.0