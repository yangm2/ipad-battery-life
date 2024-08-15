from typing import Any, Dict
from ..ipados_batteryhealth import ipados_batteryhealth as sut
import pytest # type: ignore[import-not-found]

def test_example() -> None:
    assert True

def test_div0() -> None:
    tmp: Dict[str, Any] = {
        "last_value_MaximumCapacityPercent": 999.9,
        "last_value_MaximumFCC": 0,
        "last_value_NominalChargeCapacity": 0,
    }

    cvh = sut.BatteryConfigValueHistogramFinal_V1(**tmp)
    
    with pytest.raises(ZeroDivisionError):
        assert cvh.calc() != 0
