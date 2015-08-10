import pexpect
import struct
import itertools


def grouper(iterable, n, fillvalue=None):
    """ group data """
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

class OcdInterface(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        #self.connect()

    def connect(self):
        self._child = pexpect.spawn('telnet %s %d' % (self._host, self._port))
        self._child.expect('>')
        print 'server banner:', self._child.before

    def close(self):
        self._child.close()

    def sendcmd(self, cmd_str):
        self._child.sendline(cmd_str)
        self._child.expect('>')
        return self._child.before

    def read_byte(self, vmaddr, count=1):
        res_str = self.sendcmd('mdb 0x%08x %d' % (vmaddr, count))
        print res_str
        data = []
        for line in res_str.split('\n')[1:]:  # first line is echo of cmd
            line = line.strip()
            vals = line.split(' ')[1:]
            for val in vals:
                data.append(struct.pack('>B', int(val, 16)))
        return ''.join(data)

    def read_word(self, vmaddr, count=1):
        res_str = self.sendcmd('mdw 0x%08x %d' % (vmaddr, count))
        data = []
        for line in res_str.split('\n')[1:]:  # first line is echo of cmd
            line = line.strip()
            vals = line.split(' ')[1:]
            for val in vals:
                data.append(struct.pack('>I', int(val, 16)))
        return ''.join(data)

    def write_byte(self, vmaddr, val):
        if isinstance(val, str):
            val = ord(val)
        res_str = self.sendcmd('mwb 0x%08x 0x%02x' % (vmaddr, val))
        print res_str

    def write_word(self, vmaddr, val):
        res_str = self.sendcmd('mww 0x%08x 0x%08x' % (vmaddr, val))
        print res_str

    def write_data(self, vmaddr, data, endian='little'):
        assert endian in ['little', 'big'], "endian must be little or large"
        self.connect()
        self.sendcmd('halt')

        words = grouper(data, 4)
        vmaddrs = grouper(range(vmaddr, vmaddr + len(data)), 4)

        for vmaddr, d in zip(vmaddrs, words):
            if d[-1] is not None:
                if endian == 'little':
                    d_val = struct.unpack("<I", "".join(d))[0]
                else:
                    d_val = struct.unpack(">I", "".join(d))[0]
                self.write_word(vmaddr[0], d_val)
                pass
            else:
                for vmaddr_byte, d_byte in zip(vmaddr, d):
                    self.write_byte(vmaddr_byte, d_byte)
        self.sendcmd('resume')
        self.close()
