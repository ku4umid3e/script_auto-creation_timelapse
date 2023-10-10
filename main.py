import os
from dotenv import load_dotenv
from fabric import Connection
import shutil

load_dotenv()

HOST = os.getenv('CAM_HOST')
PORT = os.getenv('CAM_PORT')
USER = os.getenv('CAM_USER')
PASSWD = os.getenv('CAM_PASSWD')
remote_dir = os.getenv('CAM_DIR')
local_dir = os.getenv('LOCAL_DIR')

connect_kwargs = {'password': PASSWD}
conn = Connection(HOST, user=USER, port=PORT, connect_kwargs=connect_kwargs)


class RemoteDirectoryOperations:
    def __init__(self, conn):
        self.conn = conn

    def list_directories(self, remote_directory):
        result = self.conn.run(f'ls -lt {remote_directory} | grep "^d" | rev | cut -d" " -f1 | rev', hide=True)
        directories = result.stdout.strip().split('\n')
        return directories

    def copy_directories(self, source_directory, destination_directory):
        directories = self.list_directories(source_directory)

        if directories:
            for directory in directories:
                source_path = f'{source_directory}/{directory}'
                destination_path = f'{destination_directory}/{directory}'
                self.conn.run(f'cp -r {source_path} {destination_path}')
                print(f'Directory "{directory}" copied successfully.')

    def delete_directories(self, source_directory):
        directories = self.list_directories(source_directory)

        if directories:
            for directory in directories:
                source_path = f'{source_directory}/{directory}'
                shutil.rmtree(source_path)
                print(f'Directory "{directory}" removed successfully.')


if __name__ == "__main__":
    print(USER)
    with Connection(
            HOST, user=USER, port=PORT,
            connect_kwargs=connect_kwargs,
            ) as conn:
        dir_ops = RemoteDirectoryOperations(conn)
        print(dir_ops.list_directories(remote_dir))
