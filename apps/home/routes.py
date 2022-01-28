from apps.home import blueprint
from flask import render_template
from database.DBManager import *


@blueprint.route('/')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route("/data")
def data():
    # trade_data = str(trade_data_to_JSON())#
    trade_data = """
    {
   "total_trades": [
      [
         16
      ]
   ],
   "total_profit": [
      [
         1.6e+19
      ]
   ],
   "supported_exchanges": 11,
   "total_pairs": 656495,
   "recent_trades": [
      {
         "token0": 0,
         "token1": 0,
         "exchange": "0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7",
         "profit": "1000000000000000000"
      },
      {
         "token0": 0,
         "token1": 0,
         "exchange": "0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7",
         "profit": "1000000000000000000"
      },
      {
         "token0": 0,
         "token1": 0,
         "exchange": "0x789c11212EaCA5312d4aa6d63148613e658CcFAd",
         "profit": "1000000000000000000"
      },
      {
         "token0": 0,
         "token1": 0,
         "exchange": "0x789c11212EaCA5312d4aa6d63148613e658CcFAd",
         "profit": "1000000000000000000"
      },
      {
         "token0": 0,
         "token1": 0,
         "exchange": "0x789c11212EaCA5312d4aa6d63148613e658CcFAd",
         "profit": "1000000000000000000"
      }
   ],
   "trades_per_month": [
      {
         "month": 12,
         "trade_amounts": 1
      },
      {
         "month": 1,
         "trade_amounts": 15
      }
   ],
   "profit_per_month": [
      {
         "month": 12,
         "profit": 1e+18
      },
      {
         "month": 1,
         "profit": 1.5e+19
      }
   ]
}
    """
    return trade_data


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
