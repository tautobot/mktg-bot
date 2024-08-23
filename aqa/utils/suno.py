import requests
import re
import urllib
from config import SUNO_COOKIE


class SunoObj:
    def __init__(self):
        self._id = None
        self._status = None
        self._title = None
        self._tags = None
        self._audio_url = None
        self._video_url = None
        self._prompt = None
        self._duration = 0


class SunoAPIHandle(object):
    def __init__(self, **kwargs):
        self.kwargs     = kwargs
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://suno.com',
            'priority': 'u=1, i',
            'referer': 'https://suno.com/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

    def _get(self, url, params):
        try:
            res_ = requests.get(url, headers=self.headers, params=params)
            if res_.status_code == 200:
                return res_.json()
            else:
                print(f"Request failed with status code: {res_.status_code}")
                # Access the error message, if available
                error_message = res_.text
                print(f"{error_message=}")
        except requests.exceptions.RequestException as e:
            print(f'RequestException: {e}')
        except ConnectionResetError:
            print('ConnectionResetError')
        return None

    def _post(self, url, payload):
        try:
            res_ = requests.request("POST", url, headers=self.headers, data=payload)
            if res_.status_code == 200:
                return res_.json()
            else:
                print(f"Request failed with status code: {res_.status_code}")
                # Access the error message, if available
                error_message = res_.text
                print(f"{error_message=}")
        except requests.exceptions.RequestException as e:
            print(f'RequestException: {e}')
        except ConnectionResetError:
            print('ConnectionResetError')
        return None

    def get_new_token(self):
        self.headers.update(
            {
                'cookie': SUNO_COOKIE
            }
        )
        url = 'https://clerk.suno.com/v1/client/sessions/sess_2iBJjVpsRfdxSBFUa9W8LSVpftf/tokens?_clerk_js_version=4.73.3'
        # return response
        res_ = self._post(url, {})
        if res_:
            self.headers.pop('cookie')
            self.headers.update({'authorization': f"Bearer {res_.get('jwt')}"})
            return {
                'success': True,
                'data'   : res_
            }
        else:
            return {
                'success': False,
                'data'   : res_
            }

    def get_metaplaylist(self):
        url = 'https://studio-api.suno.ai/api/trending/metaplaylist/'
        res_ = self._get(url, {})
        if res_:
            return {
                'success': True,
                'data'   : res_
            }
        else:
            return {
                'success': False,
                'data'   : res_
            }

    def search(self, search_text, from_index=0):
        payload = '{"search_queries":[{"name":"public_song' + search_text + '","search_type":"public_song","term":"' + search_text + '","from_index":' + str(from_index) + ',"rank_by":"trending"}]}'

        # encoded_from_index = urllib.parse.quote(str(from_index))
        # encoded_search_text = urllib.parse.quote(str(search_text))
        #
        # payload = {
        #     "search_queries": [
        #         {
        #             "name": f"public_song{encoded_search_text}",
        #             "search_type": "public_song",
        #             "term": encoded_search_text,
        #             "from_index": encoded_from_index,
        #             "rank_by": "trending"
        #         }
        #     ]
        # }
        headers = {
            'accept'            : '*/*',
            'accept-language'   : 'en-US,en;q=0.9,vi;q=0.8',
            'affiliate-id'      : 'undefined',
            'authorization'     : self.headers.get("authorization"),
            'content-type'      : 'text/plain;charset=UTF-8',
            'origin'            : 'https://suno.com',
            'priority'          : 'u=1, i',
            'referer'           : 'https://suno.com/',
            'sec-ch-ua'         : '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile'  : '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest'    : 'empty',
            'sec-fetch-mode'    : 'cors',
            'sec-fetch-site'    : 'cross-site',
            'user-agent'        : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        self.headers = headers
        url = 'https://studio-api.suno.ai/api/search/'
        res_ = self._post(url, payload)
        if res_:
            return {
                'success': True,
                'data'   : res_
            }
        else:
            return {
                'success': False,
                'data'   : res_
            }


class MediaResource(object):

    def query_data(self):
        from database.model import Multimedia
        media_rec = Multimedia.select(**{'id': 1, 'status': 'complete'})
        return media_rec


if __name__ == '__main__':
    from database.model import Multimedia
    from database.mm_schema.multimedia_schema import MULTIMEDIA_SCHEMA
    from database.helper.enums import MediaSourceEnum

    data = {
        "external_id"  : "3bcdfa43-51d2-4726-8537-50bdc9ff4d15",
        "video_url"    : "https://cdn1.suno.ai/3bcdfa43-51d2-4726-8537-50bdc9ff4d15.mp4",
        "audio_url"    : "https://cdn1.suno.ai/3bcdfa43-51d2-4726-8537-50bdc9ff4d15.mp3",
        "image_url"    : "https://cdn1.suno.ai/image_large_3bcdfa43-51d2-4726-8537-50bdc9ff4d15.png",
        "model_version": "v3.5",
        "model_name"   : "chirp-v3",
        "title"        : "lo-fi",
        "tags"         : "lo-fi,  chill,  relax,  drum,  bass, xylophone, synth, 16-bits, synthwave, melancholic",
        "lyric"        : "[intro]\n\n\n\n[melancholic xylophone solo]\n\n\n\n[16-bit melody]\n\n\n[Instrumental interlude]\n\n\n[slow]\n\n[Synthwave melody]\n\n\n[solo bass and xylophone  melancholic ]\n\n\n\n[END]\n\n[END]\n\n[silencie]\n\n[END]\n\n[END]",
        "duration"     : 184.2,
        "source"       : MediaSourceEnum.SUNO
    }
    m_media = Multimedia()
    rec = m_media.select(**{'id': 1})
    multimedia_sch = MULTIMEDIA_SCHEMA()
    # rec = multimedia_sch.dump(data)
    load_data = multimedia_sch.dump(rec)
    print(load_data.get('lyric'))

    # TODO:
    #  1. Call suno endpoint
    #  2. Extract data from suno and identify music style
    #  3. Store multimedia in mktg database
    #  4. Create job to pick multimedia in sequence

