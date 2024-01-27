import gpsoauth as go

try:
   print ("\nEnter your Google ID, the copied oauth_token cookie, and any value for the Android ID:\n")
   t = dict(go.exchange_token(input('Google ID: '), input('oauth_token Cookie: '), input('Android ID: ')))
   final_token = t["Token"]
   print ("\nCongratulations! This is your Google Keep token - you only need to extract this once. Please copy and run 'python kim.py -t <your token here>' to save the token key in your keystore. Keep-it-markdown should work on your PC from now on!\n")
   print (final_token)
except Exception as e:
   print ("\nEither you entered your ID and OAuth cookie incorrectly or the OAuth cookie has expired. Try getting the OAuth cookie and run this again - the cookie expires within 5 minutes.")



