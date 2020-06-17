import sys
import time
import typing

from nubia import command, argument

from vkb.devices import find_all_vkb
from vkb.led import ColorMode, LEDMode, LEDConfig, LED_CONFIG_COUNT
from vkb.led.effects import rainbow


@command("led")
class LED:
    """
    Set or retrieve the current LED configurations for specified VKB devices.
    """

    @command
    @argument(
        "devices",
        aliases=["-d"],
        description="Show or set the LED for specific devices. Default: All",
    )
    @argument(
        "leds",
        aliases=["-l"],
        description="Specify a specific LED to set. Default: All",
    )
    def show(self, devices: typing.List[int] = (), leds: typing.List[int] = None):
        """ Show currently set LED information """
        all_devs = find_all_vkb()
        devices = devices if devices else range(len(all_devs))

        for dev_id in devices:
            dev = all_devs[dev_id]
            print(f' {dev_id}: {dev.name} ({dev.guid})\n {"-" * 70}')
            found = False
            for led, config in dev.leds.items():
                if not leds or led in leds:
                    found = True
                    print(
                        f' led:{led:>2} {" ".join(repr(config).split()[2:]).rstrip(">")}'
                    )
            if not found:
                print("    No LED configurations")
            print("")

    @command(help="Run a rainbow effect for the given devices/LEDs")
    @argument(
        "devices",
        aliases=["-d"],
        description="Show or set the LED for specific devices. Default: All",
    )
    @argument(
        "leds",
        aliases=["-l"],
        description="Specify a specific LED to set. Default: All",
    )
    @argument(
        "speed",
        aliases=["-s"],
        description="How fast to cycle through the colors in seconds. Default: 0.1",
    )
    def rainbow(
        self,
        devices: typing.List[int] = (),
        leds: typing.List[int] = None,
        speed: float = 0.1,
    ):
        print("Press Ctrl+C to stop")
        all_devs = find_all_vkb()
        devices = devices if devices else range(len(all_devs))
        rainbows = [rainbow(all_devs[_], leds or all_devs[_].ALL_LEDS) for _ in devices]
        try:
            for _ in zip(*rainbows):
                time.sleep(speed)
        except KeyboardInterrupt:
            pass

    @command(help="Set the color of LEDs")
    @argument(
        "devices",
        aliases=["-d"],
        description="Show or set the LED for specific devices. Default: All",
    )
    @argument(
        "leds",
        aliases=["-l"],
        description="Specify a specific LED to set. Default: All",
    )
    @argument("color1", aliases=["-1"], description="HEX color code to use for color1")
    @argument("color2", aliases=["-2"], description="HEX color code to use for color2")
    @argument(
        "color_mode",
        aliases=["-c"],
        description="Color mode to set with color. 0=color1  1=color2  2=color1/2  "
        "3=color2/1  4=color1+2. Default: 0",
    )
    @argument(
        "led_mode",
        aliases=["-L"],
        description="LED mode to set with color. 0=off  1=constant  2=slow blink  "
        "3=fast blink  4=ultra fast. Default: 1",
    )
    def set(
        self,
        devices: typing.List[int] = (),
        leds: typing.List[int] = [],
        color1: str = None,
        color2: str = None,
        color_mode: int = ColorMode.COLOR1,
        led_mode: int = LEDMode.CONSTANT,
    ):
        """
            Set LED configurations for specified VKB devices. Colors are specified as hex color codes.

            e.g. vkb led set -d 0 -l 10 --color1 "#f00"

            NOTE: Setting an LEDs state will _override_ the LED configuration until the joystick is rebooted. Only the
            set LED is affected.

            Color mode:
                0 - color1
                1 - color2
                2 - color1/2
                3 - color2/1
                4 - color1+2

            LED mode:
                0 - off
                1 - constant
                2 - slow blink
                3 - fast blink
                4 - ultra fast
            """
        all_devs = find_all_vkb()
        devices = devices if devices else range(len(all_devs))

        if not devices:
            sys.stderr.write("Invalid device ID")
            sys.exit(1)
        if len(leds) > LED_CONFIG_COUNT:
            sys.stderr.write(
                "You can only specify up to 12 led configurations per device"
            )

        for dev_id in devices:
            dev = all_devs[dev_id]
            led_configs = [
                LEDConfig(
                    led=_,
                    color_mode=color_mode,
                    led_mode=led_mode,
                    color1=color1,
                    color2=color2,
                )
                for _ in leds or dev.ALL_LEDS
            ]
            dev.update_leds(led_configs)
