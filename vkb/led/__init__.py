import os
import struct
from enum import IntEnum, auto
from textwrap import wrap

import bitstruct as bs
from pywinusb.hid import HidDevice

LED_CONFIG_COUNT = 12
LED_REPORT_ID = 0x59
LED_REPORT_LEN = 129
LED_SET_OP_CODE = bytes.fromhex("59a50a")


class ColorMode(IntEnum):
    COLOR1 = 0
    COLOR2 = auto()
    COLOR1_d_2 = auto()
    COLOR2_d_1 = auto()
    COLOR1_p_2 = auto()


class LEDMode(IntEnum):
    OFF = 0
    CONSTANT = auto()
    SLOW_BLINK = auto()
    FAST_BLINK = auto()
    ULTRA_BLINK = auto()


class LEDConfig:
    """
    An configuration for an LED in a VKB device.

    Setting the LEDs consists of a possible 30 LED configs each of which is a 4 byte structure as follows:

    byte 0:  LED ID
    bytes 2-4: a 24 bit color config as follows::

        000 001 010 011 100 101 110 111
        clm lem  b2  g2  r2  b1  g1  r1

    color mode (clm):
        0 - color1
        1 - color2
        2 - color1/2
        3 - color2/1
        4 - color1+2

    led mode (lem):
        0 - off
        1 - constant
        2 - slow blink
        3 - fast blink
        4 - ultra fast

    Colors:
        VKB uses a simple RGB color configuration for all LEDs. Non-rgb LEDs will not light if you set their primary
        color to 0 in the color config. The LEDs have a very reduced color range due to VKB using 0-7 to determine the
        brightness of R, G, and B. `LEDConfig` takes in a standard hex color code and converts it into this smaller
        range, so color reproduction will not be accurate.

    Bytes:
        Convert the LEDConfig to an appropriate binary representation by using `bytes`::

        >>> led1 = LEDConfig(led=1, led_mode=LEDMode.CONSTANT)
        >>> bytes(led1)
        b'\\x01\\x07p\\x04'


    :param led: `int` ID of the LED to control
    :param color_mode: `int` color mode, see :class:`ColorMode`
    :param led_mode: `int` LED mode, see :class:`LEDMode`
    :param color1: `str` hex color code for use as `color1`
    :param color2: `str` hex color code for use as `color2`
    """

    def __init__(
        self,
        led: int,
        color_mode: int = 0,
        led_mode: int = 0,
        color1: str = None,
        color2: str = None,
    ):
        self.led = int(led)
        self.color_mode = ColorMode(color_mode)
        self.led_mode = LEDMode(led_mode)
        self.color1 = color1 or "#000"
        self.color2 = color2 or "#000"

    def __repr__(self):
        return (
            f"<LEDConfig {self.led} clm:{ColorMode(self.color_mode).name} lem:{LEDMode(self.led_mode).name} "
            f"color1:{self.color1} color2:{self.color2}>"
        )

    def __bytes__(self):
        return struct.pack(">B", self.led) + bs.byteswap(
            "3",
            bs.pack(
                "u3" * 8,
                self.color_mode,
                self.led_mode,
                *(hex_color_to_vkb_color(self.color2)[::-1]),
                *(hex_color_to_vkb_color(self.color1)[::-1]),
            ),
        )

    @classmethod
    def frombytes(cls, buf):
        """ Creates an :class:`LEDConfig` from a bytes object """
        assert len(buf) == 4
        led_id = int(buf[0])
        buf = bs.byteswap("3", buf[1:])
        clm, lem, b2, g2, r2, b1, g1, r1 = bs.unpack("u3" * 8, buf)
        return cls(
            led=led_id,
            color_mode=clm,
            led_mode=lem,
            color1=vkb_color_to_hex_color([r1, g1, b1]),
            color2=vkb_color_to_hex_color([r2, g2, b2]),
        )


def get_led_configs(dev: HidDevice):
    """
    Returns a list of :class:`LEDConfig`s that have currently been set on the given `dev` :class:`HidDevice`.

    .. warning::
        This will only return LED configs that have been set into the device. Either with this library or with the
        test LED tool in VKBDevCfg. LED profiles that are configured normally are not retrieved in this manor and not
        configured the same way.
    """
    led_report = [
        _ for _ in dev.find_feature_reports() if _.report_id == LED_REPORT_ID
    ][0]
    data = bytes(led_report.get(False))
    assert len(data) >= 8
    if data[:3] != LED_SET_OP_CODE:
        return (
            []
        )  # it wont be returned until something is set, so default to showing no configs
    num_led_configs = int(data[7])
    data = data[8:]
    leds = []
    while num_led_configs > 0:
        leds.append(LEDConfig.frombytes(data[:4]))
        data = data[4:]
        num_led_configs -= 1
    return leds


def _led_conf_checksum(num_configs, buf):
    """
    It's better not to ask too many questions about this. Why didn't they just use a CRC?
    Why do we only check (num_configs+1)*3 bytes instead of the whole buffer?
    We may never know...  it works...
    """

    def conf_checksum_bit(chk, b):
        chk ^= b
        for i in range(8):
            _ = chk & 1
            chk >>= 1
            if _ != 0:
                chk ^= 0xA001
        return chk

    chk = 0xFFFF
    for i in range((num_configs + 1) * 3):
        chk = conf_checksum_bit(chk, buf[i])
    return struct.pack("<H", chk)


def set_leds(dev: HidDevice, led_configs: [LEDConfig]):
    f"""
    Set the :class:`LEDConfig`s to a `dev` HidDevice.

    A maximum of {LED_CONFIG_COUNT} configs can be set at once.

    .. warning::
        This will overwrite the state for each given LED until the device is turned off/on again. Only the specified
        LEDs are affected, and all other LEDs will continue to behave as configured in the device profile.

    :param dev: :class:`usb.core.HidDevice` for a connected VKB device
    :param led_configs: List of :class:`LEDConfigs` to set.
    """
    if len(led_configs) > LED_CONFIG_COUNT:
        raise ValueError(f"Can only set a maximum of {LED_CONFIG_COUNT} LED configs")

    num_configs = len(led_configs)
    led_configs = b"".join(bytes(_) for _ in led_configs)
    led_configs = os.urandom(2) + struct.pack(">B", num_configs) + led_configs
    chksum = _led_conf_checksum(num_configs, led_configs)
    cmd = LED_SET_OP_CODE + chksum + led_configs
    cmd = cmd + b"\x00" * (LED_REPORT_LEN - len(cmd))
    led_report = [
        _ for _ in dev.find_feature_reports() if _.report_id == LED_REPORT_ID
    ][0]
    led_report.send(cmd)


def hex_color_to_vkb_color(hex_code: str) -> [int]:
    """ Takes a hex formatted color and converts it to VKB color format.

        >>> hex_color_to_led("#FF3300")
        [7, 1, 0]

    :param hex_code: Hex color code string to be converted to a VKB color code
    :return: List of integers in a VKB LED color code format, `[R, G, B]`
    """
    hex_code = hex_code.lstrip("#")
    if len(hex_code) != 3 and len(hex_code) != 6:
        return ValueError("Invalid hex color code")
    hex_code = [_ + _ for _ in hex_code] if len(hex_code) == 3 else wrap(hex_code, 2)
    # VKB uses a 7 as the max brightness and 0 as off - so convert the 255 range to this
    hex_code = [round(min(int(_, 16), 255) / 255.0 * 7) for _ in hex_code]
    return hex_code


def vkb_color_to_hex_color(vkb_color_code: [int]) -> str:
    """ Takes a VKB color code `[R, G, B]` and converts it into a hex code string"""
    return f'#{"".join("%02x" % round((min(int(i), 7) / 7.0) * 255) for i in vkb_color_code)}'
