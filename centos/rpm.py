from ..centos import *


class Rpm:

    """
    class Rpm supports some tools that can handle a parts of centos command rpm.

    all methods are set as static.
    """

    @staticmethod
    def check_command_belong_to(command: str, sudo_password: str = None) -> str | None:

        """
        check the rpm package's name which support the specific command.

        :param command: set the command name to check which rpm package support it.
        :param sudo_password: if you need sudo, set sudo password.
        :return: package name which the command belong to.
        """

        command_str: str = f"rpm -qf `which {command}`"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).rstrip("\n")

        return None

    @staticmethod
    def install(package_path: str, sudo_password: str = None) -> bool:

        """
        install rpm file on linux machine

        :param package_path: set the path of rpm file to install
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether rpm file is successfully installed or not.
        """

        command_str: str = f"rpm -i {package_path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def is_installed(package_name: str, sudo_password: str = None) -> bool:

        """
        check whether the specific rpm is installed or not on linux machine.

        :param package_name: set the name of rpm to check whether it is installed or not.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the specific rpm is installed or not on linux machine.
        """

        command_str: str = f"rpm -qa | grep {package_name}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0 and cp.stdout.decode(ENCODING) != "":
            return True

        return False

    @staticmethod
    def uninstall(package_name: str, sudo_password: str = None) -> bool:

        """
        uninstall rpm package on linux machine

        :param package_name: set the name of rpm to uninstall
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether rpm file is successfully uninstalled or not.
        """

        command_str: str = f"rpm -e {package_name}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False
