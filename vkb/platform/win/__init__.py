import sys
import pywinusb.hid as hid

from vkb.contrib import dinput
from vkb.devices.defs import VKB_DEVICES, VENDOR_ID


def find_all_vkb():
    """ Returns all VKB devices connected to the system sorted by GUID """
    # we're using the DirectInput GUIDs as the GUID on windows
    dinput_devices = {}
    for _ in dinput.get_devices():
        try:
            dinput_devices[
                _.get_property(
                    dinput.DIPROP_GUIDANDPATH, dinput.DIPROPGUIDANDPATH
                ).wszPath
            ] = _
        except OSError:
            pass
    devices = []
    for hiddev in hid.HidDeviceFilter(vendor_id=VENDOR_ID).get_devices():
        devcls = VKB_DEVICES.get(hiddev.product_id)
        if devcls is not None:
            if hiddev.device_path in dinput_devices:
                devices.append(
                    devcls(
                        hiddev,
                        guid=dinput.guid_to_str(
                            dinput_devices[hiddev.device_path].guid
                        ),
                    )
                )
            else:
                sys.stderr.write(
                    f"WARNING: Could not determine DirectInput GUID for device {hiddev.device_path}\n"
                )
                devices.append(devcls(hiddev, guid=""))
    return sorted(devices, key=lambda d: d.guid)
