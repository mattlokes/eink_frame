import requests
import json

# Heavily Inspired from https://github.com/bertrandom/icloud-shared-album-to-flickr
from functools import cached_property

class IcloudSharedAlbumBaseUrl():

    BASE_62_CHAR_SET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def __init__(self, token):
        self._token = token

    def __base62ToInt__(self, s):
        t = 0
        for i in s:
            t = (t * 62) + self.BASE_62_CHAR_SET.index(i)
        return t

    @property
    def token(self):
        return self._token

    @cached_property
    def url(self):
        t = self.token[0]
        n = self.__base62ToInt__( self.token[1] if t == "A" else self.token[1:3] )
        return f"https://p{n:02}-sharedstreams.icloud.com/{self.token}/sharedstreams"

class IcloudSharedAlbum():

    REQ_HEADERS = {
                    'Origin': 'https://www.icloud.com',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Content-Type': 'text/plain',
                    'Accept': '*/*',
                    'Referer': 'https://www.icloud.com/sharedalbum/',
                    'Connection': 'keep-alive',
                  }

    def __init__(self, token):
        self.base_url = IcloudSharedAlbumBaseUrl(token)

    @property
    def metadata (self):
        resp =requests.post( f"{self.base_url.url}/webstream",
                             headers=self.REQ_HEADERS,
                             data=json.dumps({"streamCtag":None}) )

        if resp.status_code != 200: raise Exception("Request for Metadata blew up")

        return { photo['photoGuid']: photo for photo in resp.json()['photos'] }

    @property
    def album (self):
        metadata = self.metadata

        resp =requests.post( f"{self.base_url.url}/webasseturls",
                             headers=self.REQ_HEADERS,
                             data=json.dumps({'photoGuids': list(metadata.keys())}) )

        if resp.status_code != 200: raise Exception("Request for Album blew up")

        urls = { id: f"https://{item['url_location']}{item['url_path']}"
                                       for id, item in resp.json()['items'].items() }

        for p in metadata.values():
            for d in p['derivatives'].values():
                d['url'] = urls.get(d['checksum'], None)

        return metadata

if __name__ == "__main__":
    import sys
    ph = IcloudSharedAlbum(sys.argv[1])
    print(ph.album)

