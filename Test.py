import re

url = "Tesla going hard"
pattern = 'r'+'tesla'+ '\\' + 'b'
company = 'tesla'
found = re.search(r'{}'.format(company), url.lower())

print(found)