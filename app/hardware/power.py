import os
import sys
import time

picdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "pic",
)

libdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "lib",
)

if os.path.exists(libdir) and libdir not in sys.path:
    sys.path.insert(0, libdir)

from app.core.logger import Logger

logger = Logger("Power")


class PowerMonitor:
    """Simple wrapper around an INA219 module to expose a battery
    percentage. Uses a default single-cell Li-ion mapping (3.0V -> 0%,
    4.2V -> 100%). If the INA219 isn't available, reads return None.
    """

    def __init__(self, i2c_bus=1, addr=0x40, min_v=3.0, max_v=4.2, smoothing=0.2):
        self.ina = None
        self.min_v = min_v
        self.max_v = max_v
        self._smoothed = None
        self.alpha = smoothing

        try:
            from waveshare_epd.INA219 import INA219

            self.ina = INA219(i2c_bus=i2c_bus, addr=addr)
            logger.info("INA219 power monitor initialized")
        except Exception as e:
            logger.warning(f"Power monitor unavailable: {e}")

    def read_voltage(self):
        if not self.ina:
            return None
        try:
            v = self.ina.getBusVoltage_V()
            # apply simple smoothing
            if self._smoothed is None:
                self._smoothed = v
            else:
                self._smoothed = self.alpha * v + (1 - self.alpha) * self._smoothed
            return self._smoothed
        except Exception as e:
            logger.warning(f"Failed to read INA219: {e}")
            return None

    def get_percentage(self):
        v = self.read_voltage()
        if v is None:
            return None
        pct = (v - self.min_v) / (self.max_v - self.min_v) * 100.0
        if pct < 0:
            pct = 0.0
        if pct > 100:
            pct = 100.0
        return int(pct)
