class SlackConfig(object):
    def __init__(self, enabled, channel):
        self.__enabled = enabled
        self.__channel = channel

    @property
    def get_enabled(self):
        return self.__enabled

    @property
    def get_channel(self):
        return self.__channel
