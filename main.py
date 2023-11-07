import os
import pathlib
from dotenv import load_dotenv
from fabric import Connection
import logging

from get_file import RemoteDirectoryOperations
from video_auto_make import video_assembly

logging.basicConfig(level=logging.INFO, filename='runtime.log', filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')


load_dotenv()

HOST = os.getenv('CAM_HOST')
PORT = os.getenv('CAM_PORT')
USER = os.getenv('CAM_USER')
PASSWD = os.getenv('CAM_PASSWD')
remote_dir = os.getenv('CAM_DIR')
local_dir = os.getenv('LOCAL_DIR')
finished_dir = os.getenv('FINISH_DIR')

connect_kwargs = {'password': PASSWD}
conn = Connection(HOST, user=USER, port=PORT, connect_kwargs=connect_kwargs)


def main():
    with Connection(
            HOST, user=USER, port=PORT,
            connect_kwargs=connect_kwargs,
            ) as conn:
        dir_ops = RemoteDirectoryOperations(conn)
        directories = dir_ops.list_directories(remote_dir)
        downloads = dir_ops.download_directories_with_files(remote_dir, local_dir, directories)
        if not os.path.isdir(finished_dir):
            logging.info(f'Directory not found{finished_dir} try create')
            os.mkdir(finished_dir)
        for folder in downloads:
            logging.info(f'{folder}')
            video_assembly(folder, finished_dir)


if __name__ == "__main__":
    main()
