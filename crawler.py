import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

from utils import extractType, IdentyfyByDict
from page import ActionTestChain

import time


def AssertFunc( condition, success_message, error_message): 
    """
    check the condition if returns true and pring success message 
                        else retruns false and pring failure message
    """
    if condition():
        print(f'AssertoinPass: {success_message}')
        return True
    else:
        print(f'AssertionError: {error_message}'),
        return False

class Crawler():

    def __init__(self, obj:ActionTestChain):
        self.driver = webdriver.Chrome()
        self.chainObj = obj
        try:
            self.driver.get(obj.url)
        except Exception as e:
            # Handle the exception
            print(f"An error occurred: {e}")
        
    def findElement(self, identyfyBy:str, identifier:str, waitFor:int):
        """
        find the element in the web page and return the html element
        act(xpath, "//a[@class='button account']") 
        """
        element = None
        if identyfyBy in IdentyfyByDict.keys():
            try : 
                element = WebDriverWait(self.driver, waitFor).until(
                     EC.presence_of_element_located((IdentyfyByDict[identyfyBy], identifier))    )
            except NoSuchElementException:
                    # If the element is not found, print an error message
                    raise ValueError(f"Element {identifier} not found by the method {identyfyBy}")
            except Exception as e:
                    # Handle the exception
                    raise(f"An error occurred: {e}")
                

            return element
            
        ### if the identyfyBy is not in IdentyfyByArr
        raise ValueError(f'identyfyBy = {identyfyBy} is not valid')
 
    def crawl(self, debug_mode:bool, show_test:bool):
        
        self.driver.implicitly_wait(0.5)
        
        element_list = [] # keep track of all the element 
        

        for dic in self.chainObj.procedureChain:
            
            if extractType(dic) == 'webAction':

                dic = dic.actions
                action =  dic['action']
                
                if action == 'single-click':
                    element = dic["element"]
                    identyfyBy, identifier, waitFor = element['identyfyBy'],element['identifier'], element['waitFor']
            
                    element = self.findElement(identyfyBy, identifier, waitFor)
                    element_list.append(element)
                    if debug_mode:
                        print('*****\t Debug Log: action \t*****')
                        print(f'Object: {json.dumps(dic, indent=1)}\n')
                        print(f'OuterHTML: {element.get_attribute("outerHTML")}')

                    element.click()

                elif action == 'enter-data':
                    data = dic["element"]

                    #input should be sent to the previously selected html element 
                    if len(element_list) == 0:
                        raise(RuntimeError("No html element to incert data"))
                    try:
                        element_list[-1].send_keys(data)
                        if debug_mode:
                            print('*****\t Debug Log: action \t*****')
                            print(f'Object: {json.dumps(dic, indent=1)}\n')
                            print(f'Operation on: {element.get_attribute("outerHTML")}')
                    except ElementNotInteractableException as e:
                        print(f"Element Not Interactable Exception: {e}")
                    except StaleElementReferenceException as e:
                        print(f"Element stale Exception: {e}")
                    except Exception as e:
                        # Handle the exception
                        print(f"An error occurred: {e}")
            
            elif extractType(dic) == 'webTest':
                
                
                if dic.TestTitle['title'] != '':
                    assertFuncResult = AssertFunc(
                        lambda : self.driver.title == dic.TestTitle['title'],
                        f"Title  $:-> {dic.TestTitle['title']} <-:$ matches the expected value.",
                        f"Title expected: $:-> {dic.TestTitle['title']} <-:$, Actual: $:-> {self.driver.title} <-:$.",
                    )
                    dic.TestTitle['status'] = 1 if assertFuncResult else - 1
                    
        
                if dic.TestURL['url'] != '':

                    assertFuncResult = AssertFunc(
                        lambda : self.driver.current_url == dic.TestURL['url'],
                        f"URL $:-> {dic.TestURL['url']} <-:$ matches the expected value.",
                        f"URL expected: $:-> {dic.TestURL['url']} <-:$, Actual: $:-> {self.driver.current_url} <-:$.",
                    )
                    dic.TestURL['status'] = 1 if assertFuncResult else - 1
                    
                    
                if dic.testTextArr != []:
                    for field in dic.testTextArr:
                        
                        data = field['element']
                        identyfyBy, identifier, text = data['identyfyBy'], data['identifier'], field['text']
                        element = self.findElement(identyfyBy, identifier, waitFor)
                        
                        assertFuncResult = AssertFunc(
                            lambda: element.text == text,
                            f"HTML Text $:-> {text} <-:$ matches the expected value.",
                            f"HTML Text expected: $:-> {text} <-:$, Actual: $:-> {element.text} <-:$.",
                        )
                        field['status'] = 1 if assertFuncResult else - 1
                

                # for printing results
                if show_test or debug_mode:
                    print(f'*****\t {"show test" if show_test else ("debug test" if debug_mode else "")} Log: test \t*****')
                    print(dic)
       
        time.sleep(10)
        
    def __del__(self):
        self.driver.close()
