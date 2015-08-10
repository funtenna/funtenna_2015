AS = /usr/local/bin/arm-none-eabi-as
ASMFLAGS = -EL -k -march=armv7-a -mcpu=cortex-a9 -mfpu=neon
SRC = $(wildcard *.as)
OBJ = $(SRC:.as=.o)

.PHONY: clean
clean:
	rm -rf ${OBJ}
	rm -rf *-linkd *.pyc

all: ${OBJ}

pantumhook.o:
	${AS} ${ASMFLAGS} -o $@ pantumhook.o

pantumpatch.o:
	${AS} ${ASMFLAGS} -o $@ pantumpatch.as

pantumreturn.o:
	${AS} ${ASMFLAGS} -o $@ pantumreturn.as

pantumhook_sensorcmd.o:
	${AS} ${ASMFLAGS} -o $@ pantumhook_sensorcmd.as

pantum_gpio_push_sensors.o:
	${AS} ${ASMFLAGS} -o $@ pantum_gpio_push_sensors.as

pantum_gpio_uart_onoff.o:
	${AS} ${ASMFLAGS} -o $@ pantum_gpio_uart_onoff.as

pantum_gpio_push_acoustic.o:
	${AS} ${ASMFLAGS} -o $@ pantum_gpio_push_acoustic.as


jtag_rf: all
	python printer_jam.py -a rf -p pantum.dump -H 1.1.1.1 -p 4444

jtag_acoustic:all
	python printer_jam.py -a acoustic -p pantum.dump -H 1.1.1.1 -p 4444

jtag_uart:all
	python printer_jam.py -a uart -f pantum.dump -H 1.1.1.1 -p 4444
