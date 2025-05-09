# Checker rambler's dead mail account

---

### This code is designed to check inactive/banned Rambler mail accounts.

---

## Setup & Running

You'll need [Python 3.11 ](https://www.python.org/downloads/) or higher installed.

All required libraries and dependencies are listed in `requirements.txt`

To install all dependencies, run in console:
```
pip install -r requirements.txt
```

Place all accounts to check in `accounts.txt` file.

File should contain accounts in this format:
```
login@rambler.ru:password
login@rambler.ru:password
login@rambler.ru:password
```

Then run main.py:
```
python main.py
```
### Console output:
```
Successfully loaded 3 accounts from file

Processing account: login@rambler.ru
⚠ login@rambler.ru - requires phone verification
✔ login@rambler.ru - login successful (LIVE)
↩ Logout successful

Processing account: login@rambler.ru
✖ login@rambler.ru - blocked (DEAD)

Processing account: login@rambler.ru
⚠ login@rambler.ru - requires phone verification
✔ login@rambler.ru - login successful (LIVE)
↩ Logout successful

==================================================
Check completed. Results:
Total accounts: 3
==================================================
```