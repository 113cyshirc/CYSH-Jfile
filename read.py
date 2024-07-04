import zipfile
import os,shutil

class NotCjFileError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("This is not a CJ file!")

class UnsupportedFileVersion(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("This file version is not supported right now!")

class FileReadError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Error reading the file, it might have been corrupted.")

class CJFile:
    """
    CYSHJ-題目檔讀取的結果
    # 使用方法
    CJFile(`路徑`)
    使用 CJFile.read()
    # 參數
    `fileVersion` (int) 編碼版本

    `difficulty` (float) 題目難度

    `compatibilityMode` (bool) 使用in out相容模式

    `sampleTests` (int) 題目顯示的測試資料

    `tests` (int) 全部測資數

    `title` (str) 題目翻譯後標題

    `titleUnicode` (str) 題目原文標題

    `author` (str) 原作者翻譯後名字

    `authorUnicode` (str) 原作者原文名字

    `creator` (str) 上傳者

    `version` (int) 版本(目前無用)

    `source` (str) 來源

    `tags` (list) 標籤

    `questionID` (str) 題目在題庫的id

    `questionSetID` (str) 題目在題庫有分類的id

    `args` (list) 所有arguments名稱

    `question` (str) 題目敘述

    """
    def __init__(self,path:str) -> None:
        self.path:str = path
        # general
        self.fileVersion:int = None # DECIDE int or str
        self.difficulty:float = None
        self.compatibilityMode:bool = None
        self.sampleTests:int = None
        self.tests:int = None

        # metadata
        self.title:str = None
        self.titleUnicode:str = None
        self.author:str = None
        self.authorUnicode:str = None
        self.creator:str = None
        self.version:int = None
        self.source:str = None
        self.tags:list = []
        self.questionID:str = None
        self.questionSetID:str = None

        # other
        self.args:list = []
        self.question:str = ""
        self.read()
    
    def read(self):
        if not self.path.endswith(".cjz"):
            raise NotCjFileError()
        if not os.path.exists(self.path):
            raise FileNotFoundError("could not find the file you want!!!")
        
        
        with zipfile.ZipFile(self.path,"r") as zip:
            zip.extractall("./temp")
        raw = ""
        with open("./temp/question.cjf","r",encoding="utf-8") as cjf:
            raw = cjf.read()
        lines = raw.split("\n")
        lines = [x for x in lines if x] # remove blanks
        self.fileVersion = int(lines[0].split("CYSHJ file format v")[1])
        result:dict = {}
        match self.fileVersion:
            case 1:
                keyed_read_done = False
                last_command = ""
                # keyed args
                keyed_args = ["Difficulty","CompatibilityMode","SampleTests","Tests","Title","TitleUnicode",
                              "author","authorUnicode","Creator","Version","Source","Tags","QuestionID","QuestionSetID"]
                for i in lines:
                    if not keyed_read_done:
                        if i.startswith(keyed_args[0]):
                            result[keyed_args[0]] = i.split(":")[1] # take the value after ":" and write to dict
                            keyed_args.pop(0)
                        if len(keyed_args) == 0:
                            keyed_read_done = True
                    else:
                        if i.startswith("[") and i.endswith("]"):
                            last_command = i
                        elif last_command == "[args]":
                            self.args.append(i)
                        elif last_command == "[question]":
                            self.question+=i+"\n"
                try:
                    self.difficulty = float(result["Difficulty"])
                    self.compatibilityMode = result["CompatibilityMode"] == "True"
                    self.sampleTests = int(result["SampleTests"])
                    self.tests = int(result["Tests"])
                    self.title = result["Title"]
                    self.titleUnicode = result["TitleUnicode"]
                    self.author = result["author"]
                    self.authorUnicode = result["authorUnicode"]
                    self.creator = result["Creator"]
                    self.version = int(result["Version"])
                    self.source = result["Source"]
                    self.tags = result["Tags"].split()
                    self.questionID = result["QuestionID"]
                    self.questionSetID = result["QuestionSetID"]
                except:
                    raise FileReadError()

            case _:
                raise UnsupportedFileVersion()

        shutil.rmtree("./temp")
            

# zip = zipfile.ZipFile("./test.cjz","r")
# print(zip.namelist())

file = CJFile("./test.cjz")
print(file.difficulty,
      file.compatibilityMode,
      file.sampleTests,
      file.tests,
      file.title,
      file.titleUnicode,
      file.author,
      file.authorUnicode,
      file.creator,
      file.version,
      file.source,
      file.tags,
      file.questionID,
      file.questionSetID,
      file.args,
      file.question)
