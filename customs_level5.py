#creando funcion, a partir de declararla con def



def saludar():
    print("Hola Juan como andas")
    







#funcion con parametros, inputs que uno asigna como condiciones o settings a una funcion
#notese la capacidad e sintesis al anidar en una misma funcion los diferentes
#parametros que daran lugar a diferentes resultados en funcion de los valores de entrada
#que asignemos a los parametros variables de la funcion

'''

def saludar(nombre,sexo):
    if (sexo == "mujer"):
        adj = "lady"
    elif (sexo == "hombre"):
        adj = "mister"
    else:
        adj = "como quiera que me consideres"
    
    print(f'que tal soy {nombre}, siendo {adj} como me siento hoy?')

saludar("juan","hombre")
saludar("carolina","mujer")
saludar("foxy","indefinido")

'''



#en esta funcion se busca crear un sistema de generacion de password, a partir de
# concatenar de forma entreverada, str y int, donde hay una cadena de caracteres str
# y se asigna que a los valores int ingresados en la funcion, se conviertan en str,
# y que los parametros de la password incluyan valores int que serviran como index de la cadena str
# mas los valores int ingresados al final duplicados pero como str, no como int, ademas
# del valor ingresado int, al especificar [0] estamos determinando que solamente va a considerar
#como valor ingresado el primer caracter del mismo, en caso de que tenga mas de uno



def creando_password(number):
    chars = "abcdefghijk"
    num_int = str(number)
    number = int(num_int[0])
    c1 = number -2
    c2 = number
    c3 = number -5
    c4 = number +2
    password = f'{chars[c1]}{chars[c2]}{chars[c3]}{num_int * 2}{chars[c4]}'
    return password,number                     #el return lo que hace es conservar el resultado de la fucion que en este
                            #caso es la password, pero sin reflejarla en consola, es decir esto es un proceso backend
                            #donde el resultado de esa funcion, por ejemplo, podria servir como valor para otra variable o fucion
                            #retornar valores de la funcion permite alojar el dato para ser reutilizado
                            #el return es clave para hacer efectiva la continuidad del valor de una funcion
                            #y su consiguiente uso en otras funciones o variables, de otro modo si queremos recuperar el resultado
                            #de una funcion si haber hecho el return, se recupera un vacio o None




password,number = creando_password(2)
message1 = f'La password ahora es: {password}'
message2 = f'Habiendo sido el caracter ingresado {number}'
print(message1)
print(message2)



'''
#my first own function using int

def definir_mayor_menor(x,y):
   if (x + y > 4):
      result = "ok"
   elif (x + y < 3):
      result = "not ok"
   elif (x + y == 4):
      result = "quiza no se"
   else:
      result = "ni idea entonces"

   print(f'la verdad que esto {result}')

definir_mayor_menor(1,3)

'''

#creando funcion que intercale valores de diferentes strings y se hagan request con valores
#de numeros convertidos en str que actuen como index para obtener caracteres letras de los strings

'''

def function_testing_entreverar(testing):
    cadena1 = "holamarcelo,agachateyconocelo"
    cadena2 = "quemarcelo"
    cadena3 = [1,6,8,5,3,9,70,96,32]
    number_index = str(testing)
    testing = int(number_index[0])
    char1 = testing + 2
    char2 = testing + 1
    char3 = testing + 3
    cadena_formada = f'{cadena3[char2]}{cadena1[char1]}{cadena3[char1]}{cadena2[char2]}{cadena3[char3]}'
    return cadena_formada
    


cadena_formada = function_testing_entreverar(5)
print(f'tu password generada satisfactoriamente es: {cadena_formada}')

'''

'''

def prueba():
    test_list = {
        "x" : 'juan',
        "y" : 'carlos',
        "z" : 'horacio'
    }
    for t_list in test_list.items():
        value = t_list[0]
        if value == 'carlos':
            continue
    testing = f'el nombre elegido es {t_list}'
    return testing

testing = prueba()
#print(testing)

'''


'''          GEOPANDAS FUNCTION

# function with geopandas

import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame

geofile = gpd.read_file('F:/CFI 2025/Proyecto Hualilán Acceso.shp')

#print(geofile)


def projection():
    if geofile.crs.to_epsg() == 3857:
       result = (geofile.to_crs(epsg=4326)).to_file('F:/CFI 2025/Proyecto Hualilán Acceso_5348.shp')
       print(f'{result}')
    
    else:
        result = print("not exported") 

    output = result
    return output

give = projection()
print(give)

'''

# parametro args (*) con el unpacking/uncompress - lo interesante de esta funcion parametro es que hace una
# suerte de conversion "on the fly" en lista de elementos pero no es una lista en si misma por lo tanto es requisito 
# tanto indicar que es una lista encerrando entre corchetes el args+nombre lista, asi como si corremos la funcion type
# obtendremos un error dado que no se interpreta como lista original

#sumando valores de una lista

'''

def adicion(personaje1,personaje2,*elementos):
    return f'{personaje1} {personaje2} esto es {sum(elementos)}'

producto = adicion("carlitos","marcela",1,5,8)
print(producto)

'''

#funciona como un loop al infinito, todo elemento ingresado en la posicion que correponda al la lista con paramentro
# args, sera considerado parte del argumento en cuestion


'''


def adicion2(elementos):
    print(type(*elementos))
    return sum([*elementos])
   
producto2 = adicion2([3,6,8])

print(producto2)


'''


'''

def adicion(numeros_listados):
    numeros_adicionados = 0
    for number in numeros_listados:
            numeros_adicionados = numeros_adicionados + number
    #print(type(numeros_listados))
    return numeros_adicionados

output = adicion([2,4,7])
print(output)

'''

'''

def adicion2(number):
    return sum([*number])

lista_args = adicion2([1,6,9])
args_sentence = f'{lista_args} es el producto de la suma de los parametros' 
print(args_sentence)

'''


#declarando forzadamente argumentos al desempaquetar para skipear el idex automatico de los valores



'''

def frase_test(dia,mes,año):
    
    return f'hoy es {dia} de {mes} del año {año}'


output = frase_test(dia=1,año=2025,mes="Marzo")

print(output)

'''

#declarando forzadamente argumentos pero como valor predefinido, el cual para desempaquetar no hace falta
#definir nuevamente al hacer return de funcion, pero se puede redefinir o dejar el valor predefinido por defecto


'''

def frase_test2(animal,color,lugar="disney"):

    return f'{animal} y {color} en {lugar}'

output2 = frase_test2("perro","azul",lugar="narnia")
print(output2) 

'''

'''name2 = "marcelo"



def test3():
    global name2
       
    print(f'que {name2}?, agachate y conocelo, ahh re que no era asi el chiste')
    return name2

output = test3() 
print(output)

'''

'''

listado = [1,5,2,3,7,6]

output = listado.sort()
print(output)

'''