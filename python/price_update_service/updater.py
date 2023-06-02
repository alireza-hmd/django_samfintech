import csv
import redis
import json

REDIS_CONTAINER = 'redis_redis_1'
r = redis.Redis(host=REDIS_CONTAINER, port=6379, db=0)

stock_price_list = {
    'stock1': {},
    'stock2': {},
    'stock3': {},
}

with open('price_data.csv') as data_file:
    stocks_data = csv.reader(data_file, delimiter=',')
    line_count = 0
    for row in stocks_data:
        if line_count == 0:
            line_count += 1
        else:
            time = row[0][:2] + ':' + row[0][2:4]
            if stock_price_list[row[1]].get(time):
                stock_price_list[row[1]][time][0] += int(row[2])
                stock_price_list[row[1]][time][1] += 1
            else:
                stock_price_list[row[1]][time] = [int(row[2]), 1]


for stock in stock_price_list:
    stock_item = json.loads(r.get(stock))
    stock_item['price_changed'] = False
    for time in stock_price_list[stock]:
        total_price, count = stock_price_list[stock][time]
        if time in stock_item['time']:
            index = stock_item['time'].index(time)
            if stock_item['price'][index] != total_price / count:
                stock_item['price'][index] = total_price / count
                stock_item['price_changed'] = True
        else:
            stock_item['time'].append(time)
            stock_item['price'].append(total_price/count)
            stock_item['price_changed'] = True

    r.set(stock, json.dumps(stock_item))
    print(r.get(stock), '\n')
