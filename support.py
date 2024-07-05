import os

class FileOperateError(Exception):
    def __init__(self, msg:str="something's wrong with the files.") -> None:
        super().__init__(msg)

class GetFolderError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Cannot get the folder, it did not exist!")

class Supporter:
    """
    # 參數說明
    `path`:題目資料夾
    `output`(選):輸出檔案名稱
    """

    def __init__(self,path:str,output:str=None) -> None:
        self.path:str = path
        self.output:str = output if output != None else path
        self.read()

    def read(self):
        if not os.path.isdir(self.path):
            raise GetFolderError()
        try:
            data_in = ""
            data_out = ""
            open(f"./tests.cjt","w").close() # clear 
            with open(f"./tests.cjt","a",encoding="utf-8") as cjt:
                for i in range(1,len(os.listdir(self.path))//2+1):
                    with open(f"{self.path}/{i}.in","r") as ind:
                        data_in = ind.read()
                    cjt.write(f"[in]\n{data_in}\n\n")
                    with open(f"{self.path}/{i}.out","r") as outd:
                        data_out = outd.read()
                    cjt.write(f"[out]\n{data_out}\n\n")
        except:
            raise FileOperateError()

if __name__ == "__main__":
    Supporter("./1")