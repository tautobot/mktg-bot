import json
import shutil
import subprocess
import paramiko
import psycopg2
# import sounddevice as sd
# import wavio as wv
# from scipy.io.wavfile import wav_write
import subprocess
import re
import urllib.request
import hashlib
import io
import requests
import contextlib
import pandas as pd
import pytube
from aqa.utils import youtube
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    TextClip,
    ImageSequenceClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
from gradio_client import Client
from gtts import gTTS
from config import *
from aqa.utils.enums import Languages, News, VNExVNCategories


class NewsObj:
    def __init__(self):
        self._thumbs = []
        self._title = None
        self._news_url = None
        self._desc = None
        self._content = None


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

    txt_clip = TextClip("Nghe Tin 2024", font='Bookman-Demi', fontsize=24, color='blue').set_duration(10).set_pos(
        'East')

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
    images_folder = f"{folder_name}/images"
    audio_folder = f"{folder_name}/audio"
    video_folder = f"{folder_name}/video"
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


def read_content_from_url(url, src=News.VNE, lang=Languages.VI, save_to=None):
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f, 'html.parser')

    # get the text content of the webpage
    text = soup.get_text()
    cleaned_text = re.sub(r'\n\s*\n', '\n', text)

    # Clean content
    cleaned_footer_text = remove_redundant_lines_up_from_char(cleaned_text)
    cleaned_header_text = remove_all_redundant_lines_from_str(cleaned_footer_text)

    # Remove duplicated lines if any
    unique_lines = '\n'.join(set(cleaned_header_text.splitlines()))

    # Add news source
    news_source = f"\nNguồn tin từ: {News.get_news_name(src)}" if lang == Languages.VI else f"\nSource: {src}"
    content = unique_lines + news_source

    # TODO: Count words. Use AI to cut down content to XXX words if long content

    # Get news title
    title = content.split('\n')[1]

    # Write content into file
    # write_content_into_file(content, save_to)
    print('Read content from URL successful')
    return title, content


def collect_mp3_url(url, src, lang, save_to):
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f, 'html.parser')

    # Find all the news articles
    news_articles = soup.find_all(lambda tag: tag.has_attr('class') and 'item-news' in tag['class'])
    # elements = soup.find_all(lambda tag: tag.has_attr('class') and 'your_text' in tag['class'])

    # Extract and print the news titles
    for art in news_articles:
        thumb1 = None
        thumb2 = None
        title = None
        news_url = None
        desc = None
        content = None

        e_thumb = art.find_next('div', class_='thumb-art')
        e_title = art.find_next('h2', class_='title-news')
        e_news_url = art.find_next('h2', class_='title-news')
        e_desc = art.find_next('p', class_='description')
        if e_thumb:
            a_thumbs = e_thumb.find_all(lambda tag: tag.has_attr('srcset') or tag.has_attr('data-srcset'))[-1]
            thumbs = a_thumbs.attrs.get('srcset') if 'srcset' in a_thumbs.attrs else a_thumbs.attrs.get('data-srcset')
            thumb1 = thumbs.split(',')[0].strip().split(' ')[0]
            thumb2 = thumbs.split(',')[1].strip().split(' ')[0]
        if e_title:
            title = e_title.find_next('a', title=True).attrs.get('title')
        if e_news_url:
            news_url = e_news_url.find_next('a', href=True).attrs.get('href')
            _, content = read_content_from_url(news_url)
        if e_desc:
            desc = e_desc.find_next('a', title=True).text.strip()

        news_obj._thumbs.append(thumb1)
        news_obj._thumbs.append(thumb2)
        news_obj._title = title
        news_obj._news_url = news_url
        news_obj._desc = desc
        news_obj._content = content

        print(f"thumb1 : {thumb1}")
        print(f"thumb2 : {thumb2}")
        print(f"title  : {title}")
        print(f"url    : {news_url}")
        print(f"desc   : {desc}")
        print(f"content: {content}")
        print('\n')

        return news_obj


def collect_all_sub_urls_from_url(url, src, lang, save_to):
    news_obj = NewsObj()
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f, 'html.parser')

    # Find all the news articles
    news_articles = soup.find_all(lambda tag: tag.has_attr('class') and 'item-news' in tag['class'])
    # elements = soup.find_all(lambda tag: tag.has_attr('class') and 'your_text' in tag['class'])

    # Extract and print the news titles
    for art in news_articles:
        thumb1 = None
        thumb2 = None
        title = None
        news_url = None
        desc = None
        content = None

        e_thumb = art.find_next('div', class_='thumb-art')
        e_title = art.find_next('h2', class_='title-news')
        e_news_url = art.find_next('h2', class_='title-news')
        e_desc = art.find_next('p', class_='description')
        if e_thumb:
            a_thumbs = e_thumb.find_all(lambda tag: tag.has_attr('srcset') or tag.has_attr('data-srcset'))[-1]
            thumbs = a_thumbs.attrs.get('srcset') if 'srcset' in a_thumbs.attrs else a_thumbs.attrs.get('data-srcset')
            thumb1 = thumbs.split(',')[0].strip().split(' ')[0]
            thumb2 = thumbs.split(',')[1].strip().split(' ')[0]
        if e_title:
            title = e_title.find_next('a', title=True).attrs.get('title')
        if e_news_url:
            news_url = e_news_url.find_next('a', href=True).attrs.get('href')
            _, content = read_content_from_url(news_url)
        if e_desc:
            desc = e_desc.find_next('a', title=True).text.strip()

        news_obj._thumbs.append(thumb1)
        news_obj._thumbs.append(thumb2)
        news_obj._title = title
        news_obj._news_url = news_url
        news_obj._desc = desc
        news_obj._content = content

        print(f"thumb1 : {thumb1}")
        print(f"thumb2 : {thumb2}")
        print(f"title  : {title}")
        print(f"url    : {news_url}")
        print(f"desc   : {desc}")
        print(f"content: {content}")
        print('\n')

        return news_obj


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


# def audio_recording(freq=44100, duration=60):
#     # Start recorder with the given values
#     # of duration and sample frequency
#     recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
#     # Record audio for the given number of seconds
#     sd.wait()
#
#     # This will convert the NumPy array to an audio
#     # file with the given sampling frequency
#     write(f"{RESOURCES_DIR}/recording0.wav", freq, recording)
#
#     # Convert the NumPy array to audio file
#     wv.write("recording1.wav", recording, freq, sampwidth=2)


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


# region YouTube

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

# endregion YouTube


# region facebook/MusicGen

def generate_music(desc, audio_sample=None):
    client = Client("https://facebook-musicgen.hf.space/")
    result = None
    if desc and audio_sample:
        result = client.predict(
            "Howdy!",  # str  in 'Describe your music' Textbox component
            "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",
            # str (filepath or URL to file) in 'File' Audio component
            fn_index=0
        )
    elif not desc and audio_sample:
        result = client.predict(
            audio_sample,  # str  in 'Condition on a melody (optional) File or Mic' Radio component
            fn_index=1
        )
    elif desc and not audio_sample:
        result = client.predict(
            desc,  # str  in 'Condition on a melody (optional) File or Mic' Radio component
            fn_index=2
        )

    print(result)


def detect_lang():
    from polyglot.detect import Detector

    mixed_text = u"""
    China (simplified Chinese: 中国; traditional Chinese: 中國),
    officially the People's Republic of China (PRC), is a sovereign state
    located in East Asia.
    """
    for language in Detector(mixed_text).languages:
        print(language)

# endregion facebook/MusicGen


def detect_lang_fasttext():
    import fasttext
    mixed_text = u"""[Verse]
こんにちは、ワールド
ピンクの髪が明るくてくるくる
白い服が軽やかに
昼も夜も踊り続ける

[Verse 2]
夢のようにかわいい
ビームのように輝く
ヘッドホンをしっかりつけて
音楽が私を新たな高みへ連れて行く

[Chorus]
私は日本の女の子
ピンクと白の渦の中
かわいい夢が広がる
踊ってくるくる踊ってくるくる"""
    text_with_escape_sequence = mixed_text.replace('\n', r'\n')

    model = fasttext.load_model('/Users/trieutruong/github/mktg-bot/aqa/utils/lid.176.bin')
    res_ = model.predict(text_with_escape_sequence, k=3)  # top 2 matching languages
    print(res_)


# def trim_audio():
#     # pipenv install ffmpeg-python
#     import ffmpeg
#
#     audio_input = ffmpeg.input("output_sounddevice.wav")
#     audio_cut = audio_input.audio.filter('atrim', duration=1)
#     audio_output = ffmpeg.output(audio_cut, 'trimmed_output_ffmpeg.wav', format='wav')
#     ffmpeg.run(audio_output)

def trim_audio():
    # pipenv install pydub
    from pydub import AudioSegment

    # start at 0 milliseconds
    # end at 1500 milliseconds
    start = 0
    end = 1500

    sound = AudioSegment.from_wav("output_pyaudio.wav")
    extract = sound[start:end]

    extract.export("trimmed_output_pydub.wav", format="wav")


def change_audio_speed():
    from pydub import AudioSegment

    sound = AudioSegment.from_mp3('input_audio.mp3')
    sound_w_new_fs = sound.set_frame_rate(16000)
    sound_w_new_fs.export("/Users/trieutruong/github/mktg-bot/output_audio.mp3", format="mp3")


def change_volume():
    from pydub import AudioSegment
    from pydub.playback import play

    sound = AudioSegment.from_wav("new_fs_output_pydub.wav")

    # 3 dB up
    louder = sound + 3
    # 3 dB down
    quieter = sound - 3

    play(louder)
    play(quieter)

    louder.export("louder_output.wav", format="wav")
    quieter.export("quieter_output.wav", format="wav")

def combine_audio():
    from pydub import AudioSegment
    from pydub.playback import play

    sound1 = AudioSegment.from_wav("louder_output.wav")
    sound2 = AudioSegment.from_wav("quieter_output.wav")

    combined = sound1 + sound2

    play(combined)
    combined.export("louder_and_quieter.wav", format="wav")

def overlay_audio():
    from pydub import AudioSegment
    from pydub.playback import play

    sound1 = AudioSegment.from_wav("louder_output.wav")
    sound2 = AudioSegment.from_wav("quieter_output.wav")

    overlay = sound1.overlay(sound2, position=1000)

    play(overlay)
    overlay.export("overlaid_1sec_offset.wav", format="wav")

def change_audio_format():
    from pydub import AudioSegment

    wav_audio = AudioSegment.from_wav("louder_output.wav")
    mp3_audio = wav_audio.export("louder.mp3", format="mp3")


def deepgram_speech_to_text_online_file():
    # pipenv install deepgram-sdk
    import requests
    from config import DEEPGRAM_API_KEY
    import asyncio, json

    PATH_TO_FILE = 'louder_output.wav'

    async def main():
        # Initializes the Deepgram SDK
        # deepgram = Deepgram(DEEPGRAM_API_KEY)
        url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"

        payload = json.dumps({
            "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
        })
        headers = {
            'Authorization': f'Token {DEEPGRAM_API_KEY}',
            'content-type' : 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Open the audio file
        with open(PATH_TO_FILE, 'rb') as audio:
            # ...or replace mimetype as appropriate
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            # response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
            json_obj = json.dumps(response, indent=4)
            print(json_obj)
            with open("transcribed.txt", "w") as f:
                f.write(json_obj)

    asyncio.run(main())

def deepgram_speech_to_text_local_file():
    # pipenv install deepgram-sdk
    from deepgram import Deepgram
    from config import DEEPGRAM_API_KEY
    import asyncio, json

    PATH_TO_FILE = 'louder_output.wav'

    async def main():
        # Initializes the Deepgram SDK
        deepgram = Deepgram(DEEPGRAM_API_KEY)
        # Open the audio file
        with open(PATH_TO_FILE, 'rb') as audio:
            # ...or replace mimetype as appropriate
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
            json_obj = json.dumps(response, indent=4)
            print(json_obj)
            with open("transcribed.txt", "w") as f:
                f.write(json_obj)

    asyncio.run(main())


def get_list_songs(res):
    result_key = None
    for key in res:
        if 'result' in output[key]:
            result_key = key
            break
    # Accessing the "result" data using the found key
    if result_key:
        result_data = res.get(result_key).get("result") or []
        # Printing the "result" data
        return result_data
    else:
        print("No 'result' data found in the output.")


def extend_audio():
    from pymusiclooper.handler import MusicLooper

    # Specify the input audio file and output file
    input_audio_file = f"{CODE_HOME}/input_audio.mp3"
    output_audio_file = f"{CODE_HOME}/output_audio_extended.mp3"

    # Create a MusicLooper instance
    music_looper = MusicLooper(input_audio_file)

    # Find loop pairs for the audio file
    loop_pairs = music_looper.find_loop_pairs()

    # Choose a loop pair (example: the first loop pair)
    loop_start = loop_pairs[0].loop_start
    loop_end = loop_pairs[0].loop_end
    # Extend the audio file to 360 seconds
    music_looper.extend(
        loop_start=loop_start,
        loop_end=loop_end,
        extended_length=360,
        format="mp3",
        output_dir='/Users/trieutruong/github/mktg-bot/LooperOutput')

    print("Audio file extended successfully to 6 minutes.")


def write_img_base64(data_url):
    import base64
    # Extract base64 data from the URL
    base64_data = data_url.split(",")[1]

    # Decode base64 data to binary
    image_data = base64.b64decode(base64_data)

    # Write binary image data to a file
    with open(f"{CODE_HOME}/image.jpg", "wb") as file:
        file.write(image_data)

    print("Image data extracted and saved to 'image.jpg'")


def add_static_image_to_audio(image_path, audio_path, output_path):
    from moviepy.editor import AudioFileClip, ImageClip
    """Create and save a video file to `output_path` after 
    combining a static image that is located in `image_path` 
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path)


if __name__ == '__main__':

    # change_audio_speed()
    url = """data:image/jpg;base64,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"""
    write_img_base64(url)
