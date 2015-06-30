from firebase import firebase
firebase = firebase.FirebaseApplication('https://intense-heat-9265.firebaseio.com', None)
new_user = 'Jim Wood'

result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print ("Result: %s" % result)
