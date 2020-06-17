import pywinusb.hid as hid
from .base import VENDOR_ID

from .gladiatork import GladiatorK

VKB_DEVICES = {0x0132: GladiatorK}


def find_all_vkb():
    devices = []
    for pid, cls in VKB_DEVICES.items():
        devices.extend(
            cls(_)
            for _ in hid.HidDeviceFilter(
                vendor_id=VENDOR_ID, product_id=pid
            ).get_devices()
        )
    return sorted(devices, key=lambda d: d.guid)
