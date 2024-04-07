import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter(fmt='[%(asctime)s]: %(module)s %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('system.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Create the logger instance
logger = logging.getLogger('system')

# Add the file handler to the logger
logger.addHandler(file_handler)