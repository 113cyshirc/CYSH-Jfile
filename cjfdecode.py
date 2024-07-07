"""
# Quick Note
- This decoder doesn't support cjf v1
- all value will be stored as str for v2

"""

from io import TextIOWrapper

class FileFormatError(Exception):
    def __init__(self, msg:str="") -> None:
        super().__init__(f"File format error: {msg}")

class Question:
    def  __init__(self) -> None:
        pass

def loadcjf(fp:TextIOWrapper) -> dict:
    return loadscjf(fp.read())

def loadscjf(text:str) -> dict:
    class_tag = ""
    type_now = "str"
    result = {}
    lines = text.split("\n")
    for i in lines:
        if len(result) == 0 and i.startswith("CYSHJ file format v"): # get the format
            result["fileformat"] = int(i[19:])
            if result["fileformat"] == 1:
                print("[warning] Decoder doesn't support file format v1, and it might produce some error.")
        elif i == "" or i.startswith("//"):
            continue
        else:
            if i.startswith("[") and i.endswith("]"):
                class_tag = i[1:-1]
                type_analyze = class_tag.split(":")
                if len(type_analyze) == 1:
                    type_now = "dict"
                    result[class_tag] = {} # create a new dict
                else:
                    match type_analyze[0]:
                        case "l":
                            type_now = "list"
                            result[type_analyze[1]] = []
                            class_tag = type_analyze[1]
                        case "s":
                            type_now = "str"
                            result[type_analyze[1]] = ""
                            class_tag = type_analyze[1]
                        case "d":
                            type_now = "int"
                            result[type_analyze[1]] = 0
                            class_tag = type_analyze[1]
                        case "f":
                            type_now = "float"
                            result[type_analyze[1]] = 0.0
                            class_tag = type_analyze[1]
                        case _:
                            raise FileFormatError("Unsupported Type")
            else:
                match type_now:
                    case "dict":
                        
                        key,value = i.split(":")
                        result[class_tag][key] = value
                    case "list":
                        result[class_tag].append(i)
                    case "str":
                        result[class_tag] = i
                    case "int":
                        result[class_tag] = int(i)
                    case "float":
                        result[class_tag] = float(i)

    return result


            

def loadcjt(file:TextIOWrapper) -> list[Question]:
    pass
