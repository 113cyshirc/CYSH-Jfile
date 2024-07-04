# Script for updating the question.cjf
import zipfile
import os

class TestsDecodeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Error reading tests file.")

class Updater:
    """
    # 參數說明
    `path` 資料夾路徑
    """
    def __init__(self,path:str) -> None:
        self.path:str = path
        self.length:int = 0
    
    def read(self):
        if os.path.exists(f"{self.path}/tests.cjt"):
            with open(f"{self.path}/tests.cjt") as tf:
                raw = tf.read().split("\n")
                for i in raw:
                    