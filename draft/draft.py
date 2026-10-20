from datetime import datetime

PYTHON_VERSION_FILE = ".pythonversion"


def read_version_from_file() -> str | None:
    """
    - Read the python version from PYTHON_VERSION_FILE
    - Return the retreived version number of None if the file is empty
    - Raises:
        - FileNotFoundError if file does not exist
    """
    try:
        with open(PYTHON_VERSION_FILE, "r") as f:
            content = f.read()
            if not content:
                return None
            return content
    except FileNotFoundError:
        raise


# how to call a function and deal with returned value and the raised Exception
try:
    result = read_version_from_file()
    if result:
        print(f"python version = {result}")
    else:
        print("file is empty, unable to detect the python version")
except Exception as e:
    print(f"log: {e}")





def logit(message: str) -> None:
    """
    Print a log message
    - message: the message to
    Return None
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} - {message}")


# logging with no possible exception
logit("message test")