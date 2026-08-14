import json
import tkinter as tk
from tkinter import messagebox

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

#***************************************************************************************

inv = Inventario()

try:
    inv.cargar_datos_inventario()
except FileNotFoundError:
    pass


ventana = tk.Tk()
ventana.state("zoomed")

#***************************************************************************************

def agregar_productos_interfaz():
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.state("zoomed")
    ventana_agregar.title("Agregar producto")
    
    tk.Label(ventana_agregar,text="Nombre: ").pack()
    entrada_nombre = tk.Entry(ventana_agregar)
    entrada_nombre.pack()
    
    tk.Label(ventana_agregar,text="Precio: ").pack()
    entrada_precio = tk.Entry(ventana_agregar)
    entrada_precio.pack()
    
    tk.Label(ventana_agregar,text="Cantidad: ").pack()
    entrada_cantidad = tk.Entry(ventana_agregar)
    entrada_cantidad.pack()
    
    tk.Label(ventana_agregar,text="Categoria: ").pack()
    entrada_categoria = tk.Entry(ventana_agregar)
    entrada_categoria.pack()
    
    def confirmar():
        nombre = entrada_nombre.get()
        precio = float(entrada_precio.get())
        cantidad = int(entrada_cantidad.get())
        categoria = entrada_categoria.get()
        p = Producto(nombre,precio,cantidad,categoria)
        inv.agregar_producto(p)
        ventana_agregar.destroy()
    
    tk.Button(ventana_agregar,text="Confirmar",command=confirmar).pack()

#***************************************************************************************

def mostrar_productos_interfaz():
    ventana_mostrar = tk.Toplevel(ventana)
    ventana_mostrar.state("zoomed")
    ventana_mostrar.title("Productos")
    
    texto = tk.Text(ventana_mostrar)
    texto.pack()
    
    for p in inv.productos:
        texto.insert(tk.END,str(p) + "\n")

#***************************************************************************************

def buscar_productos_interfaz():
    ventana_buscar = tk.Toplevel(ventana)
    ventana_buscar.state("zoomed")
    ventana_buscar.title("Busqueda de producto")

    tk.Label(ventana_buscar,text="Nombre: ").pack()
    entrada_nombre = tk.Entry(ventana_buscar)
    entrada_nombre.pack()

    def confirmar_busqueda():
        nombre = entrada_nombre.get()
        ventana_buscar.destroy()
        ventana_buscar_resultado = tk.Toplevel(ventana)
        ventana_buscar_resultado.state("zoomed")
        ventana_buscar_resultado.title("Resultado de busqueda")
        texto = tk.Text(ventana_buscar_resultado)
        texto.pack()
        for p in inv.productos:
            if nombre == p.nombre:
                texto.insert(tk.END,str(p) + "\n")
                return
        texto.insert(tk.END,"No se encontro ese producto")
        
    tk.Button(ventana_buscar,text="Confirmar",command=confirmar_busqueda).pack()

#***************************************************************************************

def eliminar_producto_interfaz():
    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.state("zoomed")
    ventana_eliminar.title("Eliminar producto")

    tk.Label(ventana_eliminar,text="Nombre: ").pack()
    entrada_nombre = tk.Entry(ventana_eliminar)
    entrada_nombre.pack()

    def confirmar_busqueda():
        nombre = entrada_nombre.get()
        ventana_eliminar.destroy()
        ventana_eliminar_resultado = tk.Toplevel(ventana)
        ventana_eliminar_resultado.state("zoomed")
        ventana_eliminar_resultado.title("Resultado de busqueda")
        texto = tk.Text(ventana_eliminar_resultado)
        texto.pack()
        for p in inv.productos:
            if nombre == p.nombre:
                inv.eliminar_producto(nombre)
                texto.insert(tk.END,"Se elimino el producto correctamente")
                return
        texto.insert(tk.END,"No se encontro ese producto")
        
    tk.Button(ventana_eliminar,text="Confirmar",command=confirmar_busqueda).pack()

#***************************************************************************************

def modificar_precio_interfaz():
    ventana_modificar_precio = tk.Toplevel(ventana)
    ventana_modificar_precio.state("zoomed")
    ventana_modificar_precio.title("Modificar precio de producto")
    
    tk.Label(ventana_modificar_precio,text="Nombre: ").pack()
    entrada_nombre = tk.Entry(ventana_modificar_precio)
    entrada_nombre.pack()

    tk.Label(ventana_modificar_precio,text="Precio: ").pack()
    entrada_precio = tk.Entry(ventana_modificar_precio)
    entrada_precio.pack()

    def confirmar():
        nombre = entrada_nombre.get()
        precio = float(entrada_precio.get())
        ventana_modificar_precio.destroy()

        ventana_resultado = tk.Toplevel(ventana)
        ventana_resultado.state("zoomed")
        ventana_resultado.title("Resultado")
        texto = tk.Text(ventana_resultado)
        texto.pack()

        for p in inv.productos:
            if nombre == p.nombre:
                inv.modificar_precio(nombre,precio)
                texto.insert(tk.END,"Se modifico el precio correctamente")
                return
        texto.insert(tk.END,"No se encontro ese producto")
    
    tk.Button(ventana_modificar_precio,text="Confirmar",command=confirmar).pack()

#***************************************************************************************

def vender_producto_interfaz():
    ventana_vender_producto = tk.Toplevel(ventana)
    ventana_vender_producto.state("zoomed")
    ventana_vender_producto.title("Vender producto")
    
    tk.Label(ventana_vender_producto,text="Nombre: ").pack()
    entrada_nombre = tk.Entry(ventana_vender_producto)
    entrada_nombre.pack()

    tk.Label(ventana_vender_producto,text="Cantidad: ").pack()
    entrada_cantidad = tk.Entry(ventana_vender_producto)
    entrada_cantidad.pack()

    def confirmar():
        nombre = entrada_nombre.get()
        cantidad = int(entrada_cantidad.get())
        ventana_vender_producto.destroy()

        ventana_resultado = tk.Toplevel(ventana)
        ventana_resultado.state("zoomed")
        ventana_resultado.title("Resultado")
        texto = tk.Text(ventana_resultado)
        texto.pack()

        for p in inv.productos:
            if nombre == p.nombre:
                restante = p.cantidad -cantidad
                inv.vender_producto(nombre,cantidad)

                if restante > 0 and restante <= 5:
                    texto.insert(tk.END,"Venta realizada correctamente")
                    texto.insert(tk.END,"--STOCK BAJO!--")
                elif restante == 0:
                    texto.insert(tk.END,"Venta realizada correctamente")
                    texto.insert(tk.END,"--STOCK AGOTADO!--")
                elif restante < 0:
                    texto.insert(tk.END,"Stock insuficiente para realizar la venta completa")
                else:
                    texto.insert(tk.END,"Venta realizada correctamente")
                return
        texto.insert(tk.END,"No se encontro ese producto")
    
    tk.Button(ventana_vender_producto,text="Confirmar",command=confirmar).pack()

#***************************************************************************************

def productos_por_categoria_interfaz():
    ventana_categoria_productos = tk.Toplevel(ventana)
    ventana_categoria_productos.state("zoomed")
    ventana_categoria_productos.title("Buscar por categoria")

    tk.Label(ventana_categoria_productos,text="Categoria: ").pack()
    entrada_categoria = tk.Entry(ventana_categoria_productos)
    entrada_categoria.pack()

    def confirmar():
        categoria = entrada_categoria.get()
        ventana_categoria_productos.destroy()

        ventana_resultado = tk.Toplevel(ventana)
        ventana_resultado.state("zoomed")
        ventana_resultado.title("Resultado")
        texto = tk.Text(ventana_resultado)
        texto.pack()
        encontrado = False

        for p in inv.productos:
            if p.categoria == categoria:
                texto.insert(tk.END,f"{p}\n")
                encontrado = True
        if not encontrado:
            texto.insert(tk.END,"No se encontro esa categoria")
    
    tk.Button(ventana_categoria_productos,text="Confirmar",command=confirmar).pack()

#***************************************************************************************

def mostrar_historial_ventas_interfaz():
    ventana_mostrar_historial_ventas = tk.Toplevel(ventana)
    ventana_mostrar_historial_ventas.state("zoomed")
    ventana_mostrar_historial_ventas.title("Historial de ventas")
    
    texto = tk.Text(ventana_mostrar_historial_ventas)
    texto.pack()

    try:
        with open("reporte de ventas.json","r") as archivo:
            datos_ventas = json.load(archivo)
    except FileNotFoundError:
        texto.insert(tk.END,"No hay ventas aun")
        return
    for i in datos_ventas:
        texto.insert(tk.END,f"Nombre: {i['nombre']} | Precio: {i['precio']} | Cantidad: {i['cantidad']} | Total: {i['total']}\n")
    
#***************************************************************************************

def mostrar_productos_mas_vendidos_interfaz():
    ventana_mostrar_historial_ventas = tk.Toplevel(ventana)
    ventana_mostrar_historial_ventas.state("zoomed")
    ventana_mostrar_historial_ventas.title("Historial de ventas")
    
    texto = tk.Text(ventana_mostrar_historial_ventas)
    texto.pack()
    
    try:
        with open("reporte de ventas.json","r") as archivo:
            datos_productos_vendidos = json.load(archivo)
    except FileNotFoundError:
        texto.insert(tk.END,"No hay ventas aun")
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
        texto.insert(tk.END,f"{nombre}: {cantidad} unidades vendidas\n")

def obtener_cantidad_vendida(tupla):
    return tupla[1]

#***************************************************************************************

def salir_interfaz():
    inv.guardar_datos_inventario()
    ventana.destroy()

#***************************************************************************************

ventana.title("--Inventario Mercado--")

boton_agregar = tk.Button(ventana,text = "Agregar producto",command = agregar_productos_interfaz)
boton_agregar.pack(pady=35)

boton_mostrar = tk.Button(ventana,text = "Mostrar productos",command = mostrar_productos_interfaz)
boton_mostrar.pack(pady=35)

boton_buscar = tk.Button(ventana,text = "Buscar producto",command = buscar_productos_interfaz)
boton_buscar.pack(pady=35)

boton_eliminar = tk.Button(ventana,text = "Eliminar producto",command = eliminar_producto_interfaz)
boton_eliminar.pack(pady=35)

boton_modificar_precio = tk.Button(ventana,text = "Modificar precio",command = modificar_precio_interfaz)
boton_modificar_precio.pack(pady=35)

boton_vender = tk.Button(ventana,text = "Vender producto",command = vender_producto_interfaz)
boton_vender.pack(pady=35)

boton_categoria = tk.Button(ventana,text = "Buscar categoria",command = productos_por_categoria_interfaz)
boton_categoria.pack(pady=35)

boton_historial_ventas = tk.Button(ventana,text = "Mostrar historial de ventas",command = mostrar_historial_ventas_interfaz)
boton_historial_ventas.pack(pady=35)

boton_mas_vendidos = tk.Button(ventana,text = "Mostrar productos mas vendidos",command = mostrar_productos_mas_vendidos_interfaz)
boton_mas_vendidos.pack(pady=35)

ventana.protocol("WM_DELETE_WINDOW",salir_interfaz)
boton_salir = tk.Button(ventana,text = "Salir",command = salir_interfaz)
boton_salir.pack(pady=35)

ventana.mainloop()
