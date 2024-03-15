import os


def red_on():
    # echo <行为> > /sys/class/leds/<名字>/trigger
    os.system("echo default-on > '/sys/class/leds/red:os/trigger'")
    pass


def red_off():
    os.system("echo usb-gadget > '/sys/class/leds/red:os/trigger'")
    pass


def green_on():
    os.system("echo default-on > '/sys/class/leds/green:internet/trigger'")
    pass


def green_off():
    os.system("echo usb-gadget > '/sys/class/leds/green:internet/trigger'")
    pass


def blue_on():
    os.system("echo default-on > '/sys/class/leds/blue:wifi/trigger'")
    pass


def blue_off():
    os.system("echo usb-gadget > '/sys/class/leds/blue:wifi/trigger'")
    pass


if __name__ == '__main__':
    red_off()
