from moviepy.editor import VideoFileClip, AudioFileClip, VideoClip, ImageClip, concatenate_videoclips
import os
import shutil
import cv2
import numpy as np
import random
import math
import time
import imageio
from aqa.utils.enums import VideoEffectType
from config import CODE_HOME
from concurrent.futures import ThreadPoolExecutor
import subprocess

# Firefly class
class Firefly:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # self.update_position()
        self.pos = [random.randint(0, self.screen_width), random.randint(0, self.screen_height)]
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.size = random.randint(1, 2)
        self.color = (255, 255, 100)
        self.brightness = 255
        self.glow_radius = random.randint(2, 4)
        self.glow_intensity = random.uniform(0.5, 1.0)
        self.transition_speed = random.uniform(0.001, 0.005)
        self.transition_offset = random.uniform(0, 3 * math.pi)
        self.start_time = time.time()

    def update_position(self):
        self.pos = [random.randint(0, self.screen_width), random.randint(0, self.screen_height)]
        # self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        # self.size = random.randint(1, 2)
        # self.brightness = (100, 255, 100)
        # self.glow_radius = random.randint(2, 4)
        # self.glow_intensity = random.uniform(0.5, 1.0)
        # self.transition_speed = random.uniform(0.001, 0.005)
        # self.transition_offset = random.uniform(0, 3 * math.pi)
        # self.start_time = time.time()

    def update(self):
        elapsed_time = (time.time() * 1000) - self.start_time
        # self.brightness = int(
        #     127.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 127.5)
        brightness_factor = 127.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 127.5

        # Transition from light green to light yellow to light gray
        if brightness_factor <= 127.5:
            # Light green to light yellow transition
            green_intensity = 255 - int(brightness_factor * 2)
            yellow_intensity = int(brightness_factor * 2)
            self.color = (green_intensity, yellow_intensity, 100)
        else:
            # Light yellow to light gray transition
            yellow_intensity = 255 - int((brightness_factor - 127.5) * 2)
            gray_intensity = int((brightness_factor - 127.5) * 2)
            self.color = (yellow_intensity, yellow_intensity, gray_intensity)

        self.brightness = int(brightness_factor)
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.pos[0] < 0 or self.pos[0] > self.screen_width or self.pos[1] < 0 or self.pos[1] > self.screen_height:
            self.update_position()


class FirefliesSimulation:
    def __init__(self, screen_width, screen_height, num_fireflies):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fireflies = [Firefly(screen_width, screen_height) for _ in range(num_fireflies)]

    def update(self):
        for firefly in self.fireflies:
            firefly.update()

    def draw(self, frame):
        frame = frame.copy()
        overlay = np.zeros_like(frame)
        for firefly in self.fireflies:
            # cv2.circle(overlay, (firefly.x, firefly.y), firefly.size, firefly.color, -1)  # Draw snowflake
            # blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
            # frame = cv2.addWeighted(frame, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame
            # color = (0, 0, 255) if firefly.brightness > 127 else (firefly.brightness, firefly.brightness, firefly.brightness)
            cv2.circle(overlay, (int(firefly.pos[0]), int(firefly.pos[1])), firefly.size + firefly.glow_radius, firefly.color, -1)
            blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
            frame = cv2.addWeighted(frame, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame
        return frame

    def draw_on_screen(self):
        screen = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)  # Create a black screen
        overlay = np.zeros_like(screen)
        for firefly in self.fireflies:
            cv2.circle(overlay, (int(firefly.pos[0]), int(firefly.pos[1])), firefly.size + firefly.glow_radius,
                       firefly.color, -1)
            blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
            screen = cv2.addWeighted(screen, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame

        cv2.imshow('Snowfall Simulation', screen)


class Snowflake:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)  # Random x position within screen width
        self.y = random.randint(0, screen_height)  # Random y position within screen height
        self.size = random.randint(2, 7)  # Random size of the snowflake
        self.speed = random.randint(1, 7)  # Random falling speed of the snowflake
        self.color = (255, 255, 255)  # White color for the snowflake
        self.transition_speed = random.uniform(0.001, 0.005)
        self.transition_offset = random.uniform(0, 5 * math.pi)
        self.start_time = time.time()

    def update(self, screen_height):
        elapsed_time = (time.time() * 1000) - self.start_time
        # Blue
        # self.color = int(127.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 127.5)
        # White
        self.color = tuple(
            int(255 * (0.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 0.5)) for _ in
            range(3))
        self.y += self.speed  # Move the snowflake down
        if self.y > screen_height:  # If snowflake goes below the screen, reset its position
            self.y = 0


class SnowfallSimulation:
    def __init__(self, screen_width, screen_height, num_snowflakes):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snowflakes = [Snowflake(screen_width, screen_height) for _ in range(num_snowflakes)]

    def update(self):
        for snowflake in self.snowflakes:
            snowflake.update(self.screen_height)

    def draw(self, frame):
        frame = frame.copy()
        overlay = np.zeros_like(frame)
        for snowflake in self.snowflakes:
            cv2.circle(overlay, (snowflake.x, snowflake.y), snowflake.size, snowflake.color, -1)  # Draw snowflake
            blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
            frame = cv2.addWeighted(frame, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame
        return frame

    def draw_on_screen(self):
        screen = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)  # Create a black screen
        for snowflake in self.snowflakes:
            cv2.circle(screen, (snowflake.x, snowflake.y), snowflake.size, snowflake.color, -1)  # Draw snowflake
            # cv2.line(screen, (snowflake.x, snowflake.y), (snowflake.x, snowflake.y + snowflake.length), snowflake.color, 1)  # Draw raindrop

        cv2.imshow('Snowfall Simulation', screen)


class Raindrop:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)  # Random x position within screen width
        self.y = random.randint(0, screen_height)  # Random y position within screen height
        self.length = random.randint(3, 20)  # Random length of the raindrop
        self.speed = random.randint(10, 30)  # Random falling speed of the raindrop
        self.color = (255, 255, 255)  # White color for the raindrop
        self.transition_speed = random.uniform(0.001, 0.005)
        self.transition_offset = random.uniform(0, 10 * math.pi)
        self.start_time = time.time()

    def update(self, screen_height):
        elapsed_time = (time.time() * 1000) - self.start_time
        # Blue
        # self.color = int(127.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 127.5)
        # White
        self.color = tuple(
            int(255 * (0.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 0.5)) for _ in
            range(3))
        self.y += self.speed  # Move the snowflake down
        if self.y > screen_height:  # If snowflake goes below the screen, reset its position
            self.y = 0


class RainSimulation:
    def __init__(self, screen_width, screen_height, num_raindrops):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.raindrops = [Raindrop(screen_width, screen_height) for _ in range(num_raindrops)]

    def update(self):
        for raindrop in self.raindrops:
            raindrop.update(self.screen_height)

    def draw(self, frame):
        frame = frame.copy()
        for raindrop in self.raindrops:
            # cv2.circle(screen, (snowflake.x, snowflake.y), snowflake.size, snowflake.color, -1)  # Draw snowflake
            cv2.line(frame, (raindrop.x, raindrop.y), (raindrop.x, raindrop.y + raindrop.length), raindrop.color, 1)  # Draw raindrop
        return frame

    def draw_on_screen(self):
        screen = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)  # Create a black screen
        overlay = np.zeros_like(screen)
        for raindrop in self.raindrops:
            cv2.line(screen, (raindrop.x, raindrop.y), (raindrop.x, raindrop.y + raindrop.length), raindrop.color, 1)  # Draw raindrop
            blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
            screen = cv2.addWeighted(screen, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame

        cv2.imshow('Snowfall Simulation', screen)

def add_effect_into_video(effect, input_video_path='input_video.mp4', output_video_path='output_video.mp4'):
    # Load input video with audio
    video_clip = VideoFileClip(input_video_path)

    # Video settings
    fps = video_clip.fps
    width, height = video_clip.size

    effects = []

    if effect == VideoEffectType.FIREFLIES:
        effects = [FirefliesSimulation(width, height, 15)]  # Create fireflies effect simulation with 7 fireflies
    elif effect == VideoEffectType.SNOWFALL:
        effects = [SnowfallSimulation(width, height, 15)]  # Create fireflies effect simulation with 15 snowflakes
    elif effect == VideoEffectType.RAINDROPS:
        effects = [RainSimulation(width, height, 20)]  # Create raindrops effect simulation with 20 raindrops

    # Main loop for processing each frame of the input video
    def process_frame(t):
        frame = video_clip.get_frame(t)
        for e in effects:
            e.update()
            frame = e.draw(frame)
        return frame

    if len(effects) > 0:
        # Process each frame and create the output video
        output_clip = VideoClip(process_frame, duration=video_clip.duration)
        output_clip = output_clip.set_audio(video_clip.audio)  # Retain the original audio

        # Write the output video with audio to a file
        output_clip.write_videofile(
            filename=output_video_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        # Close input video clip
        video_clip.close()


def create_video_f_image_n_audio(input_image_path, input_audio_path, output_video_path):
    # Load the input image
    image_clip = ImageClip(input_image_path)

    # Load the input audio file
    audio_clip = AudioFileClip(input_audio_path)

    # Get the duration of the audio clip
    audio_duration = audio_clip.duration

    # Create a video clip with the input image and audio
    video_clip = image_clip.set_audio(audio_clip)

    # Set the duration of the video clip to match the duration of the audio clip
    video_clip = video_clip.set_duration(audio_duration)

    # Write the video to a file
    video_clip.write_videofile(output_video_path, fps=24, codec="libx264", audio_codec='aac')

    print("Video has been created successfully!")


def create_gif_w_effect(input_image_path, output_image_path):
    # Load your image
    image = cv2.imread(input_image_path)

    # Create FirefliesSimulation object
    screen_width = image.shape[1]
    screen_height = image.shape[0]
    num_fireflies = 7
    simulation = FirefliesSimulation(screen_width, screen_height, num_fireflies)

    # Create a list to store frames
    frames = []

    # Loop for 10 seconds and create frames
    start_time = time.time()
    while time.time() - start_time < 1:
        simulation.update()
        frame = simulation.draw(image)
        frames.append(frame)

    # Save frames as a gif
    imageio.mimsave(output_image_path, frames, duration=0.1)

    print("Gif image has been created successfully!")


# def create_video_from_short_video(input_video_path, output_video_path):
#     # Load the original video
#     original_video = VideoFileClip(input_video_path)
#
#     # Get the duration of the original video in seconds
#     original_duration = original_video.duration
#
#     # Calculate the number of duplicates needed to reach a total duration of 3 hours
#     target_duration = 3 * 60 * 60  # 3 hours in seconds
#     num_duplicates = int(target_duration / original_duration) + 1
#
#     # Duplicate the original video to reach a total duration of 3 hours
#     duplicated_clips = [original_video.copy() for _ in range(num_duplicates)]
#
#     # Merge the duplicated video clips into a single video
#     merged_clip = concatenate_videoclips(duplicated_clips)
#
#     # Write the merged video to a new file
#     merged_clip.write_videofile(output_video_path, codec="libx264", fps=24)
#
#     print("New 3-hour video has been created successfully!")


# def duplicate_video_clip(video_clip):
#     return video_clip.copy()
#
#
# def create_video_from_short_video(input_video_path, output_video_path):
#     # Load the original video
#     original_video = VideoFileClip(input_video_path)
#
#     # Calculate the number of duplicates needed to reach a total duration of 3 hours
#     target_duration = 3 * 60 * 60  # 3 hours in seconds
#     num_duplicates = int(target_duration / original_video.duration) + 1
#
#     # Duplicate the original video clips using multi-threading
#     duplicated_clips = []
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         duplicated_clips = list(executor.map(duplicate_video_clip, [original_video] * num_duplicates))
#
#     # Merge the duplicated video clips into a single video
#     merged_clip = concatenate_videoclips(duplicated_clips)
#
#     # Write the merged video to a new file
#     merged_clip.write_videofile(output_video_path, codec="libx264", fps=24)
#
#     print("New 3-hour video has been created successfully!")


def create_video_from_short_video(input_video_path, output_video_path):
    path                      = os.path.dirname(input_video_path)
    file_name_with_extension  = os.path.basename(input_video_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    video_txt_file            = f"{path}/video_list.txt"

    # Load the original video
    original_video = VideoFileClip(input_video_path)

    # Calculate the number of duplicates needed to reach a total duration of 3 hours
    target_duration = 3 * 60 * 60  # 3 hours in seconds
    num_duplicates = int(target_duration / original_video.duration) + 1

    str_video_list = ''
    for i in range(1, num_duplicates + 1):
        # TODO: Create string for # TODO: Create string by 'ffmpeg -f concat -safe 0 -i <(echo f"{str_video_list}") -c copy output.mp4'
        fname = f'{path}/{file_name}_{i}{file_extension}'
        str_video_list += f"file '{fname}'\n"
        # if i < num_duplicates:
        #     str_video_list += '\n'
        with open(video_txt_file, 'w') as f:
            f.write(str_video_list)
        shutil.copy(input_video_path, fname)

    # Duplicate the original video using ffmpeg
    ffmpeg_cmd = f"ffmpeg -f concat -safe 0 -i {video_txt_file} -c copy {output_video_path}"

    # Write the merged video to a new file
    subprocess.call(ffmpeg_cmd, shell=True)

    print("New 3-hour video has been created successfully!")


def demo_effect(effect=VideoEffectType.FIREFLIES):
    # Example Usage
    width = 400
    height = 300

    effects = []
    if effect == VideoEffectType.FIREFLIES:
        effects = FirefliesSimulation(width, height, 15)  # Create fireflies effect simulation with 7 fireflies
    elif effect == VideoEffectType.SNOWFALL:
        effects = SnowfallSimulation(width, height, 15)  # Create fireflies effect simulation with 15 snowflakes
    elif effect == VideoEffectType.RAINDROPS:
        effects = RainSimulation(width, height, 40)  # Create raindrops effect simulation with 20 raindrops

    running = True
    while running:
        effects.update()
        effects.draw_on_screen()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # pass
    demo_effect(VideoEffectType.RAINDROPS)

    # input_image_path = f'{CODE_HOME}/input/image2.jpeg'
    # input_audio_path = f'{CODE_HOME}/input/lofi_no30_60m00s.mp3'
    # input_audio_file = os.path.basename(input_audio_path)
    # input_audio_file_name, file_extension = os.path.splitext(input_audio_file)
    # output_video_file_name = f'{CODE_HOME}/output/{input_audio_file_name}_{time.time()}.mp4'
    # create_video_f_image_n_audio(input_image_path, input_audio_path, output_video_file_name)

    # input_video_file_name = f'{CODE_HOME}/input/lofi.no30.1724843550.2877781.mp4'
    # file_name_with_extension = os.path.basename(input_video_file_name)
    # file_name, file_extension = os.path.splitext(file_name_with_extension)
    # output_video_file_name = f'{CODE_HOME}/output/{file_name}_{time.time()}.mp4'
    # effect = VideoEffectType.FIREFLIES
    # add_effect_into_video(
    #     effect,
    #     input_video_file_name,
    #     output_video_file_name
    # )

    # create_gif_w_effect(
    #     f'{CODE_HOME}/input/image2.jpeg',
    #     f'{CODE_HOME}/output/{time.time()}.gif',
    # )

    """
    Are you in need of ideal study or work music? Your search ends here! Dive into the realm of this lofi deep focus track, filled with chill, downtempo, slowly, soft piano, ambient for focusing on studying or working, serving as the quintessential backdrop to enhance your concentration and efficiency. Allow the melodic essence of Melodies in Soul to guide you in maintaining focus and drive in your everyday work environment. Whether you're preparing for exams, engrossed in a project, or simply seeking ambient accompaniment, this track caters to all your concentration requirements. Embrace the harmonies to remain in the flow and accomplish your objectives! 🎧📚🎶
    Need some background music to help you focus while studying, working, or relaxing? Check out this 1-hour study with me hip hop chill mix with lofi songs. Get in the zone and boost your productivity with this deep focus music! 🌿🎧🎶
    """
