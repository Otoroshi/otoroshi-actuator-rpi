# -*- coding: utf-8 -*-
import logging
from asyncio import coroutine, sleep
import RPi.GPIO as GPIO


class ChannelManager(object):
    channels = list()
    PINMODES = ["BCM", "BOARD"]

    def __init__(self, channels, pinmode):
        GPIO.setwarnings(False)

        pinmode = pinmode.upper()
        if pinmode in ChannelManager.PINMODES:
            GPIO.setmode(pinmode)
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        self.load(channels)

    def load(self, channels):
        # Loading channels
        self.channels = []
        for channel, config in channels:
            channel = Channel(channel, config)
            self.channels.append(channel)

    def reset(self):
        for channel in self.channels:
            channel.reset()


class Channel(object):
    config = dict()

    def __init__(self, channel, config):
        self.channel = channel
        self.reload(config)

    def reload(self, config):
        self.config = dict(config)
        GPIO.setup(self.channel, GPIO.OUT)

    def high(self):
        GPIO.output(self.channel, GPIO.UP)
        logging.info("Channel '%s' set to HIGH" % self.channel)

    def low(self):
        GPIO.output(self.channel, GPIO.DOWN)
        logging.info("Channel '%s' set to LOW" % self.channel)

    @coroutine
    def toggle(self):
        self.high()
        yield from sleep(int(self.config["reload_timeout"]))
        self.low()

    def reset(self):
        if self.config["default"] == "HIGH":
            self.high()
        else:
            self.low()
