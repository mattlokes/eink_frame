
class PluginException(Exception):
    pass

class Plugin():
    def __init__(self, opts={}):
        self.__opts__ = opts

class PluginPhotoSource(Plugin):
    @property
    def photos(self):
        assert False, "Virtual Property 'photos' needs overriding to use!"
