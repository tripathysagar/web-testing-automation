import argparse

from page import BuildActionTestChainFromJSON
from crawler import Crawler

dic = {
    'url': 'https://www.screener.in/home/',
    'chain':  [
        {
            'type': 'action',
            'object': {
                'action' : 'single-click',
                'identyfyBy' : 'xpath', 
                'identifier' :"//a[@class='button account']", 
                'waitFor' : 10
            }
        },
        {
            'type': 'test',
            'object': {
            'url': 'https://www.screener.in/login/?',
            'title': 'Login - Screener',
            'textTextArr': [
                {
                    'identyfyBy':'xpath',
                    'identifier':'//h1',
                    'text':'Welcome back!@',
                },
                {
                    'identyfyBy':'xpath',
                    'identifier':'//strong',
                    'text':'Warren Buffett',
                }
                ]
            }
        },
        {
            'type': 'action',
            'object': {
                'action' : 'single-click',
                'identyfyBy' : 'xpath', 
                'identifier' :"//input[@id='id_username']", 
                'waitFor' : 10
            }
        },
        {
            'type': 'action',
            'object': {
                'action' : 'enter-data',
                'data' : 'test123456@mailinator.com'
            }
        },
        {
            'type': 'action',
            'object': {
                'action' : 'single-click',
                'identyfyBy' : 'xpath', 
                'identifier' :"//input[@id='id_password']"
            }
        },
        {
            'type': 'action',
            'object': {
                'action' : 'enter-data',
                'data' : 'Test@123'
            }
        },
        {
            'type': 'action',
            'object': {
                'action' : 'single-click',
                'identyfyBy' : 'xpath', 
                'identifier' :"//button[contains(normalize-space(), 'Login')]"
            }
        }
    ]
}


def parse_arguments():
    parser = argparse.ArgumentParser(description='to automate web testing using python')

    # Add optional argument for debug mode
    parser.add_argument('--debug', action='store_true', help='Run the script in debug mode')

    # Add optional argument to show test
    parser.add_argument('--showTest', action='store_true', help='Show test information')

    # Parse the command-line arguments
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Parse the command-line arguments
    args = parse_arguments()

    # Access the arguments
    debug_mode = args.debug
    show_test = args.showTest

    obj = BuildActionTestChainFromJSON(dic)
    crawler = Crawler(obj)
    crawler.crawl(debug_mode, show_test)
