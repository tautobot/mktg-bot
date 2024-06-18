import shutil
import subprocess
import paramiko
import psycopg2
import sounddevice as sd
import subprocess
import wavio as wv
import re
import urllib.request
import hashlib
import io
import requests
import contextlib
import pandas as pd
import pytube
from aqa.utils import youtube_downloader
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, ImageSequenceClip, CompositeVideoClip, concatenate_videoclips
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
from scipy.io.wavfile import write
from gradio_client import Client
from gtts import gTTS
from config import *
from aqa.utils.enums import Languages, News, VNExVNCategories


def concat_videos(list_videos, outfile):
    # Concat videos
    final = concatenate_videoclips(list_videos)
    # Write output to the file
    final.write_videofile(outfile)


def read_txt(file):
    try:
        with open(file, 'r') as f:
            data = f.read()
            f.close()
            return data
    except Exception:
        print('File does not exist')


def write_txt_w_path(data, file_path):
    try:
        with open(file_path, 'w') as outfile:
            outfile.write(data)
        outfile.close()
    except Exception:
        print('File does not exist')


def add_text_into_video(video_file, edited_video_file='edited_video.mp4'):
    # Required:
    # brew install imagemagick
    # brew install ghostscript
    # loading video dsa gfg intro video
    clip = VideoFileClip(video_file)

    # # clipping of the video
    # # getting video for only starting 10 seconds
    # clip = clip.subclip(0, 10)
    #
    # # Reduce the audio volume (volume x 0.8)
    # clip = clip.volumex(0.8)

    # Generate a text clip
    # Avenir-Book, Avenir-Oblique, Avenir-Roman, Bookman-Demi, Bodoni-Moda-SemiBold, Palatino, Times-New-Roman, Verdana
    # fonts = TextClip.list('font')

    txt_clip = TextClip("Nghe Tin 2024", font='Bookman-Demi', fontsize=24, color='blue').set_duration(10).set_pos('East')

    # setting position of text in the center and duration will be 10 seconds
    txt_clip = txt_clip.set_pos((10, 20))

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])

    # Get the file name from the last "/"
    video_file_name = video_file.rsplit('/', 1)[-1]
    edited_video = video_file.replace(video_file_name, edited_video_file)
    # showing video
    video.write_videofile(edited_video)

    return edited_video


def make_images_clip(images):
    image_clips = []
    for img in images:
        if img.endswith(('.jpeg', '.png', '.jpg')):
            ic = ImageClip(img).set_duration(5)
            image_clips.append(ic)


def create_video(gif_file, mp3_file, video_folder, cat=VNExVNCategories.VN_TIN_NONG, filename="video.mp4"):
    audio = AudioFileClip(mp3_file)
    video = VideoFileClip(gif_file).set_duration(audio.duration).set_audio(audio)
    # # Speed up clip
    # video = video.speedx(1.15)

    # audio = AudioFileClip(mp3_file)
    # gf = VideoFileClip(gif_file)
    # video = VideoFileClip(gif_file).set_duration(audio.duration)
    # video = video.set_audio(audio)
    # gf = loop(gf, duration=video.duration)
    # final1 = CompositeVideoClip([video, gf])
    """
    image = ImageClip('image.png', duration=5)
    image = image.set_position(lambda t: ('center', t * 10 + 50))
    image.fps = 30
    """
    logo = (
        # ImageClip(f"{LOGO_DIR}/{VNExVNCategories.get_logo_from_category(cat)}")
        ImageClip('/Users/trieutruong/github/mktg-bot/aqa/assets/logo/logo_sample.png')
        .set_duration(video.duration)
        .resize(height=100)
        .margin(left=10, top=10, opacity=0)
        .set_position((0, 0))
    )
    final = CompositeVideoClip([video, logo])
    video_file = f"{video_folder}/{filename}"
    final.subclip(0).write_videofile(
        filename=video_file, codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    return video_file


def convert_wav_to_mp3(file_path):
    wav = file_path
    cmd = 'lame --preset insane %s' % wav
    # export will be generated the same folder
    subprocess.call(cmd, shell=True)
    return file_path.replace(".wav", ".mp3")


def resize_image_pixel(infile, pixel, outfile):
    base_width = pixel
    img = Image.open(infile)
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save(outfile)


def covert_images_to_gif(folder, f_out='image.gif'):
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.jpeg', '.png', '.jpg')):
            filenames.append(f"{folder}/{filename}")

    if not filenames:
        print("No images found to create the GIF.")
    else:
        # Use exit stack to automatically close opened images
        with contextlib.ExitStack() as stack:
            # Lazily load images
            imgs = (stack.enter_context(Image.open(f)) for f in sorted(filenames))

            # Extract the first image from the iterator
            img = next(imgs)

            gif_f_out = f"{folder}/{f_out}"
            # Save the GIF file
            img.save(fp=gif_f_out, format='GIF', append_images=imgs,
                     save_all=True, duration=10000, loop=0)

    return gif_f_out


def create_news_folder(src=News.VNE, cat=VNExVNCategories.VN_TIN_NONG):
    # Main folder of a news
    NEWS_RESOURCES_DIR = f"{RESOURCES_DIR}/{src}"
    os.makedirs(NEWS_RESOURCES_DIR, exist_ok=True)

    # Category folder
    CATEGORY_DIR = f"{NEWS_RESOURCES_DIR}/{cat}"
    os.makedirs(CATEGORY_DIR, exist_ok=True)

    # Get the current date in yyyy-mm-dd format
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create a folder name with the current date and sequence number
    sequence_number = 1
    while os.path.exists(f"{CATEGORY_DIR}/{current_date}-{sequence_number:04d}"):
        sequence_number += 1

    folder_name = f"{CATEGORY_DIR}/{current_date}-{sequence_number:04d}"
    os.makedirs(folder_name)

    # Create media folders
    content_folder = f"{folder_name}/content"
    images_folder  = f"{folder_name}/images"
    audio_folder   = f"{folder_name}/audio"
    video_folder   = f"{folder_name}/video"
    os.makedirs(video_folder)
    os.makedirs(images_folder)
    os.makedirs(audio_folder)
    os.makedirs(content_folder)

    return content_folder, images_folder, audio_folder, video_folder


def write_content_into_file(content, save_to):
    # Specify the file path
    file_path = f"{save_to}/content"

    # Open the file in write mode and write the text
    with open(file_path, 'w') as file:
        file.write(content)
    print('Write content successful')


def get_content_from_url(url):
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    return page_content


def parse_image_urls(content, classes, location, source):
    soup = BeautifulSoup(content, "html.parser")
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
    return results


def save_urls_to_csv(image_urls, save_to):
    df = pd.DataFrame({"links": image_urls})
    df.to_csv(f"{save_to}/links.csv", index=False, encoding="utf-8")


def get_and_save_image_to_file(image_url, output_dir):
    image_content = requests.get(image_url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
    file_path = output_dir / filename
    image.save(file_path, "PNG", quality=80)


def download_images_from_url(url, src, save_to):
    cont = get_content_from_url(url)

    # Each news site will have different classes
    image_urls = None
    img_classes = 'fig-picture'
    if src == News.VNE:
        img_classes = 'fig-picture'
    image_urls = parse_image_urls(
        content=cont, classes=img_classes, location="img", source="src"
    )
    save_urls_to_csv(image_urls, save_to)

    for image_url in image_urls:
        get_and_save_image_to_file(
            image_url, output_dir=Path(save_to)
        )


def read_content_from_url(url, src, lang, save_to):
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f, 'html.parser')

    # get the text content of the webpage
    text = soup.get_text()
    cleaned_text = re.sub(r'\n\s*\n', '\n', text)

    # Clean content
    cleaned_footer_text = remove_redundant_lines_up_from_char(cleaned_text)
    cleaned_header_text = remove_all_redundant_lines_from_str(cleaned_footer_text)

    # Add news source
    news_source = f"\nNguồn tin từ: {News.get_news_name(src)}" if lang == Languages.VI else f"\nSource: {src}"
    content = cleaned_header_text + news_source

    # TODO: Count words. Use AI to cut down content to XXX words if long content

    # Get news title
    title = content.split('\n')[1]

    # Write content into file
    write_content_into_file(content, save_to)
    print('Read content from URL successful')
    return title, content


def remove_redundant_lines_up_from_char(text, char='×', lines_to_remove=3):
    lines = text.split('\n')
    index_to_remove = -1

    for i, line in enumerate(lines):
        if char in line:
            index_to_remove = i
            break

    if index_to_remove != -1:
        lines = lines[:index_to_remove - lines_to_remove] + lines[index_to_remove + 1:]

    result = '\n'.join(lines)
    return result


def find_characters_before_comma_at(line, comma_at):
    comma_indices = [pos for pos, char in enumerate(line) if char == ',']
    if 0 < comma_at <= len(comma_indices):
        index = comma_indices[comma_at - 1]
        return line[:index]

    return None


def remove_all_redundant_lines_from_str(text, str_to_find='(GMT+7)'):
    lines = text.split('\n')
    index_to_remove = -1

    for i, line in enumerate(lines):
        if str_to_find in line:
            index_to_remove = i
            break

    if index_to_remove != -1:
        lines = lines[index_to_remove:]
        lines[0] = find_characters_before_comma_at(lines[0], 2)

    result = '\n'.join(lines)
    return result


def audio_recording(freq=44100, duration=60):

    # Start recorder with the given values
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    # Record audio for the given number of seconds
    sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    write(f"{RESOURCES_DIR}/recording0.wav", freq, recording)

    # Convert the NumPy array to audio file
    # wv.write("recording1.wav", recording, freq, sampwidth=2)


def gtts_text_to_speech(text, save_to, lang=Languages.VI):
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang=lang, slow=False, tld='com')

    # Save the audio file to a temporary file
    speech_file = f'{save_to}/audio.mp3'
    speech.save(speech_file)

    # # Play the audio file
    # os.system('afplay ' + speech_file)
    return speech_file


def move_file(file_path, new_path):
    # Check if the file exists at the original path
    if os.path.exists(file_path):
        # Move the file to the new location
        shutil.move(file_path, new_path)
        print("File moved successfully!")
    else:
        print("File does not exist at the specified path.")


def viet_tts(text, save_to, lang=Languages.VI, voice='female-voice'):
    response = requests.post("https://ntt123-viettts.hf.space/run/predict", json={
        "data": [
            text,
        ]
    }).json()

    data = response["data"]
    file_name = data[0].get('name')
    print(file_name)

def text_to_speech(text, save_to, lang=Languages.VI, voice='female-voice'):
    if lang == Languages.VI:
        """
        GitHub: https://github.com/NTT123/vietTTS
        :param text: Content for generating audio
        :param save_to: Path to save generated audio file
        :param voice: female-voice/male-voice
        :return: Path to generated file
        """
        client = Client(f"https://ntt123-vietnam-{voice}-tts.hf.space/")
        file_path = client.predict(
                        f"{text}",
                        api_name="/predict"
        )
        print(f"from: {file_path}")
        new_file_path = f"{save_to}/audio.wav"
        # time.sleep(3)
        move_file(file_path, new_file_path)
        print(f"to:   {new_file_path}")
        return convert_wav_to_mp3(new_file_path)
    elif lang == Languages.EN:
        # Initialize gTTS with the text to convert
        speech = gTTS(text, lang='en', slow=False, tld='com')

        # Save the audio file to a temporary file
        speech_file = f'{save_to}/audio.mp3'
        speech.save(speech_file)

        # # Play the audio file
        # os.system('afplay ' + speech_file)
        return speech_file


def generate_news_video(url, src=News.VNE, cat=VNExVNCategories.VN_TIN_NONG, lang=Languages.VI):
    c_folder, i_folder, a_folder, v_folder = create_news_folder(src, cat)
    content = read_content_from_url(url, src, lang, c_folder)
    download_images_from_url(url, src, i_folder)
    gif_file = covert_images_to_gif(i_folder)

    audio_file = text_to_speech(
        text=content,
        save_to=a_folder,
        lang=lang,
        voice='female-voice'
    )
    create_video(
        gif_file=gif_file,
        mp3_file=audio_file,
        video_folder=v_folder
    )
    print('Generated news video successful!')


# Begin region youtube
def convert_to_mp3(filename):
    clip = VideoFileClip(filename)
    clip.audio.write_audiofile(filename[:-4] + ".mp3")
    clip.close()


def download_video(url, resolution):
    itag = choose_resolution(resolution)
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    return stream.default_filename

def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)

def download_playlist(url, resolution):
    playlist = pytube.Playlist(url)
    download_videos(playlist.video_urls, resolution)

def choose_resolution(resolution):
    if resolution in ["low", "360", "360p"]:
        itag = 18
    elif resolution in ["medium", "720", "720p", "hd"]:
        itag = 22
    elif resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        itag = 137
    elif resolution in ["very high", "2160", "2160p", "4K", "4k"]:
        itag = 313
    else:
        itag = 18
    return itag


def input_links():
    print("Enter the links of the videos (end by entering 'STOP'):")

    links = []
    link = ""

    while link != "STOP" and link != "stop":
        link = input()
        links.append(link)

    links.pop()

    return links


def download_convert_youtube_to_mp3():
    print("Welcome to NeuralNine YouTube Downloader and Converter v0.2 Alpha")
    print("Loading...")
    print('''
    What do you want?
    
    (1) Download YouTube Videos Manually
    (2) Download a YouTube Playlist
    (3) Download YouTube Videos and Convert Into MP3
    
    Downloading copyrighted YouTube videos is illegal!
    I am not responsible for your downloads! Go at your own risk!
    
    Copyright (c) NeuralNine 2020
    ''')

    choice = input("Choice: ")

    if choice == "1" or choice == "2":
        quality = input("Please choose a quality (low, medium, high, very high):")
        if choice == "2":
            link = input("Enter the link to the playlist: ")
            print("Downloading playlist...")
            youtube_downloader.download_playlist(link, quality)
            print("Download finished!")
        if choice == "1":
            links = youtube_downloader.input_links()
            for link in links:
                youtube_downloader.download_video(link, quality)
    elif choice == "3":
        links = youtube_downloader.input_links()
        for link in links:
            print("Downloading...")
            filename = youtube_downloader.download_video(link, 'low')
            print("Converting...")
            convert_to_mp3(filename)
    else:
        print("Invalid input! Terminating...")


# End region youtube


if __name__ == '__main__':
    # print(create_news_folder(News.VNE, VNExVNCategories.VN_TIN_NONG))
    # generate_news_video(
    #     url='https://vnexpress.net/tp-hcm-khoi-dong-lai-trung-tam-trien-lam-dang-do-hon-10-nam-4757006.html',
    #     src=News.VNE,
    #     cat=VNExVNCategories.VN_THOI_SU,
    #     lang=Languages.VI
    # )

    # create_video(
    #     '/Users/trieutruong/github/mktg-bot/resources/vnexpress/vn_thoi_su/2024-06-12-0001/images/image.gif',
    #     '/Users/trieutruong/github/mktg-bot/resources/vnexpress/vn_thoi_su/2024-06-12-0001/audio/audio.mp3',
    #     '/Users/trieutruong/github/mktg-bot/resources/vnexpress/vn_thoi_su/2024-06-12-0001/video'
    # )

    content = 'Khi Bellingham rời sân ở phút 86, nhường vị trí cho Kobbie Mainoo, khán giả tuyển Anh đồng loạt đứng dậy vỗ tay tán thưởng tiền vệ số 10. Không chỉ ghi bàn duy nhất, anh còn chơi xông xáo, liên tiếp bị phạm lỗi và cũng khiêu khích đối thủ. Tài năng của tiền vệ CLB Real Madrid là điểm khác biệt của trận cầu khan hiếm cơ hội, khi mỗi đội chỉ dứt điểm năm lần.'
    viet_tts(text=content, save_to=CODE_HOME)
    pass
