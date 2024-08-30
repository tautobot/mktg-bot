import os
from pymusiclooper.handler import MusicLooper
from config import CODE_HOME


def extend_audio(input_audio_file, output_audio_file, extend):
    file_name_with_extension = os.path.basename(input_audio_file)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    folder_path = os.path.dirname(input_audio_file)

    def convert_sec_for_extend_fname(seconds):
        if not isinstance(seconds, int):
            return "Input must be an integer"

        # hours = seconds // 3600
        minutes = seconds // 60
        seconds = seconds % 60

        # return hours, minutes, seconds
        return "{:02d}m{:02d}s".format(minutes, seconds)

    # Specify the input audio file and output file
    # input_audio_file = f"{CODE_HOME}/input_audio.mp3"
    # output_audio_file = f"{CODE_HOME}/output_audio_extended.mp3"

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
        extended_length=extend,
        format="mp3",
        output_dir=folder_path
    )

    # Rename the file
    os.rename(f"{input_audio_file}-extended-{convert_sec_for_extend_fname(extend)}{file_extension}", output_audio_file)
    print(f"Audio file extended successfully to {convert_sec_for_extend_fname(extend)}")


if __name__ == '__main__':
    pass
    extend_audio(f'{CODE_HOME}/input/lofi_no30.mp3', f'{CODE_HOME}/output', 3600)
