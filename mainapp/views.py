from threading import Thread
import queue
from django.shortcuts import render
from yahoo_fin.stock_info import tickers_nifty50, get_quote_table


def stockpicker(request):
    stockPicker = tickers_nifty50()
    return render(
        request=request,
        template_name="mainapp/stockpicker.html",
        context={
            "stockpicker": stockPicker,
        },
    )


def stocktracker(request):
    allStocks: list = request.GET.getlist("stockpicker")
    availableStock = tickers_nifty50()
    correctStocks: list[str] = []
    errorStocks: list[str] = []

    for i in allStocks:
        if i in availableStock:
            correctStocks.append(i)
        else:
            errorStocks.append(i)

    errorStocksString: str = ", ".join(errorStocks)

    data: dict = {}

    thread_list: list = []
    result: list = []
    que: queue.Queue = queue.Queue()

    for i, stock in enumerate(correctStocks):
        thread = Thread(target=lambda q, arg1: q.put(get_quote_table(stock)), args=(que, stock))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
                
    print("Data fetched successfully")

    return render(
        request=request,
        template_name="mainapp/stocktracker.html",
        context={
            "selectedstock": "Reliance",
            "data": data,
            "errorStocks": errorStocksString,
        },
    )
