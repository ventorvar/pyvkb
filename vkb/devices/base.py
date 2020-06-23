from vkb import led


VENDOR_ID = 0x231D


class VKBDevice:
    PRODUCT_ID = None
    VENDOR_ID = VENDOR_ID
    ALL_LEDS = []

    def __init__(self, device, guid):
        assert self.PRODUCT_ID is not None
        assert self.VENDOR_ID is not None
        self.device = device
        self.guid = guid
        self.name = self.device.product_name

    def get_led(self, led_id):
        return self.leds.get(led_id, led.LEDConfig(led=led_id))

    @property
    def leds(self):
        return {_.led: _ for _ in self.led_configs}

    def set_led(
        self,
        led_id,
        color1,
        color_mode=led.ColorMode.COLOR1,
        led_mode=led.LEDMode.CONSTANT,
        color2="#000",
    ):
        """ Set the configuration for a specific LED """
        configs = self.leds
        configs[led_id] = led.LEDConfig(
            led_id,
            color_mode=color_mode,
            led_mode=led_mode,
            color1=color1,
            color2=color2,
        )
        self.set_leds(configs.values())

    def update_leds(self, led_configs):
        """ Update the given LED configurations without overwriting other set LED configurations """
        upcfgs = self.leds
        upcfgs.update({_.led: _ for _ in led_configs})
        self.set_leds(upcfgs.values())

    def set_leds(self, led_configs):
        """ Clear and set new LED configurations """
        _open = not self.device.is_opened()
        try:
            if _open:
                self.device.open()
            led.set_leds(self.device, led_configs)
        finally:
            if _open:
                self.device.close()

    @property
    def led_configs(self):
        _open = not self.device.is_opened()
        try:
            if _open:
                self.device.open()
            return led.get_led_configs(self.device)
        finally:
            if _open:
                self.device.close()
