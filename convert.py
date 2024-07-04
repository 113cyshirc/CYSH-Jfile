import zipfile
import os

with zipfile.ZipFile("test.cjz","w") as z:
    for i in os.listdir("./structure"):
        z.write(f"./structure/{i}",compress_type=zipfile.ZIP_STORED,arcname=f"{i}")