with open("file.txt", "r+") as f:
    content = f.read()
    f.seek(0)
    f.write("Write content")
    f.truncate()
    
    
