import cjfile
 
with open("./structure/tests.cjt",'r+',encoding="utf-8") as f:
    ff = cjfile.loadcjt(f)
    cjfile.dumpcjt(ff,f)