from firebase import firebase

firebase = firebase.FirebaseApplication('https://intense-heat-9265.firebaseio.com', None)
result = firebase.get('', None)
print result
