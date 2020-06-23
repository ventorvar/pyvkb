import sys
import typing

from .base import VKBDevice


if sys.platform.startswith("win"):
    from vkb.platform.win import find_all_vkb
else:
    raise NotImplementedError("This platform is not yet supported by pyvkb")


def vkb_device(index_or_guid: typing.Union[int, str]) -> typing.Optional[VKBDevice]:
    """ Returns a VKBDevice by it's `int` index or `str` GUID.

    :param index_or_guid: Either the `int` 1index of the device in the sorted VKB device list or a str of the GUID
                          or partial GUID to match. Match is done by startswith()
    :returns: :class:`VKBDevice` if is a device is matched otherwise None
    """
    try:
        return find_all_vkb()[int(index_or_guid)]
    except (ValueError, IndexError):
        return vkb_device_by_guid(index_or_guid)


def vkb_device_by_guid(guid: str) -> typing.Optional[VKBDevice]:
    """ Return the first device that matches the given full, or partial GUID

    :param guid: str of the GUID or partial GUID to match. Match is done by startswith()
    :returns: :class:`VKBDevice` if is a device is matched otherwise None
    """
    guid = guid.lower()
    for dev in find_all_vkb():
        if dev.guid.lower().startswith(guid):
            return dev
    return None
