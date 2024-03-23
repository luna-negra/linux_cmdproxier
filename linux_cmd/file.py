from linux_cmd import ENCODING, execute_command_run


class FileSystem:

    """
    class FileSystem supports some tools that can handle files or folder in linux.

    all methods are set as static.
    """

    @staticmethod
    def create_symlink(target_path: str, link_path: str, sudo_password: str = None) -> bool:

        """
        create symlink.

        :param target_path: path of link's target file or folder.
        :param link_path: path of link.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether symlink is created successfully or not.
        """

        command_str: str = f"ln -s {target_path} {link_path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def is_path_exist(path: str) -> bool:

        """
        check whether the path - file or folder - exist or not.

        :param path: set absolute path or relative path which you want to search.
        :return: bool whether the path exist or not.
        """

        command_str: str = f"ls -lhd {path}"
        cp = execute_command_run(command_str=command_str)

        if cp.returncode == 0 and cp.stdout.decode(ENCODING) != "":
            return True

        return False

    @staticmethod
    def get_file_contents(path: str, sudo_password: str = None) -> str | None:

        """
        return file contents in string format.

        :param path: set the file path.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: return file's contents in string form.
        """

        if FileSystem.get_path_type(path=path) != "file":
            return None

        command_str: str = f"cat {path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING)

        return None

    @staticmethod
    def get_list_on_path(path: str, sudo_password: str = None) -> list | None:

        """
        get the file and folder list in specific path.

        :param path: set the path you want to get a file or folder list.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: list value which contains the list of files and folders in path.
        """

        command_str: str = f"ls {path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return [ file.rstrip("\n") for file in cp.stdout.decode(ENCODING).split(" ") ]

        return None

    @staticmethod
    def get_path_type(path: str, sudo_password: str = None) -> str | None:

        """
        return the type of path. types are in ('file', 'directory', 'link', 'non-file').

        :param path: set the path of which you want to see the type.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: type of path in string.
        """

        TYPE_DICT: dict = {
            "-": "file",
            "d": "directory",
            "l": "link",
            "": "non-file"
        }

        command_str: str = f"ls -lhd {path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            result: str = cp.stdout.decode(ENCODING)
            path_type: str = result[0] if len(result) else ""

            try:
                return TYPE_DICT[path_type]

            except KeyError:
                pass

        return None

    @staticmethod
    def get_path_with_name(name: str, path: str = "/", sudo_password: str = None) -> list | None:

        """
        find specific file or folder name and get the file's path with 'find' command and option '-name'.
        if you want to get an absolute path, please set the search_path as absolute.

        :param name: set file or folder name.
        :param path: set the path of file or folder with name. default value is '/'.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: list value which contains the result of 'find' command.
        """

        command_str: str = f"find {path} -name {name}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return list(filter(lambda a: a != '', cp.stdout.decode(ENCODING).split("\n")))

        return None

    @staticmethod
    def set_file_contents(path: str, contents: str, sudo_password: str = None) -> bool:

        """
        write the contents on the specific file. if file is not exist, file will be created automatically.

        :param path: target file's path. absolute path is recommended.
        :param contents: contents in string you want to write down in a target file.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether contents are written down on the target file well or not.
        """

        command_str: str = f"echo {contents} > {path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password, shell=True)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def tar_unzip(tarball_path: str, save_path: str = None, sudo_password: str = None) -> bool:

        """
        extract tarball.

        :param tarball_path: tarball path which you want to extract.
        :param save_path: set a path where extracted folder will be located.
        :param sudo_password: if you need sudo, set the sudo password.
        :result: bool whether the tarball is extracted successfully or not.
        """

        command_str: str = f"tar -xf {tarball_path} "
        if save_path is not None:
            command_str += f"-C {save_path}"
        else:
            command_str += f"-C {'/'.join(tarball_path.split('/')[:-1])}"

        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)
        if cp.returncode == 0 or cp.returncode == 2:
            return True

        return False

    @staticmethod
    def tar_zip(list_target_file: list, save_as: str, sudo_password: str = None) -> bool:

        """
        create tarball.

        :param list_target_file: list contains files which will be in tarball.
        :param save_as: set a path where created tarball will be located.
        :param sudo_password: if you need sudo, set the sudo password.
        :result: bool whether the tarball is created successfully or not.
        """
        if not save_as.endswith(".tar"):
            save_as += ".tar"

        command_str: str = f"tar -cvf {save_as} {' '.join(list_target_file)}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def wget_download(url: str, save_path: str = None, sudo_password: str = None) -> bool:

        """
        download file from internet with wget quietly.

        :param url: set the url of file which you want to download.
        :param save_path: set the path to save downloaded file.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the file is downloaded successfully or not.
        """

        command_str: str = f"wget -q {url} "
        if save_path is not None: command_str += f"-P {save_path}"

        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)
        if cp.returncode in (0, 1):
            return True

        return False
