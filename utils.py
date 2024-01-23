import json
from selenium.webdriver.common.by import By


ActionAttributes = ['action', 'identyfyBy', 'identifier', 'data', 'waitFor']
TestAttributes = ['url', 'title', 'textTextArr']

extractType = lambda obj: 'webAction' if isinstance(obj, webAction) else ('webTest' if isinstance(obj, webTest) else False)


IdentyfyByDict = {'id':By.ID, 
                 'name': By.NAME, 
                 'xpath': By.XPATH, 
                 'link_text': By.LINK_TEXT, 
                 'partial_link_text': By.PARTIAL_LINK_TEXT, 
                 'tag_name': By.TAG_NAME, 
                 'class_name': By.CLASS_NAME, 
                 'css_selector': By.CSS_SELECTOR
                }

def webElement(identyfyBy:str, identifier:str):
        
    if identyfyBy == '' :
        raise ValueError(f'identyfyBy should not be empty')
    if identifier == '' :
        raise ValueError(f'identifier should not be empty')
    identyfyBy = identyfyBy.lower()

    if identyfyBy not in IdentyfyByDict.keys():
        raise ValueError(f'identyfyBy = {identyfyBy} is not valid')

    return {
        'identyfyBy': identyfyBy,
        'identifier': identifier
    }


class webAction:

    def __init__(self):
        #self.url = url
        self.actions = None

    def webAction(self, action:str, identyfyBy:str='', identifier:str='', data:str='', waitFor:int=0):

        if action == '':
            raise ValueError(f'action should not be empty')
        
        if action == 'single-click':
            if identyfyBy == '' :
                raise ValueError(f'identyfyBy should not be empty')
            if identifier == '' :
                raise ValueError(f'identifier should not be empty')
            self.actions = {
                'action': action,
                'element': {
                    **webElement(identyfyBy, identifier), 
                    'waitFor': waitFor
                    }}
        elif action == 'enter-data':
            if data == '' :
                raise ValueError(f'identifier should not be empty')
            self.actions = {
                'action': action,
                'element': data}

    def __str__(self):
        
        return f'{json.dumps(self.actions, indent=1)}'        





class webTest:
    def __init__(self):
        """
        status : -1 -> failed, 0 -> not started, 1 -> sucess
        """
        self.TestTitle = {
            'title': '',
            'status': 0
        }
        self.TestURL = {
            'url': '',
            'status': 0
        }

        
        # list of all html element object finding method and its coresponding text entry
        self.testTextArr = [] 
 
    def addURLTest(self, url:str):
        if url == '':
            raise ValueError(f'url should not be empty')
        self.TestURL['url'] = url
    
    def addTitleTest(self, title:str):
        if title == '':
            raise ValueError(f'title should not be empty')
        self.TestTitle['title'] = title
    
    def addTextFieldTest(self, identyfyBy:str, identifier:str, text:str, waitFor:int=0):
        if identyfyBy == '' :
                raise ValueError(f'identyfyBy should not be empty')
        if identifier == '' :
                raise ValueError(f'identifier should not be empty')
        
        self.testTextArr.append({
                'text': text,
                'element': {
                    **webElement(identyfyBy, identifier), 
                    'waitFor': waitFor
                    },
                'status': 0
                })
    def __str__(self):
        result = f"URL:\n{json.dumps(self.TestURL, indent=1)}\nTITLE:\n{json.dumps(self.TestTitle)}\ntext array:\n{json.dumps(self.testTextArr, indent=1)}"
        return result       


"""

web = webAction()
web.webAction(action = 'single-click',identyfyBy = 'xpath', identifier ="//a[@class='button account']", waitFor=10)

web.webAction(action = 'single-click',identyfyBy = 'xpath', identifier ="//input[@id='id_username']", waitFor=10)
web.webAction(action = 'enter-data', data = "test123456@mailinator.com")

web.webAction(action = 'single-click',identyfyBy = 'xpath', identifier ="//input[@id='id_password']")
web.webAction(action = 'enter-data', data = "Test@123")

web.webAction(action = 'single-click',identyfyBy = 'xpath', identifier ="//button[contains(normalize-space(), 'Login')]")

<a href="//">Register for free</a>
"""

test = webTest()
test.addURLTest('https://www.screener.in/login/?')
test.addTitleTest('Login - Screener')
test.addTextFieldTest(
     identyfyBy='xpath',
     identifier='//h1',
     text='Welcome back!',
    )

test.addTextFieldTest(
     identyfyBy='xpath',
     identifier='//strong',
     text='Warren Buffett',
     )

#print(test)