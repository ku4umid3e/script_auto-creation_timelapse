import os
import ffmpeg


def get_path():
    path = input("Please enter the absolute path to the folder with the photo collection\n")
    return path


def path_to_jpg():
    folders = []
    path = os.walk(get_path())

    for dirpath, dirnames, filenames in path:
        for dirname in dirnames:
            folders.append(os.path.join(dirpath, dirname))
    return folders


def make_video(folders):
    for folder in folders:

        (
            ffmpeg
            .input(f'{folder}/*.jpg', pattern_type='glob', framerate=30)
            .filter('deflicker', mode='am', size=15)
            .filter('scale', size='hd1080', force_original_aspect_ratio='increase')
            .output(f"{folder.split('/')[-1]}.mp4")
            .run()
        )
    print('Ok')


def main():
    make_video(path_to_jpg())



if __name__ == '__main__':
    main()
