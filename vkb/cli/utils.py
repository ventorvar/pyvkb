from vkb.devices import find_all_vkb, vkb_device


def resolve_devices(devices):
    vkb_devs = [] if devices else enumerate(find_all_vkb())
    if devices:
        for dev_id in devices:
            dev = vkb_device(dev_id)
            if dev is None:
                raise ValueError(f"Invalid device ID: {dev_id}")
            vkb_devs.append((dev_id, dev))
    return vkb_devs
