from .__init__ import ENCODING, execute_command_run, printf_colorlog


class Service:

    """
    class Service supports some tools that can handle linux daemons.

    all methods are set as static.
    """

    @staticmethod
    def is_enabled(service: str, sudo_password: str = None) -> bool:

        """
        return bool whether the service is enabled or not.

        :param service: set the linux service name which you want to see enabled or not.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is enabled or not.
        """

        command_str: str = f"systemctl is-enabled {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            if cp.stdout.decode(ENCODING) == "enabled\n":
                return True

        return False

    @staticmethod
    def is_running(service: str, sudo_password: str = None) -> bool:

        """
        return bool whether the service is running or not.

        :param service: set the linux service name which you want to see running or not.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is running or not.
        """

        command_str: str = f"systemctl is-active {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            if cp.stdout.decode(ENCODING) == "active\n":
                return True

        return False

    @staticmethod
    def set_disable(service: str, sudo_password: str = None) -> bool:

        """
        set the service disable.

        :param service: set the linux service name which you want to make disable.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is disabled or not.
        """

        command_str: str = f"systemctl disable {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def set_enable(service: str, sudo_password: str = None) -> bool:

        """
        set the service enable.

        :param service: set the linux service name which you want to make enable.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is enabled or not.
        """

        command_str: str = f"systemctl enable {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def start(service: str, sudo_password: str = None) -> bool:

        """
        start linux service(Daemon).

        :param service: set the linux service name which you want to start.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is started successfully or not.
        """

        command_str: str = f"systemctl start {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        printf_colorlog(text=f"<[ERROR] Service '{service}' was not started.>", color="b_red")
        printf_colorlog(text=f"<* reason: {cp.stderr.decode(ENCODING)}>", color="yellow")
        return False

    @staticmethod
    def stop(service: str, sudo_password: str = None) -> bool:

        """
        stop linux service(Daemon).

        :param service: set the linux service name which you want to stop.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is stopped successfully or not.
        """

        command_str: str = f"systemctl stop {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        printf_colorlog(text=f"<[ERROR] Service '{service}' was stop but there is an error.>", color="b_red")
        printf_colorlog(text=f"<* reason: {cp.stderr.decode(ENCODING)}>", color="b_yellow")
        return False

    @staticmethod
    def restart(service: str, sudo_password: str = None) -> bool:

        """
        restart linux service(Daemon).

        :param service: set the linux service name which you want to restart.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the service is restarted successfully or not.
        """

        command_str: str = f"systemctl restart {service}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        printf_colorlog(text=f"<[ERROR] Service '{service}' was not restarted.>", color="b_red")
        printf_colorlog(text=f" * reason: {cp.stderr.decode(ENCODING)}", color="b_yellow")
        return False
