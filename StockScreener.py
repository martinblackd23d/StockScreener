#Python Stock Screener with TD Ameritrade API
ameritrade = ''
import requests, time, re, os
import pandas as pd
import pickle as pkl

url = 'https://api.tdameritrade.com/v1/instruments'

def queryall():
	df = pd.read_excel('Complete_List.xlsx')
	symbols = df['Symbol'].values.tolist()

	start = 0
	end = 500
	files = []
	counter = 1


	while start < len(symbols):
		tickers = symbols[start:end]
		#if counter == 11 or counter == 12:
		#	print(tickers)


		payload = {'apikey': ameritrade,
				   'symbol': tickers,
				   'projection': 'fundamental'}

		results = requests.get(url, params = payload)
		data = results.json()
		if 'error' not in data:
			f_name = time.asctime() + '.pkl'
			f_name = re.sub('[ :]', '_ ', f_name)
			files.append(f_name)

			with open(f_name,'wb') as file:
				pkl.dump(data, file)
		#	with open(str(counter) + '.txt','w') as file:
		#		file.write(str(data))
		start = end
		end += 500
		print('file created: ' + str(counter))
		counter += 1
		time.sleep(1)

	print('finished creating files')
	data = []
	counter = 1

	for file in files:
		with open(file, 'rb') as f:
			info = pkl.load(f)
		tickers = list(info)
		points = ['symbol', 'netProfitMarginMRQ', 'peRatio', 'pegRatio', 'high52']
		for ticker in tickers:
			tick = []
			for point in points:
				tick.append(info[ticker]['fundamental'][point])
			data.append(tick)
		os.remove(file)
		print('file read: ' + str(counter))
		counter += 1

	points = ['symbol', 'Margin', 'PE', 'PEG', 'high52']

	df_results = pd.DataFrame(data, columns = points)
	print('finished reading files')

	df_peg = df_results[(df_results['PEG'] < 1) & (df_results['PEG'] > 0) & (df_results['Margin'] > 20) & (df_results['PE'] > 10)]
	df_peg.sort_values(['PEG'])

	def view(size):
		start = 0
		stop = size
		while stop < len(df_peg):
			print(df_peg[start:stop])
			start = stop
			stop += size
		print(df_peg[start:stop])

	df_symbols = df_peg['symbol'].tolist()
	new = df['Symbol'].isin(df_symbols)
	companies = df[new]
	return
