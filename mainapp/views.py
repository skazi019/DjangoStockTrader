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
    for i in correctStocks:
        # breakpoint()
        data.update({i: get_quote_table(i)})

    return render(
        request=request,
        template_name="mainapp/stocktracker.html",
        context={
            "selectedstock": "Reliance",
            "data": data,
            "errorStocks": errorStocksString,
        },
    )
