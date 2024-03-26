from linux_cmd.ubuntu import *
from linux_cmd.ubuntu.dpkg import Dpkg


class Apt:

    """
    class Apt supports some tools that can manage deb packages of debian linux.

    all methods are set as static.
    """

    @staticmethod
    def install(package: str, sudo_password: str = None) -> bool:

        """
        install ubuntu package.

        :param package: set the package name you want to install
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the package is successfully installed or not.
        """

        command_str: str = f"apt-get install -y {package}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def is_installed(package: str, sudo_password: str = None) -> bool:

        """
        check whether the package installed or not in linux machine.

        :param package: set the package name you want to search whether it is installed or not
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the package is already installed or not.
        """

        return Dpkg.is_installed(package_name=package, sudo_password=sudo_password)

    @staticmethod
    def uninstall(package: str, sudo_password: str = None) -> bool:

        """
        uninstall ubuntu package which is already installed in linux machine.

        :param package: set the package name you want to uninstall
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the package is successfully uninstalled or not.
        """

        command_str: str = f"apt-get purge -y {package}"

        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def update(sudo_password: str = None) -> bool:

        """
        update new list of deb packages for apt-get.

        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether apt-get is successfully updated or not.
        """

        command_str: str = f"apt-get update -y"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False
