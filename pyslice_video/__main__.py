import argparse
from math import ceil
from moviepy.editor import *
import os

def formatNumber(number: int = 0) -> str:
    return '0' * (4 - len(str(number))) + str(i) if len(str(number)) < 4 else str(i)

def verifyExtension(file: str) -> bool:
    return True if file.split('.')[-1].lower() in ['mkv', 'mp4'] else False

parse = argparse.ArgumentParser(description='Executes pyslice_video.', usage='python .\pyslice_video -fp "C:/Users/Video/videos_folder" -sl 15',)

parse.add_argument(
                    '-fp',
                    '--folder_path',
                    help = 'Folder where are the videos to be sliced.',
                    type = str,
                    action = 'store',
                    default = None)

parse.add_argument(
                    '-sl',
                    '--slice_lenght',
                    help = 'Lenght of slice for the videos.',
                    type = int,
                    action = 'store',
                    default = 30)

parse.add_argument(
                    '-ns',
                    '--slices_number',
                    help = 'Number of slices.',
                    type = int,
                    action = 'store',
                    default = 0)

args: dict = parse.parse_args().__dict__
video_path_folder = args['folder_path']

if args['folder_path'] is None:
    print('No folder path given. Exiting.')
    exit()
if not os.path.isdir(args['folder_path']):
    print('Folder path is not valid.')
    exit()

# Creates a list of all the videos in the folder
video_names = os.listdir(video_path_folder)

n_slices: int = args['slices_number']

# Iterates over the list of videos
for video_name in video_names:
    # Verifies if the video is a video file
    if verifyExtension(video_name):
        print(f'Slicing <{video_name}>... ')
        video_path = f'{video_path_folder}\{video_name}'
        # Stores the video in a variable
        video = VideoFileClip(video_path)
        slice_length = args['slice_lenght']
        slice_start = 0
        slice_end = slice_length
        video_length = video.duration
        # Calculates the number of slices
        slice_numbers = ceil(video_length / slice_length)

        video_parts_folder = f'{video_path_folder}/{video_name.replace(".", "_")}[IN PARTS]'
        # Creates the folder where the video will be stored
        if(not os.path.isdir(video_parts_folder)):
            os.mkdir(video_parts_folder)

        # Iterates over the number of slices
        for i in range(slice_numbers)[0:n_slices]:
            video_trim = video.subclip(slice_start, slice_end)
            video_trim.write_videofile(
                                        f'{video_parts_folder}/{video_name.replace(".", "_")}{[formatNumber(i)]}.mp4',
                                        codec = 'libx264')
            slice_start += slice_length
            if slice_end + slice_length <= video_length:
                slice_end = slice_start + slice_length
            else:
                slice_end = video_length

