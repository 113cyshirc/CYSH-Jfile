import zipfile

zip = zipfile.ZipFile("./test.cjz","r")
print(zip.namelist())

