import datetime
from typing import List


IVA_TASA = 0.16
CARGO_ENVIO = 50.0
ANCHO_TICKET = 40

class Platillo:
    def __init__(self, nombre: str, precio: float, categoria: str):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def __str__(self) -> str:
        return f"{self.nombre.ljust(25)} ${self.precio:>10.2f}"

class Orden:
    def __init__(self, tipo_servicio: int, identificador: str):
        self.tipo_servicio = tipo_servicio  
        self.identificador = identificador
        self.items: List[Platillo] = []
        self.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def agregar_item(self, platillo: Platillo):
        self.items.append(platillo)

    def calcular_totales(self):
        subtotal = sum(p.precio for p in self.items)
        impuesto = subtotal * IVA_TASA
        envio = CARGO_ENVIO if self.tipo_servicio == 2 else 0.0
        total = subtotal + impuesto + envio
        return subtotal, impuesto, envio, total

    def generar_cuerpo_ticket(self) -> str:
        subtotal, impuesto, envio, total = self.calcular_totales()
        tipo_str = "SERVICIO EN MESA" if self.tipo_servicio == 1 else "PEDIDO A DOMICILIO"
        id_label = "Mesa #" if self.tipo_servicio == 1 else "Dir:"

        t = []
        t.append("=" * ANCHO_TICKET)
        t.append(f"{'RESTAURANTE EL CHEF':^40}")
        t.append(f"{tipo_str:^40}")
        t.append(f"Fecha: {self.fecha}")
        t.append(f"{id_label} {self.identificador}")
        t.append("=" * ANCHO_TICKET)
        
        for item in self.items:
            t.append(str(item))
            
        t.append("-" * ANCHO_TICKET)
        t.append(f"SUBTOTAL:          ${subtotal:>10.2f}")
        t.append(f"IVA ({IVA_TASA*100:.0f}%):         ${impuesto:>10.2f}")
        
        if self.tipo_servicio == 2:
            t.append(f"CARGO ENVÍO:       ${envio:>10.2f}")
            
        t.append("=" * ANCHO_TICKET)
        t.append(f"TOTAL A PAGAR:     ${total:>10.2f}")
        t.append("=" * ANCHO_TICKET)
        t.append(f"{'¡GRACIAS POR SU PREFERENCIA!':^40}")
        
        return "\n".join(t)

def guardar_ticket_en_disco(contenido: str):
    """Guarda el ticket en un archivo para auditoría."""
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    nombre_archivo = f"ticket_{timestamp}.txt"
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"\n Ticket guardado como: {nombre_archivo}")
    except IOError as e:
        print(f" Error al guardar archivo: {e}")

def mostrar_menu_platos(lista_platos: List[Platillo]):
    print(f"\n{'--- MENÚ DEL DÍA ---':^40}")
    for i, p in enumerate(lista_platos, 1):
        print(f"{i}. {p}")
    print("-" * ANCHO_TICKET)

def app_restaurante():
    
    menu_del_dia = [
        Platillo("Corte New York", 450.0, "Comida"),
        Platillo("Pasta Alfredo", 180.0, "Comida"),
        Platillo("Ensalada Griega", 120.0, "Entrada"),
        Platillo("Vino Tinto Copa", 95.0, "Bebida"),
        Platillo("Refresco Mora", 35.0, "Bebida")
    ]

    print("=== SISTEMA DE GESTIÓN DE PEDIDOS ===")
    print("1. Mesa (Local)\n2. Pedido (Domicilio)")
    
    try:
        opc = int(input("Seleccione fase (1/2): "))
        if opc not in [1, 2]:
            print(" Opción no válida.")
            return

        identificador = input("Número de mesa: ") if opc == 1 else input("Dirección de entrega: ")
        nueva_orden = Orden(opc, identificador)

       
        mostrar_menu_platos(menu_del_dia)
        while True:
            escoger = input("Seleccione número de plato (o 'f' para cobrar): ")
            if escoger.lower() == 'f':
                break
            
            idx = int(escoger) - 1
            if 0 <= idx < len(menu_del_dia):
                nueva_orden.agregar_item(menu_del_dia[idx])
                print(f"   + {menu_del_dia[idx].nombre}")
            else:
                print(" Número de plato no existe.")

        if not nueva_orden.items:
            print(" No se agregaron platos. Operación cancelada.")
            return

        resultado_ticket = nueva_orden.generar_cuerpo_ticket()
        print(resultado_ticket)
        
   
        guardar_ticket_en_disco(resultado_ticket)

       
        if opc == 1:
            dividir = input("\n¿Desea dividir la cuenta? (s/n): ")
            if dividir.lower() == 's':
                pers = int(input("¿Entre cuántas personas?: "))
                _, _, _, total_final = nueva_orden.calcular_totales()
                print(f"💰 Cada persona debe pagar: ${total_final/pers:.2f}")

    except ValueError:
        print(" Error: Entrada de datos inválida.")

if __name__ == "__main__":
    app_restaurante()