from dataclasses import dataclass


@dataclass(slots=True)
class CsvExchangeReport:
    sell: bytes
    buy: bytes
