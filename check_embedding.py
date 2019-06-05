with open('./analysis/vocab') as f:
	for line in f:
		line = line.split()
		data[line[0]] = int(line[1])
mapping = []
    
with open('./embedding/GoogleNews-vectors-negative300.bin') as f:
	for i,line in enumerate(f):
		line = line.split()
		mapping.append(line[0])
ins,out=0,0
temp = []
for key in data:
	if(key in mapping):
		ins += data[key]
	else:
		ins += data[key]\n
		temp.append((key,data[key]))
       "[('it’s', 516104),\n",
       " ('“i', 325595),\n",
       " ('don’t', 316237),\n",
       " ('“the', 294077),\n",
       " ('that’s', 228057),\n",
       " ('didn’t', 183080),\n",
       " ('he’s', 168969),\n",
       " ('“we', 164853),\n",
       " ('i’m', 163063),\n",
       " ('doesn’t', 129577),\n",
       " ('there’s', 124298),\n",
       " ('trump’s', 121560),\n",
       " ('can’t', 117663),\n",
       " ('we’re', 112152),\n",
       " ('you’re', 106213),\n",
       " ('“it’s', 99038),\n",
       " ('they’re', 98922),\n",
       " ('“it', 97892),\n",
       " ('isn’t', 88420),\n",
       " ('wasn’t', 79713),\n",
       " ('“a', 72677),\n",
       " ('i’ve', 68455),\n",
       " ('“this', 67188),\n",
       " ('won’t', 64248),\n",
       " ('“you', 59522),\n",
       " ('“he', 57534),\n",
       " ('“if', 56241),\n",
       " ('we’ve', 54052),\n",
       " ('obama’s', 51945),\n",
       " ('what’s', 51420),\n",
       " ('“i’m', 48874),\n",
       " ('“but', 47602),\n",
       " ('loudoun', 44329),\n",
       " ('“they', 44164),\n",
       " ('here’s', 44000),\n",
       " ('couldn’t', 43887),\n",
       " ('aren’t', 42390),\n",
       " ('she’s', 42376),\n",
       " ('“and', 42299),\n",
       " ('wouldn’t', 40476)]"
