import sys
import mariadb
from database.config import *
import json
import re
import datetime

TRADES_TABLE = "Trades"
PAIRS_TABLES = [
    "ApeSwapPairs",
    "BiswapPairs",
    "BurgerSwapPairs",
    "CheeseSwapPairs",
    "HyperJumpPairs",
    "JetSwapPairs ",
    "JulSwapPairs ",
    "MdexPairs",
    "PancakeV1Pairs",
    "PancakeV2Pairs",
    "WaultSwapPairs",
]

try:
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


def fetch_recent_swaps():
    cmd = f"SELECT token0, token1, exchangeC, profitWETH  FROM {TRADES_TABLE} " \
          f"ORDER BY tradeID DESC " \
          f"LIMIT 5;"
    cur.execute(cmd)
    return cur


def fetch_total_trades():
    cmd = f"SELECT COUNT(*) as total_trades FROM {TRADES_TABLE} "
    cur.execute(cmd)
    result = cur.fetchall()
    return result


def fetch_total_profit():
    cmd = f"SELECT sum(profitWETH) as total_profit FROM {TRADES_TABLE} "
    cur.execute(cmd)
    result = cur.fetchall()
    return result


def fetch_amount_pairs():
    cmd = f"SELECT sum(tbl.EachTableCount) as total_pairs FROM " \
          f"({pairs_table_helper()})tbl;"
    cur.execute(cmd)
    result = cur.fetchall()
    return result


def fetch_supported_exchanges():
    cmd = "Show tables;"
    cur.execute(cmd)
    exchanges = cur.fetchall()
    amount_supported_exchanges = 0
    for exchange in exchanges:
        if "pairs" in str(exchange).lower():
            amount_supported_exchanges += 1
    return amount_supported_exchanges


def hottest_exchanges():
    cmd = f"SELECT exchangeC, count(*) from {TRADES_TABLE} " \
          f"GROUP BY exchangeC"
    cur.execute(cmd)
    result = cur.fetchall()
    print(result)


def fetch_trades_per_month():
    cmd = f"SELECT month(timestamp), count(*) from {TRADES_TABLE} " \
          f"group by timestamp;"
    cur.execute(cmd)
    result = cur.fetchall()
    return result


def fetch_profit_per_month():
    cmd = f"SELECT month(timestamp), sum(profitWETH) from {TRADES_TABLE} " \
          f"group by timestamp;"
    cur.execute(cmd)
    result = cur.fetchall()
    return result


def pairs_table_helper():
    # avoid hardcoding
    return ' UNION ALL\n'.join([f"SELECT count(*) as EachTableCount from {x}" for x in PAIRS_TABLES])


def trade_data_to_JSON():
    # total trades, total profit, total pairs, supported exchanges
    # trades by month, profit per month
    # recents swaps

    trading_data = {
        "total_trades": fetch_total_trades(),
        "total_profit": fetch_total_profit(),
        "supported_exchanges": fetch_supported_exchanges(),
        "total_pairs": int(''.join(re.findall(r"\d+", str(fetch_amount_pairs())))),  # eye cancer, but works
        "recent_trades": [],
        "trades_per_month": [],
        "profit_per_month": []
    }

    trades_per_month = []
    for month, amount in fetch_trades_per_month():
        temp = {
            "month": month,
            "trade_amounts": amount
        }
        trades_per_month.append(temp)
    trading_data["trades_per_month"] = trades_per_month

    recent_trades = []
    for token0, token1, exchangeC, profitWETH in fetch_recent_swaps():
        temp = {
            "token0": token0,
            "token1": token1,
            "exchange": exchangeC,
            "profit": profitWETH
        }
        recent_trades.append(temp)
    trading_data["recent_trades"] = recent_trades

    profit_per_month = []
    for month, profit in fetch_profit_per_month():
        temp = {
            "month": month,
            "profit": profit
        }
        profit_per_month.append(temp)
    trading_data["profit_per_month"] = profit_per_month

    return json.dumps(trading_data, indent=3)


