import dotenv

# RANDOM WALLETS MODE
RANDOM_WALLET = dotenv.get_key('.env', 'RANDOM_WALLET') == 'True' if dotenv.get_key('.env', 'RANDOM_WALLET') != None else True

# removing a wallet from the list after the job is done
REMOVE_WALLET = dotenv.get_key('.env', 'REMOVE_WALLET') == 'True' if dotenv.get_key('.env', 'REMOVE_WALLET') != None else False

SLEEP_FROM = int(dotenv.get_key('.env', 'SLEEP_FROM')) if dotenv.get_key('.env', 'SLEEP_FROM') != None else 500  # Second
SLEEP_TO = int(dotenv.get_key('.env', 'SLEEP_TO')) if dotenv.get_key('.env', 'SLEEP_TO') != None else 800  # Second  # Second

QUANTITY_THREADS = int(dotenv.get_key('.env', 'QUANTITY_THREADS')) if dotenv.get_key('.env', 'QUANTITY_THREADS') != None else 5

THREAD_SLEEP_FROM = int(dotenv.get_key('.env', 'THREAD_SLEEP_FROM')) if dotenv.get_key('.env', 'THREAD_SLEEP_FROM') != None else 300
THREAD_SLEEP_TO = int(dotenv.get_key('.env', 'THREAD_SLEEP_TO')) if dotenv.get_key('.env', 'THREAD_SLEEP_TO') != None else 600

# PROXY MODE
USE_PROXY = dotenv.get_key('.env', 'USE_PROXY') == 'True' if dotenv.get_key('.env', 'USE_PROXY') != None else False
CHECK_PROXY = dotenv.get_key('.env', 'CHECK_PROXY') == 'True' if dotenv.get_key('.env', 'CHECK_PROXY') != None else False

# GWEI CONTROL MODE
CHECK_GWEI = dotenv.get_key('.env', 'CHECK_GWEI') == 'True' if dotenv.get_key('.env', 'CHECK_GWEI') != None else False  # True or False
MAX_GWEI = float(dotenv.get_key('.env', 'MAX_GWEI')) if dotenv.get_key('.env', 'MAX_GWEI') != None else 1

GAS_MULTIPLIER = float(dotenv.get_key('.env', 'GAS_MULTIPLIER')) if dotenv.get_key('.env', 'GAS_MULTIPLIER') != None else 1

# RETRY MODE
RETRY_COUNT = int(dotenv.get_key('.env', 'RETRY_COUNT')) if dotenv.get_key('.env', 'RETRY_COUNT') != None else 1

# INCH API KEY
INCH_API_KEY = ""
