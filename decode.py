import cjfdecode

with open("./structure/question.cjf","r",encoding="utf-8") as f:
    print(cjfdecode.loadcjf(f))

    # for i in cjfdecode.loadcjt(f):
    #     print(i.input,i.output)