from __future__ import annotations
from typing import DefaultDict
import click


class Date:

    DAYS_IN_MONTH = [
        31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ]

    def __init__(self, day: int, month: int, year: int) -> None:
        self._d = day
        self._m = month
        self._y = year

    def _count_leap_years(self) -> int:
        """ Count number of leap years since big bang (0) to current date """
        cur_year = self._y
        if self._m <= 2:
            # Don't count current year as leap year,
            # as leap year only effects number of days in Feb
            cur_year -= 1
        return (
            cur_year // 4
            - cur_year // 100   # Some years divisible for 100 but not leap year, e.g 2100
            + cur_year // 400   # Add back years divisible by 100 but also leap year, e.g 2000
        )

    @property
    def days(self) -> int:
        """ Return number of days between big bang (0) till current date """
        num_days = 365 * self._y + self._d
        for i in range(self._m - 1):
            num_days += self.DAYS_IN_MONTH[i]
        # Add extra day for each leap year
        num_days += self._count_leap_years()
        return num_days


class DateParser:

    @classmethod
    def parse(cls, date_str: str) -> Date:
        """ Input must be in DD/MM/YYYY format, and represent a valid date """
        # TODO: can add validation to make sure input in right format!
        d, m, y = map(int, date_str.split('/'))
        return Date(d, m, y)


def _parse_date_range(date_range: str):
    """ Assume the input date range is in dd/MM/YYYY - dd/MM/YYYY format """
    start_date_str, end_date_str = date_range.split("-")
    return DateParser.parse(start_date_str.strip()), DateParser.parse(end_date_str.strip())


def calculate_days(date_range: str) -> int:
    """ Return number of fulls between start and end date, exclude start and end date """
    start_date, end_date = _parse_date_range(date_range)
    # Need to cater for case where stat and end date are the same, just return 0
    return max(abs(end_date.days - start_date.days) - 1, 0)


@click.command()
@click.option(
    "--input-file", default=None,
    help="Input file which contain date range on each line with format dd/MM/YYYY - dd/MM/YYYY"
)
@click.option(
    "--date-range", default=None,
    help="Specific date range with format dd/MM/YYYY - dd/MM/YYYY"
)
def main(input_file, date_range):
    if input_file and date_range:
        raise Exception("Please choose one option only!")
    if input_file:
        with open(input_file, "r", encoding="utf-8") as input_fobj:
            for line in input_fobj:
                days = calculate_days(line)
                print("%s = %d" % (line.strip(), days))
        return
    elif not date_range:
        # Iteractive mode
        print("Please enter the date range (with format dd/MM/YYYY - dd/MM/YYYY):")
        date_range = input()
    days = calculate_days(date_range)
    print("%s = %d" % (date_range, days))

if __name__ == "__main__":
    main()
