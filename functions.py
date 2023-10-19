from binance.client import Client
import math
import time
import config

client = Client(config.API_KEY, config.API_SECRET, tld='com')


def get_quantity_precision(current_symbol):
    global step_size
    global tick_size
    while True:
        try:
            info = client.futures_exchange_info()
        except Exception as e_rror:
            print(e_rror)
            archivo_e = open("log.txt", "a")
            mensaje_e = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e_rror) + "\n"
            archivo_e.write(mensaje_e)
            archivo_e.close()
            time.sleep(2)
        else:
            break
    info = info['symbols']
    for x in range(len(info)):
        if info[x]['symbol'] == current_symbol:
            for f in info[x]['filters']:
                if f['filterType'] == 'LOT_SIZE':
                    step_size = float(f['stepSize'])
                if f['filterType'] == 'PRICE_FILTER':
                    tick_size = float(f['tickSize'])
            return info[x]['pricePrecision'], info[x]['quantityPrecision']
    return None


def positionInfo(tick):
    while True:
        try:
            currentPosition = client.futures_position_information(symbol=tick)
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S',
                                    time.localtime()) + ' ERROR: ' + str(
                e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break
    return currentPosition


def takeProfit(entryPrice, pricePrecision):
    sellPrice = "{:0.0{}f}".format(entryPrice, pricePrecision)
    precision = int(round(-math.log(tick_size, 10), 0))
    return float(round(float(sellPrice), precision))


def createTpOrder(tick, monedas, sellPrice, side):
    if monedas < 0:
        monedas = monedas*-1
    while True:
        try:
            crear = client.futures_create_order(
                symbol=tick,
                type='LIMIT',
                side=side,
                quantity=monedas,
                price=sellPrice,
                reduceOnly=True,
                timeInforce='GTC'
            )
            time.sleep(1)
            return crear
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S',
                                    time.localtime()) + ' ERROR: ' + str(e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break
