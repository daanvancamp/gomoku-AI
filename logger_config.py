# logger_config.py

import logging

def setup_logger():
    # Create a logger object
    logger = logging.getLogger('my_logger')
    
    # Set the minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)
    
    # Create a console handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Create a formatter for the logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    if not logger.hasHandlers():  # To avoid adding multiple handlers if the function is called multiple times
        logger.addHandler(console_handler)
    
    return logger

# Call setup_logger() once in the main module to set up logging for all modules
