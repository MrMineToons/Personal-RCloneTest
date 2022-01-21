import logging

logging.basicConfig(filename=r"C:\AutoRClone\LOG\LogDoPython.log",
                    encoding="utf-8",
                    filemode="a",
                    format="%(asctime)s, %(levelname)s: %(message)s",
                    datefmt="%d/%m/%Y às %H:%M:%S",
                    level=logging.INFO)

logging.getLogger('apscheduler').setLevel(logging.WARNING)
logger = logging.getLogger("LogDoPython")
