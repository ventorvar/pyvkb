from nubia import command

from vkb.devices import find_all_vkb


@command("list")
def list_devices():
    """
    List all VKB USB devices
    """
    devs = find_all_vkb()
    if not devs:
        print("No VKB devices found")
        return

    for i, dev in enumerate(devs):
        print(f" {i:>2}: {dev.name} ({dev.guid})")
