import xlrd
import json
# class FiletoJson:
def transfer(filename):
    workbook=xlrd.open_workbook(filename)
    sheet= workbook.sheet_by_index(0)
    rows=sheet.nrows
    result={}
    domainlist=[]
    contentlist=[]
    entitylist=[]
    for i in range(2,49):            
        intentValue=sheet.cell_value(i,0)
        if len(intentValue)>0:
            if i>2:
                if len(domaindict)>0:
                    domaindict["entities"]=entitylist.copy()
                    domainlist.append(domaindict.copy())
                    entitylist.clear()
                    domaindict.clear()
            intent=sheet.cell_value(i,1)
            tag=sheet.cell_value(i,3)
            huashu=sheet.cell_value(i,4)
            domaindict={"intent":intent,"value":intentValue,"tag":tag,"huashu":huashu}
        else:
            entity=sheet.cell_value(i,1)
            if len(entity)>0:
                if i>3:
                    if len(contentlist)>0:
                        entitydict["content"]=contentlist.copy()
                        contentlist.clear()
                        entitylist.append(entitydict.copy())
                        entitydict.clear()
                entitydict={"entity":entity}
            entityValue=sheet.cell_value(i,2)
            tag=sheet.cell_value(i,3)
            huashu=sheet.cell_value(i,4)
            contentdict={"value":entityValue,"tag":tag,"huashu":huashu}
            contentlist.append(contentdict.copy())
            contentdict.clear()
            if len(sheet.cell_value(i+1,0))>0:
                if len(contentlist)>0:
                    entitydict["content"]=contentlist.copy()
                    contentlist.clear()
                    entitylist.append(entitydict.copy())
                    entitydict.clear()
    result["domain"]=domainlist
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    with open("1.json","w+",encoding="utf-8") as f:
        # f.write(json.dumps(result))
        f.write(json.dumps(result, ensure_ascii=False))
        # f.write(result)
    
    return result

if __name__ == '__main__':
    transfer("IVR.xlsx")
        