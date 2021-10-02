import requests

base_url = "http://localhost:8080/opendata/base"
class Base(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])
    def __str__ (self):
        return '({}, {})'.format(self.contentId, self.intro)


def create_base_data():
    response = requests.post(base_url)
    return response

def get_base_data():
    base_list = []
    intro_list = []
    json_data = requests.get(base_url + "/intro").json()
    for j in json_data:
        base = Base(j)

        intro_list.append(j.get('intro'))
        base_list.append(base)

    return base_list, intro_list