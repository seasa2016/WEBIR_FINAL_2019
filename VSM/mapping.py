import sys
mapping = []
with open('./model/mapping') as f:
	for line in f:
		line = line.split('\t')
		mapping.append(line[1])

with open(sys.argv[1]) as f:
	with open(sys.argv[2],'w') as f_out:
		f.readline()
		for line in f:
			line = line.split(',')
			f_out.write(mapping[int(line[1])])
			f_out.write(':')
			for num in line[2:30]:
				f_out.write('{0},'.format(mapping[int(num)]))
			f_out.write('\n')
		

