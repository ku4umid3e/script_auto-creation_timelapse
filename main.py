import os
from dotenv import load_dotenv
from fabric import Connection
from fabric.transfer import Transfer
# import shutil

from get_file import RemoteDirectoryOperations


load_dotenv()

HOST = os.getenv('CAM_HOST')
PORT = os.getenv('CAM_PORT')
USER = os.getenv('CAM_USER')
PASSWD = os.getenv('CAM_PASSWD')
remote_dir = os.getenv('CAM_DIR')
local_dir = os.getenv('LOCAL_DIR')

connect_kwargs = {'password': PASSWD}
conn = Connection(HOST, user=USER, port=PORT, connect_kwargs=connect_kwargs)

def main():
    pass



if __name__ == "__main__":
    print(USER)
    with Connection(
            HOST, user=USER, port=PORT,
            connect_kwargs=connect_kwargs,
            ) as conn:
        dir_ops = RemoteDirectoryOperations(conn)
        dir_ops.download_directories_with_files(remote_dir, '/tmp')
