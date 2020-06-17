from nubia import command

from vkb.devices import find_all_vkb


@command("list")
def list_devices():
    """
    List all VKB USB devices
    """
    for i, dev in enumerate(find_all_vkb()):
        print(f" {i:>2}: {dev.name} ({dev.guid})")
