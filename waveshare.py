import logging
import time

import RPi.GPIO
import spidev

logger = logging.getLogger(__name__)


class RaspberryPi:
    CS_PIN = 8
    RST_PIN = 17
    BUSY_PIN = 24
    DC_PIN = 25

    def __init__(self):
        self.GPIO = RPi.GPIO
        self.SPI = spidev.SpiDev()

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def delay_ms(self, delay_time):
        time.sleep(delay_time / 1000.0)

    def spi_writebyte(self, data):
        self.SPI.writebytes(data)

    def spi_writebyte2(self, data):
        self.SPI.writebytes2(data)

    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.BUSY_PIN, self.GPIO.IN)

        # SPI device, bus = 0, device = 0
        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00
        logger.debug("raspberrypi GPIO & SPI init done")
        return 0

    def module_exit(self):
        self.SPI.close()
        self.GPIO.output(self.RST_PIN, 0)
        self.GPIO.output(self.DC_PIN, 0)
        self.GPIO.cleanup([self.RST_PIN, self.DC_PIN, self.CS_PIN, self.BUSY_PIN])
        logger.debug("raspberrypi GPIO & SPI power off done")


class EPD:
    WIDTH = 104
    HEIGHT = 212

    def __init__(self, r):
        self.reset_pin = r.RST_PIN
        self.dc_pin = r.DC_PIN
        self.busy_pin = r.BUSY_PIN
        self.cs_pin = r.CS_PIN
        self.raspberry = r

    def reset(self):
        self.raspberry.digital_write(self.reset_pin, 1)
        self.raspberry.delay_ms(200)
        self.raspberry.digital_write(self.reset_pin, 0)
        self.raspberry.delay_ms(200)
        self.raspberry.digital_write(self.reset_pin, 1)
        self.raspberry.delay_ms(200)

    def send_command(self, command):
        self.raspberry.digital_write(self.dc_pin, 0)
        self.raspberry.digital_write(self.cs_pin, 0)
        self.raspberry.spi_writebyte([command])
        self.raspberry.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.raspberry.digital_write(self.dc_pin, 1)
        self.raspberry.digital_write(self.cs_pin, 0)
        self.raspberry.spi_writebyte([data])
        self.raspberry.digital_write(self.cs_pin, 1)

    def read_busy(self):
        self.send_command(0x71)
        while self.raspberry.digital_read(self.busy_pin) == 0:
            self.send_command(0x71)
            self.raspberry.delay_ms(100)

    def init(self):
        if self.raspberry.module_init() != 0:
            return -1

        self.reset()
        self.send_command(0x04)
        # waiting for the electronic paper IC to release the idle signal
        self.read_busy()
        # panel setting
        self.send_command(0x00)
        # LUT from OTP,128x296
        self.send_data(0x0f)
        # Temperature sensor, boost and other related timing settings
        self.send_data(0x89)
        # resolution setting
        self.send_command(0x61)
        self.send_data(0x68)
        self.send_data(0x00)
        self.send_data(0xD4)
        # VCOM AND DATA INTERVAL SETTING
        self.send_command(0X50)
        # WBmode:VBDF 17|D7 VBDW 97 VBDB 57
        self.send_data(0x77)
        # WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7
        return 0

    def get_buffer(self, image):
        buf = [0xFF] * (int(self.WIDTH / 8) * self.HEIGHT)
        image_mono_color = image.convert('1')
        im_width, im_height = image_mono_color.size
        pixels = image_mono_color.load()
        if im_width == self.WIDTH and im_height == self.HEIGHT:
            for y in range(im_height):
                for x in range(im_width):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.WIDTH) / 8)] &= ~(0x80 >> (x % 8))
        elif im_width == self.HEIGHT and im_height == self.WIDTH:
            for y in range(im_height):
                for x in range(im_width):
                    new_x = y
                    new_y = self.HEIGHT - x - 1
                    if pixels[x, y] == 0:
                        buf[int((new_x + new_y * self.WIDTH) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, image_black, image_red):
        self.send_command(0x10)
        for i in range(0, int(self.WIDTH * self.HEIGHT / 8)):
            self.send_data(image_black[i])
        self.send_command(0x13)
        for i in range(0, int(self.WIDTH * self.HEIGHT / 8)):
            self.send_data(image_red[i])
        # REFRESH
        self.send_command(0x12)
        self.raspberry.delay_ms(100)
        self.read_busy()

    def clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.WIDTH * self.HEIGHT / 8)):
            self.send_data(0xFF)
        self.send_command(0x13)
        for i in range(0, int(self.WIDTH * self.HEIGHT / 8)):
            self.send_data(0xFF)
        # REFRESH
        self.send_command(0x12)
        self.raspberry.delay_ms(100)
        self.read_busy()

    def sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)
        self.send_command(0X02)
        self.read_busy()
        # DEEP_SLEEP
        self.send_command(0x07)
        # check code
        self.send_data(0xA5)
        self.raspberry.delay_ms(2000)
        self.raspberry.module_exit()
