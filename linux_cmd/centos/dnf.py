from linux_cmd.centos import *


class Dnf:

    """
    class Dnf supports some tools that can manage rpm packages of ubuntu.

    all methods are set as static.
    """

    @staticmethod
    def install(package: str, sudo_password: str = None) -> bool:

        """
        install centos package.

        :param package: set the package name you want to install
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the package is successfully installed or not.
        """

        command_str: str = f"dnf install -y {package}"
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

        command_str: str = f"dnf list --installed | grep {package}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def uninstall(package: str, sudo_password: str = None) -> bool:

        """
        uninstall centos package which is already installed in linux machine.

        :param package: set the package name you want to uninstall
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the package is successfully uninstalled or not.
        """

        command_str: str = f"dnf remove -y {package}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def update(sudo_password: str = None) -> bool:

        """
        update new list of rpm packages for dnf or yum.

        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether dnf or yum is successfully updated or not.
        """

        command_str: str = f"dnf update -y"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False
