from plugins.base import PluginPhotoSource, PluginException

from .icloud_shared_album import IcloudSharedAlbum

class PluginIcloudSharedAlbum(PluginPhotoSource):
    def __init__(self, opts={}):
        super().__init__(opts)

        if "token" not in self.__opts__:
            raise PluginException(f"'{self.__class__.__name__}' expects "
                                  f" 'token' opt to by passed from config.yaml")
        self.__icloud__ = IcloudSharedAlbum(self.__opts__['token'])

    @property
    def photos(self):
         photos = {}
         for id, photo in self.__icloud__.album.items():
             hi_res = photo['derivatives'][str(max([int(d) for d in photo['derivatives'].keys()]))]
             photos[id] = { k:v for k,v in hi_res.items() if k in ['url', 'width', 'height'] }
             photos[id]['landscape'] = photos[id]['width'] > photos[id]['height']
         return photos

if __name__ == "__main__":
    import sys
    photo_source = PluginIcloudSharedAlbum(opts={'token': sys.argv[1] })
    print(photo_source.photos)
