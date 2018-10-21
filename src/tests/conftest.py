import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(scope='function')
def Notifier(wpilib):
    with patch('pidcontroller.Notifier', new=MagicMock()) as notifier:
        yield notifier
