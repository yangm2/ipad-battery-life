#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any
import pathlib
import pprint
import re


@dataclass(frozen=False)
class BatteryConfigValueHistogramFinal_V1:
    last_value_MaximumCapacityPercent: float
    last_value_MaximumFCC: int  # mAh capacity when new
    last_value_NominalChargeCapacity: int  # mAh capcity when data acquired

    def __init__(self, kwargs: Dict[str, Any]) -> None:
        if "last_value_MaximumCapacityPercent" in kwargs.keys():
            self.last_value_MaximumCapacityPercent = kwargs[
                "last_value_MaximumCapacityPercent"
            ]
        if "last_value_MaximumFCC" in kwargs.keys():
            self.last_value_MaximumFCC = kwargs["last_value_MaximumFCC"]
        if "last_value_NominalChargeCapacity" in kwargs.keys():
            self.last_value_NominalChargeCapacity = kwargs[
                "last_value_NominalChargeCapacity"
            ]

    def calc(self) -> float:
        return self.last_value_NominalChargeCapacity / self.last_value_MaximumFCC

    def __repr__(self) -> str:
        return (
            f"reported capacity: {self.last_value_MaximumCapacityPercent}%\n"
            f"calculated capacity: {round(self.calc() * 100, 2)}%"
        )


@dataclass(frozen=False)
class Item:
    name: Optional[str] = None
    message: Optional[BatteryConfigValueHistogramFinal_V1] = None

    # pattern for constructing dataclass with subset of data from sloppy invocation
    def __init__(self, kwargs: Dict[str, Any]) -> None:
        battery_config_re = re.compile(r"BatteryConfigValueHistogramFinal_V\d+")

        if "name" in kwargs.keys():
            self.name = kwargs["name"]

            if self.name is None:
                raise ValueError

            if battery_config_re.match(self.name):
                self.message = BatteryConfigValueHistogramFinal_V1(**kwargs["message"])


def main() -> None:
    parser = argparse.ArgumentParser(
        None,
        description="parse iPad Analytics and print battery health",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "analytics_filepaths",
        type=(lambda p: pathlib.Path(p).resolve(strict=True)),
        nargs="+",
        help="iPad Analytics input file(s)",
    )

    args = parser.parse_args()

    for file in args.analytics_filepaths:
        print(file)

        with pathlib.Path(file).open(mode="r") as log:
            for line in log:
                j = json.loads(line)
                i = Item(**j)

                if i.message is not None:
                    pprint.pp(i.message)


if __name__ == "__main__":
    main()
