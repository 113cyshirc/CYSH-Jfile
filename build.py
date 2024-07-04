import zipfile
import os

# with zipfile.ZipFile("test.cjz","w") as z:
#     for i in os.listdir("./structure"):
#         z.write(f"./structure/{i}",compress_type=zipfile.ZIP_STORED,arcname=f"{i}")


def build_cjz(dir:str,name:str=None):
    if name == None:
        name = dir
    with zipfile.ZipFile(f"{name}.cjz","w") as z:
        for i in os.listdir(dir):
            z.write(f"{dir}/{i}",compress_type=zipfile.ZIP_STORED,arcname=f"{i}")

build_cjz("./structure","test")