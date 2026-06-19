# Sistema de Gestión de Vacaciones Organizacionales

## 📖 Descripción General

Este proyecto implementa un sistema interactivo en **Python** para la gestión de vacaciones dentro de una organización.  
El sistema utiliza archivos **CSV** como base de datos persistente, permitiendo simular el registro de empleados, solicitudes de vacaciones y su procesamiento por parte del área de Recursos Humanos.

El programa está diseñado como una **máquina de estados**, ofreciendo menús diferenciados según el rol del usuario (empleado u organización).

## 🎯 Objetivos del Sistema

- Facilitar la **consulta de días disponibles** por parte de los empleados.
- Permitir la **solicitud de períodos de vacaciones**, registrando el trámite en estado _Pendiente_.
- Ofrecer a la organización un **panel de control** para aprobar o rechazar solicitudes.
- Mantener actualizados los saldos de días y el historial de solicitudes mediante persistencia en archivos CSV.

## ⚙️ Funcionalidades Principales

- **Carga de empleados**: inicializa el archivo `empleados.csv` con datos de ejemplo si no existe.
- **Guardar empleados**: actualiza los saldos de días disponibles en el archivo.
- **Carga de solicitudes**: lee el historial completo desde `solicitudes.csv`.
- **Guardar solicitudes**: persiste los cambios en el estado de las solicitudes.
- **Máquina de estados**: controla la interacción del bot mediante menús de login, empleado y organización.

## 📐 Diagrama de Procesos BPMN

<img width="2898" height="1414" alt="BPMN_TPI" src="https://github.com/user-attachments/assets/e65c9258-e340-4874-8572-6e2b93149532" />

## 📂 Estructura de Archivos

```bash
BOT GESTION DE VACACIONES/
├── datos/
│   ├── empleados.csv     # Base de datos de empleados
│   └── solicitudes.csv   # Historial de solicitudes de vacaciones
├── script/
│   └── main.py           # Código fuente principal
├── .gitignore
└── README.md
```

## 🚀 Ejecución del Programa

1. Clonar o descargar el repositorio.
2. Verificar que se dispone de **Python 3.x** instalado.
3. Ubicarse en la carpeta raíz del proyecto.
4. Ejecutar el programa desde la terminal con:

   ```bash
   python script/main.py
   ```

5. Interactuar con el sistema a través de la consola.

## 👥 Roles en el Sistema

Empleado

- Consultar saldo de días disponibles.
- Solicitar vacaciones (estado inicial: Pendiente).
- Revisar historial y estado de solicitudes.

Organización / RRHH

- Revisar solicitudes pendientes.
- Aprobar o rechazar solicitudes.
- Actualizar automáticamente los saldos de días de los empleados.

## 📌 Ejemplo de Uso

1. El empleado con legajo 1024 inicia sesión.
2. Solicita 5 días de vacaciones → la solicitud queda registrada como Pendiente.
3. El usuario con legajo 2048 (rol organización) inicia sesión.
4. Revisa la solicitud y la aprueba → se descuenta del saldo del empleado y se actualiza el estado a Aprobada.

## 🔧 Requisitos Técnicos

- Python 3.x
- Librerías estándar:
  - csv
  - os
