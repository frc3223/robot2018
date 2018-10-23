import pytest
from drivecontroller import DriveController


@pytest.mark.parametrize("v, a, V, expected", [
    (0, 0, 0, 0),
    (100, 0, 0, 0),
    (0, 100, 0, 0),
    (100, 0, 12.7, 0.213),
    (1, 100, 12.7, 0.149),
    (-100, 0, 12.7, -0.213),
])
def test_calculateFeedForward(Notifier, v, a, V, expected):
    c = DriveController(Kp=0, Kd=0, 
            Ks=1.293985, Kv=0.014172, Ka=0.005938,
            get_voltage=lambda: V,
            source=lambda: v,
            output=lambda: None)

    c.setSetpoint(v)
    c.setAccelerationSetpoint(a)
    
    result = c.calculateFeedForward()
    assert result == pytest.approx(expected, 0.01)
