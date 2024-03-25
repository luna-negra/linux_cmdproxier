from linux_cmd import ENCODING, execute_command_run


class Account:

    """
    class Service supports some tools that can handle or check related in linux account.

    all methods are set as static.
    """

    @staticmethod
    def get_current_username() -> str | None:

        """
        return the current linux username.

        :return: current linux username with string format.
        """

        command_str: str = "whoami"
        cp = execute_command_run(command_str=command_str)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).rstrip("\n")

        return None

    @staticmethod
    def get_current_user_home_path() -> str | None:

        """
        return the absolute path of current user's home directory on linux.

        :return: absolute path of current user's home directory.
        """

        command_str: str = f"echo $HOME"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password, shell=True)

        if cp.returncode == 0 and cp.stdout.decode(ENCODING) is not None:
            return cp.stdout.decode(ENCODING).rstrip("\n")

        return None

    @staticmethod
    def is_root_or_has_sudo(sudo_password: str = None) -> bool:

        """
        return bool for whether the current user is root or not, or has sudo privilege or not.

        :param sudo_password: if the current user is not root, set the sudo password to validate.
        :return: bool for current user's root or sudo privilege.
        """

        command_str: str = f"head -n 1 /etc/sudo.conf"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password, shell=True)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def is_user_exist(username: str, sudo_password: str = None) -> bool:

        """
        return bool for whether username exist on the local machine or not.

        :param username: set the username you want to search.
        :param sudo_password: if /etc/passwd need sudo, set sudo password.
        :return: bool for linux user is in local machine or not.
        """

        command_str: str = f"cat /etc/passwd | grep {username}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        for line in cp.stdout.decode(ENCODING).split("\n")[-1:]:
            if line.startswith(username):
                return True

        return False
