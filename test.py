a = '재우'
encoded = a.encode('utf-8')
print(encoded)
encoded2 = a.encode('euc-kr')
print(encoded2)
# b'\xec\x9e\xac\xec\x9a\xb0'
# b'\xc0\xe7\xbf\xec'

b = b'\xec\x9e\xac\xec\x9a\xb0'
decoded = b.decode('utf-8')
print(decoded)

import