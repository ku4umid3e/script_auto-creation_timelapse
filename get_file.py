class RemoteDirectoryOperations:
    def __init__(self, conn):
        self.conn = conn

    def list_directories(self, remote_directory):
        result = self.conn.run(f'ls -lt {remote_directory} | grep "^d" | rev | cut -d" " -f1 | rev', hide=True)
        directories = result.stdout.strip().split('\n')
        return directories

    def list_files_in_directory(self, remote_directory, directory):
        result = self.conn.run(f'ls {remote_directory}/{directory}', hide=True)
        files = result.stdout.strip().split('\n')
        return files

    def download_directories_with_files(self, source_directory, local_directory):
        directories = self.list_directories(source_directory)
        print(directories)

        for directory in directories:
            local_subdirectory = f'{local_directory}/{directory}'
            self.conn.local(f'mkdir -p {local_subdirectory}')
            files = self.list_files_in_directory(source_directory, directory)
            print(files[:5])
            print(directory)
            for file in files:
                source_path = f'{source_directory}/{directory}/{file}'
                print(f' что копируем и откуда: {source_path}')
                local_path = f'{local_subdirectory}/{file}'
                print(f'куда копируем и что: {local_path}')
                self.conn.get(source_path, local=local_path)
                print(f'File "{file}" downloaded to "{local_path}"')

    def delete_directories(self, source_directory):
        directories = self.list_directories(source_directory)

        if directories:
            for directory in directories:
                self.conn.run(f'rm -r {source_directory}/{directory}')
                print(f'Directory "{directory}" removed successfully.')
