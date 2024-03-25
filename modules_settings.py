import asyncio
from utils.progress_checker import LineaScan
from modules import *


########################################################################
#                          Setup Modules                               #
########################################################################

async def withdraw_okx(wallet_info):
    """
    Withdraw ETH from OKX

    WARNING! OKX DOES NOT SUPPORT SCROLL CHAIN
    ______________________________________________________
    min_amount - min amount (ETH)
    max_amount - max_amount (ETH)
    chains - ['zksync', 'arbitrum', 'linea', 'base', 'optimism']
    terminate - if True - terminate program if money is not withdrawn
    skip_enabled - If True, the skip_threshold check will be applied; otherwise, it will be ignored
    skip_threshold - If skip_enabled is True and the wallet balance is greater than or equal to this threshold,
                     skip the withdrawal
    """
    token = 'ETH'
    chains = ['linea']

    min_amount = 0.0031
    max_amount = 0.004

    terminate = False

    skip_enabled = False
    skip_threshold = 0.00327

    wait_unlimited_time = False
    sleep_between_attempts = [10, 20]  # min, max

    okx_exchange = Okx(wallet_info, chains)
    await okx_exchange.okx_withdraw(
        min_amount, max_amount, token, terminate, skip_enabled, skip_threshold,
        wait_unlimited_time, sleep_between_attempts
    )


async def transfer_to_okx(wallet_info):
    from_chains = ["optimism", "arbitrum"]

    min_amount = 0.0012
    max_amount = 0.0012
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    save_funds = [0.0001, 0.00012]
    min_required_amount = 0.002

    bridge_from_all_chains = True
    sleep_between_transfers = [120, 350]

    transfer_inst = Transfer(wallet_info)
    await transfer_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent,
        max_percent, save_funds, False, 0, min_required_amount,
        bridge_from_all_chains=bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers
    )


async def bridge_orbiter(wallet_info):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chains – source chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one or more
                  If more than one chain is specified, the software will check the balance in each network and
                  select the chain with the highest balance.
    to_chain – destination chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one

    min_amount - the minimum possible amount for sending
    max_amount - maximum possible amount to send
    decimal - to which digit to round the amount to be sent

    all_amount - if True, percentage values will be used for sending (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be sent
    max_percent - the maximum possible percentage of the balance to send

    check_balance_on_dest - if True, it will check the balance in the destination network.
    check_amount - amount to check the balance in the destination network. if the balance is greater than this amount,
                   the bridge will not be executed.
    save_funds - what amount to leave in the outgoing network [min, max], chosen randomly from the range
    min_required_amount - the minimum required balance in the network to make the bridge.
                          if there is no network with the required balance, the bridge will not be made
    bridge_from_all_chains - if True, will be produced from all chains specified in the parameter from_chains
    sleep_between_transfers - only if bridge_from_all_chains=True. sleep between few transfers
    """

    from_chains = ["arbitrum", "optimism", "base"]
    to_chain = "linea"

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 6

    all_amount = True

    min_percent = 98
    max_percent = 100

    check_balance_on_dest = True
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0.005

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    orbiter_inst = Orbiter(wallet_info)
    await orbiter_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers
    )

########################################################################
#                    Linea Park Setup Modules                          #
########################################################################


async def wrap_eth(wallet_info):
    """
    Week 2, Task 2
    """
    min_amount = 0.000001
    max_amount = 0.00001

    decimal = 7

    all_amount = False
    min_percent = 2
    max_percent = 5

    linea_inst = Linea(wallet_info)
    await linea_inst.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def sendingme_task(wallet_info):
    """
    Week 2, Task 6. Send some amount of ETH
    """
    min_amount = 0.0000001
    max_amount = 0.000001
    decimal = 8

    week3_inst = Week3(wallet_info)
    await week3_inst.sendingme_send(min_amount, max_amount, decimal)


########################################################################
#                             Routes                                   #
########################################################################


async def custom_routes(wallet_info):
    """
    Week 1 modules:
        - game_boom_proof (Task 2, main)
        - game_boom_mint (Task 2, bonus)
        - nidum_mint (Task 3, main)
        - townstory_mint (Task 4, main)
        - townstory_travelbag (Task 4, bonus)

    Week 2 modules:
        - abuse_world_mint (Task 1, main)
        - pictographs_mint (Task 2, main)
        - pictographs_stake (Task 2, bonus)
        - satoshi_universe_mint (Task 4)
        - yooldo_daily_task (Task 5)

    Week 3 modules:
        - send_mail (Task 1, main)
        - wrap_eth (Task 2, main)
        - asmatch_mint (Task 3, main)
        - bitavatar_checkin (Task 4, main)
        - readon_curate (Task 5, main)
        - sendingme_task (Task 6, main)

    Week 4 modules:
        - sarubol_mint (Task 2, main)
        - z2048_game (Task 3, main)
        - adopt_cat (Task 8, main)

    Week 5 modules:
        - omnizone_mint (Task 1, main)
        - battlemon_mint(Task 2, main)
        - play_nouns (Task 3, main)

    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, then select a random one from module 3 and 4, and end with 5

    You can also specify None in [], and if None is selected by random, this module will be skipped

    You can also specify () to perform the desired action a certain number of times
    example (send_mail, 1, 10) run this module 1 to 10 times
    """
    use_modules = [game_boom_proof, game_boom_mint, townstory_mint, townstory_travelbag,  # week 1
                   abuse_world_mint, pictographs_mint, satoshi_universe_mint, yooldo_daily_task,  # week 2
                   send_mail, wrap_eth, asmatch_mint, bitavatar_checkin, readon_curate, sendingme_task,  # week 3
                   sarubol_mint, z2048_game, adopt_cat,  # week 4
                   omnizone_mint, battlemon_mint, play_nouns]  # week 5

    sleep_from = 300
    sleep_to = 500

    random_module = True

    routes_inst = Routes(wallet_info)
    await routes_inst.start(use_modules, sleep_from, sleep_to, random_module)


async def automatic_routes(wallet_info):
    """
    The module automatically generates the paths a wallet will take,
    changing the probabilities of selecting one or another module for each wallet
    ______________________________________________________
    transaction_count - number of transactions (not necessarily all transactions are executed, modules can be skipped)
    cheap_ratio - from 0 to 1, the share of cheap transactions when building a route
    cheap_modules - list of modules to be used as cheap ones
    expensive_modules - list of modules to be used as expensive ones
    use_none - adds probability to skip module execution
    """

    transaction_count = 15
    cheap_ratio = 1

    sleep_from = 84000
    sleep_to = 90000

    use_none = True
    cheap_modules = [yooldo_daily_task]
    expensive_modules = []

    routes_inst = Routes(wallet_info)
    await routes_inst.start_automatic(transaction_count, cheap_ratio,
                                      sleep_from, sleep_to,
                                      cheap_modules, expensive_modules,
                                      use_none)


# -------------------------------------------- NO NEED TO SET UP MODULES
########################################################################
#                             Week 1                                   #
########################################################################


async def game_boom_mint(wallet_info):
    """
    Task 2, Bonus Part (optional)
    """

    week1_inst = Week1(wallet_info)
    await week1_inst.gamer_boom_mint()


async def game_boom_proof(wallet_info):
    """
    Task 2, part 1
    """
    week1_inst = Week1(wallet_info)
    await week1_inst.gamer_boom_proof()


async def nidum_mint(wallet_info):
    """
    Task 3. DOESN'T WORK
    """
    week1_inst = Week1(wallet_info)
    await week1_inst.nidum_mint()


async def townstory_mint(wallet_info):
    """
    Task 4.1
    """
    week1_inst = Week1(wallet_info)
    await week1_inst.townstory_mint()


async def townstory_travelbag(wallet_info):
    """
    Task 4.2 bonus
    """

    week1_inst = Week1(wallet_info)
    await week1_inst.travelbag_mint()

########################################################################
#                             Week 2                                   #
########################################################################


async def abuse_world_mint(wallet_info):
    """
    Task 1
    """

    week2_inst = Week2(wallet_info)
    await week2_inst.abuse_world_mint()


async def pictographs_mint(wallet_info):
    """
    Task 2 Main
    """

    week2_inst = Week2(wallet_info)
    await week2_inst.pictograph_mint()


async def pictographs_stake(wallet_info):
    """
    Task 2 Bonus
    """

    week2_inst = Week2(wallet_info)
    await week2_inst.pictograph_stake()


async def satoshi_universe_mint(wallet_info):
    """
    Task 4
    """

    week2_inst = Week2(wallet_info)
    await week2_inst.satoshi_universe_mint()


async def yooldo_daily_task(wallet_info):
    """
    Task 5
    """

    week2_inst = Week2(wallet_info)
    await week2_inst.yooldo_daily_task()

########################################################################
#                             Week 3                                   #
########################################################################


async def send_mail(wallet_info):
    """
    Task 1
    """
    dmail_inst = Dmail(wallet_info)
    await dmail_inst.send_mail()


async def asmatch_mint(wallet_info):
    """
    Task 3
    """

    week3_inst = Week3(wallet_info)
    await week3_inst.asmatch_mint()


async def bitavatar_checkin(wallet_info):
    """
    Task 4
    """

    week3_inst = Week3(wallet_info)
    await week3_inst.bitavatar_checkin()


async def readon_curate(wallet_info):
    """
    Task 5
    """

    week3_inst = Week3(wallet_info)
    await week3_inst.readon_curate()


########################################################################
#                             Week 4                                   #
########################################################################

async def sarubol_mint(wallet_info):
    """
    Task 2
    """
    week4_inst = Week4(wallet_info)
    await week4_inst.sarubol_mint()


async def z2048_game(wallet_info):
    """
    Task 3.1
    """
    week4_inst = Week4(wallet_info)
    await week4_inst.z2048_start_game()


async def adopt_cat(wallet_info):
    """
    Task 8
    """
    week4_inst = Week4(wallet_info)
    await week4_inst.lucky_cat_mint()

########################################################################
#                             Week 5                                   #
########################################################################


async def omnizone_mint(wallet_info):
    """
    Task 1
    """
    week5_inst = Week5(wallet_info)
    await week5_inst.omnizone_mint()


async def battlemon_mint(wallet_info):
    """
    Task 2
    """
    week5_inst = Week5(wallet_info)
    await week5_inst.battlemon_mint()


async def play_nouns(wallet_info):
    """
    Task 3
    """
    week5_inst = Week5(wallet_info)
    await week5_inst.play_nouns()

########################################################################
#                             Checker                                  #
########################################################################


def progress_check(wallets_data):

    replace = True

    LineaScan(wallets_data).get_wallet_progress(replace)
