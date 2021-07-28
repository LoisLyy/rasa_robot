import json
def JsontoNlu(nlufile,jsonfile):
    with open(nlufile,"a",encoding="utf-8") as nlufile,open(jsonfile,"r",encoding="utf-8") as jsonfile:
        domainfile.write("nlu:\n")
        jsonText=json.loads(jsonfile.read().splitlines()[0])
        # print(jsonText)
        for item in jsonText["domain"]:
            domainfile.write("  - "+item["intent"]+"\n")

        domainfile.write("entities:\n")
        entities=[]
        for item in jsonText["domain"]:
            for item2 in item["entities"]:
                if item2 not in entities:
                    entities.append(item2)
                    # print(item2)
                    domainfile.write("  - "+item2["entity"]+"\n")
                
if __name__ == '__main__':
    JsontoDomain("domain_programming.yml")