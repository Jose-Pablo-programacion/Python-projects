import json

class Producto:
    def __init__(self,nombre,precio,cantidad,categoria):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria
    def __str__(self):
        return f"{self.nombre} | ${self.precio} | Stock: {self.cantidad} | Categoria: {self.categoria}"
    
class Inventario:
    def __init__(self):
        self.productos = []
    
    def agregar_producto(self,producto):
        for i in self.productos:
            if i.nombre == producto.nombre:
                i.cantidad += producto.cantidad
                print("El producto ya existe, se sumo la cantidad")
                return
        self.productos.append(producto)
        print("Producto agregado correctamente")
    
    def mostrar_productos(self):
        if len(self.productos)==0:
            print("No hay productos para mostrar")
            return
        for i in self.productos:
            print(i)
        
    def buscar_producto(self,nombre):
        for i in self.productos:
            if i.nombre == nombre:
                print(i)
                return
        print("No se encontro ese producto.")

    def eliminar_producto(self,nombre):
        for i in self.productos:
            if i.nombre == nombre:
                self.productos.remove(i)
                print("Se elimino el producto correctamente")
                return
        print("No se encontro el producto")
    
    def modificar_precio(self,nombre,precio):
        for i in self.productos:
            if i.nombre == nombre:
                i.precio = precio
                print("El precio se modifico correctamente")
                print(i)
                return
        print("No se encontro ese producto")

    def vender_producto(self,nombre,cantidad):
        for i in self.productos:
            if i.nombre == nombre:
                restante = i.cantidad - cantidad
                total = i.precio * cantidad
                if restante > 0 and restante <= 5:
                    print("Venta realizada correctamente")
                    print("--STOCK BAJO!--")
                    self.guardar_historial_ventas(i.nombre,i.precio,cantidad,total)
                    i.cantidad = restante
                elif restante == 0:
                    i.cantidad = restante
                    print("Venta realizada correctamente")
                    print("--STOCK AGOTADO!--")
                    self.guardar_historial_ventas(i.nombre,i.precio,cantidad,total)
                elif restante < 0:
                    print("Stock insuficiente para realizar la venta completa")
                elif restante > 5:
                    print("Venta realizada correctamente")
                    self.guardar_historial_ventas(i.nombre,i.precio,cantidad,total)
                    i.cantidad = restante
                return
        print("No se encontro el producto")

    def mostrar_productos_por_categoria(self,categoria):
        encontrado = False
        for i in self.productos:
            if i.categoria == categoria:
                print(i)
                encontrado = True
        if not encontrado:
            print("No se encontro esa categoria")
    
    def guardar_datos_inventario(self):
        with open("inventario.json","w") as archivo:
            lista_productos = []
            for i in self.productos:
                lista_productos.append({"nombre": i.nombre,"precio": i.precio,"cantidad": i.cantidad,"categoria": i.categoria})
            json.dump(lista_productos,archivo,indent=4)
    
    def cargar_datos_inventario(self):
        with open("inventario.json","r") as archivo:
            datos_inventario = json.load(archivo)
            for datos_producto in datos_inventario:
                p = Producto(datos_producto["nombre"],datos_producto["precio"],datos_producto["cantidad"],datos_producto["categoria"])
                self.productos.append(p)
    
    def guardar_historial_ventas(self,nombre,precio,cantidad,total):
        try:
            with open("reporte de ventas.json","r") as archivo:
                ventas_historial = json.load(archivo)
        except FileNotFoundError:
            ventas_historial = []
        ventas_historial.append({"nombre": nombre,"precio": precio,"cantidad": cantidad,"total": total})
        with open("reporte de ventas.json","w") as archivo:
            json.dump(ventas_historial,archivo,indent=4)
    
    def mostrar_historial_ventas(self):
        try:
            with open("reporte de ventas.json","r") as archivo:
                datos_ventas = json.load(archivo)
        except FileNotFoundError:
            print("No hay ventas aun")
            return
        for i in datos_ventas:
            print(f"Nombre: {i['nombre']} | Precio: {i['precio']} | Cantidad: {i['cantidad']} | Total: {i['total']}")

    def mostrar_productos_mas_vendidos(self):
        try:
            with open("reporte de ventas.json","r") as archivo:
                datos_productos_vendidos = json.load(archivo)
        except FileNotFoundError:
            print("No hay ventas aun")
            return
        acumulado = {}
        for i in datos_productos_vendidos:
            nombre = i["nombre"]
            cantidad = i["cantidad"]
            if nombre in acumulado:
                acumulado[nombre] += cantidad
            else:
                acumulado[nombre] = cantidad
        ordenado = sorted(acumulado.items(),key = obtener_cantidad_vendida,reverse = True)
        top_3 = ordenado[:3]
        for nombre,cantidad in top_3:
            print(f"{nombre}: {cantidad} unidades vendidas")

def obtener_cantidad_vendida(tupla):
    return tupla[1]

         
         
inv = Inventario()

try:
    inv.cargar_datos_inventario()
except FileNotFoundError:
    pass

while True:
    print("--Inventario mercado--")
    print("1.Agregar producto")
    print("2.Mostrar productos")
    print("3.Buscar producto")
    print("4.Eliminar producto")
    print("5.Modificar precio")
    print("6.Vender producto")
    print("7.Buscar categoria")
    print("8.Mostrar historial de ventas")
    print("9.Mostrar productos mas vendidos")
    print("10.Salir")
    
    try:
        opcion = int(input("Elija una opcion: "))
    except ValueError:
        print("Opcion invalida")
        continue

    if opcion == 1:
        nombre = input("Escriba el nombre del producto: ")
        precio = float(input("Escriba el precio del producto: "))
        cantidad = int(input("Escriba la cantidad que hay del producto: "))
        categoria = input("Escriba la categoria a la que pertenece el producto: ")
        p = Producto(nombre,precio,cantidad,categoria)
        inv.agregar_producto(p)
    elif opcion == 2:
        inv.mostrar_productos()
    elif opcion == 3:
        nombre_producto_buscar = input("Escriba el nombre del producto que busca: ")
        inv.buscar_producto(nombre_producto_buscar)
    elif opcion == 4:
        nombre_producto_eliminar = input("Escriba el nombre del producto que desea eliminar: ")
        inv.eliminar_producto(nombre_producto_eliminar)
    elif opcion == 5:
        nombre_modificar_precio = input("Escriba el nombre del producto que desea modificar su precio: ")
        precio_modificar = int(input("Escriba el nuevo precio del producto: "))
        inv.modificar_precio(nombre_modificar_precio,precio_modificar)
    elif opcion == 6:
        nombre_producto_vender = input("Escriba el nombre del producto a vender: ")
        cantidad_a_vender = int(input("Escriba la cantidad que se vendera del producto: "))
        inv.vender_producto(nombre_producto_vender,cantidad_a_vender)
    elif opcion == 7:
        categoria_productos_mostrar = input("Escriba la categoria de productos que quiere ver: ")
        inv.mostrar_productos_por_categoria(categoria_productos_mostrar)
    elif opcion == 8:
        inv.mostrar_historial_ventas()
    elif opcion == 9:
        inv.mostrar_productos_mas_vendidos()
    elif opcion == 10:
        print("Saliendo del programa :)")
        inv.guardar_datos_inventario()
        break
    else:
        print("Opcion invalida")


