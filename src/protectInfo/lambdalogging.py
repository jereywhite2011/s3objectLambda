########################################################
## lambdalogger.py - provides the logger
########################################################
## Author: Jeremiah White
## License: MIT License
## Credits: Amazon.com
## Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


"""
Lambda logging helper.
Returns a Logger with log level set based on env variables.
"""

import logging

# translate log level from string to numeric value
LOG_LEVEL = logging.INFO

# setup logging levels for botocore
logging.getLogger('botocore.endpoint').setLevel(LOG_LEVEL)
logging.getLogger('botocore.retryhandler').setLevel(LOG_LEVEL)
logging.getLogger('botocore.parsers').setLevel(LOG_LEVEL)


def getLogger(name):
    """Return a logger configured based on env variables."""
    logger = logging.getLogger(name)
    # in lambda environment, logging config has already been setup so can't use logging.basicConfig to change log level
    logger.setLevel(LOG_LEVEL)
    return logger
