import configparser


config = configparser.ConfigParser()
config.read('config.ini')

URL = config['urls']['local']
PORT = config['ports']['default']
