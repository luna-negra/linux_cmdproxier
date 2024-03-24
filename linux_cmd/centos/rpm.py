from linux_cmd.centos import *


class Rpm:

    """
    class Rpm supports some tools that can handle a parts of centos command yum or rpm.

    all methods are set as static.
    """

    @staticmethod
    def check_command_belong_to(command: str, sudo_password: str = None) -> str | None:

        """
        check the rpm package's name which support the specific command.

        :param command: set the command name to check which rpm support it.
        :param sudo_password: if /etc/passwd need sudo, set sudo password.
        :return: package name which the command belong to.
        """

        command_str: str = f"rpm -qf `which {command}`"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).rstrip("\n")

        return None

    @staticmethod
    def install(rpm_path: str, sudo_password: str = None) -> bool:

        """
        install rpm file on linux machine

        :param rpm_path:
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether rpm file is successfully installed or not.
        """

        command_str: str = f"rpm -i {rpm_path}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def uninstall(rpm_name: str, sudo_password: str = None) -> bool:

        """
        uninstall rpm file on linux machine

        :param rpm_name:
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether rpm file is successfully uninstalled or not.
        """
        command_str: str = f"rpm -e {rpm_name}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False
