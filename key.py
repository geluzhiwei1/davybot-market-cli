import pyotp 
key = 'GUMGLRVCM2DLYUQ5ZZ7L56ZNNQCELHZ3' 
totp = pyotp.TOTP(key) 
print(totp.now())