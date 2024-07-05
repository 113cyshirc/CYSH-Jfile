# Script for updating the question.cjf
import zipfile
import os
import logging
import time
tm = time.localtime()
logtime = f"{tm.tm_year}-{tm.tm_mon}-{tm.tm_mday}-{tm.tm_hour}-{tm.tm_min}-{tm.tm_sec}"
logging.basicConfig(filename=f"./log/update-{logtime}.log",encoding="utf-8",level=logging.DEBUG,format="[%(levelname)s]  %(message)s")


class TestsDecodeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Error reading tests file.")

class FileNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("File not found!!!")

class FileReadError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Error reading the file, it might have been corrupted.")

class Updater:
    """
    # 參數說明
    `path` 資料夾路徑
    """
    def __init__(self,path:str) -> None:
        logging.debug("updater: starting updater")
        self.path:str = path
        self.length:int = 0

        self.read()
        self.write()
        logging.info(f"updater: successfully updated {self.path}/question.cjf")
    
    def read(self):
        logging.debug(f"updater: reading {self.path}/tests.cjt")
        if not os.path.exists(f"{self.path}/tests.cjt"):
            logging.error("updater: file not found!")
            raise FileNotFoundError()
        with open(f"{self.path}/tests.cjt","r") as tf:
            raw = tf.read().split("\n")
            raw = [x for x in raw if x]
            now_command = ""
            for i in raw:
                if i.startswith("[") and i.endswith("]"):
                    if now_command == "[in]" and i == "[out]":
                        self.length += 1
                    now_command = i
            if now_command == "[in]" or now_command == "":
                self.length = 0
                logging.error("updater: Error reading the file, it might have been corrupted.")
                raise FileReadError()
        logging.debug(f"updater: read done")
    def write(self):
        logging.debug(f"updater: writing {self.path}/question.cjf")
        if not os.path.exists(f"{self.path}/question.cjf"):
            logging.error("updater: file not found!")
            raise FileNotFoundError()
        complete = ""
        raw = ""
        with open(f"{self.path}/question.cjf","r",encoding="utf-8") as jf:
            raw = jf.read().split("\n")
        
        for i in raw:
            if i.startswith("Tests:"):
                complete += i.split(":")[0] + ":"+ str(self.length)
            else:
                complete += i
            complete += "\n"
        with open(f"{self.path}/question.cjf","w",encoding="utf-8") as jf:
            jf.write(complete)
        logging.debug(f"updater: write done")

if __name__ == "__main__":
    Updater("./structure")
