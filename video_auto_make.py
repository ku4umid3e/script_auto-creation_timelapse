import os
import ffmpeg


def get_path():
    path = input(
        """Please enter the absolute path to
        the folder with the photo collection\n"""
        )
    return path


def path_to_jpg(path):
    folders = []
    route = os.walk(path)

    for dirpath, dirnames, filenames in route:
        for dirname in dirnames:
            folders.append(os.path.join(dirpath, dirname))
    return folders


def make_video():
    path = get_path()
    folders = path_to_jpg(path)
    for folder in folders:
        (
            ffmpeg
            .input(f'{folder}/*.jpg', pattern_type='glob', framerate=30)
            .filter('deflicker', mode='am', size=15)
            .filter('scale', size='hd1080', force_original_aspect_ratio='increase')
            .output(f"data/{folder.split('/')[-1]}.mp4")
            .run()
        )
        print('Ok')
        print(">-<"*10)
        remove_folder(path, folder)


def remove_folder(path, folder):
    files = os.listdir(folder)
    for file in files:
        os.remove(os.path.join(path, folder, file))
    os.rmdir(folder)


if __name__ == '__main__':
    make_video()
