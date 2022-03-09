
class PluginException(Exception):
    pass

class PluginBase():
    def __init__(self, opts={}):
        self.__opts__ = opts

class PluginPhotoSource(PluginBase):
    @property
    def photos(self):
        assert False, "Virtual Property 'photos' needs overriding to use!"
