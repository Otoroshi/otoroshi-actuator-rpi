# -*- coding: utf-8 -*-
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession
import logging


from actuator_rpi.config import Config
from actuator_rpi.channel import ChannelManager


class AppSession(ApplicationSession):
    rpi_config = Config()

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.rpi_config.from_env(config.extra['rpi_config'])

        channels = []
        for section in self.rpi_config.parser.sections():
            if section != 'general':
                channels.append(
                    (section, self.rpi_config.parser.items(section)))
        self.channels = ChannelManager(channels, self.rpi_config.get('general', 'pinmode'))

    def onConnect(self):
        self.join(
            self.config.realm,
            [u"ticket"],
            self.rpi_config.get('general', 'username'))

    def onDisconnect(self):
        logging.info("Exiting... Resetting channel to default mode")
        self.channels.reset()

    def onChallenge(self, challenge):
        if challenge.method == u"ticket":
            return self.rpi_config.get('general', 'password')
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    @coroutine
    def onJoin(self, details):
        for channel in self.channels.channels:
            proc_prefix = 'io.otoroshi.actuator.%s.%s' % (
                self.rpi_config.get('general', 'username'),
                channel.channel)
            yield from self.register(channel.high, '%s.high' % proc_prefix)
            yield from self.register(channel.low, '%s.low' % proc_prefix)
            yield from self.register(channel.toggle, '%s.toggle' % proc_prefix)
            channel.reset()
