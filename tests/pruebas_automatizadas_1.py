import pyrebase
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

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

# Todos los representantes de la tabla de particiones de equivalencia funcionalidad 2.1 "Crear nueva historia clínica"
data = [
"Fernando Hernandez Rodriguez",
"8189831!!#%",
"25",
"-10",
"0.5",
"d!!ykjlagg",
"Av 5B Norte #21-23a",
"111112",
"1243582014",
"1243884",
"124358201421234",
"12435820142.235",
"qskklj!&%",
"EMSSANAR,IMBANACO",
"323123",
"!IMBAN4CO;34444_",
]

# Cada indice de cada caso de prueba representa las variables nombre completo,edad,direccion,cedula,ips (en ese orden y saltandonos 'sexo')
# Eg, el "0" en la posición 0 del primer caso representa el dato "Fernando Hernandez Rodriguez" de la variable "nombre completo".
testcases = [
[0,2,6,8,13],  #CPV01
[1,2,6,8,13],  #CPNV01
[0,3,6,8,13],  #CPNV02
[0,4,6,8,13],  #CPNV03
[0,5,6,8,13],  #CPNV04
[0,2,7,8,13],  #CPNV05
[0,2,6,9,13],  #CPNV06
[0,2,6,10,13], #CPNV07
[0,2,6,11,13], #CPNV08
[0,2,6,12,13], #CPNV09
[0,2,6,8,14],  #CPNV10
[0,2,6,8,15],  #CPNV11
]

# test case label
tcl = dict(zip(range(1,len(testcases)+1), ["CPV01", "CPNV01", "CPNV02", "CPNV03", "CPNV04", "CPNV05", "CPNV06", "CPNV07", "CPNV08", "CPNV09", "CPNV10", "CPNV11"]))

driver = Firefox()
driver.get("http://181.62.170.37:8000/")

# Hacemos login
driver.find_element_by_name('email').send_keys("gargal@gmail.com")
driver.find_element_by_name('pass').send_keys("test123") 
driver.find_element_by_xpath("/html/body/div/div/form/button").click()

# Vamos a vista de creación de nueva HC
driver.find_element_by_name("newHC").click()

nombre = driver.find_element_by_name("nombre")
edad = driver.find_element_by_name("edad")
direccion = driver.find_element_by_name("direccion")
cedula = driver.find_element_by_name("cedula")
ips = driver.find_element_by_name("ips")

create_button = driver.find_element_by_xpath("/html/body/div[2]/form/button")

# successful test cases
stc = 0

# failed test cases
ftc = 0

# test case number
tc = 1



# ------------------ CPV01 ------------------ 
# Para este caso, queremos probar que los valores de entrada (que son validos) son guardados correctamente en la DB.

nombre.send_keys(data[testcases[0][0]])
edad.send_keys(data[testcases[0][1]])
direccion.send_keys(data[testcases[0][2]])
cedula.send_keys(data[testcases[0][3]])
ips.send_keys(data[testcases[0][4]])
create_button.click()

# Esperar 2 segundos a que la Realtime Database de Firebase tenga tiempo de guardar un nuevo registro.
try: WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, "none"))) # Nunca encuentra el elemento "none", siempre espera 2 segundos.
except TimeoutException: pass

try:
    # Si encuentra el campo de "cedula_search", quiere decir que volvimos a la pantalla de inicio del sistema.
    driver.find_element_by_name("cedula_search")

    # Verificar que el registro SI fue guardado en la DB.
    try:
        if db.child(data[testcases[0][3]]).get().val():
            print(f"Caso {tcl[tc]}: exitoso")
            stc += 1
        else:
            print(f"Caso {tcl[tc]}: fallido")
            ftc += 1
    except:
        print(f"Error: hubo un problema con la petición de la cédula <{testcases[0][3]}>; caso {tcl[tc]} fallido")
        ftc += 1

except:
    # Si no encuentra el campo de "cedula_search", lanza una excepción y entramos en este except.
    # Quiere decir que aún estamos en la pantalla de creación de nueva HC.

    # Verificar que el registro SI fue guardado en la DB.
    try:
        if db.child(data[testcases[0][3]]).get().val():
            print(f"Caso {tcl[tc]}: exitoso - el registro fue guardado en DB; pero no hubo cambio de vista")
            stc += 1
        else:
            print(f"Caso {tcl[tc]}: fallido - el registro no fue guardado en DB; y no hubo cambio de vista")
            ftc += 1
    except:
        print(f"Error: hubo un problema con la petición de la cédula <{testcases[0][3]}>; caso {tcl[tc]} fallido")
        ftc += 1

    nombre.clear()
    edad.clear()
    direccion.clear()
    cedula.clear()
    ips.clear()

try: driver.find_element_by_name("newHC").click()
except: pass

nombre = driver.find_element_by_name("nombre")
edad = driver.find_element_by_name("edad")
direccion = driver.find_element_by_name("direccion")
cedula = driver.find_element_by_name("cedula")
ips = driver.find_element_by_name("ips")
create_button = driver.find_element_by_xpath("/html/body/div[2]/form/button")

# Se elimina el registro asociado a la cédula data[8], porque interfiere en el funcionamiento del resto de casos de prueba.
try: db.child(data[8]).remove()
except: print("Error: se intentó eliminar un registro no existente en la DB")

# Se esperan 2 segundos a que el registro anterior se borre en DB.
try: WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, "none")))
except TimeoutException: pass





# ------------------ CPNV01 -> CPNV11 ------------------ 
# Para estos casos de prueba, nos interesa que NO se guarden los registros en DB,
# porque cada uno cuenta con 1 valor de entrada no válido.

for testcase in testcases[1:]:
    tc += 1

    nombre.send_keys(data[testcase[0]])
    edad.send_keys(data[testcase[1]])
    direccion.send_keys(data[testcase[2]])
    cedula.send_keys(data[testcase[3]])
    ips.send_keys(data[testcase[4]])
    create_button.click()

    # Esperar 2 segundos a que la Realtime Database de Firebase tenga tiempo de guardar un nuevo registro.
    try: WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, "none")))
    except TimeoutException: pass

    try:
        driver.find_element_by_name("cedula_search")
        try:
            if not db.child(data[testcase[3]]).get().val():
                print(f"Caso {tcl[tc]}: exitoso - el registro no fue guardado en DB; aunque hubo cambio de vista")
                stc += 1
            else:
                print(f"Caso {tcl[tc]}: fallido - el registro fue guardado en DB; y hubo cambio de vista")
                ftc += 1
        except:
            print(f"Error: hubo un problema con la petición de la cédula <{data[testcase[3]]}>; No se guardó ningún registro en DB\nCaso {tcl[tc]} exitoso")
            stc += 1

    except:
        try:
            if not db.child(data[testcase[3]]).get().val():
                print(f"Caso {tcl[tc]}: exitoso")
                stc += 1
            else:
                print(f"Caso {tcl[tc]}: fallido - el registro fue guardado en DB")
                ftc += 1
        except:
            print(f"Error: hubo un problema con la petición de la cédula <{data[testcase[3]]}>; No se guardó ningún registro en DB\nCaso {tcl[tc]} exitoso")
            stc += 1

        nombre.clear()
        edad.clear()
        direccion.clear()
        cedula.clear()
        ips.clear()

    try: driver.find_element_by_name("newHC").click()
    except: pass

    nombre = driver.find_element_by_name("nombre")
    edad = driver.find_element_by_name("edad")
    direccion = driver.find_element_by_name("direccion")
    cedula = driver.find_element_by_name("cedula")
    ips = driver.find_element_by_name("ips")
    create_button = driver.find_element_by_xpath("/html/body/div[2]/form/button")

    # Se elimina registro asociado a data[8] en el caso de que alguno de los casos sean fallidos.
    try: db.child(data[8]).remove()
    except: print("Error: se intentó eliminar un registro no existente en la DB")

print(f"\nResultado de pruebas: {ftc} casos fallidos, {stc} casos exitosos")

driver.quit()
