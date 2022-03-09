from .plugins.registry  import PluginRegistryEntry
from .plugins.base      import PluginPhotoSource, PluginException

from icloud_shared_album import IcloudSharedAlbum

import pdb

class PluginIcloudSharedAlbum(PluginPhotoSource):
    def __init__(self, opts={}):
        super().__init__(opts)

        if "token" not in self.__opts__:
            raise PluginException(f"'{self.__class__.__name__}' expects "
                                  f" 'token' opt to by passed from config.yaml")
        self.__icloud__ = IcloudSharedAlbum(self.__opts__['token'])

    @property
    def photos(self):
         album = self.__icloud__.album
         pdb.set_trace()


class PluginRegistry(PluginRegistryEntry):
    name  = "icloud_shared_album"
    cls   = PluginIcloudSharedAlbum
    type  = PluginPhotoSource

if __name__ == "__main__":
    import sys
    photo_source = PluginIcloudSharedAlbum(opts={'token': sys.argv[1] })
    print(photo_source.photos)
