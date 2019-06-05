import sys
import math
import numpy as np

total_map,total_NDCG = [],[]

for pred_file in sys.argv[1:]:
	data = []
	with open(pred_file) as f:
		line = f.readline()

		for line in f:
			data.append( line.split(',')[1:] )

	ans = []
	prev = '支持陳前總統保外就醫'
	with open('TD.csv') as f:
		line = f.readline()
		ans.append({})

		for line in f:
			line = line.split(',')
			if(prev != line[0]):
				prev = line[0]
				ans.append({})
			
			ans[-1][ line[1] ] = int(line[2])

	#count MAP,NDCG here
	MAP,NDCG = [],[]
	for i,preds in enumerate(data):
		ch = [0,0,0,0]
		MAP.append(0)
		NDCG.append(0)
		
		for j,pred in enumerate(preds):
			try:
				ch[ ans[i][pred] ] += 1
				MAP[-1] += 1
				if(j==0):
					NDCG[-1] += ans[i][pred]
				else:
					NDCG[-1] += ans[i][pred]/ math.log(j+1,2)

			except:
				pass
		#print(ch)

		temp = 0
		total = 0
		for a in range(3,0,-1):
			for b in range(ch[a]):
				if(total==0):
					temp += a
				else:
					temp += a / math.log(total+1,2)
				total += 1
		
		if(NDCG[-1]==0):
			continue
		NDCG[-1] = NDCG[-1]/temp
		MAP[-1] = MAP[-1]/300

	total_map.append( sum(MAP)/20 )
	total_NDCG.append( sum(NDCG)/20 )

total_map = np.array(total_map)
total_NDCG = np.array(total_NDCG)

file_name = np.array(sys.argv[1:])
print(file_name[total_map.argsort()[-1:-10:-1]])
print(total_map[total_map.argsort()[-1:-10:-1]])
print(file_name[total_NDCG.argsort()[-1:-10:-1]])
print(total_NDCG[total_NDCG.argsort()[-1:-10:-1]])
