########################################################
## constants.py - A module to load constants
########################################################
## Author: Jeremiah White
## License: MIT License
## Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


import os
import lambdalogging

LOG = lambdalogging.getLogger(__name__)

# defaults
PROTECTED_FIELDS = []
REDACTION_MODE = "EXPLICIT"  # can be EXPLICIT or REPLACE
REDACTION_GROUP_NAME = ""
TOKENIZATION_GROUP_NAME = ""
TOKENIZATION_STRING = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ."
TOKENIZATION_INTEGER = "0123456789"
ROTATION = 4

# Read OS Variables
if os.getenv('PROTECTED_KEYS') is not None:
    PROTECTED_FIELDS = list(os.getenv('PROTECTED_KEYS').split(","))
LOG.info("Fields to be protected: " + str(PROTECTED_FIELDS))
if os.getenv('REDACTION_MODE') is not None:
    REDACTION_MODE = os.getenv('REDACTION_MODE')
LOG.info("REDACTION mode: " + REDACTION_MODE)
if os.getenv('REDACTION_GROUP') is not None:
    REDACTION_GROUP_NAME = os.getenv('REDACTION_GROUP')
LOG.info("Name of usergroup to redact data for: " + REDACTION_GROUP_NAME)
if os.getenv('TOKENIZATION_GROUP') is not None:
    TOKENIZATION_GROUP_NAME = os.getenv('TOKENIZATION_GROUP')
LOG.info("Name of usergroup to tokenize data for: " + TOKENIZATION_GROUP_NAME)
if os.getenv('TOKENIZATION_STRING') is not None:
    TOKENIZATION_STRING = os.getenv('TOKENIZATION_STRING')
if os.getenv('TOKENIZATION_INTEGER') is not None:
    TOKENIZATION_INTEGER = os.getenv('TOKENIZATION_INTEGER')
if os.getenv('ROTATION') is not None:
    ROTATION = int(os.getenv('ROTATION'))

# Create dict for tokenization
CHR_TOKENS = dict(zip(range(len(TOKENIZATION_STRING)),
                      list(TOKENIZATION_STRING)))
NUM_TOKENS = dict(zip(range(10), list(TOKENIZATION_INTEGER)))
CHR_TOKENS_REV = dict(zip(list(TOKENIZATION_STRING),
                          range(len(TOKENIZATION_STRING))))
NUM_TOKENS_REV = dict(zip(list(TOKENIZATION_INTEGER), range(10)))
