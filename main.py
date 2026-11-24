import math
import dataset

dbase = dataset.connect("sqlite:///dbase.db")
tabla_productos = dbase["Productos"]


def formato_de_cadenas(cadena):
  return cadena.strip().title()


def agregar_producto():
  producto = formato_de_cadenas(input("\nProducto: "))
  categoria = formato_de_cadenas(input("\nCategoría: "))

  if not producto or not categoria:
    print("\nProducto y categoría son obligatorios.")
    return

  try:
    precio = float(input("\nPrecio: ").strip().replace(",", "."))
    stock = int(input("\nStock: ").strip())

    if not math.isfinite(precio) or precio < 0 or stock < 0:
      print("\nPrecio y stock deben ser valores válidos y no negativos.")
      return

    tabla_productos.insert({
        "Nombre": producto,
        "Categoria": categoria,
        "Precio": precio,
        "Stock": stock,
    })
    print(f"\nProducto agregado: {producto}")
  except ValueError:
    print("\nError: ingresá un precio numérico válido y un stock entero.")


def buscar_productos():
  producto_buscado = formato_de_cadenas(
      input("\nIngrese el nombre del producto a buscar: ")
  )

  if not producto_buscado:
    print("\nDebés ingresar un nombre para buscar.")
    return

  encontrados = [
      fila
      for fila in tabla_productos.all()
      if producto_buscado.lower() in str(fila.get("Nombre", "")).lower()
  ]

  if not encontrados:
    print(
        f"\nNo se encontraron productos que coincidan con {producto_buscado}."
    )
    return

  print("\n---- Resultados de búsqueda ----")
  for numero, producto in enumerate(encontrados, start=1):
    precio = float(producto.get("Precio") or 0)
    stock = int(producto.get("Stock") or 0)
    valor_neto = precio * stock
    print(
        f"N°:{numero} | Producto: {producto['Nombre']} | "
        f"Categoria: {producto['Categoria']} | Precio: {precio:.2f} | "
        f"Stock: {stock} | Valor neto: {valor_neto:.2f}"
    )


def eliminar_producto():
  producto_a_eliminar = formato_de_cadenas(
      input("\nIngrese el nombre del producto a eliminar: ")
  )

  if not producto_a_eliminar:
    print("\nDebés ingresar un nombre para eliminar.")
    return

  if tabla_productos.find_one(Nombre=producto_a_eliminar):
    tabla_productos.delete(Nombre=producto_a_eliminar)
    print(f"\nEl producto '{producto_a_eliminar}' fue eliminado exitosamente.")
  else:
    print(f"\nNo se encontró el producto '{producto_a_eliminar}'.")


def listar_productos():
  print("\n---- Lista de productos ----")
  productos = list(tabla_productos.all())

  if not productos:
    print("No hay productos cargados.")
    return

  for numero, producto in enumerate(productos, start=1):
    precio = float(producto.get("Precio") or 0)
    stock = int(producto.get("Stock") or 0)
    print(
        f"N°:{numero} | Producto: {producto['Nombre']} | "
        f"Categoria: {producto['Categoria']} | Precio: {precio:.2f} | "
        f"Stock: {stock}"
    )


while True:
  print("\n---- Menú ----")
  print(
      "\nA - Agregar Producto\nB - Buscar productos\nE - Eliminar"
      " producto\nL - Listar productos\nS - Salir"
  )

  opcion_menu = formato_de_cadenas(input("Ingrese su opción: ")).upper()

  match opcion_menu:
    case "A":
      agregar_producto()
    case "B":
      buscar_productos()
    case "E":
      eliminar_producto()
    case "L":
      listar_productos()
    case "S":
      print("\nGracias por utilizar el sistema, hasta luego")
      break
    case _:
      print("\nOpción incorrecta")