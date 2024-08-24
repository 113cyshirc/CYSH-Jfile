import cjfile



 
with open("./structure/tests.cjt",'r+',encoding="utf-8") as f:
    print(cjfile.loadcjt(f))