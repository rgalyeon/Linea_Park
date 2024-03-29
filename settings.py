SAVE_LOGS = True

# RANDOM WALLETS MODE
RANDOM_WALLET = True  # True/False

USE_PROXY = True

CHECK_QUESTS_PROGRESS = True

SLEEP_FROM = 500  # Second
SLEEP_TO = 800  # Second

# Sleep after a transaction has been executed. Blocks threads so that wallets do not make a transaction in 1 second.
SLEEP_AFTER_TX_FROM = 60
SLEEP_AFTER_TX_TO = 120

QUANTITY_THREADS = 1

THREAD_SLEEP_FROM = 300
THREAD_SLEEP_TO = 600

# GWEI CONTROL MODE
CHECK_GWEI = True  # True/False
MAX_GWEI = 1.02
REALTIME_GWEI = True  # if true - you can change gwei while program is working

# Рандомизация гвея. Если включен режим, то максимальный гвей будет выбираться из диапазона
RANDOMIZE_GWEI = True  # if True, max Gwei will be randomized for each wallet for each transaction
MAX_GWEI_RANGE = [0.3, 0.3]  # linea gwei

# сколько ждать перед чеком газа
GAS_SLEEP_FROM = 60
GAS_SLEEP_TO = 150

GAS_MULTIPLIER = 1.1

# RETRY MODE
RETRY_COUNT = 2

LAYERSWAP_API_KEY = ""
