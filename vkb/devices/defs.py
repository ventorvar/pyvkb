from .base import VENDOR_ID
from .gladiatork import GladiatorK, GladiatorKLH

VKB_DEVICES = {0x0132: GladiatorK, 0x0133: GladiatorKLH}
