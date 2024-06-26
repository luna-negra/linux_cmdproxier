import subprocess


ENCODING: str = "utf-8"


def execute_command_run(command_str: str,
                        stdout: int = subprocess.PIPE,
                        stderr: int = subprocess.PIPE,
                        shell: bool = False,
                        sudo_password: str = None
                        ) -> subprocess.CompletedProcess:

    """
    execute os command and return subprocess.CompletedProcess.

    :param command_str: os command you want to execute.
    :param stdout:  set where the result will be stored. default is subprocess.PIPE.
                    if you want to print the result on the screen, set the value None.
    :param stderr:  set where the error will be stored. default is subprocess.PIPE.
                    if you want to print the result on the screen, set the value None
    :param shell:   set the 'shell' options for subprocess.run()
    :param sudo_password: if you want to execute command with sudo, set the sudo password.
    :return: executed result with subprocess.CompletedProcess
    """

    if sudo_password is not None:
        shell: bool = True
        command_str = f"echo {sudo_password} | sudo -S {command_str}"

    if not shell:
        command_str = command_str.split(" ")

    return subprocess.run(args=command_str, stdout=stdout, stderr=stderr, shell=shell)


def execute_command_popen(command_str: str,
                          stdout: int = subprocess.PIPE,
                          stderr: int = subprocess.PIPE,
                          shell: bool = False,
                          sudo_password: str = None
                          ) -> subprocess.Popen:

    """
    execute os command and return subprocess.Popen.
    If you need to execute command and get result in real-time, use this function instead of 'execute_command_run()'

    :param command_str: os command you want to execute.
    :param stdout:  set where the result will be stored. default is subprocess.PIPE.
                    if you want to print the result on the screen, set the value None.
    :param stderr:  set where the error will be stored. default is subprocess.PIPE.
                    if you want to print the result on the screen, set the value None
    :param shell:   set the 'shell' options for subprocess.Popen()
    :param sudo_password: if you want to execute command with sudo, set the sudo password.
    :return: executed result with subprocess.Popen
    """

    if sudo_password is not None:
        shell: bool = True
        command_str = f"echo {sudo_password} | sudo -S {command_str}"

    if not shell:
        command_str = command_str.split(" ")

    return subprocess.Popen(args=command_str, stdout=stdout, stderr=stderr, shell=shell)


def get_specific_env_values(grep_str: str = None) -> str | None:
    """
    get the environmental variables on linux machine.

    :param grep_str: if you want to get a specific variables with grep, set the variables' name.
    :return: result of 'env' command or 'env' command with 'grep'.
    """

    command_str: str = f"env"
    if grep_str is not None:
        command_str += f" | grep {grep_str}"

    cp = execute_command_run(command_str=command_str, shell=True)
    if cp.returncode == 0:

        for line in cp.stdout.decode(ENCODING).split("\n"):
            if line.startswith(grep_str):
                return line.split("=")[1]

    return None


def get_linux_dist() -> str | None:

    """
    return what linux distro are you working with.

    :return: result of command cat /etc/os-release as string.
    """

    command_str: str = "cat /etc/os-release | grep PRETTY_NAME"
    cp = execute_command_run(command_str=command_str, shell=True)

    if cp.returncode == 0:
        return cp.stdout.decode(ENCODING).split("\"")[1]

    return None


def get_interface_ipv4_addr(ifc_name: str) -> str | None:

    """
    return only ipv4 address of ifc_name on linux machine.

    :param ifc_name: name of interface that you want to check the ipv4 address
    :return : ipv4 address of ifc_name.
    """

    command_str: str = f"ip add | grep {ifc_name} | grep inet"
    cp = execute_command_run(command_str=command_str, shell=True)

    if cp.returncode == 0:
        return list(filter(lambda a: a != "", cp.stdout.decode(ENCODING).split(" ")))[1]

    return None


def printf_colorlog(text: str, color: str = "white") -> None:

    """
    print colorful text on the terminal.
    set the <> at the start and end of the sentence you want to highlight.

    :param text: set the text you want to print out on your terminal. don't forget to insert '<' and '>'.
    :param color: set the text color you want to highlight. please refer to variable 'color_code'.
    :return: None
    """

    color_code: dict = \
        {
            "white": "\033[0m",
            "gray": "\033[30m",
            "red": "\033[31m",
            "b_red": "\033[1;31m",
            "green": "\033[32m",
            "b_green": "\033[1;32m",
            "yellow": "\033[33m",
            "b_yellow": "\033[1;33m",
            "blue": "\033[34m",
            "b_blue": "\033[1;34m",
            "purple": "\033[35m",
            "b_purple": "\033[1;35m",
            "turquoise": "\033[36m",
            "b_turquoise": "\033[36m"
        }

    if "<" in text and ">" not in text:
        text += ">"

    text: str = text.replace("<", color_code[color]).replace(">", color_code["white"])
    command_str: str = f"echo -e {text}"

    execute_command_run(command_str=command_str, stdout=None, stderr=None)
    return None


def print_wo_change_line(text: str) -> None:

    """
    print text on the terminal but not change the line at the end of the text.

    :param text: set the text you want to print out on your terminal without changing line.
    :return: None
    """

    command_str: str = f"echo -n {text}"
    cp = execute_command_run(command_str=command_str, stdout=None, stderr=None)

    if cp.returncode != 0:
        print(cp.stderr.decode(ENCODING))

    return None
