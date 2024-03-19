import random
from typing import List

from loguru import logger
from utils.sleeping import sleep
from .account import Account


class Routes(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info, chain="linea")
        self.wallet_info = wallet_info

    def process_module(self, module):
        if isinstance(module, list):
            return self.process_module(random.choice(module))
        elif isinstance(module, tuple):
            return [self.process_module(module[0]) for _ in range(random.randint(module[1], module[2]))]
        else:
            return module

    def run_modules(self, use_modules) -> List:
        modules_to_run = []
        for module in use_modules:
            result = self.process_module(module)
            if isinstance(result, list):
                modules_to_run.extend(result)
            else:
                modules_to_run.append(result)
        return modules_to_run

    def generate_module_sequence(self, cheap_modules, expensive_modules, num_transactions, cheap_ratio, use_none):
        """
        Генерирует случайную последовательность модулей.

        :param num_transactions: количество транзакций
        :param cheap_ratio: доля дешевых транзакций от общего числа (от 0 до 1)
        :param cheap_modules
        :param expensive_modules
        :param use_none
        """
        sequence = []
        for _ in range(num_transactions):
            if random.random() < cheap_ratio:
                module = random.choice(cheap_modules + ([None] if use_none else []))
            else:
                module = random.choice(expensive_modules + ([None] if use_none else []))

            # Случайно решаем, добавлять ли вложенность или повторения
            if random.random() < 0.2:  # 20% шанс добавить вложенность
                module = [module, self.generate_nested_module(cheap_modules, use_none)]
            elif random.random() < 0.1:  # 10% шанс добавить повторения
                module = (module, 1, random.randint(1, 2))

            sequence.append(module)
        return sequence

    def generate_nested_module(self, cheap_modules, use_none):
        """ Генерирует вложенный модуль. """
        if random.random() < 0.5:
            return random.choice(cheap_modules + ([None] if use_none else []))
        else:
            return [random.choice(cheap_modules + ([None] if use_none else [])),
                    self.generate_nested_module(cheap_modules, use_none)]

    async def start(self, use_modules: list, sleep_from: int, sleep_to: int, random_module: bool):
        logger.info(f"[{self.account_id}][{self.address}] Start using routes")

        run_modules = self.run_modules(use_modules)

        if random_module:
            random.shuffle(run_modules)

        for module in run_modules:
            if module is None:
                logger.info(f"[{self.account_id}][{self.address}] Skip module")
            else:
                await module(self.wallet_info)
            await sleep(sleep_from, sleep_to)

    async def start_automatic(self, transaction_count, cheap_ratio,
                              sleep_from, sleep_to,
                              cheap_modules, expensive_modules, use_none):
        logger.info(f"[{self.account_id}][{self.address}] Start using automatic routes")

        use_modules = self.generate_module_sequence(cheap_modules, expensive_modules,
                                                    transaction_count, cheap_ratio,
                                                    use_none)

        run_modules = self.run_modules(use_modules)

        for module in run_modules:
            if module is None:
                logger.info(f"[{self.account_id}][{self.address}] Skip module")
            else:
                await module(self.wallet_info)
            await sleep(sleep_from, sleep_to)
