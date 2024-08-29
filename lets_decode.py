import cjfile

with open("./editor/test/question.cjf",'r+',encoding="utf-8") as f:
    print(cjfile.loadcjf(f))
print()
with open("./editor/test/tests.cjt",'r+',encoding="utf-8") as f:
    print(cjfile.loadcjt(f))
