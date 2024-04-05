from __init__ import execute_command_run, printf_colorlog, ENCODING, get_linux_dist
from .centos.nmcli import NetworkManager


class Firewall:
    """
    class Firewall supports some tools that can handle linux firewall.
    only support firewall-cmd so do not use this class with iptables.

    all methods are set as static.
    """

    @staticmethod
    def is_running(sudo_password: str = None) -> bool:

        """
        return bool whether the firewalld is running or not

        :param sudo_password: if you need sudo, set the sudo password
        :return : bool whether the firewalld is running or not
        """

        command_str: str = "firewall-cmd --state"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            if cp.stdout.decode(ENCODING) == "running\n":
                return True

        printf_colorlog(text=f"<{cp.stderr.decode(ENCODING)}>", color="b_red")
        return False

    @staticmethod
    def get_active_zone_names(sudo_password: str = None) -> list | None:

        """
        return all active zone's name of firewalld.

        :param sudo_password: if you need sudo, set the sudo password.
        :return : a list of active zone's name.
        """

        command_str: str = "firewall-cmd --get-active-zone"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return list(filter(lambda a: not a.startswith(" ") and a != '', cp.stdout.decode(ENCODING).split("\n")))

        return None

    @staticmethod
    def get_all_zones(sudo_password: str = None) -> list | None:

        """
        return the all zone's name of firewalld.

        :param sudo_password: if you need sudo, set the sudo password.
        :return : a list which contains names of all zone in firewalld.
        """

        command_str: str = "firewall-cmd --get-zones"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).split(" ")

        return None

    @staticmethod
    def get_default_zone(sudo_password: str = None) -> str | None:

        """
        return the firewalld's default zone name
        be advised that you will get only 'public' if you do not have root or sudo privilege

        :param sudo_password: if you need sudo, set the sudo password
        :return : a name of default zone in firewalld
        """

        command_str: str = "firewall-cmd --get-default-zone"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).rstrip("\n")

        return None

    @staticmethod
    def get_zone_interfaces(zone: str, sudo_password: str = None) -> list | None:

        """
        get names of interfaces that belong to the specific firewall zone.

        :param zone: specific zone name to check what interfaces belong to.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: list of interfaces that belong to zone.
        """

        command_str: str = f"firewall-cmd --list-all --zone={zone} | grep interface"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password, shell=True)

        if cp.returncode == 0:
            return cp.stdout.decode(ENCODING).split("interfaces: ")[1].rstrip("\n").split(" ")

        return None

    @staticmethod
    def rich_rule(action: str,
                  rule_action: str,
                  family: str = "ipv4",
                  zone: str = None,
                  permanent: bool = False,
                  sudo_password: str = None,
                  **kwargs) -> bool:

        """
        add or remove rich rule in specific zone

        :param action: assign "add" or "remove" for rich_rule
        :param rule_action: assign rule action for rich rule. ['accept', 'reject', 'drop', 'mark']
        :param family: assign among "ipv4" or "ipv6"
        :param zone: specify the zone name in string form where you want to add or remove object. default is default zone
        :param permanent: bool for applying or removing port and number in permanently
        :**kwargs:
        - srcip: source ip. [IP, IP/PREFIX]
        - dstip: destination ip. [IP, IP/PREFIX]
        - svcname: name of service that registered in /etc/services
        - port: port_number(or port range with number1-number2)/protocol
        - protocol: protocol name or ID registered in /etc/protocols.
        :param sudo_password: if you need sudo, set the sudo password.
        :return: bool whether the rich rule are successfully added / removed or not
        """

        if action not in ("add", "remove"):
            return False

        kwargs_keys = kwargs.keys()
        command_str: str = "firewall-cmd"
        rich_rule_str: str = f"rule family=\"{family}\""

        if zone is not None:
            command_str += f" --zone={zone}"

        if permanent:
            command_str += f" --permanent"

        if "srcip" in kwargs_keys:
            rich_rule_str += f" source address=\"{kwargs['srcip']}\""

        if "dstip" in kwargs_keys:
            rich_rule_str += f" destination address=\"{kwargs['dstip']}\""

        if "svcname" in kwargs_keys:
            rich_rule_str += f" service name=\"{kwargs['svcname']}\""

        if "port" in kwargs_keys:
            tmp: list = kwargs['port'].split("/")
            rich_rule_str += f" port port=\"{tmp[0]}\" protocol=\"{tmp[1]}\""

        if "protocol" in kwargs_keys:
            rich_rule_str += f" protocol name=\"{kwargs['protocol']}\""

        command_str += f" --{action}-rich-rule=\'{rich_rule_str} {rule_action}\'"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password, shell=True)

        if cp.returncode == 0:
            if permanent:
                Firewall.reload(sudo_password=sudo_password)
            return True

        else:
            printf_colorlog(text=f"<{cp.stderr.decode(ENCODING)}>", color="b_red")

        return False

    @staticmethod
    def rule_object(action: str,
                    obj_type: list,
                    value: str,
                    zone: str = None,
                    permanent: bool = False,
                    sudo_password: str = None) -> bool:

        """
        add or remove firewalld rule object in specific zone
        be advised that you can not remove interface from the specific zone in CentOS.

        :param action: assign "add" or "remove" for rule object
        :param obj_type: assign an object type. ['interface', 'port', 'protocol', 'service', 'source']
        :param value: set the value that you want to add or remove. follow the reference with param type
        - interface: name of interface on linux machine
        - port: port_number/protocol
        - protocol: protocol name or ID registered in /etc/protocols.
        - service: name of service that registered in /etc/services
        - sources: ipv4_address_or_network_segment/prefix
        :param zone: specify the zone name in string form where you want to add or remove rule objects. default is default zone
        :param permanent: bool for applying or removing rule objects in permanently
        :param sudo_password: if you need sudo, set the sudo password
        :return: bool whether the rule objects are successfully added / removed or not
        """

        # centos can not add interface to the zone with firewall-cmd.
        # instead firewall-cmd, this code uses nmcli.
        # removing interface with firewall-cmd command and --permanent option can not be allowed due to the SELINUX.
        if obj_type == "interface" and get_linux_dist() == "CentOS Stream 8" and permanent:
            if action == "add":
                return NetworkManager.set_interface_zone(ifc=value, zone=zone, sudo_password=sudo_password)
            return False

        command_str: str = f"firewall-cmd --{action}-{obj_type}={value}"

        if zone is not None:
            command_str += f" --zone={zone}"

        if permanent:
            command_str += f" --permanent"

        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            if permanent:
                Firewall.reload(sudo_password=sudo_password)
            return True

        else:
            printf_colorlog(text=f"<{cp.stderr.decode(ENCODING)}>", color="b_red")

        return False

    @staticmethod
    def set_default_zone(zone: str, sudo_password: str = None) -> bool:

        """
        set the default zone with specific zone

        :param zone: a name of zone which you want to set as default zone
        :param sudo_password: if you need sudo, set the sudo password
        :result : bool whether the default zone is successfully set or not
        """

        if zone not in Firewall.get_all_zones():
            return False

        command_str: str = f"firewall-cmd --set-default-zone={zone}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        printf_colorlog(text=f"<{cp.stderr.decode(ENCODING)}>", color="b_red")
        return False

    @staticmethod
    def reload(sudo_password: str = None) -> bool:

        """
        reload firewalld

        :param sudo_password: if you need sudo, set the sudo password
        :result: bool whether the firewalld is successfully reloaded or not
        """

        command_str: str = "firewall-cmd --reload"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return True

        printf_colorlog(text=f"<{cp.stdout.decode(ENCODING)}>", color="b_red")
        return False
