from vkb import led
from .base import VKBDevice


# TODO: refactor this into something more elegant. This was just kinda add things as you thought of 'em kinda dev


class GladiatorK(VKBDevice):
    PRODUCT_ID = 0x0132

    LED_BASE = 0
    LED_TOP = 10
    LED_POV = 11
    ALL_LEDS = [LED_BASE, LED_TOP, LED_POV]

    @property
    def led_top(self):
        return self.get_led(self.LED_TOP)

    @led_top.setter
    def led_top(self, color1):
        self.set_led(
            self.LED_TOP,
            color1=color1,
            color_mode=led.ColorMode.COLOR1,
            led_mode=led.LEDMode.CONSTANT,
        )

    @property
    def led_base(self):
        return self.get_led(self.LED_BASE)

    @led_base.setter
    def led_base(self, color):
        vc = led.hex_color_to_vkb_color(color)
        self.set_led(
            self.LED_BASE,
            color1=color,
            color_mode=led.ColorMode.COLOR1,
            led_mode=led.LEDMode.CONSTANT,
        )

    @property
    def led_pov(self):
        return self.get_led(self.LED_POV)

    @led_pov.setter
    def led_pov(self, color1):
        self.set_led(
            self.LED_POV,
            color1=color1,
            color_mode=led.ColorMode.COLOR1,
            led_mode=led.LEDMode.CONSTANT,
        )


class GladiatorKLH(GladiatorK):
    PRODUCT_ID = 0x0133
