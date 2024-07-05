# Script for updating the question.cjf
import zipfile
import os

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
        self.path:str = path
        self.length:int = 0

        self.read()
        self.write()
    
    def read(self):
        if not os.path.exists(f"{self.path}/tests.cjt"):
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
                raise FileReadError()
    def write(self):
        if not os.path.exists(f"{self.path}/question.cjf"):
            raise FileNotFoundError()
        complete = ""
        raw = ""
        with open(f"{self.path}/question.cjf","r",encoding="utf-8") as jf:
            raw = jf.read().split("\n")
        #raw = [x for x in raw if x]
        for i in raw:
            if i.startswith("Tests:"):
                complete += i.split(":")[0] + ":"+ str(self.length)
            else:
                complete += i
            complete += "\n"
        with open(f"{self.path}/question.cjf","w",encoding="utf-8") as jf:
            jf.write(complete)

Updater("./structure")
