import time

from functions import *

print("")
print("##################################")
print("########-CRIPTO SPARTANS-#########")
print("###############TP#################")
print("                 By ElgafasTrading")
print("")

tick = ""
entryPrice = 0.0
positionAMT = 0.0
tpAuto = 0
orderID = 0

tick_size = 0.0


while True:
    while len(tick) == 0:
        tick = input("INGRESE EL TICK: ").upper()
        tick = tick + 'USDT'
    if tpAuto == 0:
        while True:
            try:
                tpAuto = float(input("INGRESE EL PORCENTAJE DEL TAKE PROFIT: "))
                break
            except:
                print("VALOR INVALIDO, INGRESE UN NUMERO VALIDO")
    info = positionInfo(tick)
    if info:
        if float(info[0].get('positionAmt')) != 0:
            print("positionAmt: " + str(info[0].get('positionAmt')) + " entryPrice: " + str(
                info[0].get('entryPrice')) + " leverage: " + str(info[0].get('leverage')))
            if entryPrice != float(info[0].get('entryPrice')) or positionAMT != float(info[0].get('positionAmt')):
                entryPrice = float(info[0].get('entryPrice'))
                positionAMT = float(info[0].get('positionAmt'))

                if orderID != 0:
                    client.futures_cancel_order(symbol=tick, orderId=orderID)
                    print("ORDEN TAKE PROFIT CANCELADA")
                    time.sleep(1)

                precioTP = 0
                side = 'BUY'

                if positionAMT < 0:
                    precioTP = entryPrice - (entryPrice * tpAuto) / 100
                else:
                    precioTP = entryPrice + (entryPrice * tpAuto) / 100
                    side = 'SELL'

                pricePrecision = get_quantity_precision(tick)
                precioTP = takeProfit(precioTP, pricePrecision[0])
                crear = createTpOrder(tick, positionAMT, precioTP, side)
                orderID = crear['orderId']

        else:
            print("NO HAY POSICIONES ABIERTAS EN: " + tick)
            openOrders = client.futures_get_open_orders(symbol=tick)
            if len(openOrders) > 0:
                client.futures_cancel_all_open_orders(symbol=tick)
            tick = ""
            tpAuto = 0
            entryPrice = 0.0
            positionAMT = 0.0
            orderID = 0
        time.sleep(2)
    else:
        tick = ""
        tpAuto = 0
        entryPrice = 0.0
        positionAMT = 0.0
        orderID = 0

    time.sleep(2)
