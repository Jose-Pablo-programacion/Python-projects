#Proyecto 2: Sistema de gestión de biblioteca
#
#Un programa que permita:
#1. Agregar libro (título, autor, año)
#2. Ver todos los libros
#3. Buscar libro por título o autor
#4. Marcar como leído/no leído
#5. Eliminar libro
#6. Salir
#
#Los libros se guardan en un archivo libros.txt y usaremos una clase Libro

class Libro:
    def __init__(self,titulo,autor,año):
        self.titulo = titulo
        self.autor = autor
        self.año = año
        self.leido = False

    def mostrar(self):
        print(f"Titulo: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Año: {self.año}")
        print(f"Leido: {'Si' if self.leido else 'No'}")


def agregar_libro():
    titulo = input("Titulo: ")
    autor = input("Autor: ")
    año = int(input("Año:"))
    leido = False

    with open ("libros.txt","a") as archivo: 
            archivo.write(f"Titulo: {titulo}\n")
            archivo.write(f"Autor: {autor}\n") 
            archivo.write(f"Año: {año}\n")
            archivo.write(f"Leido: No\n\n") 

def ver_libro():
     with open ("libros.txt","r") as archivo:
          libros = archivo.read()
          print(libros)
    

def buscar_libro():
    while True:
         nombre_libro = input("Dame el nombre del libro que estas buscando(escribe 'salir' para volver al menu):")
         if nombre_libro.lower() =="salir":
             break
         with open ("libros.txt","r") as archivo:
            libros = archivo.readlines()

         libro_encontrado = False

         for i,libro in enumerate(libros):
              if f"Titulo: {nombre_libro}" in libro:
                   print(libros[i].strip())
                   print(libros[i+1].strip())
                   print(libros[i+2].strip())
                   print(libros[i+3].strip())
                   libro_encontrado = True


def marcar_leido():
     nombre_libro = input("Dame el nombre del libro que quieres marcar como leido: ")

     with open ("libros.txt","r") as archivo:
      libros = archivo.read()

     if f"Titulo: {nombre_libro}" in libros:
        libros = libros.replace(f"Leido: No","Leido: Si",1)
        with open ("libros.txt","w") as archivo:
            archivo.write(libros)
        print("El libro se marco como leido")
     else:
        print("No se encontro el libro")


def eliminar_libro():
    nombre_libro = input("Dame el nombre del libro que quieres eliminar: ")

    with open ("libros.txt","r") as archivo:
        libros = archivo.read()
     
    if f"Titulo: {nombre_libro}" in libros:
        libros = libros.split("\n\n")
        libros_filtrados= []   
        for libro in libros:
          if nombre_libro not in libro:
               libros_filtrados.append(libro)
        with open ("libros.txt","w") as archivo:
            archivo.write("\n\n".join(libros_filtrados))
        print(f"Se elimino el libro {nombre_libro}")
    else:
        print(f"No se encontro el libro {nombre_libro}")
                            
while True:
    print("----Sistema de gestion de biblioteca----")
    print("1.Agregar libro (titulo, autor, año)")
    print("2.Ver todos los libros")
    print("3.Buscar libro por titulo")
    print("4.Marcar como leido/no leído")
    print("5.Eliminar libro")
    print("6.Salir")

    opcion = input("Elija la opcion que desea:")

    if opcion == "1":
        agregar_libro()
        

    if opcion == "2":
         ver_libro()
         
    
    if opcion == "3":
         buscar_libro()
         
    
    if opcion == "4":
         marcar_leido()
         
    
    if opcion == "5":
         eliminar_libro()
         

    if opcion == "6":
         print("Saliendo del programa,adios :)")
         break
    
