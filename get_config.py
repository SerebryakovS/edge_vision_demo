
def get_config():
    params = dict();
    with open("config","r") as config:
        lines = config.readlines()
        for line in lines:
            line = line.split('=');
            params.update({line[0]:line[1].rstrip()});
    return params
