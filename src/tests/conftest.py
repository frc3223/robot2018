import pytest
from unittest.mock import MagicMock, patch
import hal
import hal_impl
from hal_impl.sim_hooks import SimHooks as BaseSimHooks


@pytest.fixture(scope='function')
def Notifier(wpilib):
    with patch('pidcontroller.Notifier', new=MagicMock()) as notifier:
        yield notifier


class SimHooks(BaseSimHooks):
    def __init__(self):
        super().__init__()
        self.time = 0.0

    def getTime(self):
        return self.time


@pytest.fixture(scope='function')
def sim_hooks():
    with patch('hal_impl.functions.hooks', new=SimHooks()) as hooks:
        hal_impl.functions.reset_hal()
        yield hooks
