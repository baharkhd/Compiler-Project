import json
  
f = open('table.json')
  

data = json.load(f)
  

# keys: ['terminals', 'non_terminals', 'first', 'follow', 'grammar', 'parse_table']
print(data.keys())
print()
for k, v in data['parse_table'].items():
    print(k, ":", v)
#print(data['parse_table'])


f.close()