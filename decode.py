import cjfdecode

# with open("./structure/question.cjf","r",encoding="utf-8") as f:
#     print(cjfdecode.loadcjf(f))

with open("./structure/tests.cjt","r",encoding="utf-8") as f:
    for i in cjfdecode.loadcjt(f):
        print(i.input,i.output)