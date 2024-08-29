"""
# Quick Note
- Every [] tag and //comment will have a new line on top of them
- only long string, list uses [] tag

# cjf syntax
- `key:value` <- key to value syntax
- `[type:name]` <- only for list and long strings
- `//` <- comments

# cjt syntax
- `[in],[out]` <- in,out tag
- `==sub:n==` <- sub points
- `//` <- comments
```python
return [
    ([input:list,output:list,isSub:bool])
]
```
"""

from io import TextIOWrapper
import zipfile
import os

# Exceptions
class FileCorrupt(Exception):
    def __init__(self, line:int, content:str,msg:str="") -> None:
        msg = '\n'+msg if msg!='' else ''
        super().__init__(f"An Error occured when reading line{line}\n{line}| {content}\n{' '*len(str(line))}  ^{msg}")

class FileWriteError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("cannot write to file, please check if the file is writable")

def loadcjf(fp:TextIOWrapper) -> dict:
    return loadscjf(fp.read())

def loadscjf(text:str) -> dict:
    # [comment description]
    # EOF: End Of File

    lines = text.split("\n") # get each line
    result = {}
    result["_format"] = int(lines[0][19:]) # get format version

    # temps
    comment_count = 0
    is_reading_tag = False
    tag_class = "string"
    tag_name = ""
    builder = ""
    for l,i in enumerate(lines[1:]): # for everyline from line 1
        if not is_reading_tag: # if it's not reading a long data
            if i == "": # is a blank line, then skip it
                continue
            elif i.startswith("//"): # is a comment
                result[f"_comment{comment_count}"] = i[2:]
                comment_count += 1
            elif i.startswith("[") and i.endswith("]"): # is a tag
                is_reading_tag = True # flag the tag reading
                tag_p = i[1:-1].split(":") # seperate type and name
                tag_class = tag_p[0] # the type of the data of the tag
                tag_name = tag_p[1] # the name of the tag
                match tag_p[0]: # see what type to build
                    case "l":
                        builder = []
                    case "s":
                        builder = ""
            else: # the data is a normal key:value
                kv = i.split(":")
                result[kv[0]] = kv[1] # kv[0] is key, and kv[1] is value
        else: # if it is reading a tag
            try: # to prevent EOF
                if not lines[1:][l+1].startswith("["): # if the next line is not a tag, then keep reading
                    match tag_class: # see what type to build
                        case "l":
                            builder.append(i)
                        case "s":
                            builder += i+"\n"
                else: # if the next line is a tag, then save the read value and reset builder
                    result[tag_name] = builder # dump thing have been read in to the result
                    builder = "" # reset builder
                    is_reading_tag = False # well, this line is actually useless
            except: # next line is EOF, so save the read value
                builder += i+"\n"
                result[tag_name] = builder # dump thing have been read in to the result
                builder = ""
                is_reading_tag = False
    return result

def tocjf(d:dict) -> str:
    # [comment description]
    # kv, kv pair: key,value (pair)
    # dict: dictionary

    result = "" 
    for k,v in d.items(): # go through all k,vs in the dict
        if k == "_format": # format encode
            result += f"CYSHJ file format v{v}"
        elif k.startswith("_comment"): # the comments
            result += f"\n//{v}"
        elif type(v) == list: # if the value is list, then add [l:]
            result += f"\n[l:{k}]"
            for j in v: # make every item in the list a new line 
                result += f"\n{j}"
        elif "\n" in v: # if the value is a string (it doesn't matter a kv pair or string, they will all be decode as the same)
            result += f"\n[s:{k}]\n{v[:-1]}" # [:-1] to fix the extra \n
        else: # kv pair
            result += f"{k}:{v}"
        result += "\n"
    return result

def dumpcjf(d:dict,fp:TextIOWrapper):
    if fp.writable():
        fp.seek(0)
        fp.write(tocjf(d))
        fp.truncate()
    else:
        raise FileWriteError()

def loadcjt(fp:TextIOWrapper) -> list[tuple]:
    return loadscjt(fp.read())

def loadscjt(text:str) -> list[tuple]: 
    # [comment description]
    # sub: sub question points

    lines = text.split("\n") # get each line
    result = []

    # temp
    tag_class = ""
    in_record = []
    out_record = []
    for i in lines: # for each line
        if i == "" or i.startswith("//"): # ignore comment and blank, comments will be overwritten every update
            continue
        elif i == "[in]" or (i.startswith("==") and i.endswith("==")): # [in] or ==sub:n==
            if in_record != []: # save the read values..., if they exist
                result.append((in_record,out_record,False)) # append in the result, False mean it's not a sub
                in_record = [] # reset all builders
                out_record = []
            if i.startswith("==") and i.endswith("=="): # this is a sub syntax
                percent = int(i[2:-2].split(":")[1].replace(" ","")) # get the sub value
                result.append((percent,True)) # append to the result list with True, which mean it's a sub
            elif i == "[in]": # if it's a [in] tag, then change reading type
                tag_class = "in"
        elif i == "[out]": # if the tag is out, then change the reading type
            tag_class = "out"
        else: # reading the content of a tag
            match tag_class: # check which type is reading 
                case "in": # append to the correct builder
                    in_record.append(i)
                case "out":
                    out_record.append(i)
    if in_record != []: # if the after the last line, there's still thing didn't append, append it
        result.append((in_record,out_record,False))
    return result

def appendTests(input_:list,output:list,original:list):
    original.append((input_,output,False)) # simply append
    return original

def tocjt(l:list) -> str:
    # [comment description]
    # sub: sub question points
    # [notice]
    # I made up the \n new line amount, so 頑張って！

    result = ""
    for i in l: # for each line
        if i[-1]: # if it's a sub
            result += f"==sub:{i[0]}==\n\n" # rjust append it
        else: # if it's a (in, out)
            in_string = "" # string builders
            out_string = ""
            for j in i[0]: # build in string
                in_string += j + "\n"
            for j in i[1]: # build out string
                out_string += j + "\n"
            result += f"[in]\n{in_string}\n[out]\n{out_string}\n" # append it
    return result

def dumpcjt(l:list,fp:TextIOWrapper):
    if fp.writable():
        fp.seek(0) # move to first char
        fp.write(tocjt(l)) # write
        fp.truncate()
    else:
        raise FileWriteError()
    
def packcjz(dir:str):
    if os.path.isdir(dir):
        with zipfile.ZipFile(f"{dir}.cjz","w") as z:
            for i in os.listdir(dir):
                z.write(f"{dir}/{i}",compress_type=zipfile.ZIP_STORED,arcname=f"{i}")
    else:
        return FileWriteError()