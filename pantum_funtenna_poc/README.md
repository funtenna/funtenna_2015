#This is part of the FUNTENNA program.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Ang Cui
# 0xAC
# ang.cui@gmail.com

Prerequisite: 
GCC ARM toolchain -> GNU AS for ARM.

This repo contains open source scripts to reprogram a Pantum P2502W printer over
JTAG into an acoustic and RF transmitter over GPIO/UART. The UART transmission
can be demodulated/decoded via the custom funtenna_demod python module.
 
All scripts can be executed via the included Makefile. Targets and explanations
are provided below:

`uart_cmd` and `jtag_uart`:
Will generate a commands list to take over the Pantum boot process and transmit
a pre-set message over the UART Tx pin.  The `jtag_uart` target will initiate
a telnet session with an OpenOCD-compatible JTAG debugger on port 4444 and
program the device automatically.  This is the same demo that was shown at
Black Hat 2015  and can be demodulated using the gr-funtenna_ook_demod block. 


`acoustic_cmd` and `jtag_acoustic`:
Will generate OpenOCD commands to replay the Pantum printer's boot code over
audio! The `jtag_acoustic` target will program the remote device.

`rf_cmd` and `jtag_rf`:
Will generate a list of commands to take over the Pantum boot process and
transmit a pre-set message over all GPIO pins.  The `jtag_rf` target will
program the remote device.


To get started:

1. Change 1.1.1.1:4444 to your OpenOcd server and port in Makefile.
2. Change AS to the path to your own arm-none-eabi-as assembler.
2. Edit LINKER in printer_jam.py with the path to your own arm-none-eabi-ld linker.

See pantum.cfg for OpenOCD configuration file.
See http://www.funtenna.org/CuiBH2015.pdf for UART and JTAG pinout.
