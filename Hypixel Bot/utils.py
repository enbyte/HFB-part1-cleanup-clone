import ast
import requests

def open_safe_ast(file_handle):
    try:
        with open(file_handle, "r") as fileh:
            parsed_dict = ast.literal_eval(fileh.read())
    except FileNotFoundError:
        parsed_dict = {}

    return parsed_dict

def blocking_query_apis(urls):
    if type(urls) == str:
        urls = [urls]
    found_yet = [0] * len(urls)
    responses = [''] * len(urls)

    while sum(found_yet) < len(urls):
        for i in urls:
            if found_yet[urls.index(i)] == 0:
                try:
                    responses[i] = requests.get(urls[i], timeout=5).json()
                    found_yet[i] = 1
                except:
                    pass

    return responses
    