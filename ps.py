from .__init__ import execute_command_run, ENCODING


class ProcessMonitor:

    @staticmethod
    def get_process_by_id(pid: int, sudo_password: str = None) -> list | None:

        """
        get process information by process id.

        :param pid: process id which you want to see.
        :param sudo_password: if you need sudo, set the sudo password
        :return: return the result of command 'ps -aux | grep {PSID}'
        """

        command_str: str = f"ps -aux | grep {pid}"
        cp = execute_command_run(command_str=command_str, sudo_password=sudo_password)

        if cp.returncode == 0:
            return list(filter(lambda a: a != '', cp.stdout.decode(ENCODING).split("\n")))[:-1]

        return None
