ALPHAVANTAGE_API_KEY = '7aa99ffd0e1a4339b919861f2f63f641'

# Replace 'YOUR_NEWS_API_KEY' with your actual News API key
NEWS_API_KEY = '7aa99ffd0e1a4339b919861f2f63f641'

import requests
import pandas as pd


NYT_API_KEY='qbNDwYiXxRbpo6c8HqgLBcBkYKSDCVvx'
  # Replace this with your actual New York Times API key

def scrape_nyt_news(keyword, from_date, to_date):
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {
        'q': keyword,
        'begin_date': from_date,
        'end_date': to_date,
        'api-key': NYT_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    news_data = []
    if 'response' in data and 'docs' in data['response']:
        for article in data['response']['docs']:
            headline = article.get('headline', {}).get('main', '')
            snippet = article.get('snippet', '')
            published_at = article.get('pub_date', '')
            news_data.append({
                'headline': headline,
                'snippet': snippet,
                'publishedAt': published_at
            })

    return news_data



def get_stock_news(symbol, from_date):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': symbol,
        'from': from_date,
        # 'to': to_date
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'articles' in data:
        stock_news_json = json.dumps(data['articles'])

        # Save news articles to a file
        with open(f'{symbol}_stock_news_{from_date}_.json', 'w') as f:
            f.write(stock_news_json)
        return stock_news_json
    else:
        return None



import json
from datetime import datetime

# Keep only the required fields for each item in the data list

#return formatted news

def convert_date_format(iso_date):
    date_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S%z")
    return date_obj.strftime("%Y-%m-%d")

def formatted_news(news_list):

    filtered_data = []
    for item in news_list:
            item["publishedAt"] = convert_date_format(item["publishedAt"])

    return news_list


import yfinance as yf
import json

def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    stock_data_list = stock_data.reset_index().to_dict(orient='records')

    for item in stock_data_list:
        item['Date'] = item['Date'].strftime('%Y-%m-%d')

    return stock_data_list

def calculate_percentage_change(prev_day, curr_day):
    percentage_change = {}
    for key in ["Open", "Close", "High"]:
        prev_value = float(prev_day[key])
        curr_value = float(curr_day[key])
        change = curr_value - prev_value
        percentage = (change / prev_value) * 100
        percentage_change[key] = round(percentage, 2)
    return percentage_change
def format_stocks(data):
    comparison_data = []
    for i in range(1, len(data)):
        prev_day = data[i - 1]
        curr_day = data[i]
        comparison_date = prev_day["Date"]
        percentage_change = calculate_percentage_change(prev_day, curr_day)
        comparison_data.append({"Date": comparison_date, "PercentageChange": percentage_change})
    return comparison_data
def convert_to_two_digit(number):
    if 0 <= number < 10:
        return f"0{number}"
    else:
        return str(number)
# Function to map stock data with publishedAt
def map_stock_to_data(stock_list, data_list):
    mapped_data = []
    for stock_item in stock_list:
        for data_item in data_list:
            if stock_item["Date"] == data_item["publishedAt"]:
                mapped_item = {
                    "Date": stock_item["Date"],
                    "PercentageChange": stock_item["PercentageChange"],
                    "snippet": data_item["snippet"],
                    "publishedAt": data_item["publishedAt"],
                    "headline": data_item["headline"]
                }
                mapped_data.append(mapped_item)
                break
    return mapped_data



def finalize_data(symbol,iter,year_last):
    stock=get_stock_data(symbol,'20'+convert_to_two_digit(year_last)+'-'+convert_to_two_digit(iter)+'-01',end_date='20'+convert_to_two_digit(year_last)+'-'+convert_to_two_digit(iter)+'-31')
    with open('stocks'+str(iter)+'.json', "w") as f:
            json.dump(stock, f, indent=2)

    stock=json.load(open('stocks'+str(iter)+'.json',encoding='utf-8'))

    stock=format_stocks(stock)
    news_list=scrape_nyt_news(keyword='Paypal',from_date='20'+convert_to_two_digit(year_last)+'-'+convert_to_two_digit(iter)+'-01',to_date='20'+convert_to_two_digit(year_last)+'-'+convert_to_two_digit(iter)+'-31')
    with open('news'+str(iter)+'.json', "w") as f:
            json.dump(news_list, f, indent=2)

    news_list=json.load(open('news'+str(iter)+'.json',encoding='utf-8'))
    data=formatted_news(news_list)




    return map_stock_to_data(stock,data)

for j in range(10,23):
    for i in range(1,13):
        print(""+str(i)+" "+str(j)+"")
        mapped=finalize_data('PYPL',i,j)
        output='mapped_'+convert_to_two_digit(j)+convert_to_two_digit(i)+''
        with open(output, "w") as f:
            json.dump(mapped, f, indent=2)

