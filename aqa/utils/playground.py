import requests
import json


class PlaygroundAPIHandle(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.headers = {
            'accept'            : 'application/json, text/plain, */*',
            'accept-language'   : 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type'      : 'application/json',
            'origin'            : 'https://playground.com',
            'priority'          : 'u=1, i',
            'referer'           : 'https://playground.com/create',
            'sec-ch-ua'         : '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile'  : '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest'    : 'empty',
            'sec-fetch-mode'    : 'cors',
            'sec-fetch-site'    : 'same-origin',
            'user-agent'        : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Cookie'            : '__Host-next-auth.csrf-token=9bb866f76662f12c17620181dd32d2ea38008756a96b0e6e611b9e03ffb98427%7C4eae30e797160f4d744ad35ef05438bdeb238bfd901f6101eeb6094e003a1591; __Secure-next-auth.callback-url=https%3A%2F%2Fplayground.com; __Secure-next-auth.session-token=ca8bb54e-bd96-4e74-bf62-235a02512512'
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

    def create_img(self, prompt):
        url = "https://playground.com/api/models"
        payload = json.dumps({
            "width"                  : 1920,
            "height"                 : 1080,
            "cfg_scale"              : 7,
            "guidance_scale"         : 7,
            "strength"               : 1.45,
            "steps"                  : 30,
            "seed"                   : 744442870,
            "sampler"                : 9,
            "num_images"             : 1,
            "negativePrompt"         : "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers, nudity, nude, ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers, photo, realistic, text, watermark, signature, username, artist name, nudity, nude",
            "prompt"                 : prompt,
            "filter"                 : "Real_Cartoon_XL",
            "high_noise_frac"        : 1,
            "modelType"              : "stable-diffusion-xl",
            "isPrivate"              : False,
            "baseImageId"            : "cluwchcdz00x5s601tlyo8mr2",
            "batchId"                : "ZagJJW3w4D",
            "generateVariants"       : False,
            "dream_booth_model"      : "Real_Cartoon_XL",
            "initImageFromPlayground": False,
            "statusUUID"             : "846fb2fd-97ea-43ca-95d3-c5cdd80d1bf9"
        })

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

    def write_img_base64(self, data_url):
        import base64
        from config import CODE_HOME
        # Extract base64 data from the URL
        base64_data = data_url.split(",")[1]

        # Decode base64 data to binary
        image_data = base64.b64decode(base64_data)

        # Write binary image data to a file
        with open(f"{CODE_HOME}/image.jpg", "wb") as file:
            file.write(image_data)

        print("Image data extracted and saved to 'image.jpg'")


if __name__ == '__main__':
    # change_audio_speed()
    prompt = """
Draw a cozy bedroom scene with a girl lying in bed, wearing headphones and looking out the window. She is immersed in the music, her eyes fixed on the horizon beyond the window.
The room is lightly lit, conveying a feeling of calm and tranquility. Details such as posters on the wall, a bookshelf and soft lighting add depth to the space. The girl's facial expression reflects a mixture of contemplation and serenity.
anime style

Digital painting of Lofi girl, wearing headphones, engrossed in a thick book, legs hanging over the edge of the comfy chair, main color blue, blurry city view visible through the window, raining outside, the surrounding room filled with scattered study materials and a cozy bed, ultra-smooth textures, sharp 4k resolution, atmospheric light, cozy, volumetric feeling.

anime art style, girl studying, hot coffee, she's writing something, computer. books, earbuds on her ear, Tokyo city scene through window, raining outside, 8pm, cozy and warm in her
room, cellphone, detail, realistic, aesthetic, wallpaper, acryl ic painting, horizontal

Face prompt
5oclock shadow: no, age: 17 (60%), arched eyebrows: yes (35%), attractive: yes, bags under eyes: no, bald: no (95%), bangs: no (71%), beard: no, big lips: no (23%), big nose: no, black hair: no (49%), blond hair: no, blurry: no, brown hair: yes (77%), bushy eyebrows: yes (2%), chubby: no (92%), double chin: no, expression: neutral (82%), gender: female (93%), glasses: no, goatee: no, gray hair: no, heavy makeup: yes (95%), high cheekbones: no (52%), mouth open: no (86%), mustache: no, narrow eyes: no (56%), oval face: yes (91%), pale skin: yes (47%), pitch: -8.73, pointy nose: yes (10%), race: asian (52%), receding hairline: no (75%), rosy cheeks: no (60%), sideburns: no, straight hair: no (8%), wavy hair: yes (17%), wearing earrings: no (0%), wearing hat: no, wearing lipstick: yes (91%), wearing necklace: no (51%), wearing necktie: no (73%), yaw: 8.82, young: yes, chin size: extra small, color background: a9abae (4%), color clothes middle: 212026 (12%), color clothes sides: 212026 (1%), color eyes: 3f2926 (29%), color hair: 392622 (76%), color skin: cfa793, eyebrows corners: average, eyebrows position: extra low, eyebrows size: extra thin, eyes corners: average, eyes distance: far, eyes position: low, eyes shape: extra round, glasses rim: no, hair beard: none, hair color type: brown (76%), hair forehead: yes, hair length: very short, hair mustache: none, hair sides: thin, hair top: short, head shape: average, head width: wide, mouth corners: low, mouth height: average, mouth width: extra small, nose shape: extra straight, nose width: extra wide, teeth visible: no,
"""

    playground = PlaygroundAPIHandle()

    res = playground.create_img(prompt)

    if res and res.get('success'):
        data = res.get('data')
        images = data.get('images')
        for i in images:
            playground.write_img_base64(i)
