![linea_park](https://github.com/rgalyeon/Linea_Park/assets/28117274/55f4e191-2145-4b30-aba4-1ece5374ee1a)
# Linea Park 
Soft for an easy Linea Park campaign walkthrough. Supports multiple OKX accounts, multithreading, encrypts sensitive data, after encryption wallets can be started using only the wallet address (no need to re-enter data).

Main features: custom routes, realtime/custom linea gwei, modules for completing most of the tasks from the Linea Park campaign (onchain), smart bridge, ETH collector from networks to OKX

## 🗂️ Description
With the help of the software you can make a withdrawal from the OKX exchange, bridge to Linea, complete most of the Layer3 tasks. The software will be updated as new tasks become available.

**Modules**
1. `encrypt_privates_and_proxy` - module is necessary for the first launch of the software. Reads data from the table `wallet_data.xlsx`, encrypts and deletes sensitive data from the table. For repeated runs it is enough to specify only the wallet address, because the rest of the data is stored in encrypted form. If you want to add new data (add wallets or change proxies), you will need to use this module again.
2. `withdraw_okx` - module for withdrawing tokens from the OKX. Supports checking the balance on the wallet to avoid withdrawing money in case it is already in the chain
3. `custom_routes` - module for customizing your own route (radnomize transactions)
4. Orbiter bridge
5. Transfer ETH (to OKX or another wallet)

**Linea Park Quests**
Week 1: Game Boom [Main + Bonus], Nidum, Townstory [Main + Bonus]
Week 2: Abuse World [Main], Pictographs [Main + Bonus], Satoshi Universe, Yooldo Daily Task
Week 3: Dmail, GameHub [Main + Bonus], Asmatch, BitAvatar, ReadOn, SendingMe
Week 4: Sarubol, z2048 [Main], Lucky Cat
Week 5: soon...
Week 6: soon...

## ⚙️ Installation
```bash
git clone https://github.com/rgalyeon/Linea_Park.git
cd Linea_Park
python -m venv venv
source venv/bin/activate (on MacOs) or .\venv\Scripts\activate (on Windows)
pip install -r requirements.txt
```

## 🚀 How to run software
### 1. First, you must fill in the appropriate columns in the `wallet_data.xslx` table:
- `name` - name/index of wallet (optional)
- `address` - wallet address
- `private` - private key 
- `proxy` - proxy, if used for wallet in the format `login:pass@ip:port` (optional)
- `okx_api` - api okx account in the format `api;secret;password` (you can customize okx api for each wallet) (optional)
- `okx_address` - address for transfer eth to OKX (optional)

### 2. Encrypt data
- Run script with `python main.py` command and choose `Encrypt private keys and proxies`
- Set up a password to access the data

#### 3. Customize the modules and get them up and running. 
- Set up general settings in `settings.py` (thread_count, retry_count, etc...)
- Set up modules settings in `module_settings.py`
- Add the wallet addresses you want to run to the `wallet_data.xlsx` file (only wallet addresses are needed after encryption)
- Run script with `python main.py` command and choose necessary module.

## 🔗 Contacts
**Buy me a coffee:** `rgalyeon.eth`

[![Channel](https://img.shields.io/badge/-channel-090909?style=for-the-badge&logo=telegram)](https://t.me/block_nine)
[![Channel](https://img.shields.io/badge/-group-090909?style=for-the-badge&logo=telegram)](https://t.me/block_nine_chat)
[![Channel](https://img.shields.io/badge/-tradium-090909?style=for-the-badge&logo=telegram)](https://t.me/tradium)

