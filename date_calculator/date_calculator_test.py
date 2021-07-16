import pytest
import datetime
from date_calculator.date_calculator import calculate_days


class TestDateCalculator:

    def _calculate_days_verifier(self, date_range: str):
        d1_str, d2_str = date_range.split("-")
        date_format = "%d/%m/%Y"
        d1 = datetime.datetime.strptime(d1_str.strip(), date_format)
        d2 = datetime.datetime.strptime(d2_str.strip(), date_format)
        return max(abs((d2 - d1).days) - 1, 0)

    @pytest.mark.parametrize(
        "date_range",
        [
            "03/08/2018 - 04/08/2018",
            "01/01/2000 - 03/01/2000",
            "01/01/2000 - 01/01/2000",
            "02/06/1983 - 22/06/1983",
            "04/07/2018 - 25/12/2018",
            "03/01/1989 - 03/08/1983",
            "01/01/1901 - 31/12/2999"
        ]
    )
    def test_calculate_dates(self, date_range: str):
        assert (
            calculate_days(date_range) ==
            self._calculate_days_verifier(date_range)
        )
