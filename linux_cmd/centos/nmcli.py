from linux_cmd.centos import *


class NetworkManager:

    """
    class NetworkManager supports some tools that can handle parts of command nmcli in centos 8.

    all methods are set as static.
    """

    @staticmethod
    def get_connection_id(ifc: str, sudo_password: str = None) -> str | None:

        """
        get connection name of interface. the result of `nmcli -g GENERAL.CONNECTION device show {ifc}`

        :param ifc: set the interface name to get the connection name of interface.
        :param sudo_password: if you need sudo, set sudo password.
        :return: connection name of interface in string format.
        """

        command_str: str = f"nmcli -g GENERAL.CONNECTION device show {ifc}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).rstrip("\n")

        return None

    @staticmethod
    def get_interface_zone(ifc: str, sudo_password: str = None) -> str | None:

        """
        get connection name of interface. the result of `nmcli -g GENERAL.CONNECTION device show {ifc}`

        :param ifc: set the interface name to get the connection name of interface.
        :param sudo_password: if you need sudo, set sudo password.
        :return: connection name of interface in string format.
        """

        delimiter: str = "connection.zone"
        conn_id: str = NetworkManager.get_connection_id(ifc=ifc, sudo_password=sudo_password)
        command_str: str = f"nmcli connection show '{conn_id}' | grep {delimiter}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).split(f"{delimiter}:")[1].strip(" ").strip("\n")

        return None

    @staticmethod
    def ifc_up(ifc: str, sudo_password: str = None) -> bool:

        """
        activate the specific interface

        :param ifc: set the interface name to activate.
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the interface is successfully activated or not.
        """

        command_str: str = f"nmcli connection up '{ifc}'"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def ifc_down(ifc: str, sudo_password: str = None) -> bool:

        """
        deactivate the specific interface. main interface is not able to be shutdown due to the security.

        :param ifc: set the interface name to deactivate.
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the interface is successfully deactivated or not.
        """

        conn_id: str = NetworkManager.get_connection_id(ifc=ifc, sudo_password=sudo_password)
        if conn_id != ifc:
            return False

        command_str: str = f"nmcli connection down '{conn_id}'"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

    @staticmethod
    def reload_connection(sudo_password: str = None) -> bool:

        """
        reload the connection setting of nmcli.

        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the connection reload was success or not.
        """

        command_str: str = f"nmcli connection reload"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False


    @staticmethod
    def set_interface_zone(ifc: str, zone:str, sudo_password: str = None) -> bool:

        """
        set the interface to the specific firewalld's zone.

        :param ifc: set the interface name to get the connection name of interface.
        :param sudo_password: if you need sudo, set sudo password.
        :return: bool whether the interface are successfully belong to zone's interface or not.
        """

        conn_id: str = NetworkManager.get_connection_id(ifc=ifc, sudo_password=sudo_password)
        command_str: str = f"nmcli connection modify '{conn_id}' CONNECTION.ZONE {zone}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        return False

