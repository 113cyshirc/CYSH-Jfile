"""
# Quick Note
- This decoder doesn't support cjf v1
- all value will be stored as str for v2
## v2 types
    - dict  [name]
    - list  [l:name]
    - str   [s:name]
    - int   [d:name]
    - float [f:name]
"""

from io import TextIOWrapper
import json

class FileFormatError(Exception):
    def __init__(self, msg:str="") -> None:
        super().__init__(f"File format error: {msg}")

class Question:
    def  __init__(self,input_:list,output_:list) -> None:
        self.input:list = input_
        self.output:list = output_

def loadcjf(fp:TextIOWrapper) -> dict:
    return loadscjf(fp.read())

def loadscjf(text:str) -> dict:
    class_tag = ""
    type_now = "str"
    result = {}
    lines = text.split("\n")
    file_format = 0
    for i in lines: # read each line
        if len(result) == 0 and i.startswith("CYSHJ file format v"): # get the format
            result["fileformat"] = int(i[19:])
            file_format = result["fileformat"]
            if result["fileformat"] == 1:
                print("[warning] Decoder doesn't support file format v1, and it might produce some error.")
        elif i == "" or i.startswith("//"): # ignore comments and blank line
            continue
        else:
            match file_format:
                case 2:
                    if i.startswith("[") and i.endswith("]"): # read tag
                        class_tag = i[1:-1]
                        type_analyze = class_tag.split(":") # normal tag
                        if len(type_analyze) == 1: # type is a dict
                            type_now = "dict"
                            result[class_tag] = {} # create a new dict
                        else:
                            match type_analyze[0]: # other types
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
                case _:
                    raise FileFormatError("Unsupported Format Version.")
    return result


            

def loadcjt(fp:TextIOWrapper) -> list[Question]:
    return loadscjt(fp.read())

def loadscjt(text:str) -> list[Question]:
    lines = text.split("\n")
    result = []
    class_tag = ""
    in_record = []
    out_record = []
    for i in lines:
        if i == "" or i.startswith("//"):
            continue
        elif i == "[in]":
            if in_record != []:
                result.append(Question(in_record,out_record))
            class_tag = "in"
            in_record = []
            out_record = []
        elif i == "[out]":
            class_tag = "out"
        else:
            match class_tag:
                case "in":
                    in_record.append(i)
                case "out":
                    out_record.append(i)
    result.append(Question(in_record,out_record))

    return result

