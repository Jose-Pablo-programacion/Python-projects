#Primer proyecto

#Proyecto: Agenda de contactos 
#Un programa que corra en la terminal y permita:

#1.Agregar un contacto (nombre y teléfono)
#2.Ver todos los contactos
#3.Buscar un contacto por nombre
#4.Salir
#Los contactos se guardan en un archivo contactos.txt para que no se pierdan al cerrar el programa.


def agregarContacto():
     
    nombre = input("Dame tu nombre: ")
    telefono = int(input("Dame tu telefono: "))

    with open ("contactos.txt","a") as archivo: 
            archivo.write(f"Nombre: {nombre}\n")
            archivo.write(f"Telefono: {telefono}\n\n") 


def verContactos():
     with open ("contactos.txt","r") as archivo:
          contactos = archivo.read()
          print(contactos)

def buscarContacto():
     while True:
          
        nombre = input("Dame nombre del contacto que estas buscando:")

        with open ("contactos.txt","r") as archivo:
            contactos = archivo.readlines() # readline = lee el archivo y guarda cada linea como elemento de una lista

        encontrado =False
    
        for i, contacto in enumerate(contactos):
            if nombre in contacto:
                print(contactos[i].strip())
                print(contactos[i+1])
                encontrado = True
            
        if encontrado:
             break
        else:
             print("Ese nombre no coincide con algún contacto, intenta de nuevo")
          

while True:
    print("----Agenda de contactos----")
    print("1.Agregar un contacto (nombre y teléfono)")
    print("2.Ver todos los contactos")
    print("3.Buscar un contacto por nombre")
    print("4.Salir")

    opcion = input("Elija la opcion que desea:")

    if opcion == "1":
        agregarContacto()

    if opcion == "2":
         verContactos()
    
    if opcion == "3":
         buscarContacto()
    
    if opcion == "4":
         print("Saliendo del programa,adios :)")
         break
        


        

    





        