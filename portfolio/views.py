from django.shortcuts import render
from .models import Currencies
from django.http import HttpResponse, JsonResponse
from .models import InvestmentDetails
import requests
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

data = {}


def index(request):
    """
    Render home page.
    """
    results = Currencies.objects.all()
    return render(request, 'home.html', {"show_currencies": results})


def details(request, currency: str, percent_of_investment: str, year: str, month: str, day: str) -> HttpResponse:
    """
    Save data.
    """
    start_date = datetime(int(year), int(month), int(day))
    start_date = start_date.strftime('%Y-%m-%d')
    today = date.today()
    min_start_date = today - timedelta(days=int(30))

    if start_date > min_start_date.strftime('%Y-%m-%d'):
        year = min_start_date.year
        month = min_start_date.month
        day = min_start_date.day

    new = InvestmentDetails(currency=currency, percent_of_investment=percent_of_investment, year=year, month=month,
                            day=day)
    new.save()

    return HttpResponse(status=204)


def calculate(request) -> HttpResponse:
    """Download portfolio details data from NBP api, calculate and save into global data dictionary"""
    global data

    # constants
    START_VALUE = int(1000)
    INVESTMENT_TIME = int(30)
    currencies = {}
    initial_weight = []

    # get last 3 objects from ORM (portfolio details)
    investments = InvestmentDetails.objects.all().order_by('-id')[:3]

    # create portfolio
    portfolio = [investment.return_details() for investment in investments]

    # date time formatting
    start_date = datetime(portfolio[0][2], portfolio[0][3], portfolio[0][4])
    end_date = start_date + timedelta(days=INVESTMENT_TIME)

    # convert date time format to RR-MM-DD format
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    for investment in portfolio:
        url = f'http://api.nbp.pl/api/exchangerates/rates/c/{investment[0]}/{start_date}/{end_date}/?format=json'
        request_currency_data = requests.get(url).json()

        currency_data = pd.DataFrame(request_currency_data['rates'])
        currency_data = currency_data.drop('no', axis=1)

        currencies[investment[0]] = currency_data.set_index("effectiveDate")
        currencies[investment[0]] = (currencies[investment[0]]['bid'] + currencies[investment[0]]['ask']) / 2

        portfolio_df = pd.concat(currencies, axis=1)
        initial_weight.append(float(investment[1]) / 100)

    initial_weight = np.array(initial_weight)
    return_stocks = portfolio_df.pct_change().dropna()

    # calculate portfolio daily returns
    return_stocks['portfolio_daily_returns'] = return_stocks.dot(initial_weight)

    cumulative_returns_daily = (1 + return_stocks[
        'portfolio_daily_returns']).cumprod() * START_VALUE

    # currencies rates
    data['labels'] = portfolio_df.index.to_list()

    data['cur1_name'] = portfolio[0][0]
    data['cur1_data'] = [round(value, 4) for value in portfolio_df[data['cur1_name']]]

    data['cur2_name'] = portfolio[1][0]
    data['cur2_data'] = [round(value, 4) for value in portfolio_df[data['cur2_name']]]

    data['cur3_name'] = portfolio[2][0]
    data['cur3_data'] = [round(value, 4) for value in portfolio_df[data['cur3_name']]]

    # start value
    data['start_value'] = START_VALUE

    # portfolio balance
    data['labels_balance'] = cumulative_returns_daily.index.to_list()
    data['balance_data'] = [round(value, 2) for value in cumulative_returns_daily]

    # initial weight
    data['label_weight'] = [portfolio[0][0], portfolio[1][0], portfolio[2][0]]
    data['data_weight'] = [round(value * 100, 2) for value in initial_weight]

    # value at the end of investment
    data['portfolio_value'] = data['balance_data'][-1]

    # data for histograms
    data['histogram_cur1'] = [round(value * (START_VALUE * initial_weight[0]), 4) for value in
                              return_stocks[data['cur1_name']]]
    data['histogram_cur2'] = [round(value * (START_VALUE * initial_weight[1]), 4) for value in
                              return_stocks[data['cur2_name']]]
    data['histogram_cur3'] = [round(value * (START_VALUE * initial_weight[2]), 4) for value in
                              return_stocks[data['cur3_name']]]

    if data['portfolio_value'] < START_VALUE:
        data['portfolio_changes'] = round(((data['portfolio_value'] - START_VALUE) / START_VALUE) * 100, 2)
    else:
        data['portfolio_changes'] = round(((data['portfolio_value'] - START_VALUE) / START_VALUE) * 100, 2)

    data['portfolio_diff'] = round((data['portfolio_value'] - START_VALUE), 2)

    # charts titles details (percent of currency in portfolio)
    data['portfolio_cur1'] = str(round(initial_weight[0] * 100, 0)) + '%'
    data['portfolio_cur2'] = str(round(initial_weight[1] * 100, 0)) + '%'
    data['portfolio_cur3'] = str(round(initial_weight[2] * 100, 0)) + '%'

    return HttpResponse(status=204)


def charts_data(request):
    """
    Return a global dictionary containing the details of the created portfolio
    """
    global data
    return JsonResponse(data=data)
