import pyotp 
key = 'XIVQ45257OR6WE6HVI6GSXCOFJ342SWV' 
totp = pyotp.TOTP(key) 
print(totp.now())