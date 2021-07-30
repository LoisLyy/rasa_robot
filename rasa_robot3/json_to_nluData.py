import json
class JsontoNluData:
    def JsontoNlu(nlufile,jsonfile):
        with open(nlufile,"a",encoding="utf-8") as nlufile,open(jsonfile,"r",encoding="utf-8") as jsonfile:
            nlufile.write("nlu:\n")
            jsonText=json.loads(jsonfile.read().splitlines()[0])
            # print(jsonText)
            for item in jsonText["domain"]:
                nlufile.write("- intent: "+item["intent"]+"\n")
                nlufile.write("  examples: |\n")
                for item2 in item["examples"].split("、"):
                    nlufile.write("    - "+item2+"\n")

    def JsontoDomain(domainfile,jsonfile):
        with open(domainfile,"a",encoding="utf-8") as domainfile,open(jsonfile,"r",encoding="utf-8") as jsonfile:
            domainfile.write("intents:\n")
            jsonText=json.loads(jsonfile.read().splitlines()[0])
            # print(jsonText)
            for item in jsonText["domain"]:
                domainfile.write("  - "+item["intent"]+"\n")

            # domainfile.write("entities:\n")
            # entities=[]
            # for item in jsonText["domain"]:
            #     for item2 in item["entities"]:
            #         if item2 not in entities:
            #             entities.append(item2)
            #             # print(item2)
            #             domainfile.write("  - "+item2["entity"]+"\n")  
    def JsontoStories(domainfile,jsonfile):
        with open(domainfile,"a",encoding="utf-8") as domainfile,open(jsonfile,"r",encoding="utf-8") as jsonfile:
            jsonText=json.loads(jsonfile.read().splitlines()[0])
            for item in jsonText["domain"]:
                domainfile.write("- story: 异议处理\n")
                domainfile.write("  steps:\n")
                # print(jsonText)
                domainfile.write("    - intent: "+item["intent"]+"\n")
                domainfile.write("    - action: action_handle_objection\n")            
                domainfile.write("    - action: utter_to_ivr\n")            
if __name__ == '__main__':
    # JsontoNluData.JsontoNlu("nlu_programming.yml","huashu.json")
    JsontoNluData.JsontoStories("stories_programming.yml","huashu.json")