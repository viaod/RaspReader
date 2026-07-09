import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from encoder import Encoder

encoder = Encoder()
encoder.initialise()

while True:
    encoder.update()
    time.sleep(0.05)
