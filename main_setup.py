#! /usr/bin/env python

"""
#---------------------------------------------------------+
    _    _                            _                   |
   / \  | |__  _   _ _ __   __ _  ___| |__   __ _ _ __    |
  / _ \ | '_ \| | | | '_ \ / _` |/ __| '_ \ / _` | '__|   |
 / ___ \| |_) | |_| | | | | (_| | (__| | | | (_| | |      |    
/_/   \_\_.__/ \__,_|_| |_|\__,_|\___|_| |_|\__,_|_|      |
                                                          |
#----------------------------------+----------------------+
    Filname : main_setup.py  |
    Author  : Abunachar      |
    Github  : knight-byte    |
#----------------------------+                                                     
"""

# -------- IMPORT ------

import subprocess
import time
import os

# ------ COLOR CLASS --------


class color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def win_remove(self):
        self.HEADER = ""
        self.BLUE = ""
        self.CYAN = ""
        self.GREEN = ""
        self.WARNING = ""
        self.FAIL = ""
        self.RESET = ""
        self.BOLD = ""
        self.UNDERLINE = ""
# ----- MAIN SETUP CLASS


class Setup:
    required_package = ["requests", "python-telegram-bot"]
    DEBUG = True

    def __init__(self) -> None:
        self.color = color()
        self.PY3 = False
        self.PY = False
        self.PIP = False
        self.PYVER = ""
        self.USER_OS = None
        self.BOT_TOKEN = None
        self.PROJECT_NAME = None
        self.ISEMPTY = True if len(os.listdir(os.getcwd())) == 1 else False
        self.run_setup()

    def run_setup(self):
        if os.name.lower() == "nt":
            self.color.win_remove()
        self.head_banner()
        if not self.ISEMPTY and not self.DEBUG:
            print(self.warning_highlight(
                "Folder is not empty, Please start in a Empty Folder"))
            self.exit_program()
        self.python_version()
        self.check_pip()
        self.setup_virtualenv()
        self.detect_os()
        self.install_packages()
        self.user_input()
        self.replace_and_setup_variables()
        self.heroku_setup()
        self.message_after_done()

    # ---- HEAD BANNER --------
    def head_banner(self) -> None:
        banner = f"""\
{self.color.RESET}
{self.color.BLUE} _           _{self.color.WARNING}     ____       _
{self.color.BLUE}| |__   ___ | |_{self.color.WARNING}  / ___|  ___| |_ _   _ _ __
{self.color.BLUE}| '_ \\ / _ \\| __| {self.color.WARNING}\\___ \\ / _ \\ __| | | | '_ \\
{self.color.BLUE}| |_) | (_) | |_ {self.color.WARNING}  ___) |  __/ |_| |_| | |_) |
{self.color.BLUE}|_.__/ \\___/ \\__|{self.color.WARNING} |____/ \\___|\\__|\\__,_| .__/
                                       |_|
                                {self.color.GREEN}-> knight-byte{self.color.RESET}
"""
        print(banner)

    # ------------ SHELL COMMAND EXECUTE ------
    def command_execute(self, command="") -> tuple:
        if command in [[], None, ""]:
            return (69, "Please pass command list")
        else:
            # command = command.split()
            execute = subprocess.Popen(
                args=command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
            success_msg, error_msg = execute.communicate()
            if execute.returncode == 0:
                return (0, success_msg.decode('utf-8'))
            else:
                return (execute.returncode, error_msg.decode('utf-8'))

    # -------------- DETECT OS -----------
    def detect_os(self):
        try:
            user_os = os.name.lower()

            if user_os == "posix":
                text = "OS detected"
                print(self.success_highlight(text=text))
                self.USER_OS = 0
            elif user_os == "nt":
                text = "OS detected"
                print(self.success_highlight(text=text))
                self.USER_OS = 1
        except ImportError:
            text = "Fail to detect OS"
            print(self.warning_highlight(text=text))
            self.exit_program()

    # ---------- SUCCESS / FAIL / WARNING message format -------

    def success_highlight(self, text):
        return f"{self.color.GREEN}[+] {text}{self.color.RESET}"

    def error_highlight(self, text):
        return f"{self.color.FAIL}[x] {text}{self.color.RESET}"

    def warning_highlight(self, text):
        return f"{self.color.FAIL}[!]{self.color.WARNING} {text}{self.color.RESET}"

    def unknown_hightlight(self, text):
        return f"{self.color.WARNING}[?]{self.color.RESET} {text}"

    def exit_program(self) -> None:
        print(f"exit...")
        time.sleep(3)
        exit()

    # --------- PYTHON VERSION CHECK -----------
    def python_version(self) -> None:
        py_ver = "python3 --version"
        status, msg = self.command_execute(command=py_ver)
        if status == 0:
            ver = msg.split()[1]
            text = f"Python3 Found v{ver}"
            print(self.success_highlight(text))
            self.PY3 = True
            self.PYVER = ver
        else:
            py_ver = "python --version"
            status, msg = self.command_execute(command=py_ver)
            ver = msg.split()
            temp = float(".".join(ver.split(".")[:2]))
            if temp > 3.6:
                text = f"Python Found v{ver}"
                print(self.success_highlight(text))
                self.PY = True
                self.PYVER = ver
            else:
                text = f"Python Found v{ver} but required >= 3.6"
                print(self.warning_hightlight(text))
                self.PY = False
                self.exit_program()

    # -------- CHECK PIP -----
    def check_pip(self) -> None:
        py = "python" + ("3" if self.PY3 else "")
        pip3v_c = f"{py} -m pip --version"
        status, msg = self.command_execute(command=pip3v_c)
        if status == 0:
            ver = msg.split()[1]
            text = f"Pip Found v{ver}"
            self.PIP = True
            print(self.success_highlight(text))

            self.command_execute(command=f"{py} -m pip install requirements")
        else:
            text = f"Pip Not found"
            print(self.error_highlight(text))
            self.exit_program()

    # ------ SETUP virtual env -------
    def setup_virtualenv(self):
        text = "setting up Virtual env"
        print(self.unknown_hightlight(text), end="\r")
        py = "python" + ("3" if self.PY3 else "")
        env_c = f"{py} -m pip install virtualenv"
        status, _ = self.command_execute(command=env_c)
        if status == 0:

            print(" "*(2*len(text)), end="\r")
            text = "Install Virualenv, setting up..."
            print(self.unknown_hightlight(text), end="\r")

            start_env = f"{py} -m virtualenv env"
            status, _ = self.command_execute(command=start_env)
            if status == 0:
                print(" "*(2*len(text)), end="\r")
                text = "Virtualenv setup done"
                print(self.success_highlight(text))

            else:
                print(" "*(2*len(text)), end="\r")
                text = "Fail to setup virtualenv"
                print(self.error_highlight(text))
                self.exit_program()
        else:
            print(" "*(2*len(text)), end="\r")
            print(self.error_highlight("Fail to install virtualenv"))
            self.exit_program()

    # ------- PACKAGE INSTALL ------
    def install_packages(self):
        text = "Installing required pip packages"
        time.sleep(1)
        print(self.unknown_hightlight(text), end="\r")
        py = "python" + ("3" if self.PY3 else "")
        for package in self.required_package:
            path = "env/local/bin/" if self.USER_OS == 0 else "env\\Scripts\\"
            install_req = f"{path}{py} -m pip install {package}"
            status, _ = self.command_execute(install_req)
            print(" "*(2*len(text)), end="\r")
            text = f"Installing {package}"
            print(self.unknown_hightlight(text), end="\r")

            if status != 0:
                print(" "*(2*len(text)), end="\r")
                text = f"Error while installing {package}"
                print(self.warning_highlight(text))
                self.exit_program()
        else:
            print(" "*(2*len(text)), end="\r")
            text = f"Successfully installed all packages"
            print(self.success_highlight(text))

    def user_input(self):
        bot_token = input(
            f"{self.color.WARNING}[-] {self.color.CYAN}Enter Bot Token    : {self.color.RESET}").strip()
        proj_name = input(
            f"{self.color.WARNING}[-] {self.color.CYAN}Enter Project Name : {self.color.RESET}").strip()
        self.BOT_TOKEN = bot_token
        self.PROJECT_NAME = "".join(proj_name.split())

    def replace_and_setup_variables(self):
        import requests

        text = "Setting all files and Environment variables"
        time.sleep(1)
        print(self.unknown_hightlight(text), end="\r")
        urls = {
            "__init__": "https://raw.githubusercontent.com/knight-byte/bot-setup/main/BotFunc/bot_init",
            "__main__": "https://raw.githubusercontent.com/knight-byte/bot-setup/main/BotFunc/bot_main",
            "utility/constants": "https://raw.githubusercontent.com/knight-byte/bot-setup/main/BotFunc/bot_constants",
            "utility/basic_func": "https://raw.githubusercontent.com/knight-byte/bot-setup/main/BotFunc/basic_func",

        }
        os.mkdir(self.PROJECT_NAME)
        os.mkdir(f"{self.PROJECT_NAME}/utility")
        os.mkdir(f"{self.PROJECT_NAME}/pyfunc")
        os.mkdir(f"{self.PROJECT_NAME}/test")
        for url in urls:
            try:
                print(" "*(2*len(text)), end="\r")
                text = f"setting {url}.py"
                print(self.unknown_hightlight(text), end="\r")
                data = requests.get(url=urls[url]).text
                data = data.replace("<UserDirName>", self.PROJECT_NAME)
                with open(f"{self.PROJECT_NAME}/{url}.py", "w") as f:
                    f.write(data)
            except Exception:
                print(" "*(2*len(text)), end="\r")
                text = f"Error in {url}.py"
                print(self.error_hightlight(text))
                self.exit_program()

        export_txt = f"""\n\n
# --------- EXPORTS ----------
export bot_token={self.BOT_TOKEN}
"""
        ext = ""
        if self.USER_OS == 1:
            export_txt = f'set "bot_token={self.BOT_TOKEN}"'
            ext = ".bat"

        path = "env/local/bin/" if self.USER_OS == 0 else "env\\Scripts\\"
        with open(f"{path}activate{ext}", "a") as f:
            f.write(export_txt)

        print(" "*(2*len(text)), end="\r")
        text = f"Done setting up"
        print(self.success_highlight(text))

    def heroku_setup(self):
        # ------heroku setup
        text = "Setting up heroku config"
        print(self.unknown_hightlight(text), end="\r")
        py = "python" + ("3" if self.PY3 else "")
        # ---- requirements.txt setup
        print(" "*(2*len(text)), end="\r")
        text = f"Adding requirements.txt"
        print(self.unknown_hightlight(text), end="\r")
        path = "env/local/bin/" if self.USER_OS == 0 else "env\\Scripts\\"
        req_com = f"{path}{py} -m pip freeze"
        status, msg = self.command_execute(command=req_com)
        if status == 0:
            with open("requirements.txt", "w") as f:
                f.write(msg)
        else:
            print(" "*(2*len(text)), end="\r")
            text = f"Error in requirements.txt, Ignoring"
            print(self.warning_hightlight(text))
        # ------- Procfile
        print(" "*(2*len(text)), end="\r")
        text = f"Adding Procfile"
        print(self.unknown_hightlight(text), end="\r")
        with open("Procfile", "w") as f:
            f.write(f"web: {py} -m {self.PROJECT_NAME}")
        # ------ runtime.txt
        print(" "*(2*len(text)), end="\r")
        text = f"Adding runtime.txt"
        print(self.unknown_hightlight(text), end="\r")
        with open("runtime.txt", "w") as f:
            f.write(f"python-{self.PYVER}")
        # ------ .gitignore ----
        print(" "*(2*len(text)), end="\r")
        text = f"Adding .gitignore"
        print(self.unknown_hightlight(text), end="\r")
        ign = f"env/*\n{self.PROJECT_NAME}/test/*\n{self.PROJECT_NAME}/**/__pycache__/*"
        with open(".gitignore", "w") as f:
            f.write(ign)

        print(" "*(2*len(text)), end="\r")
        text = f"Done heroku setup"
        print(self.success_highlight(text))

    def message_after_done(self):
        win = r".\env\Scripts\activate"
        text = f"""
{self.color.WARNING}[ 1 ]{self.color.BLUE} : start up virtualenv
        {self.color.HEADER}{"source env/local/bin/activate" if self.USER_OS==0 else win} 
{self.color.WARNING}[ 2 ]{self.color.BLUE} : start bot
        {self.color.HEADER}{"python" + ("3" if self.PY3 else "")} -m {self.PROJECT_NAME}
{self.color.CYAN}
+--------------------------------+
|     (c) abunachar 2021         |
+--------------------------------+
"""

        print(text)


def main():
    Setup()


if __name__ == '__main__':
    main()
