from moviepy.editor import VideoFileClip, VideoClip
import cv2
import numpy as np
import random
import math
import time
from aqa.utils.enums import VideoEffectType


# Firefly class
class Firefly:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # self.update_position()
        self.pos = [random.randint(0, self.screen_width), random.randint(0, self.screen_height)]
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.size = random.randint(1, 3)
        self.brightness = 255
        self.glow_radius = random.randint(4, 8)
        self.glow_intensity = random.uniform(0.5, 1.0)
        self.transition_speed = random.uniform(0.001, 0.005)
        self.transition_offset = random.uniform(0, 3 * math.pi)
        self.start_time = time.time()

    def update_position(self):
        self.pos = [random.randint(0, self.screen_width), random.randint(0, self.screen_height)]
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.size = random.randint(1, 3)
        self.brightness = 255
        self.glow_radius = random.randint(4, 8)
        self.glow_intensity = random.uniform(0.5, 1.0)
        self.transition_speed = random.uniform(0.001, 0.005)
        self.transition_offset = random.uniform(0, 3 * math.pi)
        self.start_time = time.time()

    def update(self):
        elapsed_time = (time.time() * 1000) - self.start_time
        self.brightness = int(
            127.5 * math.sin(elapsed_time * self.transition_speed + self.transition_offset) + 127.5)
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.pos[0] < 0 or self.pos[0] > self.screen_width or self.pos[1] < 0 or self.pos[1] > self.screen_height:
            self.update_position()

    # def draw(self, frame):
    #     color = (255, 255, 100) if self.brightness > 127 else (self.brightness, self.brightness, self.brightness)
    #     frame = frame.copy()
    #     overlay = np.zeros_like(frame)
    #     cv2.circle(overlay, (int(self.pos[0]), int(self.pos[1])), self.size + self.glow_radius, color, -1)
    #     blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
    #     frame = cv2.addWeighted(frame, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame
    #     return frame


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
            color = (255, 255, 100) if firefly.brightness > 127 else (firefly.brightness, firefly.brightness, firefly.brightness)
            cv2.circle(overlay, (int(firefly.pos[0]), int(firefly.pos[1])), firefly.size + firefly.glow_radius, color, -1)
            blurred_overlay = cv2.GaussianBlur(overlay, (15, 15), 0)  # Apply Gaussian blur to the overlay
            frame = cv2.addWeighted(frame, 1, blurred_overlay, 0.5, 0)  # Blend the blurred overlay with the frame
        return frame


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


class Raindrop:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)  # Random x position within screen width
        self.y = random.randint(0, screen_height)  # Random y position within screen height
        self.length = random.randint(3, 12)  # Random length of the raindrop
        self.speed = random.randint(10, 25)  # Random falling speed of the raindrop
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


# def add_fireflies_in_video(input_video_path='input_video.mp4', output_video_path='output_video.mp4'):
#     # Load input video with audio
#     video_clip = VideoFileClip(input_video_path)
#
#     # Video settings
#     fps = video_clip.fps
#     width, height = video_clip.size
#
#     # Create fireflies
#     fireflies = [Firefly(width, height) for _ in range(7)]
#
#     # Main loop for processing each frame of the input video
#     def process_frame(t):
#         frame = video_clip.get_frame(t)
#         for firefly in fireflies:
#             firefly.update()
#             frame = firefly.draw(frame)
#         return frame
#
#     # Process each frame and create the output video
#     output_clip = VideoClip(process_frame, duration=video_clip.duration)
#     output_clip = output_clip.set_audio(video_clip.audio)  # Retain the original audio
#
#     # Write the output video with audio to a file
#     output_clip.write_videofile(
#         filename=output_video_path,
#         fps=fps,
#         codec='libx264',
#         audio_codec='aac',
#         temp_audiofile='temp-audio.m4a',
#         remove_temp=True
#     )
#
#     # Close input video clip
#     video_clip.close()


def add_snowfall_in_video(input_video_path='input_video.mp4', output_video_path='output_video.mp4'):
    # Load input video with audio
    video_clip = VideoFileClip(input_video_path)

    # Video settings
    fps = video_clip.fps
    width, height = video_clip.size

    snowfall = [SnowfallSimulation(width, height, 10)]  # Create a snowfall simulation with 50 snowflakes

    # Main loop for processing each frame of the input video
    def process_frame(t):
        frame = video_clip.get_frame(t)
        for snow in snowfall:
            snow.update()
            frame = snow.draw(frame)
        return frame

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


def add_raindrops_in_video(input_video_path='input_video.mp4', output_video_path='output_video.mp4'):
    # Load input video with audio
    video_clip = VideoFileClip(input_video_path)

    # Video settings
    fps = video_clip.fps
    width, height = video_clip.size

    raindrops = [RainSimulation(width, height, 15)]  # Create a snowfall simulation with 50 snowflakes

    # Main loop for processing each frame of the input video
    def process_frame(t):
        frame = video_clip.get_frame(t)
        for raindrop in raindrops:
            raindrop.update()
            frame = raindrop.draw(frame)
        return frame

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


def add_effect_in_video(effect, input_video_path='input_video.mp4', output_video_path='output_video.mp4'):
    # Load input video with audio
    video_clip = VideoFileClip(input_video_path)

    # Video settings
    fps = video_clip.fps
    width, height = video_clip.size

    effects = []

    if effect == VideoEffectType.FIREFLIES:
        effects = [FirefliesSimulation(width, height, 10)]  # Create fireflies effect simulation with 15 fireflies
    elif effect == VideoEffectType.SNOWFALL:
        effects = [SnowfallSimulation(width, height, 15)]  # Create fireflies effect simulation with 15 fireflies
    elif effect == VideoEffectType.RAINDROPS:
        effects = [RainSimulation(width, height, 20)]  # Create raindrops effect simulation with 20 raindrops

    # Main loop for processing each frame of the input video
    def process_frame(t):
        frame = video_clip.get_frame(t)
        for e in effects:
            e.update()
            frame = e.draw(frame)
        return frame

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


if __name__ == '__main__':
    pass
    # add_effect_in_video(
    #     VideoEffectType.FIREFLIES,
    #     '/Volumes/BUFFALO-HD/trieutruong/github/mktg-bot/input_video.mp4',
    #     f'/Volumes/BUFFALO-HD/trieutruong/github/mktg-bot/output_video_w_{VideoEffectType.FIREFLIES}.mp4'
    # )
