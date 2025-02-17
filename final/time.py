'''
Author: Sumeet Bansal
Title: Time-Based Analysis of Comments
'''

# reads in the training dataset and retains the timetamped comments
import pandas as pd
file = 'train.csv'
train = pd.read_csv(file, header=0)
train = train[train['comment_text'].str.contains('UTC')]

# sets up dict of timestamped comments, key=profanity type, value=count for each year
df = {}
df['toxic'] = []
df['severe_toxic'] = []
df['obscene'] = []
df['threat'] = []
df['insult'] = []
df['none'] = []
df['identity_hate'] = []
for i, row in train.iterrows():
	ct = row['comment_text']
	if ' (UTC)' not in ct:
		continue
	eit = ct.index(' (UTC)')
	if ct[eit-4:eit-2] != '20':
		continue
	year = int(ct[eit-4:eit])
	if year not in years:
		years[year] = 0
	years[year] += 1
	profane = False
	for key in df:
		if key != 'none' and row[key] == 1:
			df[key].append(year)
			profane = True
	if not profane:
		df['none'].append(year)

# determines the counts per year for each profanity type
minyear = 3000
maxyear = -1
for key in df:
	minyear = min(min(df[key]), minyear)
	maxyear = max(max(df[key]), maxyear)
for key in df:
	counts = {}
	for y in range(minyear, maxyear + 1):
		counts[y] = df[key].count(y)
	df[key] = counts

# writes the counts to a .csv
with open('counts-' + file, 'w') as csv:
	csv.write('classification, %s\n' % str(list(df['toxic'].keys()))[1:-1])
	for key in df:
		csv.write("%s, %s\n" % (key, str(list(df[key].values()))[1:-1]))

# determines the percentages per year for each profanity type
for key in df:
	for y in df[key]:
		df[key][y] /= years[y]

# writes the percentages to a .csv
del df['none']
with open('percentage-' + file, 'w') as csv:
	csv.write('classification, %s\n' % str(list(df['toxic'].keys()))[1:-1])
	for key in df:
		csv.write("%s, %s\n" % (key, str(list(df[key].values()))[1:-1]))
