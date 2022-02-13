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


def video_assembly(folder, path):
    finished_video = os.path.join(path, "finished_video")
    if not os.path.isdir(finished_video):
        os.mkdir(finished_video)
    (
        ffmpeg
        .input(f'{folder}/*.jpg', pattern_type='glob', framerate=30)
        .filter('deflicker', mode='am', size=15)
        .filter('scale', size='hd1080', force_original_aspect_ratio='increase')
        .output(f"{finished_video}/{folder.split('/')[-1]}.mp4")
        .run()
    )


def make_video():
    path = get_path()
    folders = path_to_jpg(path)
    for folder in folders:
        files = os.listdir(folder)
        if len(files) > 1000:
            video_assembly(folder, path)
            print('Ok')
            print(">-<"*10)
            remove_folder(path, folder, files)


def remove_folder(path, folder, files):
    for file in files:
        os.remove(os.path.join(path, folder, file))
    os.rmdir(folder)


if __name__ == '__main__':
    make_video()
