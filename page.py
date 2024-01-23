import json
from utils import webAction, webTest, ActionAttributes, TestAttributes, extractType

class ActionTestChain:
    def __init__(self, url:str):
        if url == '':
            raise ValueError("URL is empty")
        self.url = url
        """
        a page object consists of a list with map of webAction and webTest
        """
        self.procedureChain = []
        #self.testChain = []
    
    def addAction(self, obj):
        action, identyfyBy, identifier, data, waitFor=('','','','',0)
        web = webAction()

        for key in ActionAttributes:
            if key in obj.keys():
                if key == 'action':
                    action = obj[key]
                elif key == 'identyfyBy':
                    identyfyBy = obj[key]
                elif key == 'identifier':
                    identifier = obj[key]
                elif key == 'data':
                    data = obj[key]
                elif key == 'waitFor':
                    waitFor = obj[key]
        try:
            web.webAction(action, identyfyBy, identifier, data, waitFor)
            self.procedureChain.append(web)
        except Exception as e:
            print(f"An error occurred: {e}")

    def addTests(self, obj):
        
        test = webTest()

        for key in TestAttributes:
            if key in obj.keys():
                if key == 'url':
                    test.addURLTest(obj[key])
                elif key == 'title':
                    test.addTitleTest(obj[key])
                elif key == 'textTextArr':
                    try :
                        #print(f"textTextArr -> {obj[key]}")
                        for dic in obj[key]:
                            waitFor = dic['waitFor'] if 'waitFor' in dic.keys() else 0
                            identyfyBy, identifier, text,   = dic['identyfyBy'], dic['identifier'], dic['text']
                            test.addTextFieldTest(identyfyBy, identifier, text, waitFor)
                        
                    except Exception as e:
                        print(f"An error occurred: {e}")

        self.procedureChain.append(test)
    def __str__(self):

        action = "\n".join(f"****\t{index} : {extractType(val)}\t****\n" + str(val) for index, val in enumerate(self.procedureChain))

        return f'url = {self.url} \nAction and test obj list: \n {action}'        



def BuildActionTestChainFromJSON(obj):
    chain = ActionTestChain(obj['url'])

    data = obj['chain']
    for d in data:
        if d['type'] == 'action':
            chain.addAction(d['object'])
        elif d['type'] == 'test':
            chain.addTests(d['object'])
    
    return chain
