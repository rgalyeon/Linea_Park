import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import questionary
from loguru import logger
from questionary import Choice

from settings import (
    RANDOM_WALLET,
    SLEEP_TO,
    SLEEP_FROM,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO,
    SAVE_LOGS,
    CHECK_QUESTS_PROGRESS
)
from modules_settings import *
from utils.sleeping import sleep
from utils.logs_handler import filter_out_utils
from utils.password_handler import get_wallet_data
from utils.progress_checker import LineaScan
from itertools import count
import threading
from config import HEADER

transaction_lock = threading.Lock()


def get_module():
    counter = count(1)
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice(f"{next(counter)}) Encrypt private keys", encrypt_privates),
            Choice(f"{next(counter)}) Withdraw from OKX", withdraw_okx),
            Choice(f"{next(counter)}) Transfer to OKX", transfer_to_okx),
            Choice(f"{next(counter)}) Bridge Orbiter", bridge_orbiter),
            Choice(f"{next(counter)}) Use custom routes", custom_routes),
            Choice(f"{next(counter)}) Quest progress checker (need proxy)", progress_check),
            Choice(f"{next(counter)}) PoH checker (need proxy)", poh_check),
            Choice(f"{next(counter)}) Deposit LayerBank", deposit_layerbank),
            Choice(f"{next(counter)}) Withdraw LayerBank", withdraw_layerbank),
            Choice(f"{next(counter)}) Exit\n", "exit"),

            Choice(f"CSZN Week 1/Task 1 OctoMos mint", octomos_mint),
            Choice(f"CSZN Week 1/Task 2 Clutch mint", clutchai_mint),
            Choice(f"CSZN Week 1/Task 3 Push mint", mintpad_mint),
            Choice(f"CSZN Week 1/Task 4 Wizards mint", wizards_mint),
            Choice(f"CSZN Week 1/Task 5 Efrogs mint\n", efrogs_mint),

            Choice(f"CSZN Week 2/Task 1 Satoshi Universe mint", satoshi_mint),
            Choice(f"CSZN Week 2/Task 2 Linus Eggs mint", linus_mint),
            Choice(f"CSZN Week 2/Task 3 Yooldo mint", yooldo_mint),
            Choice(f"CSZN Week 2/Task 4 Frog Wars mint", frog_wars_mint),
            Choice(f"CSZN Week 2/Task 5 ACG mint", acg_mint),
            Choice(f"CSZN Week 2/Task 6 Toad The Great mint\n", toadthegreat_mint),

            Choice(f"CSZN Week 3/Task 1 AscendTheEnd mint", ascendtheend_mint),
            # Choice(f"Week 1/Task 2 [Main] Game Boom Proof", game_boom_proof),
            # Choice(f"Week 1/Task 2 [Bonus] Game Boom Mint", game_boom_mint),
            # Choice(f"Week 1/Task 3 [Main] Nidum mint", nidum_mint),
            # Choice(f"Week 1/Task 3 [Bonus] Nidum bonus", nidum_bonus),
            # Choice(f"Week 1/Task 4 [Main] Townstory mint", townstory_mint),
            # Choice(f"Week 1/Task 4 [Bonus] Townstory mint travelbag\n", townstory_travelbag),

            # Choice(f"Week 2/Task 1 [Main] Abuse World mint", abuse_world_mint),
            # Choice(f"Week 2/Task 2 [Main] Pictographs mint", pictographs_mint),
            # Choice(f"Week 2/Task 2 [Bonus] Pictographs stake", pictographs_stake),
            # Choice(f"Week 2/Task 4 [Main] Satoshi universe mint", satoshi_universe_mint),
            # Choice(f"Week 2/Task 5 [Main] Yooldo daily task\n", yooldo_daily_task),

            # Choice(f"Week 3/Task 1 [Main] Dmail send message", send_mail),
            # Choice(f"Week 3/Task 2 [Main + Bonus] Gamic Hub swap", wrap_eth),
            # Choice(f"Week 3/Task 3 [Main] AsMatch mint", asmatch_mint),
            # Choice(f"Week 3/Task 4 [Main] BitAvatar checkin", bitavatar_checkin),
            # Choice(f"Week 3/Task 5 [Main] ReadOn curate", readon_curate),
            # Choice(f"Week 3/Task 6 [Main] SendingMe task\n", sendingme_task),

            # Choice(f"Week 4/Task 2 [Main] Sarubol mint", sarubol_mint),
            # Choice(f"Week 4/Task 3 [Main] z2048 start game", z2048_game),
            # Choice(f"Week 4/Task 8 [Main] Lucky Cat mint\n", adopt_cat),
            #
            # Choice(f"Week 5/Task 1 [Main] Omnizone mint", omnizone_mint),
            # Choice(f"Week 5/Task 2 [Main] Battlemon mint", battlemon_mint),
            # Choice(f"Week 5/Task 3 [Main] Play Nouns\n", play_nouns),
            #
            # Choice(f"Week 6/Task 1 [Main] zAce check-in", zace_check_in),
            # Choice(f"Week 6/Task 2 [Main] micro3 mint", micro3_mint),
            # Choice(f"Week 6/Task 3 [Main] Alienswap mint", alienswap_mint),
            # Choice(f"Week 6/Task 4 [Main] Frog War mint", frog_war_mint),
            # Choice(f"Week 6/Task 4 [Bonus] Warrior mint", frog_war_bonus),
            # Choice(f"Week 6/Task 6 [Main] ACG WORLDS mint", acg_worlds_mint),
            # Choice(f"Week 6/Task 7 [Main] Bilinear mint", bilinear_mint),
            # Choice(f"Week 6/Task 10 [Main] ImagineAiNFTs mint", imagineairynfts_mint),
            # Choice(f"Week 6/Task 11 [Main] Arena Games mint\n", arenagames_mint),

            Choice(f"Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("❤️ Author – https://t.me/block_nine\n")
        sys.exit()
    return result


def get_wallets():
    wallets_data = get_wallet_data()
    return list(wallets_data.values())


async def run_module(module, wallet_data):
    try:
        await module(wallet_data)
    except Exception as e:
        logger.error(e)
        import traceback

        traceback.print_exc()

    await sleep(SLEEP_FROM, SLEEP_TO)


def _async_run_module(module, wallet_data):
    asyncio.run(run_module(module, wallet_data))


def main(module):
    if module == encrypt_privates:
        return encrypt_privates(force=True)

    wallets_data = get_wallets()

    if module == poh_check:
        return poh_check(wallets_data)

    if module == progress_check:
        return progress_check(wallets_data)

    if RANDOM_WALLET:
        random.shuffle(wallets_data)

    # if CHECK_QUESTS_PROGRESS:
    #     LineaScan(wallets_data).get_wallet_progress()

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, wallet_data in enumerate(wallets_data, start=1):
            executor.submit(
                _async_run_module,
                module,
                wallet_data
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':

    print(HEADER)
    print("Author – https://t.me/block_nine\n")

    if SAVE_LOGS:
        logger.add('logs.txt', filter=filter_out_utils)

    module = get_module()
    main(module)

    print("ALL DONE")
    print("Author – https://t.me/block_nine\n")
