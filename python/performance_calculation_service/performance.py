import redis
import time
import json
import multiprocessing

REDIS_CONTAINER = 'redis_redis_1'
r = redis.Redis(host=REDIS_CONTAINER, port=6379, db=0)


def calculate_performance(stock_price):
	time.sleep(3)
	return 0


def performance(stock, queue):
	item = json.loads(r.get(stock))
	perf = queue.get()
	perf[1] = calculate_performance(item['price'])
	queue.put(perf)


if __name__ == '__main__':
	while(True):
		stocks = ['stock1', 'stock2', 'stock3']
		process_list = []
		queue = multiprocessing.Queue()
		for stock in stocks:
			stock_item = json.loads(r.get(stock))
			if stock_item['price_changed']:
				queue.put([stock, 0])
				process = multiprocessing.Process(target=performance, args=[stock, queue])
				process_list.append(process)
				process.start()

		for process in process_list:
			process.join()

		while not queue.empty():
			item = queue.get()
			stock = json.loads(r.get(item[0]))
			stock['performance'] = item[1]
			stock['price_changed'] = False
			r.set(item[0], json.dumps(stock))
			print('done')
		time.sleep(60)
