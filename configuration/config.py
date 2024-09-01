# config.py
import configparser

# Create a global ConfigParser object
config = configparser.ConfigParser()

# Load the INI file
config.read('configuration/config.ini')