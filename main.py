#!/bin/python3

"""
main.py
==================

Reads a date in the format DD/MM/YYYY from stdin and prints the weekday of that date.

Author: Urpagin
"""

from dataclasses import dataclass
from enum import Enum


def main() -> None:
    """Program entrypoint."""
    date: Date = read_user_date()
    weekday: Weekday = date_to_weekday(date)

    print(f"{date} is a {weekday_to_string(weekday)}.")


@dataclass
class Date:
    """Represents a safe date."""

    day: int
    month: int
    year: int

    def __init__(self, day: int, month: int, year: int) -> None:

        if day < 1 or day > 31:
            raise ValueError("Invalid day range")

        if month < 1 or month > 12:
            raise ValueError("Invalid month range")

        # Negative years not yet accounted for in the formula.
        if year < 1:
            raise ValueError("Invalid year range")

        self.day = day
        self.month = month
        self.year = year

    def __str__(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year:02d}"


def read_user_date() -> Date:
    """
    Parses a `Date` from stdin.
    """
    while True:
        usr_input: str = input("Enter the date (DD/MM/YYYY)\n-> ").strip()

        if not usr_input or len(usr_input.split("/")) != 3:
            print("Error: malformed date\n")
            continue

        splitted: list[str] = usr_input.split("/")

        try:
            day: int = int(splitted[0])
            month: int = int(splitted[1])
            year: int = int(splitted[2])

            date = Date(day, month, year)

        except ValueError:
            print("Error: malformed date\n")
            continue

        return date


class Weekday(Enum):
    """Represent a Weekday"""

    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


def weekday_to_string(weekday: Weekday) -> str:
    """Converts a Weekday enum member to its string representation."""

    return weekday.name.title()


def date_to_weekday(date: Date) -> Weekday:
    """
    Parses a `Date` into a `Weekday` using Zeller's congruence formula.

    Credit: https://en.wikipedia.org/wiki/Zeller%27s_congruence
    """

    d: int = date.day
    m: int = date.month

    year: int = date.year

    # Adjust month and year for January and February
    if m < 3:
        m += 12
        year -= 1

    # Number made of the two last digits of the year
    k: int = year % 100
    # Century
    j: int = year // 100

    # Zeller's congruence formula
    res = (d + (13 * (m + 1) // 5) + k + k // 4 + j // 4 - 2 * j) % 7

    # Adjust result for 0-based indexing (0 = Sunday, 6 = Saturday)
    res = (res + 6) % 7

    return Weekday(res)


if __name__ == "__main__":
    main()
