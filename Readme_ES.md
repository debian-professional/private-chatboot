# DeepSeek Chat – Un Cliente de Chat Privado y Seguro para la API de DeepSeek

**DeepSeek Chat** es un cliente de chat completamente autónomo y alojado localmente para la API de DeepSeek. Fue desarrollado con un enfoque en **seguridad, simplicidad y usabilidad profesional**. La arquitectura no requiere frameworks exóticos y utiliza únicamente tecnologías probadas: Apache como servidor web, Python CGI para la lógica del lado del servidor, y HTML/JavaScript/CSS puro en el lado del cliente.

Características destacadas:
- **Gestión de contexto única** – Elimina mensajes individuales junto con todos los posteriores. El chat permanece consistente y el uso de tokens se actualiza dinámicamente.
- **Máxima seguridad** – La clave API nunca es visible en el lado del cliente, las cargas de archivos están protegidas contra ejecutables mediante inspección de bytes mágicos, y las sesiones se almacenan con permisos de archivo restrictivos.
- **Sin frameworks exóticos** – Todo se basa en Apache, Python, Bash y HTML/JS puro.
- **Funciones de exportación profesionales** – PDF, Markdown, TXT, RTF para todo el chat o mensajes individuales.
- **Herramienta incluida** – El script `repo2text.sh` exporta el repositorio completo como archivo de texto, ideal para trabajar con asistentes de IA (como este).

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura](#arquitectura)
- [Gestión de Contexto Única](#gestión-de-contexto-única)
- [Características en Detalle](#características-en-detalle)
  - [Interfaz de Chat](#interfaz-de-chat)
  - [Carga de Archivos con Verificación de Seguridad](#carga-de-archivos-con-verificación-de-seguridad)
  - [Modo DeepThink](#modo-deepthink)
  - [Configuración (Interruptores en lugar de Botones de Radio)](#configuración-interruptores-en-lugar-de-botones-de-radio)
  - [Gestión de Sesiones](#gestión-de-sesiones)
  - [Funciones de Exportación](#funciones-de-exportación)
  - [Botones de Feedback y Registro](#botones-de-feedback-y-registro)
  - [Visualización Dinámica del Contexto](#visualización-dinámica-del-contexto)
- [El Script Auxiliar `repo2text.sh`](#el-script-auxiliar-repo2textsh)
- [Arquitectura de Seguridad en Detalle](#arquitectura-de-seguridad-en-detalle)
- [Despliegue y Uso](#despliegue-y-uso)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalación](#instalación)
  - [Configuración](#configuración)
  - [Scripts de Despliegue](#scripts-de-despliegue)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Dependencias](#dependencias)
- [Conclusión / Por Qué Este Proyecto Destaca](#conclusión--por-qué-este-proyecto-destaca)

---

## Descripción General

DeepSeek Chat es una **aplicación web local** que se comunica a través de la API de DeepSeek (modelos `deepseek-chat` y `deepseek-reasoner`). Desarrollada para un entorno de servidor privado (Debian), puede ejecutarse en cualquier sistema con Apache y Python 3. El objetivo fue crear un cliente de chat **seguro, extensible y fácil de usar** que funcione sin dependencias de la nube y ofrezca control total sobre los datos.

---

## Arquitectura

La arquitectura está intencionalmente simplificada pero bien pensada:

1. **Cliente**
   - HTML/JavaScript/CSS puro, servido a través de Apache.
   - Sin herramientas de compilación, sin Node.js, sin bibliotecas externas (excepto PDF.js para la extracción de PDF).
   - Toda la lógica (procesamiento de mensajes, actualizaciones de UI, recepción de streaming) está encapsulada en un único `index.html`.

2. **Servidor**
   - **Apache** con soporte CGI.
   - **Scripts Python CGI** bajo `/cgi-bin/` manejan:
     - Comunicación con la API de DeepSeek (`deepseek-api.py`)
     - Almacenamiento y recuperación de sesiones (`save-session.py`, `load-session.py`, `delete-session.py`)
     - Exportaciones en varios formatos (`export-*.py`)
     - Registro de feedback (`feedback-log.py`)
     - Visualización de registros (`get-log.py`)
   - La **clave API** se proporciona exclusivamente a través de una variable de entorno de Apache (`DEEPSEEK_API_KEY` en `/etc/apache2/envvars`) — **nunca en el código del cliente**.

3. **Almacenamiento de Datos**
   - Las **sesiones** se almacenan como archivos JSON en `/var/www/deepseek-chat/sessions/` con `chmod 700`.
   - Los **registros** se escriben en `/var/www/deepseek-chat/cgi-bin/deepseek-chat.log` (sin clave API).
   - La **configuración** permanece localmente en el navegador (`localStorage`).

4. **Scripts Auxiliares**
   - `deploy.sh`, `sync-back.sh`, `install.sh`, `tag-release.sh` facilitan el despliegue entre directorios de desarrollo y producción.
   - `repo2text.sh` exporta el repositorio completo como archivo de texto para asistentes de IA.

---

## Gestión de Contexto Única

Una de las características más destacadas es la posibilidad de **eliminar mensajes individuales junto con todos los posteriores**. Esto va mucho más allá del típico "eliminar último mensaje" y permite una corrección flexible del historial de conversación.

**Implementación**:
- Cada mensaje (usuario e IA) recibe un `id` único y se almacena en un array `contextHistory.messages`.
- La función `deleteMessage(msgId)` determina el índice del mensaje, trunca el array desde `index` en adelante y elimina todos los elementos posteriores del DOM.
- La estimación de tokens (`updateContextEstimation()`) se actualiza inmediatamente, al igual que el porcentaje de utilización del contexto.
- La sesión modificada se guarda automáticamente (`saveSession()`).

**¿Por qué es único?**
Muchos clientes de chat solo permiten eliminar el último mensaje o ninguna manipulación del historial. Aquí, el usuario puede **definir cualquier punto de la conversación como nuevo punto de partida** — perfecto para pruebas, correcciones o para limpiar la ventana de contexto sin perder todo el chat.

---

## Características en Detalle

### Interfaz de Chat

- **Modo oscuro** (fijo, sin opción) — agradable para los ojos, profesional.
- **Encabezado del servidor** muestra el nombre del servidor, IP y utilización dinámica del contexto (con advertencia por encima del 90%).
- **Contenedor de mensajes** con botones al pasar el cursor (ver más abajo).
- **Área de texto** se expande al recibir foco de 40px a 120px — Enter envía, Shift+Enter crea una nueva línea.

### Carga de Archivos con Verificación de Seguridad

- Formatos compatibles: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.png`, `.csv`, `.xlsx`, `.pptx`.
- **Inspección de bytes mágicos** (primeros 20 bytes) detecta archivos ejecutables (EXE, ELF, Mach-O, scripts de shell, bytecode de Python) y bloquea la carga — incluso si el archivo ha sido renombrado.
- Extracción de PDF con PDF.js (fallback en múltiples CDNs), límite de caracteres de 50.000, indicador de progreso.
- Los archivos de texto se leen directamente y también se truncan a 50k caracteres.

### Modo DeepThink

- Conmutable mediante un botón dedicado (estilo píldora).
- En el modo DeepThink se utiliza el modelo `deepseek-reasoner` (razonamiento real).
- La configuración de límites de tokens (`MODEL_CONFIG`) está almacenada centralmente y puede extenderse fácilmente.

### Configuración (Interruptores en lugar de Botones de Radio)

- El **tratamiento** (formal/informal) y el **modo predeterminado** (Chat/DeepThink) se controlan mediante **interruptores de palanca**.
- Los interruptores se comportan como botones de radio: activar uno desactiva automáticamente el otro.
- **Interruptor de privacidad** "No usar datos para entrenamiento" establece el encabezado `X-No-Training: true`.
- Toda la configuración se almacena en `localStorage` con control de versiones (`SETTINGS_VERSION`).

### Gestión de Sesiones

- Cada sesión de chat recibe un ID único en el formato `YYYY-MM-DD_HHMMSS_aleatorio`.
- **Guardado automático** después de cada mensaje (usuario + IA).
- **Modal "Cargar historial de chat"** muestra todas las sesiones guardadas con vista previa y número de mensajes.
- Las sesiones se pueden cargar o eliminar individualmente. Al cargar, el chat actual se guarda automáticamente.

### Funciones de Exportación

- **Menú desplegable de exportación global** (junto a enviar): PDF, Markdown, TXT, RTF, cargar historial de chat.
- **Exportación individual** por mensaje: el botón "Exportar" al pasar el cursor abre un menú desplegable con TXT, Markdown, RTF, PDF.
  - TXT, Markdown, RTF se generan **en el lado del cliente** como blobs (sin ida y vuelta al servidor).
  - El PDF se crea en el lado del servidor con ReportLab (diseño profesional con estadísticas, tabla de contenidos, mensajes coloreados).
- Las exportaciones contienen metadatos (servidor, fecha, configuración) y estadísticas (número de mensajes, modos, tokens, archivos).

### Botones de Feedback y Registro

- Al pasar el cursor, aparecen cuatro botones para cada respuesta de IA:
  - **Copiar** (con feedback "¡Copiado!")
  - **Me gusta** / **No me gusta** (registran LIKE/DISLIKE en `deepseek-chat.log`, exclusivos)
  - **Regenerar** (elimina la respuesta anterior y genera una nueva)
- El registro del lado del servidor captura el feedback así como todos los accesos a la API (IP, método, ruta, estado) — **nunca claves API ni contenidos de sesión**.

### Visualización Dinámica del Contexto

- Debajo de la IP del servidor se muestra la utilización actual del contexto en porcentaje, p.ej. `Contexto: 45% (deepseek-chat)`.
- Por encima del 90%, el texto se vuelve rojo y parpadea — advirtiendo al usuario antes de que se alcance el límite de tokens.
- La visualización se actualiza con cada mensaje, cada eliminación y cada cambio de modelo.

---

## El Script Auxiliar `repo2text.sh`

Este script Bash fue desarrollado específicamente para **exportar el código fuente completo de un repositorio de GitHub como un único archivo de texto** — ideal para proporcionar el contexto completo del proyecto a un asistente de IA como ChatGPT.

**Cómo funciona**:
- Clona el repositorio con `git clone --depth 1`.
- Analiza todos los archivos de texto (tipo MIME + `grep -Iq .`) y los escribe con separadores en un archivo de salida (TXT, JSON o Markdown).
- Respeta explícitamente los archivos `.gitignore` y `.gitattributes`.
- Crea un archivo ZIP del archivo de exportación.

**Opciones especiales**:
- `--flat`: Usar solo nombres de archivo sin rutas en la exportación.
- `-o, --only RUTA`: Exportar solo un subdirectorio específico.
- `-md5, --md5`: Calcular e incluir la suma MD5 para cada archivo.
- Detección inteligente de la URL remota cuando el script se ejecuta dentro de un repositorio Git.

**Ejemplos**:

```bash
# Exportación simple del repositorio (solicitud interactiva de URL)
./repo2text.sh

# Exportación con URL y en formato Markdown
./repo2text.sh -f md https://github.com/debian-professional/private-chatboot.git

# Exportar solo el directorio 'shell-scipts' con estructura plana
./repo2text.sh --flat -o shell-scipts https://github.com/debian-professional/private-chatboot.git

# Exportación con sumas MD5 para cada archivo
./repo2text.sh -md5 https://github.com/debian-professional/private-chatboot.git
```

**¿Por qué es útil?**
- Permite la documentación completa del proyecto en un único archivo.
- Perfecto para insertar todo el código en chats de IA o para fines de archivo.
- La opción MD5 ayuda a verificar la integridad de los archivos después de una exportación.

> `repo2text` también está disponible como proyecto independiente: [github.com/debian-professional/repo2text](https://github.com/debian-professional/repo2text)

---

## Arquitectura de Seguridad en Detalle

La seguridad fue la máxima prioridad en este proyecto. Aquí están las medidas clave:

1. **Clave API invisible**
   - La clave se mantiene **exclusivamente** en la variable de entorno de Apache `DEEPSEEK_API_KEY` (en `/etc/apache2/envvars`).
   - El script CGI `deepseek-api.py` la recupera mediante `os.environ.get('DEEPSEEK_API_KEY')`.
   - **El cliente nunca tiene acceso** — incluso en caso de un ataque XSS, la clave no podría ser leída.

2. **Inspección de bytes mágicos contra archivos ejecutables**
   - Antes de leer un archivo cargado, los primeros 20 bytes se verifican en busca de firmas típicas de formatos ejecutables (PE, ELF, Mach-O, shebang, bytecode de Python).
   - Si se detecta tal firma, la carga es **bloqueada** — incluso si el archivo se llama `imagen.jpg` pero en realidad es un EXE.
   - La lista de firmas es extensible y cubre Windows, Linux, macOS, ARM y scripts.

3. **Almacenamiento seguro de sesiones**
   - Las sesiones se encuentran en `/var/www/deepseek-chat/sessions/`.
   - El directorio se crea con `chmod 700` (solo el usuario del servidor web tiene acceso).
   - Cada archivo de sesión recibe `chmod 600`.
   - El ID de sesión se genera en el lado del cliente pero es validado por el servidor (formato `YYYY-MM-DD_HHMMSS_aleatorio`).

4. **Registro sin datos sensibles**
   - El registro contiene marcas de tiempo, IP, método, ruta, estado HTTP y cualquier mensaje de error — **nunca claves API ni contenidos de sesión**.
   - Las solicitudes OPTIONS se ignoran para evitar la saturación del registro.

5. **Separación de cliente y servidor**
   - Todas las operaciones críticas de seguridad (llamadas a la API, accesos de escritura a sesiones) tienen lugar en el lado del servidor.
   - El cliente se comunica exclusivamente a través de endpoints CGI bien definidos.

6. **Sin dependencias externas con vulnerabilidades de seguridad**
   - Aparte de PDF.js (CDN) y ReportLab (lado del servidor), no se incluyen bibliotecas de terceros.
   - PDF.js tiene mecanismos de fallback; ReportLab solo se usa para la exportación de PDF y está bien mantenido.

---

## Despliegue y Uso

### Requisitos Previos

- Sistema basado en Debian (o cualquier otro Linux con Apache, Python 3, Bash)
- Apache con módulo CGI (`a2enmod cgi`)
- Python 3 y paquetes requeridos: `reportlab`, `jq`, `pv` (para repo2text.sh)
- Git (para clonar y scripts auxiliares)

### Instalación

1. **Clonar el repositorio** (p.ej. como usuario `source`):

   ```bash
   git clone https://github.com/debian-professional/private-chatboot.git /home/source/private-chatboot
   ```

2. **Configurar Apache**
   - Activar la configuración SSL (ejemplo en `etc/apache2/sites-available/deepseek-chat-ssl.conf`).
   - Introducir la clave API en `/etc/apache2/envvars`:
     `export DEEPSEEK_API_KEY="tu-clave-api-de-deepseek"`
   - Activar el sitio y reiniciar Apache.

3. **Crear directorios**
   ```bash
   mkdir -p /var/www/deepseek-chat/sessions
   chown www-data:www-data /var/www/deepseek-chat/sessions
   chmod 700 /var/www/deepseek-chat/sessions
   ```

4. **Ejecutar script de despliegue**
   Como `root` (o con sudo), ejecutar `deploy.sh <usuario>` para copiar los archivos actuales del repositorio fuente al directorio de producción y recargar Apache.
   Ejemplo:
   ```bash
   sudo /var/www/deepseek-chat/deploy.sh source
   ```

5. **Instalar scripts auxiliares**
   `install.sh` (como root) copia `deploy.sh` y `sync-back.sh` al directorio de producción.

### Configuración

- El archivo `manifest` contiene **todas las decisiones de diseño y convenciones**. Cada cambio en el proyecto debe documentarse allí — esto garantiza consistencia y trazabilidad.
- La configuración de Apache ya está optimizada (no se necesitan entradas ScriptAlias individuales, solo un alias genérico `/cgi-bin/`).
- La configuración del modelo (`MODEL_CONFIG` en `index.html`) puede extenderse fácilmente cuando se añaden nuevos modelos.

### Scripts de Despliegue

- **`deploy.sh <usuario>`** — Copia archivos desde `/home/<usuario>/private-chatboot/var/www/deepseek-chat/` a `/var/www/deepseek-chat/`, establece propietario y permisos, y recarga Apache.
- **`sync-back.sh <usuario>`** — Copia archivos modificados desde producción de vuelta al repositorio fuente (p.ej. después de cambios manuales).
- **`install.sh`** — Instala los dos scripts en el directorio de producción.
- **`tag-release.sh`** — Crea una nueva etiqueta Git con número de versión incrementado automáticamente (p.ej. v0.80 → v0.81) y la envía.

---

## Estructura del Proyecto (Extracto)

```
/
├── etc/apache2/sites-available/
│   ├── deepseek-chat.conf              (desactivado, solo HTTP->HTTPS)
│   └── deepseek-chat-ssl.conf          (activo, con CGI y envvars)
├── shell-scipts/
│   ├── repo2text.sh                     # Herramienta de exportación del repositorio
│   ├── deploy.sh                        # Copia fuente → producción
│   ├── sync-back.sh                     # Copia producción → fuente
│   ├── install.sh                       # Instala deploy/sync-back
│   └── tag-release.sh                   # Crea etiquetas Git
├── var/www/deepseek-chat/
│   ├── index.html                       # Aplicación principal (JS/CSS/HTML)
│   ├── manifest                         # Manifiesto de diseño
│   ├── files-directorys                 # Resumen de archivos
│   ├── cgi-bin/
│   │   ├── deepseek-api.py              # Proxy a la API de DeepSeek
│   │   ├── save-session.py              # Guarda sesiones de chat
│   │   ├── load-session.py              # Carga sesiones / lista
│   │   ├── delete-session.py            # Elimina sesión
│   │   ├── export-pdf.py                # Exportación PDF
│   │   ├── export-markdown.py           # Exportación Markdown
│   │   ├── export-txt.py                # Exportación TXT
│   │   ├── export-rtf.py                # Exportación RTF
│   │   ├── feedback-log.py              # Registro de feedback
│   │   ├── get-log.py                   # Leer archivo de registro
│   │   └── deepseek-chat.log            # Archivo de registro (crece)
│   └── sessions/                        # Archivos de sesión JSON
├── LICENSE
└── .gitignore
```

---

## Dependencias

| Componente | Propósito | Instalación |
|------------|-----------|-------------|
| Apache2 | Servidor web, soporte CGI | `apt install apache2` |
| Python3 | Scripts del lado del servidor | `apt install python3` |
| reportlab | Exportación PDF | `pip3 install reportlab` |
| jq | Procesamiento JSON en `repo2text.sh` | `apt install jq` |
| pv | Indicador de progreso en `repo2text.sh` | `apt install pv` |
| git | Clonación y gestión de versiones | `apt install git` |
| zip | Archivo de exportación en `repo2text.sh` | `apt install zip` |
| pdf.js (CDN) | Extracción de PDF en el cliente | Cargado via CDN (fallback) |

**Sin frameworks exóticos** — todo es estándar en un entorno Debian.

---

## Conclusión / Por Qué Este Proyecto Destaca

Este proyecto demuestra desarrollo a nivel profesional:

- **Arquitectura limpia y segura** — protección de clave API, inspección de bytes mágicos, seguridad de sesiones, separación de cliente y servidor.
- **Experiencia de usuario cuidada** — eliminación intuitiva de mensajes incluyendo contexto posterior, advertencia dinámica de contexto, botones al pasar el cursor, interruptores de palanca.
- **Extensibilidad** — configuración central de modelos, scripts CGI modulares, manifiesto documentado.
- **Herramientas prácticas** — `repo2text.sh` simplifica enormemente el trabajo con asistentes de IA.
- **Minimalismo** — Sin Node, sin React, sin Docker — funciona en cualquier servidor Apache.

Para un **desarrollador profesional**, este proyecto demuestra:
- **Conciencia de seguridad** (manejo de claves API, protección contra cargas de malware).
- **Trabajo estructurado** (manifiesto, etiquetas de versión, scripts de despliegue).
- **Características innovadoras** (gestión de contexto, respuestas en streaming).
- **Documentación completa** — tanto en el código como en este README.

DeepSeek Chat es un **showcase de desarrollo web profesional** — sin sobrecarga innecesaria, pero con los más altos estándares de seguridad y facilidad de uso.

---

**Nota:** Todos los cambios en este proyecto deben documentarse en el `manifest`. Este archivo es la fuente central de decisiones de diseño y convenciones y nunca debe eliminarse ni dejarse incompleto.
