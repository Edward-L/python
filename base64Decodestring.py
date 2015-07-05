import base64

test = raw_input("input what do you want to decode: \n")
testa = base64.decodestring(test)

print testa