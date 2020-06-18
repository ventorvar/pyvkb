=====
Usage
=====

To use pyvkb in a project::

    import pyvkb


CLI
---

pyvkb can also be used from via it's CLI application::


    $ pip install pyvkb
    $ vkb list
     0:  VKB-Sim Gladiator K  (4d1e55b2-f16f-11cf-88cb-001111000030)
    $ vkb led show
     0:  VKB-Sim Gladiator K  (4d1e55b2-f16f-11cf-88cb-001111000030)
     ----------------------------------------------------------------------
     led:10 clm:COLOR1 lem:OFF color1:#000000 color2:#000000
     led:11 clm:COLOR1 lem:OFF color1:#000000 color2:#000000
     led: 0 clm:COLOR1 lem:OFF color1:#000000 color2:#000000

    $ vkb led set --device 0 --leds 10 --color1 "#f00" --led-mode=1
    $ vkb led show
     0:  VKB-Sim Gladiator K  (4d1e55b2-f16f-11cf-88cb-001111000030)
     ----------------------------------------------------------------------
     led:10 clm:COLOR1 lem:CONSTANT color1:#ff0000 color2:#000000
     led:11 clm:COLOR1 lem:OFF color1:#000000 color2:#000000
     led: 0 clm:COLOR1 lem:OFF color1:#000000 color2:#000000

