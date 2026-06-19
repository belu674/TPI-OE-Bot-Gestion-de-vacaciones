import csv
import os

ARCH_EMPLEADOS = "empleados.csv"
ARCH_SOLICITUDES = "solicitudes.csv"

# =====================================================================
# FUNCIONES DE PERSISTENCIA (BASE DE DATOS EN EXCEL/CSV)
# =====================================================================
def cargar_empleados():
    """Si el archivo no existiera por algún motivo, con esta función se crearía"""
    if not os.path.exists(ARCH_EMPLEADOS):
        with open(ARCH_EMPLEADOS, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["legajo", "nombre", "apellido", "rol", "dias_disponibles"])
            writer.writerow(["1024", "Belén", "Molina", "empleado", "14"])
            writer.writerow(["1025", "Pablo", "Gomez", "empleado", "10"])
            writer.writerow(["1026", "Maria", "Ruiz", "empleado", "6"])
            writer.writerow(["2048", "Carlos", "Diaz", "organización", "0"])
    
    """Lee el archivo de empleados simulando la BD de RRHH y los guarda en un diccionario"""            
    usuarios = {}
    with open(ARCH_EMPLEADOS, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            usuarios[int(fila["legajo"])] = {
                "nombre": fila["nombre"],
                "apellido": fila["apellido"],
                "rol": fila["rol"],
                "dias_disponibles": int(fila["dias_disponibles"])
            }
    return usuarios

def guardar_empleados(usuarios):
    """Guarda los saldos actualizados de vacaciones."""
    with open(ARCH_EMPLEADOS, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["legajo", "nombre", "apellido", "rol", "dias_disponibles"])
        for legajo, datos in usuarios.items():
            writer.writerow([legajo, datos["nombre"], datos["apellido"], datos["rol"], datos["dias_disponibles"]])

def cargar_solicitudes():
    """Lee el historial completo de solicitudes desde el archivo CSV."""
    solicitudes = []
    if not os.path.exists(ARCH_SOLICITUDES):
        with open(ARCH_SOLICITUDES, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["legajo_empleado", "nombre_empleado", "apellido_empleado", "dias", "estado"])
        return solicitudes

    with open(ARCH_SOLICITUDES, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            solicitudes.append({
                "legajo_empleado": int(fila["legajo_empleado"]),
                "nombre_empleado": fila["nombre_empleado"],
                "apellido_empleado": fila["apellido_empleado"],
                "dias": int(fila["dias"]),
                "estado": fila["estado"]
            })
    return solicitudes

def guardar_solicitudes(solicitudes):
    """Reescribe el archivo de solicitudes con los estados actualizados (Persistencia)."""
    with open(ARCH_SOLICITUDES, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["legajo_empleado", "nombre_empleado", "apellido_empleado", "dias", "estado"])
        for s in solicitudes:
            writer.writerow([s["legajo_empleado"], s["nombre_empleado"], s["apellido_empleado"], s["dias"], s["estado"]])

# =====================================================================
# LÓGICA PRINCIPAL DEL BOT (MÁQUINA DE ESTADOS)
# =====================================================================
def ejecutar_bot():
    db_usuarios = cargar_empleados()
    historial_solicitudes = cargar_solicitudes()

    ESTADO_LOGIN = "LOGIN"
    ESTADO_MENU_EMPLEADO = "MENU_EMPLEADO"
    ESTADO_SOLICITANDO_DIAS = "SOLICITANDO_DIAS"
    ESTADO_MENU_ORGANIZACION = "MENU_ORGANIZACION"
    
    estado_actual = ESTADO_LOGIN
    usuario_activos = None

    print("🤖 Bot: Sistema de Gestión de Vacaciones Organizacionales Activo.")

    while True:
        # -----------------------------------------------------------------
        # ESTADO: LOGIN
        # -----------------------------------------------------------------
        if estado_actual == ESTADO_LOGIN:
            print("\n--- INICIO DE SESIÓN ---")
            entrada = input("Por favor, ingresá tu número de legajo (o 'SALIR'): ").strip()
            
            if entrada.upper() == "SALIR":
                break
                
            if not entrada.isdigit():
                print("❌ Camino Infeliz: El legajo debe contener solo números.")
                continue
                
            legajo = int(entrada)
            if legajo in db_usuarios:
                usuario_activos = db_usuarios[legajo]
                usuario_activos["legajo"] = legajo
                print(f"\n✅ Bienvenido/a {usuario_activos['nombre']} | Rol: {usuario_activos['rol'].upper()}")
                
                if usuario_activos["rol"] == "organización":
                    estado_actual = ESTADO_MENU_ORGANIZACION
                else:
                    estado_actual = ESTADO_MENU_EMPLEADO
            else:
                print("❌ Camino Infeliz: Legajo no encontrado.")

        # -----------------------------------------------------------------
        # ESTADO: MENÚ EMPLEADO
        # -----------------------------------------------------------------
        elif estado_actual == ESTADO_MENU_EMPLEADO:
            print(f"\n--- MENÚ EMPLEADO ({usuario_activos['nombre']}) ---")
            print("1. Consultar días disponibles")
            print("2. Solicitar periodo de vacaciones")
            print("3. Ver historial y estado de mis solicitudes")
            print("4. Cerrar Sesión")
            
            opcion = input("Opción: ").strip()
            
            if opcion == "1":
                print(f"\n📊 Saldo actual: Disponés de {usuario_activos['dias_disponibles']} días.")
            
            elif opcion == "2":
                if usuario_activos['dias_disponibles'] == 0:
                    print("\n⚠️ Regla de Negocio: No poseés saldo disponible.")
                else:
                    estado_actual = ESTADO_SOLICITANDO_DIAS
            
            elif opcion == "3":
                # AQUÍ SE RESPONDE TU PREGUNTA: El empleado consulta el registro del Excel
                print("\n📋 ESTADO DE TUS SOLICITUDES:")
                mis_solicitudes = [s for s in historial_solicitudes if s["legajo_empleado"] == usuario_activos["legajo"]]
                
                if not mis_solicitudes:
                    print("- No tenés trámites registrados en el sistema.")
                else:
                    for i, s in enumerate(mis_solicitudes, 1):
                        print(f" {i}. {s['dias']} días solicitados -> Estado: [{s['estado'].upper()}]")
            
            elif opcion == "4":
                usuario_activos = None
                estado_actual = ESTADO_LOGIN
            
            else:
                print("❌ Fuera de rango: solo son válidas las opciones del 1 al 4")

        # -----------------------------------------------------------------
        # ESTADO: SOLICITANDO DÍAS
        # -----------------------------------------------------------------
        elif estado_actual == ESTADO_SOLICITANDO_DIAS:
            print(f"\n--- INICIAR TRÁMITE --- (Disponibles: {usuario_activos['dias_disponibles']})")
            entrada_dias = input("Ingresá la cantidad de días requeridos (o 'VOLVER'): ").strip()
            
            if entrada_dias.upper() == "VOLVER":
                estado_actual = ESTADO_MENU_EMPLEADO
                continue
                
            if not entrada_dias.isdigit():
                print("❌ Camino Infeliz: Entrada inválida.")
                continue
                
            dias_tramite = int(entrada_dias)
            
            if dias_tramite <= 0 or dias_tramite > usuario_activos["dias_disponibles"]:
                print("❌ Error de validación: Cantidad de días incorrecta o saldo insuficiente.")
            else:
                # El trámite se guarda inicialmente con estado "PENDIENTE" en el archivo Excel
                nueva_solicitud = {
                    "legajo_empleado": usuario_activos["legajo"],
                    "nombre_empleado": usuario_activos["nombre"],
                    "apellido_empleado": usuario_activos["apellido"],
                    "dias": dias_tramite,
                    "estado": "Pendiente"
                }
                historial_solicitudes.append(nueva_solicitud)
                guardar_solicitudes(historial_solicitudes) # Impacta en solicitudes.csv
                
                print(f"\n✅ Solicitud enviada. Queda registrada como PENDIENTE en el sistema.")
                estado_actual = ESTADO_MENU_EMPLEADO

        # -----------------------------------------------------------------
        # ESTADO: MENÚ ORGANIZACIÓN
        # -----------------------------------------------------------------
        elif estado_actual == ESTADO_MENU_ORGANIZACION:
            # Filtramos únicamente las solicitudes del CSV que sigan "Pendiente"
            pendientes = [s for s in historial_solicitudes if s["estado"] == "Pendiente"]
            
            print(f"\n--- PANEL DE CONTROL - ORGANIZACIÓN/RRHH ({usuario_activos['nombre']}) ---")
            print(f"Solicitudes pendientes en el sistema: {len(pendientes)}")
            print("1. Revisar y procesar solicitudes")
            print("2. Cerrar Sesión")
            
            opcion = input("Opción: ").strip()
            
            if opcion == "1":
                if not pendientes:
                    print("\n☕ No hay trámites pendientes de evaluación en el archivo de datos.")
                    continue
                
                # Evaluamos la primera solicitud pendiente de la lista
                solicitud_a_evaluar = pendientes[0]
                print(f"\n📋 EVALUANDO SOLICITUD:")
                print(f"-> Empleado: {solicitud_a_evaluar['nombre_empleado']} (Legajo: {solicitud_a_evaluar['legajo_empleado']})")
                print(f"-> Cantidad de días solicitados: {solicitud_a_evaluar['dias']} días.")
                
                decision = input("¿La organización aprueba esta solicitud? (S/N): ").strip().upper()
                
                if decision == "S":
                    legajo_emp = solicitud_a_evaluar["legajo_empleado"]
                    dias_a_restar = solicitud_a_evaluar["dias"]
                    
                    if db_usuarios[legajo_emp]["dias_disponibles"] >= dias_a_restar:
                        # 1. Modificamos el saldo en empleados.csv
                        db_usuarios[legajo_emp]["dias_disponibles"] -= dias_a_restar
                        guardar_empleados(db_usuarios)
                        
                        # 2. Cambiamos el estado en solicitudes.csv a Aprobada
                        solicitud_a_evaluar["estado"] = "Aprobada"
                        guardar_solicitudes(historial_solicitudes)
                        
                        print(f"✅ TRÁMITE APROBADO. Se actualizaron ambos archivos Excel.")
                    else:
                        print("❌ Error: El empleado ya no cuenta con días. Rechazada automáticamente.")
                        solicitud_a_evaluar["estado"] = "Rechazada"
                        guardar_solicitudes(historial_solicitudes)
                        
                elif decision == "N":
                    # Cambiamos el estado en solicitudes.csv a Rechazada
                    solicitud_a_evaluar["estado"] = "Rechazada"
                    guardar_solicitudes(historial_solicitudes)
                    print(f"❌ TRÁMITE RECHAZADO. Se registró la denegación en el archivo Excel.")
                else:
                    print("❌ Camino Infeliz: Opción inválida.")
                    
            elif opcion == "2":
                usuario_activos = None
                estado_actual = ESTADO_LOGIN

if __name__ == "__main__":
    ejecutar_bot()