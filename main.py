import csv, os, sys, time, numpy, tulipy, config, ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Colugo: trading bot")
from terminaltables import SingleTable
from datetime import date, datetime
from binance.client import Client
from binance.enums import *
from numpy import genfromtxt
import ansicolors as ac
from ansicolors import clo, clp, fg, bg

def Create_executable_file():
    cwd = os.getcwd()
    myBat = open(rf'{cwd}\\run.bat','w')
    myBat.write(f'python {cwd}\\main.py')
    myBat.close()
    os.system('cls||clear')
Create_executable_file()


HEADER = f"""
    {fg.Bred}  ..|'''.|{fg.Bgreen}        {fg.Byellow} '|| {fg.Bblue}         {fg.Bmagenta}        {fg.Bcyan}        {fg.Bwhite}
    {fg.Bred}.|'     ' {fg.Bgreen}   ...  {fg.Byellow}  || {fg.Bblue} ... ... {fg.Bmagenta}   ... .{fg.Bcyan}  ...   {fg.Bwhite}
    {fg.Bred}||        {fg.Bgreen} .|  '|.{fg.Byellow}  || {fg.Bblue}  ||  || {fg.Bmagenta}  || || {fg.Bcyan}.|  '|. {fg.Bwhite}
    {fg.Bred}'|.      .{fg.Bgreen} ||   ||{fg.Byellow}  || {fg.Bblue}  ||  || {fg.Bmagenta}   |''  {fg.Bcyan}||   || {fg.Bwhite}
    {fg.Bred} ''|....' {fg.Bgreen}  '|..|'{fg.Byellow} .||.{fg.Bblue}  '|..'|.{fg.Bmagenta}  '||||.{fg.Bcyan} '|..|' {fg.Bwhite}
    {fg.Bred}          {fg.Bgreen}        {fg.Byellow}     {fg.Bblue}         {fg.Bmagenta} .|....'{fg.Bcyan}        {fg.Bwhite}
"""

STRAT_LIST = f"""{fg.yellow}    Current Strategies:\n
    
        1. RSIemaCross\n
        2. GoldenCross\n
"""


in_position = False
asset_qauntity = 0
pair = ''
interval = ''
strat = ''
output = 'Colugo:'+''
inputs_done = False


def Get_user_inputs():
    global HEADER, strat, inputs_done, STRAT_LIST
    print(HEADER)
    global asset_qauntity, pair
    pair            = input("What pair would you like to trade:    ").upper()
    asset_qauntity  = input("How many tokens are you looking to trade:    ")
    clp(STRAT_LIST, fg.Bwhite)
    strat           = input("What strat would you like to use?    ")
    interval        = 'KLINE_INTERVAL_' + input("Lastly, what interval:    ").upper()
    os.system('cls||clear')
Get_user_inputs()


def Order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    global asset_qauntity
    client = Client(config.binance_api_key, config.binance_secret_key)
    try:
        last_message = "sending order"
        order_with_info = client.create_order(symbol=symbol, side=side, type=order_type, quantity=asset_qauntity)
        #print(order_with_info)
    except Exception as e:
        #print("an exception occured - {}".format(e))
        return False
    return True

# set globals
last_rsi    = 0
last_rsiema = 0
last_ema22  = 0
last_ema50  = 0
last_ema200 = 0
last_obv    = 0
last_obvema = 0
last_open   = 0
last_high   = 0
last_low    = 0
last_close  = 0


def Main():
    global pair, HEADER, interval, last_rsi, last_rsiema
    """Convert Binance api output into data usable by Python """
    binance_client = Client(config.binance_api_key, config.binance_secret_key)
    binance_data   = binance_client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1MINUTE)
    """ Creates/Opens a CSV-file then overwrites it with data from binance_data """
    with open('ohlc_data.csv', 'w', newline='') as csvfile:
        reader    = csv.DictReader(csvfile)
        csvwriter = csv.writer(csvfile, delimiter=',')
        for i in binance_data:
            csvwriter.writerow(i)

    """ Specify which columns are which """
    ohlc_data = genfromtxt('ohlc_data.csv', delimiter=',')
    opentimes    = numpy.array(ohlc_data[:,0])
    opens        = numpy.array(ohlc_data[:,1])
    highs        = numpy.array(ohlc_data[:,2])
    lows         = numpy.array(ohlc_data[:,3])
    closes       = numpy.array(ohlc_data[:,4])
    volumes      = numpy.array(ohlc_data[:,5])
    closetimes   = numpy.array(ohlc_data[:,6])
    quotevolumes = numpy.array(ohlc_data[:,7])

    """ Indicators """
    rsis    = tulipy.rsi(closes, period = 14)
    rsiemas = tulipy.ema(rsis,   period = 22)
    ema200s = tulipy.ema(closes, period = 200)
    ema50s  = tulipy.ema(closes, period = 50)
    ema22s  = tulipy.ema(closes, period = 22)
    obvs    = tulipy.obv(closes, volumes)
    obvemas = tulipy.ema(obvs,   period = 100)

    last_rsi    =    rsis[-1]
    last_rsiema = rsiemas[-1]
    last_ema22  =  ema22s[-1]
    last_ema50  =  ema50s[-1]
    last_ema200 = ema200s[-1]
    last_obv    =    obvs[-1]
    last_obvema = obvemas[-1]

    """ Last ohlc """
    last_open   = opens[-1]
    last_high   = highs[-1]
    last_low    = lows[-1]
    last_close  = closes[-1]
    
    open_updown_color  = fg.Bwhite
    close_updown_color = fg.Bwhite
    high_updown_color  = fg.Bwhite
    low_updown_color   = fg.Bwhite
    

    next_to_last_open  =  opens[-2]
    next_to_last_high  =  highs[-2]
    next_to_last_low   =   lows[-2]
    next_to_last_close = closes[-2]

    if last_open > next_to_last_open:
        open_updown_color  = fg.Bgreen
    else:
        open_updown_color  = fg.Bred
        
    
    if last_close > next_to_last_close:
        close_updown_color = fg.Bgreen
    else:
        open_updown_color  = fg.Bred
        
    
    if last_high > next_to_last_high:
        high_updown_color  = fg.Bgreen
    else:
        high_updown_color  = fg.Bred
        
    
    if last_low > next_to_last_low:
        low_updown_color   = fg.Bgreen
    else:
        low_updown_color   = fg.Bred
        
    if last_obv > last_obvema:
        obv_emoji_signal = '🟢'
    else:
        obv_emoji_signal = '🟥'
        
    if last_rsi > last_rsiema:
        rsi_emoji_signal = '🟢'
    else:
        rsi_emoji_signal = '🟥'
        
    if last_close > last_ema50 and last_close > last_ema200:
        ema_emoji_signal = '🟢'
    else:
        ema_emoji_signal = '🟥'

            
    INFO_TABLE = f"""In Trade:{bg.red}False{ac.clear}     Pair:{pair} Strat:{strat} Quantity:{asset_qauntity} {fg.Bwhite}
    LAST:{ac.clear}
        Open   - {open_updown_color}{last_open}{ac.clear}
        Close  - {close_updown_color}{last_close}{ac.clear}
        High   - {high_updown_color}{last_close}{ac.clear}
        Low    - {low_updown_color}{last_close}{fg.Bwhite}
        
INDICATORS:{ac.clear}
        RSI    - {round(last_rsi, 4)}
        RSIema - {round(last_rsiema, 4)}
        EMA22  - {round(last_ema22, 4)}
        EMA50  - {round(last_ema50, 4)}
        EMA200 - {round(last_ema200, 4)}
{fg.white}RSI bull/bear - {rsi_emoji_signal} EMA bull/bear - {ema_emoji_signal} OBV bull/bear - {obv_emoji_signal}
"""

    """UI logic."""
    table_grid = [[''],
                  [''],
                  ['']]
    table = SingleTable(table_grid)
    table.table_data[1][0] = INFO_TABLE
    table.table_data[0][0] = HEADER
    table.table_data[2][0] = output
    print(table.table)


in_position=False





def RSIemaCross():
    global in_position
    if config.TESTING == False:
        if last_rsi > last_rsiema and last_rsi > 50:
            if in_position:
                output = "Conditions are currently being met, but you're already in a position"
            else:
                output = f"I've spotten an oppurtunity accourding to the\n {strat} Strat Sending a BUY order :)"
                order_succeeded = Order(SIDE_BUY, asset_qauntity, pair)
                if order_succeeded:
                    in_position = True
        elif in_position:
            output = f"According to the {strat}, it\'s time to sell\n Sending a SELL order!"
            order_succeeded = Order(SIDE_SELL, asset_qauntity, pair)
            if order_succeeded:
                in_position = False



def GoldenCross():
    global in_position
    if config.TESTING == False:
        if last_close > last_ema22 and last_close > last_ema50 and last_close > last_ema200:
            if in_position:
                output = "Conditions are currently being met, but you're already in a position"
            else:
                output = f"I've spotten an oppurtunity accourding to the\n {strat} Strat Sending a BUY order :)"
                order_succeeded = Order(SIDE_BUY, asset_qauntity, pair)
                if order_succeeded:
                    in_position = True
        elif in_position:
            output = f"According to the {strat}, it\'s time to sell\n Sending a SELL order!"
            order_succeeded = Order(SIDE_SELL, asset_qauntity, pair)
            if order_succeeded:
                in_position = False



        
while True:
    Main()
    # RSI strat initiation
    RSIstrat = False
    if strat == 'RSIemaCross' or '1':
        RSIstrat = True
        RSIemaCross()

    # EMA strat initiation
    EMAstrat    = False
    if strat == 'GoldenCross' or '2':
        EMAstrat = True
        GoldenCross()
    
    # interval between updates
    time.sleep(1)
    # This counts how many lines have been drawn, 
    # then deletes said amound before drawing the next, 
    # simple animation methotd I suppose.
    terminal_length = os.get_terminal_size().lines
    for i in range(terminal_length):
        sys.stdout.write('\033[F')