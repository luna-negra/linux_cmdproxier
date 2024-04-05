from ..ubuntu import *


class Dpkg:

    """
    class Dpkg supports some tools that can handle a parts of ubuntu command dpkg.

    all methods are set as static.
    """

    @staticmethod
    def check_command_belong_to(command: str, sudo_password: str = None) -> str | None:

        """
        check the deb package's name which support the specific command.

        :param command: set the command name to check which deb package support it.
        :param sudo_password: if you need sudo, set sudo password.
        :return: package name which the command belong to.
        """

        command_str: str = f"dpkg --search `which {command}`"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).rstrip("\n").split(":")[0]

        return None

    @staticmethod
    def install(package_path: str, sudo_password: str = None) -> bool:

        """
        install deb file on linux machine

        :param package_path: set the path of deb file to install
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether deb file is successfully installed or not.
        """

        command_str: str = f"dpkg --install {package_path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def is_installed(package_name: str, sudo_password: str = None) -> bool:

        """
        check whether the specific deb is installed or not on linux machine.

        :param package_name: set the name of deb to check whether it is installed or not.
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the specific deb is installed or not on linux machine.
        """

        command_str: str = f"dpkg --list | grep {package_name}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0 and cp.stdout.decode(ENCODING) != "":
            return True

        return False

    @staticmethod
    def uninstall(package_name: str, sudo_password: str = None) -> bool:

        """
        uninstall deb package on linux machine

        :param package_name: set the name of deb to uninstall.
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether deb file is successfully uninstalled or not.
        """

        command_str: str = f"dpkg --purge {package_name}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            if cp.stderr.decode(ENCODING).startswith("dpkg: warning:"):
                return False
            return True

        return False
