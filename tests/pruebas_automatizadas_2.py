import pyrebase
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

# Todos los representantes de la tabla de particiones de equivalencia funcionalidad 2.6 "Añadir nueva cita"
data = [
"80",
"-80",
"1000001",
"85.5",
"loajhgy!&",
"200",
"-88838",
"4300001",
"100.123",
"aslñba¿$",
"papa,arroz,pollo",
"$!#!!#;_!d!1231",
"Dolor de cabeza y náuseas durante más de 10 horas",
"",
"El paciente presenta síntomas de malnutrición y deshidratación",
""
]

# Cada indice de cada caso de prueba representa las variables peso,estatura,dieta alimenticia,motivo de consulta,observaciones (en ese orden y saltandonos 'actividad física', 'enfermedades' y 'valor preliminar')
# Eg, "0" en la posición 0 del primer caso representa el dato "80" de la variable "peso".
testcases = [
[0,5,10,12,14], #CPV02
[0,5,10,12,15], #CPV03
[1,5,10,12,15], #CPNV12
[2,5,10,12,15], #CPNV13
[3,5,10,12,15], #CPNV14
[4,5,10,12,15], #CPNV15
[0,6,10,12,15], #CPNV16
[0,7,10,12,15], #CPNV17
[0,8,10,12,15], #CPNV18
[0,9,10,12,15], #CPNV19
[0,5,10,13,15], #CPNV20
[0,5,11,12,15]  #CPNV21
]

cedula = "1112223334"

# test case label
tcl = dict(zip(range(1,len(testcases)+1), ["CPV02", "CPV03", "CPNV12", "CPNV13", "CPNV14", "CPNV15", "CPNV16", "CPNV17", "CPNV18", "CPNV19", "CPNV20", "CPNV21"]))

driver = Firefox()
driver.get("http://181.62.170.37:8000/editHC/1112223334/")

# Hacemos login
#driver.find_element_by_name('email').send_keys("gargal@gmail.com")
#driver.find_element_by_name('pass').send_keys("test123") 
#driver.find_element_by_xpath("/html/body/div/div/form/button").click()
#
#""" No me funciona a mi, por alguna razon
# Buscamos la cédula "1112223334"
#driver.find_element_by_xpath('//*[@id="dateInput"]').send_keys(Keys.RETURN)
#"""
#driver.find_element_by_tag_name('html').send_keys(Keys.END)
#driver.find_element_by_xpath("//a[@href='/editHC/1112223334']").click()

# Click a botón nueva cita
driver.find_element_by_xpath("/html/body/div[2]/button[2]").click()

peso = driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/div[1]/input")
estatura = driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/div[2]/input")
dieta = driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[2]/input")
motivo = driver.find_element_by_xpath('//*[@id="motivo"]')
comentario = driver.find_element_by_xpath('//*[@id="comentario"]')
send_button = driver.find_element_by_xpath("/html/body/div[2]/form/button")

# successful test cases
stc = 0

# failed test cases
ftc = 0

# test case number
tc = 0

# Se eliminan todas las citas para la HC de la cédula 1112223334 antes de empezar las pruebas
try: db.child(cedula).child('citas').remove()
except: pass
# Esperar 3 segundos a que la Realtime Database de Firebase tenga tiempo de guardar un nuevo registro.
try: WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "none")))
except TimeoutException: pass

# ------------------ CPV02 -> CPV03 ------------------ 
# Para estos casos, queremos probar que los valores de entrada (que son validos) son guardados correctamente en la DB.
for testcase in testcases[:2]:
    tc += 1

    peso.send_keys(data[testcase[0]])
    estatura.send_keys(data[testcase[1]])
    dieta.send_keys(data[testcase[2]])
    motivo.send_keys(data[testcase[3]])
    comentario.send_keys(data[testcase[4]])
    send_button.click()

    # Esperar 3 segundos a que la Realtime Database de Firebase tenga tiempo de guardar un nuevo registro.
    try: WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "none")))
    except TimeoutException: pass
    
    try:
        # Si encuentra el botón de "Historial de cambios", quiere decir que volvimos a la pantalla de edición de HC
        driver.find_element_by_xpath("/html/body/div[2]/button[1]")
        if db.child(cedula).child('citas').get().val():
            print(f"Caso {tcl[tc]}: exitoso")
            stc += 1
        else:
            print(f"Caso {tcl[tc]}: fallido - el registro de cita no fue guardado en DB")
            ftc += 1

    except:
        # Si no encuentra el botón de "Historial de cambios", lanza una excepción y entramos en este except.
        # Quiere decir que aún estamos en la pantalla de creación de nueva cita.
        if db.child(cedula).child('citas').get().val():
            print(f"Caso {tcl[tc]}: exitoso - el registro de cita fue guardado en DB; pero no hubo cambio de vista")
            stc += 1
        else:
            print(f"Caso {tcl[tc]}: fallido - el registro no fue guardado en DB; y no hubo cambio de vista")
            ftc += 1

        peso.clear()
        estatura.clear()
        dieta.clear()
        motivo.clear()
        comentario.clear()

    try: driver.find_element_by_xpath("/html/body/div[2]/button[2]").click()
    except: pass

    peso = driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/div[1]/input")
    estatura = driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/div[2]/input")
    dieta = driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[2]/input")
    motivo = driver.find_element_by_xpath('//*[@id="motivo"]')
    comentario = driver.find_element_by_xpath('//*[@id="comentario"]')
    send_button = driver.find_element_by_xpath("/html/body/div[2]/form/button")

    # Se elimina registro de cita asociado en el caso de que alguno de los casos sean fallidos.
    try: db.child(cedula).child('citas').remove()
    except: print("Error: se intentó eliminar un registro de cita no existente en la DB")

    # Esperar 2 segundos a que la Realtime Database de Firebase tenga tiempo de remover un registro.
    try: WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "none")))
    except TimeoutException: pass





# ------------------ CPNV12 -> CPNV21 ------------------ 
# Para estos casos de prueba, nos interesa que NO se guarden los registros en DB,
# porque cada uno cuenta con 1 valor de entrada no válido.

for testcase in testcases[2:]:
    tc += 1

    peso.send_keys(data[testcase[0]])
    estatura.send_keys(data[testcase[1]])
    dieta.send_keys(data[testcase[2]])
    motivo.send_keys(data[testcase[3]])
    comentario.send_keys(data[testcase[4]])
    send_button.click()

    # Esperar 2 segundos a que la Realtime Database de Firebase tenga tiempo de guardar un nuevo registro.
    try: WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "none")))
    except TimeoutException: pass
    
    try:
        # Si encuentra el botón de "Historial de cambios", quiere decir que volvimos a la pantalla de edición de HC
        driver.find_element_by_xpath("/html/body/div[2]/button[1]")
        if db.child(cedula).child('citas').get().val():
            print(f"Caso {tcl[tc]}: fallido - el registro de cita fue guardado en DB; y hubo cambio de vista")
            ftc += 1
        else:
            print(f"Caso {tcl[tc]}: exitoso - el registro de cita no fue guardado en DB; pero hubo cambio de vista")
            stc += 1

    except:
        # Si no encuentra el botón de "Historial de cambios", lanza una excepción y entramos en este except.
        # Quiere decir que aún estamos en la pantalla de creación de nueva cita.
        if db.child(cedula).child('citas').get().val():
            print(f"Caso {tcl[tc]}: fallido - el registro de cita fue guardado en DB")
            ftc += 1
        else:
            print(f"Caso {tcl[tc]}: exitoso")
            stc += 1

        peso.clear()
        estatura.clear()
        dieta.clear()
        motivo.clear()
        comentario.clear()

    try: driver.find_element_by_xpath("/html/body/div[2]/button[2]").click()
    except: pass

    peso = driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/div[1]/input")
    estatura = driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/div[2]/input")
    dieta = driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/div[2]/input")
    motivo = driver.find_element_by_xpath('//*[@id="motivo"]')
    comentario = driver.find_element_by_xpath('//*[@id="comentario"]')
    send_button = driver.find_element_by_xpath("/html/body/div[2]/form/button")

    # Se elimina registro de cita asociado en el caso de que alguno de los casos sean fallidos.
    try: db.child(cedula).child('citas').remove()
    except: print("Error: se intentó eliminar un registro de cita no existente en la DB")

    # Esperar 3 segundos a que la Realtime Database de Firebase tenga tiempo de remover un registro.
    try: WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "none")))
    except TimeoutException: pass


print(f"\nResultado de pruebas: {ftc} casos fallidos, {stc} casos exitosos")

driver.quit()
