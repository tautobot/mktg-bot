import os
import shutil
from datetime import datetime
from aqa.utils.audio_creator import extend_audio
from aqa.utils.video_creator import create_video_f_image_n_audio, add_effect_into_video, create_video_from_short_video
from aqa.utils.enums import VideoEffectType
from config import CODE_HOME


def _task_generate_video():
    image_file          = f"{CODE_HOME}/progress/image.jpg"
    audio_file          = f"{CODE_HOME}/progress/audio.mp3"
    extended_audio_file = f"{CODE_HOME}/progress/extended_audio.mp3"
    video_file          = f"{CODE_HOME}/progress/video.mp4"
    effected_video_file = f"{CODE_HOME}/progress/effected_video.mp4"
    complete_video_file = f"{CODE_HOME}/progress/complete_video.mp4"

    one_hours = 3600
    # Check for audio.mp3 file in the "progress" folder
    if os.path.exists(audio_file) and not os.path.exists(extended_audio_file):
        print("Extend audio file: Start...")
        extend_audio(
            input_audio_file=audio_file,
            output_audio_file=extended_audio_file,
            extend=one_hours
        )
        print("Extend audio file: Done")

    # Check for extended_audio.mp3 and image.jpg files in the "progress" folder
    if os.path.exists(image_file) and os.path.exists(extended_audio_file) and not os.path.exists(video_file):
        print("Create video file: Start...")
        create_video_f_image_n_audio(
            input_image_path=image_file,
            input_audio_path=extended_audio_file,
            output_video_path=video_file
        )
        print("Create video file: Done")

    # Check for video.mp4 file in the "progress" folder
    if os.path.exists(video_file) and not os.path.exists(effected_video_file):
        print("Add effect into video file: Start...")
        effect = VideoEffectType.FIREFLIES
        add_effect_into_video(
            effect=effect,
            input_video_path=video_file,
            output_video_path=effected_video_file
        )
        print("Add effect into video file: Done")

    # Duplicate videos
    if os.path.exists(effected_video_file) and not os.path.exists(complete_video_file):
        print("Duplicate video file: Start...")
        create_video_from_short_video(
            input_video_path=effected_video_file,
            output_video_path=complete_video_file
        )
        print("Duplicate video file: Done")

    # Cleanup files after completion
    if os.path.exists(complete_video_file):
        cleanup_files()


def cleanup_files():
    progress_folder   = f"{CODE_HOME}/progress"
    completion_folder = f"{CODE_HOME}/completion"
    logs_folder       = f"{CODE_HOME}/logs"
    current_datetime = datetime.now().strftime("%Y%m%d.%H%M%S")
    file_list = os.listdir(progress_folder)
    print("Cleanup files: Start...")
    for file in file_list:
        file_path = os.path.join(progress_folder, file)
        new_file_name = f"{os.path.splitext(file)[0]}_{current_datetime}{os.path.splitext(file)[1]}"
        new_file_path = os.path.join(logs_folder, new_file_name)
        if file.startswith('complete_'):
            complete_file_path = os.path.join(completion_folder, new_file_name)
            shutil.copy(file_path, complete_file_path)
        shutil.move(file_path, new_file_path)
        print(f"Moved {file} to {new_file_name} in 'logs' folder.")

    print("Cleanup files: Done")

    # # Cleanup: Remove all files in the "progress" folder
    # for file in os.listdir("progress"):
    #     file_path = os.path.join("progress", file)
    #     os.remove(file_path)
    #
    # print("All files in 'progress' folder have been removed.")


if __name__ == '__main__':
    _task_generate_video()
