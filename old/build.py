import zipfile
import os
import logging
import time
tm = time.localtime()
logtime = f"{tm.tm_year}-{tm.tm_mon}-{tm.tm_mday}-{tm.tm_hour}-{tm.tm_min}-{tm.tm_sec}"
logging.basicConfig(filename=f"./log/build-{logtime}.log",encoding="utf-8",level=logging.DEBUG,format="[%(levelname)s]  %(message)s")


import update

def build_cjz(dir:str,name:str=None):
    logging.debug("builder: building cjz")
    if name == None:
        name = dir
    print(dir)
    with zipfile.ZipFile(f"{name}.cjz","w") as z:
        for i in os.listdir(dir):
            z.write(f"{dir}/{i}",compress_type=zipfile.ZIP_STORED,arcname=f"{i}")
    logging.info(f"builder: Successfully build {name}.cjz")
    print(f"Successfully build {name}.cjz")


if __name__ == "__main__":
    PATH = "./structure"
    update.Updater(PATH)
    build_cjz(PATH,)