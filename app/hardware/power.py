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

        # Try several possible import paths for the INA219 class
        ina_cls = None
        import importlib
        for imp_path in ("waveshare_epd.INA219", "lib.waveshare_epd.INA219", "lib.INA219", "INA219"):
            try:
                mod = importlib.import_module(imp_path)
                ina_cls = getattr(mod, "INA219", None)
                if ina_cls:
                    break
            except Exception:
                continue

        if ina_cls is None:
            logger.warning("Power monitor unavailable: INA219 module not found (check lib path)")
            return

        # Try to instantiate INA219 at the given address; if it fails with
        # an I/O error, attempt common alternate addresses before giving up.
        candidate_addrs = [addr]
        for a in (0x40, 0x41, 0x43, 0x44, 0x45):
            if a not in candidate_addrs:
                candidate_addrs.append(a)

        last_exc = None
        for a in candidate_addrs:
            try:
                self.ina = ina_cls(i2c_bus=i2c_bus, addr=a)
                logger.info(f"INA219 power monitor initialized at address 0x{a:02x}")
                break
            except OSError as e:
                # Common on missing device; keep trying other addresses
                last_exc = e
                continue
            except Exception as e:
                last_exc = e
                break

        if self.ina is None:
            # Provide actionable diagnostic advice when I/O errors occur
            if isinstance(last_exc, OSError):
                logger.warning(
                    "Power monitor unavailable: I/O error when probing INA219. "
                    "Check I2C wiring, enable I2C in raspi-config, and run 'sudo i2cdetect -y 1' to see the device address."
                )
            else:
                logger.warning(f"Power monitor unavailable: {last_exc}")

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
