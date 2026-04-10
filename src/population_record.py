"""Проста модель одного запису: країна, рік, населення."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CountryPopulationRecord:
    """Зберігає дані про населення країни за конкретний рік."""

    country: str
    year: int
    population: int

    def __post_init__(self) -> None:
        if not self.country or not self.country.strip():
            raise ValueError("Country name cannot be empty.")

        if self.year < 0:
            raise ValueError("Year must be non-negative.")
        if self.population < 0:
            raise ValueError("Population must be non-negative.")
