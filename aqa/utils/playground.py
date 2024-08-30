import requests
import json
import time

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
            'Cookie'            : '_ga=GA1.1.93763482.1719421853; intercom-id-h3v14f8j=7d7bc1dd-5e0a-49c9-9e15-229b608665e2; intercom-device-id-h3v14f8j=c39db4ce-a5d5-4dac-b4a5-4b151b33601e; __stripe_mid=9e2ca8ba-c013-4b66-8bd2-aad3b8226759bcbb69; __Host-next-auth.csrf-token=3df66c1be9a46003c28129e35b1da64d67301816c2de90135e49f3a0c8f8bcb4%7C4adc5b32723f6211814c55cd50b95c9b5a2c683c2d25ecaed6d47ac55569cffb; _gcl_au=1.1.1743712450.1724834353; _fbp=fb.1.1724834352769.492870341575443283; __Secure-next-auth.callback-url=https%3A%2F%2Fplayground.com%2Fdesign; __Secure-next-auth.session-token=458d5543-38a0-46f5-a95b-8c7dbc9cfcf7; __stripe_sid=fd7a501e-5cdd-4a58-95f4-a1230161b706a89b23; intercom-session-h3v14f8j=YXdZL1dydXhXYkZCLzlZenllMm1YVXRBWmh3TmlueUFYZnZTam5yZjNCbmFmNkp2ZlZyaUJvWFd6K1QrWUFBVi0tcGtWQXNKZWhyRU45ZVdNK3QzcEFUdz09--a0d62bd5b44c93f92614fd139cb947e4291cbe72; _ga_PLJRH784LG=GS1.1.1724852935.14.1.1724852995.0.0.0; _ga_Q8NE5DKVZ5=GS1.1.1724852935.2.1.1724852995.0.0.0; mp_6b1350e8b0f49e807d55acabb72f5739_mixpanel=%7B%22distinct_id%22%3A%20%22clxw3hn8n0j03g9llsz0hdxth%22%2C%22%24device_id%22%3A%20%2219055875b44d6e-0a1ebf8520b606-19525637-2a3000-19055875b44d6e%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%22clxw3hn8n0j03g9llsz0hdxth%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22email%22%3A%20%22trieutruong.dev%40gmail.com%22%2C%22__alias%22%3A%20%22clxw3hn8n0j03g9llsz0hdxth%22%7D'
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
            "width"                  : 1280,  # 1920
            "height"                 : 720,   # 1080
            "cfg_scale"              : 7,
            "guidance_scale"         : 7,
            "strength"               : 1.45,
            "steps"                  : 30,
            "seed"                   : 744442870,
            "sampler"                : 9,
            "num_images"             : 1,
            "negativePrompt"         : "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers, nudity, nude, ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers, photo, realistic, text, watermark, signature, username, artist name, nudity, nude, duplicate laptop screens, poor laptop",
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
        output_file = f"{CODE_HOME}/output/playground_{time.time()}.jpg"
        with open(output_file, "wb") as file:
            file.write(image_data)

        print(f"Image data extracted and saved to {output_file}")


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

    # prompt = "Digital painting of Lofi girl, wearing headphones, engrossed in a thick book, legs hanging over the edge of the comfy chair, main color blue, blurry city view visible through the window, raining outside, fireflies light effects around the room, the surrounding room filled with scattered study materials and nude on a cozy bed, ultra-smooth textures, sharp 4k resolution, atmospheric light, cozy, volumetric feeling."

    # playground_prompt = "Digital painting of Lofi girl, wearing headphones, engrossed in a thick book, legs hanging over the edge of the comfy chair, main color blue, city at night view is visible through the window, raining outside, the surrounding room filled with some books, a pen, a laptop, ultra-smooth textures, sharp 4k resolution, atmospheric light, cozy, volumetric feeling."

    # playground_prompt = "Digital painting of a Lofi girl, wearing headphones, immersed in a thick book, her legs hanging over the edge of a comfortable armchair. The main color is blue, the night view of the city can be seen through the window, it is snowing outside. The room has a bookshelf, a desk with a laptop, notebooks, and pens. The texture is extremely smooth, the resolution is sharp 4k, the light is warm, the feeling is cozy and spacious."

    # playground_prompt = "Digital painting of a Lofi girl, wearing short clothes, revealing a lot of skin, wearing headphones, immersed in a macbook, legs hanging over the edge of a comfortable armchair. The main color is blue, the night view of the city can be seen through the window. The room has a small bookshelf, the desk has a few decorations and a macbook. The texture is extremely smooth, the resolution is sharp 4k, the light is warm, the feeling is cozy, spacious."

    playground_prompt = "Digital painting of a Lofi girl, wearing short clothes, revealing a lot of skin, full body visible, wearing headphones, sitting on the comfy chair, immersed in a macbook on the desk with a coffe cup, a few decorations. The main color is blue, the night view of the city can be seen through the window. The room has a small bookshelf, the desk has a few decorations and a macbook. The texture is extremely smooth, the resolution is sharp 4k, the light is warm, the feeling is cozy, spacious."

    playground = PlaygroundAPIHandle()

    res = playground.create_img(playground_prompt)

    if res and res.get('success'):
        data = res.get('data')
        images = data.get('images')
        for i in images:
            playground.write_img_base64(i.get('url'))
