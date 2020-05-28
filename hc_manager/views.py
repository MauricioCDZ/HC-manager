"""
Archivo donde se enlazan las acciones y eventos del código con las 
vistas en html.
"""

from django.shortcuts import render
import pyrebase

# Configuración del wrap pyrebase
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
db = firebase.database()

def newHC(request):
	if request.method == 'POST':
		inputs = ['cedula','fecha_nac','nombre']
		cedula = request.POST.get('cedula')
		for inp in inputs:
			db.child(cedula).child(inp).set(request.POST.get(inp))
		return render(request, "hc_manager/welcome.html", {'data': db.get().val()})
	return render(request, "hc_manager/creation.html")

def editHC(request, cedula):
	if request.method == 'GET':
		users = {cedula:db.child(cedula).get().val()}
		return render(request, "hc_manager/edition.html", {'data':users})
	elif request.method == 'POST':
		inputs = ['fecha_nac','nombre']
		for inp in inputs:
			db.child(cedula).update({inp:request.POST.get(inp)})
		return render(request, "hc_manager/welcome.html", {'data': db.get().val()})