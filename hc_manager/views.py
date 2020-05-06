from django.shortcuts import render
import pyrebase

config = {
	    'apiKey': "AIzaSyBeSa2PSyHEtt9jPRYZXjRP4myOvGBXoGc",
	    'authDomain': "hc-manager-e2356.firebaseapp.com",
	    'databaseURL': "https://hc-manager-e2356.firebaseio.com",
	    'projectId': "hc-manager-e2356",
	    'storageBucket': "hc-manager-e2356.appspot.com",
	    'messagingSenderId': "869491009077",
	    'appId': "1:869491009077:web:35468c3d8127791a55337c",
	    'measurementId': "G-C33NC6SJCB"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def signIn(request):
	return  render(request, "signIn.html")

def postSign(request):
	email = request.POST.get('email')
	passw = request.POST.get('pass')
	user = auth.sign_in_with_email_and_password(email,passw)
	return render(request, "welcome.html", {'e':email})