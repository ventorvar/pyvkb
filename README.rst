=====
pyvkb
=====


.. image:: https://img.shields.io/pypi/v/pyvkb.svg
        :target: https://pypi.python.org/pypi/pyvkb

.. image:: https://img.shields.io/travis/ventorvar/pyvkb.svg
        :target: https://travis-ci.org/ventorvar/pyvkb

.. image:: https://readthedocs.org/projects/pyvkb/badge/?version=latest
        :target: https://pyvkb.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/ventorvar/pyvkb/badge.svg?branch=devel
        :target: https://coveralls.io/github/ventorvar/pyvkb?branch=devel

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


Python library for controlling VKB devices


* Free software: MIT license
* Documentation: https://pyvkb.readthedocs.io.

.. warning::
    pyvkb is in very early stages of development, things are likely to change.

.. warning::
    Currently pyvkb only works on Windows.

.. warning::
    The techniques used are the same that the VKBDevCfg tools use. Every effort is made to ensure
    that nothing will harm the device. Even though, use at your own risk.


Features
--------

* CLI
* List connected VKB devices
* Get and set custom LED configurations


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

See `vkb --help` for more information
