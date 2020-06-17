# For the LaWls
from vkb.devices.base import VKBDevice
from vkb.led import vkb_color_to_hex_color, set_leds, LEDConfig, ColorMode, LEDMode


def rainbow(dev, led_or_leds):
    """ Device and which LED(s) to make rainbow.

    This will yield each color that is set, as it is set. It is up to you to control how quickly to continue the loop,
    and when to stop, it will loop indefinitely.
    """
    leds = [led_or_leds] if isinstance(led_or_leds, int) else led_or_leds
    color = [0, 0, 0]
    i = 0
    d = 1
    while True:
        color[i] += d
        if 0 == color[i] or color[i] == 7:
            i += abs(d)
        if i > 2 or i < 0:
            d *= -1
            i = 0
        led_configs = [
            LEDConfig(
                _,
                color1=vkb_color_to_hex_color(color),
                color2=vkb_color_to_hex_color(color),
                color_mode=ColorMode.COLOR1_p_2,
                led_mode=LEDMode.CONSTANT,
            )
            for _ in leds
        ]
        if isinstance(dev, VKBDevice):
            dev.set_leds(led_configs)
        else:
            set_leds(dev, led_configs)
        yield color
