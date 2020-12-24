import pandas as pd
pd.set_option('display.max_colwidth', -1)
import re

def get_tests(text, test_dict) -> object:
    text = text.replace('(','')
    text = text.replace(')','')
    test_list = pd.DataFrame(columns = ['Test', 'URL'])
    for test in test_dict['VALUE']:
        test = test.replace('(','')
        test = test.replace(')','')
        if re.search(test, text, re.IGNORECASE):
            url = test_dict.loc[test_dict['VALUE'] == test]['URL'].to_string(index=False)
            test_list = test_list.append({'Test': test, 'URL':url}, ignore_index=True)
    test_list = test_list.drop_duplicates('URL')
    return test_list