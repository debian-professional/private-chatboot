# Multi-LLM Chat Client – OpenAI, DeepSeek, Google Gemini, Hugging Face & GroqCloud

**Multi-LLM Chat Client** es un cliente de chat completamente autónomo, alojado localmente, compatible con múltiples proveedores de IA: OpenAI, DeepSeek, Google Gemini, Hugging Face y GroqCloud. Desarrollado con foco en **seguridad, simplicidad y usabilidad profesional**, utilizando únicamente tecnologías probadas: Apache como servidor web, Python CGI para la lógica del servidor y HTML/JavaScript/CSS puro en el lado del cliente.

Características principales:
- **Soporte Multi-LLM** – Cambia entre OpenAI, DeepSeek, Google Gemini, Hugging Face y GroqCloud mediante un toggle de proveedor en el panel de configuración LLM.
- **Carga de múltiples archivos** – Selecciona y envía varios archivos a la vez. Los contenidos se combinan y se envían juntos como contexto.
- **Grabación de audio por micrófono** – Graba audio directamente en el navegador y envíalo a la IA. Compatible con Google Gemini (todos los modelos) y OpenAI (gpt-4o, gpt-4.1). El botón aparece automáticamente solo cuando hay un modelo con capacidad de audio activo.
- **Gestión de contexto única** – Elimina mensajes individuales junto con todos los posteriores. El chat permanece consistente y el uso de tokens se actualiza dinámicamente.
- **Máxima seguridad** – La clave API nunca es visible en el lado del cliente, las cargas están protegidas contra archivos ejecutables mediante inspección de magic bytes, y las sesiones se almacenan con permisos restrictivos.
- **Sin frameworks exóticos** – Todo se basa en Apache, Python, Bash y HTML/JS puro.
- **Funciones de exportación profesionales** – PDF, Markdown, TXT, RTF para el chat completo o mensajes individuales, más copia directa al portapapeles.
- **Soporte multilingüe** – Traducción completa de la interfaz mediante `language.xml` externo (inglés, alemán, español, ampliable con idiomas personalizados).
- **Grabación de audio** – Botón de micrófono integrado (API MediaRecorder) para entrada de voz directa. Visible automáticamente solo cuando hay un modelo con capacidad de audio activo (todos los modelos Gemini, OpenAI gpt-4o y gpt-4.1). El audio se transmite como base64 WebM/MP4 — sin transcripción, el modelo procesa el habla de forma nativa.
- **Kompressor (compresión de contexto)** – Compresión inteligente y automática del historial de chat cuando la ventana de contexto se llena. Un segundo LLM resume el 50% más antiguo de los mensajes e inyecta el resumen en el prompt del sistema — la conversación puede continuar indefinidamente sin perder el hilo. Umbrales configurables (70%/85%/95%), banner animado como retroalimentación visual, archivos de resultados guardados en disco. El resumen se descarta automáticamente si el contexto cae por debajo del último umbral activado tras la eliminación manual de mensajes.
- **Banners de crédito y límite diario** – Banners visuales persistentes para crédito agotado (rojo, proveedores de pago) y límites diarios (azul, proveedores de nivel gratuito), cada uno con botón de cierre.
- **Gestión de ventana de contexto excedida** – Cuando se alcanza el tamaño máximo de contexto, aparece directamente en el chat un cuadro interactivo con dos opciones: iniciar un nuevo chat llevando el contexto actual (Opción C: último resumen de compresión + mensajes posteriores), o iniciar un chat limpio. La sesión actual se guarda automáticamente en ambos casos.
- **Integración del portapapeles** – Manejador Ctrl+V con diálogo para texto, imágenes y protección contra pegado accidental de rutas de archivo.
- **Respuestas en streaming** – Las respuestas de la IA aparecen token a token, igual que ChatGPT o Claude.
- **Gestión de límite de tasa 429** – Reintento automático con visualización de cuenta regresiva para los límites del nivel gratuito de Google Gemini.
- **Herramienta incluida** – El script `repo2text.sh` exporta todo el repositorio como archivo de texto, ideal para trabajar con asistentes de IA (como éste).

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Arquitectura](#arquitectura)
- [Gestión de contexto única](#gestión-de-contexto-única)
- [Características en detalle](#características-en-detalle)
  - [Interfaz de chat](#interfaz-de-chat)
  - [Respuestas en streaming](#respuestas-en-streaming)
  - [Manejador del portapapeles (Ctrl+V)](#manejador-del-portapapeles-ctrlv)
  - [Carga de archivos con verificación de seguridad](#carga-de-archivos-con-verificación-de-seguridad)
  - [Sistema de marcadores de posición para diéresis](#sistema-de-marcadores-de-posición-para-diéresis)
  - [Modo DeepThink](#modo-deepthink)
  - [Detección de modelos y capacidades](#detección-de-modelos-y-capacidades)
  - [Sistema multilingüe](#sistema-multilingüe)
  - [Configuración (toggles en lugar de botones de radio)](#configuración-toggles-en-lugar-de-botones-de-radio)
  - [Gestión de sesiones](#gestión-de-sesiones)
  - [Funciones de exportación](#funciones-de-exportación)
  - [Botones de feedback y registro](#botones-de-feedback-y-registro)
  - [Visualización dinámica del contexto](#visualización-dinámica-del-contexto)
  - [Visualización de tarjeta de archivo](#visualización-de-tarjeta-de-archivo)
  - [Grabación de audio](#grabación-de-audio)
  - [Kompressor — Compresión inteligente de contexto](#kompressor--compresión-inteligente-de-contexto)
  - [Banners de crédito y límite diario](#banners-de-crédito-y-límite-diario)
  - [Gestión de ventana de contexto excedida](#gestión-de-ventana-de-contexto-excedida)
- [El script auxiliar `repo2text.sh`](#el-script-auxiliar-repo2textsh)
- [Arquitectura de seguridad en detalle](#arquitectura-de-seguridad-en-detalle)
- [Despliegue y uso](#despliegue-y-uso)
  - [Requisitos previos](#requisitos-previos)
  - [Instalación](#instalación)
  - [Configuración](#configuración)
  - [Scripts de despliegue](#scripts-de-despliegue)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración de modelos](#configuración-de-modelos)
- [Manifiesto de diseño](#manifiesto-de-diseño)
- [Limitaciones conocidas y notas técnicas](#limitaciones-conocidas-y-notas-técnicas)
- [Dependencias](#dependencias)
- [Conclusión / Por qué destaca este proyecto](#conclusión--por-qué-destaca-este-proyecto)

---

## Descripción general

Multi-LLM Chat Client es una **aplicación web local** que se comunica a través de diversas APIs. Desarrollada para un entorno de servidor privado (Debian), puede ejecutarse en cualquier sistema con Apache y Python 3. El objetivo fue crear un cliente de chat **seguro, extensible y fácil de usar** que funcione sin dependencias en la nube y ofrezca control total sobre los datos.

El proyecto ha crecido continuamente durante varias semanas de desarrollo activo, añadiendo funciones como streaming, gestión de sesiones, exportaciones, soporte multilingüe, integración del portapapeles, compresión inteligente de contexto y medidas de seguridad robustas — todo sin introducir frameworks JavaScript externos.

---

## Arquitectura

La arquitectura es intencionalmente simple pero bien pensada:

### 1. Cliente
- HTML/JavaScript/CSS puro, servido mediante Apache.
- Sin herramientas de compilación, sin Node.js, sin bibliotecas externas (excepto PDF.js para extracción de texto PDF en el navegador).
- Toda la lógica del cliente (procesamiento de mensajes, actualizaciones de UI, recepción de streaming, cambio de idioma, manejo del portapapeles) está encapsulada en un único `index.html`.
- Todos los textos de la interfaz se cargan desde un `language.xml` externo al inicio — sin cadenas codificadas en el HTML.

### 2. Servidor
- **Apache** con soporte CGI (`mod_cgi`).
- **Scripts Python CGI** bajo `/cgi-bin/` gestionan:
  - Comunicación con la API de OpenAI (`openai-api.py`) — endpoint nativo con streaming (Server-Sent Events)
  - Comunicación con la API de DeepSeek (`deepseek-api.py`) — con streaming (Server-Sent Events)
  - Comunicación con la API de Google Gemini (`google-api.py`) — convierte el formato OpenAI al formato Gemini
  - Comunicación con la API de Hugging Face Inference (`hugging-api.py`) — endpoint de router compatible con OpenAI
  - Comunicación con la API de GroqCloud (`groq-api.py`) — endpoint compatible con OpenAI, inferencia acelerada por LPU
  - Compresión de contexto (`compress-context.py`) — resume el 50% más antiguo de los mensajes mediante una segunda llamada LLM cuando se alcanzan los umbrales de contexto
  - Descubrimiento de modelos (`deepseek-models.py`) — consulta `/v1/models` al inicio
  - Almacenamiento y recuperación de sesiones (`save-session.py`, `load-session.py`, `delete-session.py`)
  - Exportaciones en varios formatos (`export-pdf.py`, `export-markdown.py`, `export-txt.py`, `export-rtf.py`)
  - Registro de feedback (`feedback-log.py`)
  - Visualización de registros (`get-log.py`)
- Las claves API se proporcionan exclusivamente mediante variables de entorno de Apache (`OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `GOOGLE_API_KEY`, `HF_API_KEY`, `GRQ_API_KEY` en `/etc/apache2/envvars`) — **nunca en el código del cliente**.
- Un único `ScriptAlias /cgi-bin/ /var/www/deepseek-chat/cgi-bin/` cubre todos los scripts — no se necesitan cambios en Apache al añadir nuevos scripts.

### 3. Almacenamiento de datos
- Las **sesiones** se almacenan como archivos JSON en `/var/www/deepseek-chat/sessions/` con `chmod 700`.
- Los **registros** se escriben en `/var/www/deepseek-chat/logs/multi-llm-chat.log` (sin clave API ni contenido de sesiones).
- Los **resultados del Kompressor** se escriben en `/var/www/deepseek-chat/kompressor/` — un archivo por ronda de compresión.
- La **configuración** permanece localmente en el navegador (`localStorage`) con control de versiones.
- Los **datos de idioma** se cargan desde `language.xml` al cargar la página mediante `fetch()`.

### 4. Scripts auxiliares
- `deploy.sh`, `sync-back.sh`, `install.sh`, `tag-release.sh` facilitan el despliegue entre los directorios de desarrollo y producción.
- `repo2text.sh` exporta todo el repositorio como archivo de texto para asistentes de IA.

---

## Gestión de contexto única

Una de las características más destacadas es la capacidad de **eliminar mensajes individuales junto con todos los posteriores**. Esto va mucho más allá del típico "eliminar último mensaje" y permite la corrección flexible del historial de conversación.

**Implementación**:
- Cada mensaje (usuario e IA) recibe un `id` único (formato: `msg_N`) y se almacena en un array `contextHistory.messages`.
- La función `deleteMessage(msgId)` determina el índice del mensaje, trunca el array desde `index` en adelante y elimina todos los elementos siguientes del DOM (incluidos divisores).
- La estimación de tokens (`updateContextEstimation()`) se recalcula inmediatamente, al igual que el porcentaje de utilización del contexto en el encabezado.
- Si el contexto cae por debajo del último umbral del Kompressor activado tras la eliminación, el resumen de compresión se descarta automáticamente y el seguimiento de umbrales se reinicia.
- La sesión modificada se guarda automáticamente a continuación (`saveSession()`).

**¿Por qué es esto único?**
Muchos clientes de chat solo permiten eliminar el último mensaje o ninguna manipulación del historial. Aquí, el usuario puede **definir cualquier punto de la conversación como nuevo punto de inicio** — perfecto para pruebas, correcciones o limpieza del contexto sin perder todo el chat.

**Función de regeneración**: Además de la eliminación, cada respuesta de la IA tiene un botón "Regenerar" que elimina la respuesta anterior y genera automáticamente una nueva basada en el mismo mensaje del usuario — utilizando el contexto completo de la conversación hasta ese punto.

---

## Características en detalle

### Interfaz de chat

- **Modo oscuro** (fijo, sin opción) — agradable a la vista, apariencia profesional.
  - Fondo: `#121212`, texto: `#f0f0f0`, acento: `#0056b3`
- **Encabezado del servidor** muestra el nombre del servidor, dirección IP interna, utilización dinámica del contexto y nombres de modelos detectados.
- **Contenedores de mensajes** con botones al pasar el cursor (feedback, exportar, eliminar).
- **Textarea** se expande al enfocarse de 40px a 120px con animación CSS suave — Enter envía, Shift+Enter crea una nueva línea.
- Todos los botones siguen un diseño estricto de **estilo pastilla** (border-radius: 20px, height: 36px) — sin botones cuadrados.
- Los mensajes del usuario aparecen en azul (`#4dabf7`), las respuestas de la IA en blanco sobre fondo oscuro.
- Preservación automática de saltos de línea (`white-space: pre-wrap`) para todo el contenido de los mensajes.
- Desplazamiento automático al mensaje más reciente durante y después del streaming.

### Respuestas en streaming

Las respuestas de la IA se reciben y muestran **token a token** usando Server-Sent Events (SSE):

- Los cinco scripts proxy CGI envían solicitudes a sus respectivas APIs con `stream: True` y reenvían el flujo de eventos directamente.
- `index.html` lee el flujo mediante la API `ReadableStream` y `TextDecoder`.
- Cada token recibido se añade al elemento de mensaje en tiempo real.
- El efecto psicológico es significativo: los primeros tokens aparecen en ~0,3 segundos en lugar de esperar 8+ segundos por una respuesta completa.
- Tanto `sendMessage()` como `handleRegenerate()` usan lógica de streaming idéntica.
- El desplazamiento automático permanece activo durante el streaming.

**Cabeceras técnicas** establecidas por todos los scripts proxy CGI para streaming correcto:
```
Content-Type: text/event-stream
X-Accel-Buffering: no
Cache-Control: no-cache
```

### Integración de OpenAI

El cliente admite OpenAI como primer proveedor de IA (mostrado en la parte superior de la selección LLM) mediante `openai-api.py`:

- **Arquitectura**: Utiliza el endpoint nativo de OpenAI Chat Completions — no se requiere conversión de formato. El flujo SSE se reenvía directamente.
- **Endpoint**: `https://api.openai.com/v1/chat/completions`
- **Clave API**: `OPENAI_API_KEY` en `/etc/apache2/envvars` — nunca expuesta al cliente.
- **Nivel gratuito**: `gpt-4o-mini`, `gpt-5-mini`.
- **Nivel de pago**: `gpt-5.4`, `gpt-5.2-chat-latest`, `gpt-4o`, `gpt-4.1`, `gpt-4o-mini`.
- El menú desplegable de modelos en la configuración LLM se actualiza automáticamente según el nivel seleccionado.
- **Entrada de audio**: `gpt-4o` y `gpt-4.1` admiten grabaciones de micrófono directas. Cuando cualquiera de estos modelos está activo, el botón de grabación de audio se vuelve visible. El audio se envía como `input_audio` en formato OpenAI.
- El botón DeepThink y el indicador DeepThink se ocultan cuando OpenAI está activo.
- El prompt del sistema identifica el modelo activo: *"You are [model], an AI assistant made by OpenAI."*

### Integración de Google Gemini

El cliente admite Google Gemini como segundo proveedor de IA mediante `google-api.py`:

- **Arquitectura**: El script CGI convierte el formato de mensajes compatible con OpenAI utilizado internamente al formato específico `contents` de Gemini, envía la solicitud al endpoint `streamGenerateContent` de Gemini y convierte la respuesta de vuelta al formato SSE de OpenAI esperado por `index.html`.
- **Clave API**: `GOOGLE_API_KEY` en `/etc/apache2/envvars` — nunca expuesta al cliente.
- **Nivel gratuito** (predeterminado): `gemini-2.5-flash` — 5 solicitudes por minuto, 20 solicitudes por día.
- **Nivel de pago**: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`, `gemini-2.0-flash`.
- El menú desplegable de modelos se actualiza automáticamente según el nivel seleccionado.
- **Entrada de audio**: Todos los modelos Gemini admiten grabaciones de micrófono directas. El botón de grabación de audio siempre es visible cuando Google Gemini es el proveedor activo. El audio se envía como `inline_data` en el formato nativo de Gemini.
- El botón DeepThink y el indicador DeepThink se ocultan cuando Google Gemini está activo.

### Integración de Hugging Face

El cliente admite Hugging Face Inference Providers como tercer proveedor de IA mediante `hugging-api.py`:

- **Arquitectura**: Utiliza el endpoint de router de Hugging Face compatible con OpenAI — no se requiere conversión de formato. El flujo SSE se reenvía directamente.
- **Endpoint**: `https://router.huggingface.co/v1/chat/completions` — el router selecciona automáticamente el proveedor disponible más rápido.
- **Clave API**: `HF_API_KEY` en `/etc/apache2/envvars` — un token de escritura de huggingface.co/settings/tokens con el permiso "Make calls to Inference Providers".
- **Nivel gratuito**: `Qwen/Qwen2.5-72B-Instruct`, `mistralai/Mistral-7B-Instruct-v0.3`, `microsoft/Phi-3.5-mini-instruct`.
- **Nivel de pago**: `meta-llama/Meta-Llama-3.1-70B-Instruct`, `meta-llama/Meta-Llama-3.1-405B-Instruct`, `Qwen/Qwen2.5-72B-Instruct`, `mistralai/Mixtral-8x7B-Instruct-v0.1`.
- El menú desplegable de modelos se actualiza automáticamente según el nivel seleccionado.
- El botón DeepThink y el indicador DeepThink se ocultan cuando Hugging Face está activo.

### Integración de GroqCloud

El cliente admite GroqCloud como cuarto proveedor de IA mediante `groq-api.py`:

- **Arquitectura**: Utiliza el endpoint de GroqCloud compatible con OpenAI — no se requiere conversión de formato. El flujo SSE se reenvía directamente.
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **Clave API**: `GRQ_API_KEY` en `/etc/apache2/envvars`.
- **Nota**: Se requiere una cabecera `User-Agent` para eludir la protección de Cloudflare (sin ella: código de error 1010).
- **Nivel gratuito y de pago**: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `meta-llama/llama-4-scout-17b-16e-instruct`, `qwen/qwen3-32b`. Solo de pago: `moonshotai/kimi-k2-instruct-0905`.
- El menú desplegable de modelos se actualiza automáticamente según el nivel seleccionado.
- El botón DeepThink y el indicador DeepThink se ocultan cuando GroqCloud está activo.
- Todos los modelos se ejecutan en el hardware LPU (Language Processing Unit) de GroqCloud para una latencia muy baja.

### Panel de configuración LLM

Un panel dedicado de **configuración LLM** (separado del panel de configuración principal) mantiene las opciones específicas del proveedor fuera de la interfaz principal:

- **Selección de proveedor**: Alternar entre OpenAI, DeepSeek, Google Gemini, Hugging Face y GroqCloud — solo uno activo a la vez.
- **Opciones de OpenAI**: Selección de plan gratuito/de pago con actualización automática de la lista de modelos.
- **Opciones de DeepSeek**: Modo predeterminado (Chat Normal / DeepThink), toggle de privacidad (cabecera X-No-Training).
- **Opciones de Google**: Selección de plan gratuito/de pago con actualización automática de la lista de modelos.
- **Opciones de Hugging Face**: Selección de plan gratuito/de pago con actualización automática de la lista de modelos.
- **Opciones de GroqCloud**: Selección de plan gratuito/de pago con actualización automática de la lista de modelos.
- **Opciones del Kompressor**: Toggle de activación, selección de proveedor LLM de compresión (solo proveedores de pago), selección de modelo de compresión. Predeterminado: activado, DeepSeek / `deepseek-chat`.
- **Menú desplegable de modelos**: Siempre visible, el contenido se actualiza automáticamente según el proveedor y el plan activos.
- Toda la configuración se guarda en `localStorage` y persiste tras recargar la página.

### Gestión del límite de tasa 429

El nivel gratuito de Google Gemini aplica límites de tasa estrictos (5 RPM, 20 RPD). El cliente los gestiona de forma elegante:

- Ante una respuesta 429, el cliente reintenta automáticamente hasta **3 veces** con **intervalos de 15 segundos**.
- Durante la espera, se muestra una cuenta regresiva directamente en el chat: *"Límite de tasa alcanzado – esperando 15 segundos y reintentando... (Intento 1/3)"*
- Tras 3 intentos fallidos, la verificación del límite diario activa el banner azul de límite diario si corresponde.
- Los detalles de error detallados se escriben en el registro del servidor para diagnóstico.
- La lógica de reintento distingue entre límites RPM temporales (reintentables) y cuota diaria agotada (no reintentable).

### Manejador del portapapeles (Ctrl+V)

Un sofisticado manejador del portapapeles intercepta los eventos de pegado y responde de forma inteligente según el tipo de contenido:

**Contenido de texto** → Aparece un diálogo de pegado con dos opciones:
- "Insertar en la posición del cursor" — inserta el texto directamente en el campo de entrada en el cursor
- "Adjuntar como archivo" — trata el texto del portapapeles como `clipboard.txt` y lo adjunta como archivo al siguiente mensaje

**Contenido de imagen** → Aparece un cuadro de vista previa sobre el campo de entrada con la imagen, su tamaño en KB y un botón de eliminar. La imagen está lista para enviarse con el siguiente mensaje (si el modelo admite imágenes).

**Rutas de archivo del gestor de archivos (XFCE/Thunar, KDE/Dolphin)** → Estas se bloquean y se muestra una alerta:
> "Los archivos copiados en el gestor de archivos no pueden ser leídos por el navegador. Por favor, utiliza el botón de carga en su lugar."

**Trasfondo técnico**: En Linux/X11/Firefox, `e.preventDefault()` no bloquea de forma fiable los eventos de pegado. La solución es permitir el pegado, luego verificar inmediatamente el contenido del campo de entrada mediante `setTimeout(0)` y limpiarlo si se detectan rutas de archivo. Lógica de detección: 2 o más líneas donde cada una comienza con `/` o `file://`. Una llamada a `requestAnimationFrame` garantiza que el campo de entrada se limpie visualmente antes de que aparezca el diálogo de alerta.

### Carga de archivos con verificación de seguridad

- Formatos aceptados: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.csv`, `.xlsx`, `.pptx`
- Formatos procesables (extracción de contenido): `.txt`, `.pdf`
- Otros formatos aceptados: adjuntados como contexto binario (sin extracción de texto)
- Tamaño máximo de archivo: **10 MB**
- Contenido extraído máximo: **250.000 caracteres**

**Inspección de magic bytes** (primeros 20 bytes) detecta y bloquea archivos ejecutables independientemente de su extensión:

| Plataforma | Formato | Firma |
|------------|---------|-------|
| Windows 32/64 bit | PE/MZ Executable | `4D 5A` |
| Linux 32 bit | ELF32 | `7F 45 4C 46 01` |
| Linux 64 bit | ELF64 | `7F 45 4C 46 02` |
| ARM 32 bit | ELF32 ARM | `7F 45 4C 46 01 01 01 00 ... 02 00 28 00` |
| ARM 64 bit | ELF64 AArch64 | `7F 45 4C 46 02 01 01 00 ... 02 00 B7 00` |
| macOS 32 bit | Mach-O | `CE FA ED FE` |
| macOS 64 bit | Mach-O | `CF FA ED FE` |
| macOS Universal | Fat Binary | `CA FE BA BE` |
| macOS/iOS ARM 32 | Big Endian | `FE ED FA CE` |
| macOS/iOS ARM 64 | Big Endian | `FE ED FA CF` |
| Linux/macOS | Script de shell | `23 21` (#!) |
| Python | Bytecode (.pyc) | `55 0D 0D 0A` |

**Extracción de PDF**: Utiliza PDF.js 3.11.174 cargado desde CDN con respaldo automático a un CDN secundario. El progreso se muestra página a página. Tiempo límite de extracción: 30 segundos.

**Los archivos cargados se muestran como tarjetas de archivo** en el mensaje del usuario (ver [Visualización de tarjeta de archivo](#visualización-de-tarjeta-de-archivo)).

### Sistema de marcadores de posición para diéresis

Una solución única para un problema fundamental con la API de DeepSeek y el texto en alemán:

**Problema**: DeepSeek reemplaza internamente las diéresis alemanas en el contenido de archivos con equivalentes ASCII (p.ej. `Ä → AeNDERUNG`, `Ü → MUeSSEN`). Este comportamiento no puede suprimirse mediante prompts del sistema o parámetros de la API.

**Solución**: Antes de enviar el contenido del archivo a DeepSeek, las diéresis se reemplazan con marcadores de posición únicos. DeepSeek devuelve estos marcadores sin cambios. JavaScript los reemplaza de nuevo con diéresis reales tras recibir la respuesta.

| Original | Marcador |
|----------|----------|
| `ä` | `[[AE]]` |
| `ö` | `[[OE]]` |
| `ü` | `[[UE]]` |
| `ß` | `[[SS]]` |
| `Ä` | `[[CAE]]` |
| `Ö` | `[[COE]]` |
| `Ü` | `[[CUE]]` |

**Detalle de implementación importante**: Las funciones `encodeUmlautsForAI()` y `decodeUmlautsFromAI()` usan **exclusivamente secuencias de escape Unicode** (`\u00e4` en lugar de `ä`) y `split/join` en lugar de expresiones regulares — esto es fundamental para evitar la corrupción al transferir archivos mediante Git.

La decodificación se ejecuta **tanto durante el streaming** (token a token) como después de recibir la respuesta completa.

Este sistema se **aplica únicamente al contenido de archivos**, no a los mensajes normales del usuario ni a los prompts del sistema.

### Modo DeepThink

- Conmutable mediante un botón dedicado (estilo pastilla) en la segunda fila de botones.
- En modo DeepThink se utiliza el modelo `deepseek-reasoner` (razonamiento real de cadena de pensamiento).
- El botón cambia visualmente: oscuro/inactivo (`#2d2d2d`) → azul activo (`#1e3a5f` fondo, `#4dabf7` borde y texto).
- Aparece una barra indicadora debajo de los botones mostrando "Modo DeepThink activo: Análisis en profundidad en curso".
- Los límites de contexto y tokens de salida se ajustan automáticamente (ver [Configuración de modelos](#configuración-de-modelos)).
- El modo se registra con cada mensaje y se muestra en las exportaciones.
- El modo predeterminado (Chat o DeepThink) puede configurarse en Ajustes y persiste en `localStorage`.

### Detección de modelos y capacidades

Al inicio, el cliente consulta `/cgi-bin/deepseek-models.py` que a su vez llama al endpoint `/v1/models` de DeepSeek:

- Los IDs de modelos detectados se muestran en el encabezado del servidor: `Modelo: deepseek-chat, deepseek-reasoner`
- Un mapa `MODEL_CAPABILITIES` define qué modelos admiten imágenes:
  ```javascript
  const MODEL_CAPABILITIES = {
      'deepseek-chat':     { images: false, text: true },
      'deepseek-reasoner': { images: false, text: true },
      'deepseek-v4':       { images: true,  text: true },  // listo para modelos futuros
      'default':           { images: false, text: true },
  };
  ```
- Si se pega una imagen mediante el portapapeles o se carga un archivo `.jpg`/`.png` y el modelo actual no admite imágenes, una alerta bloquea la operación.
- Esta arquitectura es **compatible hacia adelante**: cuando se lance DeepSeek V4 con soporte de imágenes, funcionará automáticamente sin cambios en el código.

### Sistema multilingüe

La interfaz admite múltiples idiomas cargados desde un archivo `language.xml` externo:

**Idiomas actualmente incluidos**:
- Inglés (`en`) — predeterminado
- Alemán (`de`) — con forma de tratamiento formal/informal (Sie/Du)
- Español (`es`) — con forma de tratamiento formal/informal (Usted/Tú)
- Ranura personalizada (`custom`) — activable mediante `visible="true"` en `language.xml`

**Cómo funciona**:
- Todos los textos de la interfaz se referencian mediante IDs numéricas (p.ej. `t(205)` = etiqueta del botón Enviar).
- `loadLanguage()` obtiene y analiza `language.xml` al cargar la página.
- `t(id)` devuelve el texto para el idioma actual, con reserva al inglés si no se encuentra.
- `tf(id, ...args)` admite sustitución de marcadores de posición (`{0}`, `{1}`, ...).
- `tform(idFormal, idInformal)` devuelve el texto apropiado según la forma de tratamiento seleccionada.
- El cambio de idioma es inmediato sin recargar la página.
- El idioma seleccionado persiste en `localStorage`.

**Sistema de forma de tratamiento (alemán/español)**:
- Los idiomas pueden declarar `has_address_form="true"` en `language.xml`.
- Para dichos idiomas, el panel de ajustes muestra un grupo "Forma de tratamiento" (Formal/Informal).
- La forma seleccionada afecta: el prompt del sistema (fuerza respuestas coherentes de la IA), el marcador de posición de entrada, todas las descripciones de ajustes.
- El inglés no tiene distinción de forma de tratamiento.

**El prompt del sistema** se construye dinámicamente según el idioma, la forma de tratamiento y el modo:
- Prompt base (IDs de texto 29/30 para formal/informal)
- Adición DeepThink (IDs de texto 31/32)
- Siempre se añade en inglés una instrucción estricta para la visualización de archivos, para garantizar un comportamiento coherente independientemente del idioma de la interfaz.

### Configuración (toggles en lugar de botones de radio)

Toda la configuración usa **interruptores toggle** (deslizantes de izquierda a derecha), nunca botones de radio ni casillas de verificación:

| Grupo | Configuración | Color del toggle |
|-------|---------------|-----------------|
| Idioma | EN / DE / ES / Personalizado | Verde (preferencia personal) |
| Forma de tratamiento | Formal / Informal | Verde (preferencia personal) |
| Modo predeterminado | Chat Normal / DeepThink | Azul (modo técnico) |
| Privacidad | No usar datos para entrenamiento | Verde |

**Comportamiento del toggle**:
- Dentro de un grupo, los toggles se comportan como botones de radio: activar uno desactiva los demás.
- Hacer clic en cualquier lugar de la fila `setting-item` activa ese toggle (no solo el elemento toggle en sí).
- Retroalimentación visual: los elementos activos obtienen un fondo de color (`#1a2e1a` verde o `#1e3a5f` azul).

**Toggle de privacidad**: Establece la cabecera `X-No-Training: true` en las solicitudes API (compatible con el mecanismo de exclusión de DeepSeek).

**Persistencia de configuración**: Toda la configuración se almacena en `localStorage` bajo la clave `deepseekSettings`. `SETTINGS_VERSION` actual: `1.7`. La función `migrateSettings()` proporciona compatibilidad retroactiva con configuraciones almacenadas más antiguas.

### Gestión de sesiones

Cada conversación se gestiona automáticamente como una sesión con nombre:

- **Formato de ID de sesión**: `YYYY-MM-DD_HHMMSS_random` (p.ej. `2026-02-16_143045_abc123`) — generado en el cliente, validado en el servidor.
- **Guardado automático**: Después de cada par de mensajes (usuario + IA), el array completo `contextHistory.messages` se guarda como archivo JSON en el servidor.
- **Formato de archivo de sesión**: `{sessionId}.json` en `/var/www/deepseek-chat/sessions/`, `chmod 600`.
- **Modal de carga del historial de chat**: Muestra todas las sesiones guardadas con ID, fecha, vista previa del mensaje y recuento de mensajes. Cada sesión tiene botones [Cargar] (verde) y [Eliminar] (rojo).
- **Comportamiento de carga**: Al cargar una sesión, el chat actual se guarda automáticamente primero, luego se restaura la sesión seleccionada con el historial completo de mensajes y reconstrucción de la interfaz.
- **Eliminación de sesión**: El archivo JSON se elimina del servidor inmediatamente.

**Scripts CGI**:
- `save-session.py` — POST: recibe `{sessionId, messages}`, valida el formato del ID, escribe JSON
- `load-session.py` — GET: devuelve lista con vistas previas; GET con `?id=`: devuelve datos completos de la sesión
- `delete-session.py` — DELETE: elimina el archivo de sesión

### Funciones de exportación

**Exportación global** (botón desplegable en la fila principal):

| Formato | Generación | Contiene |
|---------|-----------|---------|
| PDF | En el servidor (ReportLab) | Encabezado, estadísticas, tabla de contenidos, chat completo |
| Markdown | En el servidor | Estructura idéntica al PDF, con anclas Markdown |
| TXT | En el servidor | Texto plano con separadores |
| RTF | En el servidor | Formato RTF, diéresis como códigos RTF (sin biblioteca externa) |
| **Copiar al portapapeles** | **En el cliente (sin roundtrip al servidor)** | **Texto plano, formato idéntico a la exportación TXT** |

**Exportación por mensaje** (botón al pasar el cursor sobre cada mensaje):

| Formato | Generación |
|---------|-----------|
| TXT | En el cliente (JavaScript Blob, sin roundtrip al servidor) |
| Markdown | En el cliente |
| RTF | En el cliente |
| PDF | En el servidor (mensaje único enviado a `export-pdf.py`) |

**Contenido de exportación** (PDF/Markdown):
- Encabezado con nombre del servidor, IP, fecha de exportación, configuración de idioma/forma de tratamiento
- Sección de estadísticas: recuento de mensajes, modos utilizados, archivos adjuntos, tokens estimados, duración
- Tabla de contenidos con todos los mensajes
- Historial completo del chat con marcas de tiempo e indicadores de modo
- Codificación de colores por rol del mensaje y modo

**Copiar al portapapeles**: El chat completo se ensambla en el cliente en formato de texto plano y se escribe directamente en el portapapeles del sistema mediante `navigator.clipboard.writeText()`. Aparece una breve confirmación "¡Copiado!" en el botón Exportar durante 2 segundos.

**Nota técnica sobre PDF**: Los datos PDF binarios se escriben exclusivamente mediante `sys.stdout.buffer` con cabeceras HTTP codificadas como bytes — evita el error "Bad header" que ocurre al mezclar `print()` (modo texto) con salida binaria.

### Botones de feedback y registro

Cuatro botones aparecen al pasar el cursor sobre cada respuesta de la IA (parte inferior izquierda):

- **Copiar** — Copia el texto del mensaje al portapapeles; muestra "¡Copiado!" durante 2 segundos y luego se restablece.
- **Me gusta** — Marca la respuesta positivamente (resaltado en azul); envía una entrada LIKE al registro del servidor. Hacer clic de nuevo elimina el me gusta.
- **No me gusta** — Marca la respuesta negativamente (resaltado en rojo); envía una entrada DISLIKE. Me gusta y No me gusta son mutuamente excluyentes.
- **Regenerar** — Elimina la respuesta actual de la IA del contexto y el DOM, luego llama de nuevo a la API con el mismo mensaje del usuario y el historial completo anterior.

**Formato del registro en el servidor** (`multi-llm-chat.log`):
```
2026-02-17 17:30:00 | IP: 192.168.1.x | POST /cgi-bin/deepseek-api.py | Estado: 200
2026-02-17 17:30:00 | IP: 192.168.1.x | FEEDBACK | LIKE | msg_5 | "Primeros 60 chars del mensaje..."
```
**Nunca registrado**: Claves API, contenido de sesiones o texto de mensajes más allá de la vista previa de feedback de 60 caracteres.

### Visualización dinámica del contexto

El encabezado del servidor muestra cuatro líneas de información:
1. Nombre del servidor (en azul, `#4dabf7`)
2. `IP: xxx.xxx.xxx.xxx`
3. `Contexto: XX% (nombre-modelo)`
4. `Modelo: deepseek-chat, deepseek-reasoner`

**Cálculo de la utilización del contexto**:
- Tokens estimados = caracteres totales en mensajes recientes × `TOKENS_PER_CHAR` (0,25)
- Solo se cuentan los últimos N mensajes (N = `maxContextMessages` de `MODEL_CONFIG`)
- Los tokens del prompt del sistema se añaden por separado
- Porcentaje = tokens estimados / `maxContextTokens` × 100

**Sistema de advertencia**: Por encima del 90%, la línea de contexto se vuelve roja y parpadea (animación CSS, opacidad 0 → 1, ciclo de 1 segundo) — una advertencia muy visible de que la ventana de contexto está casi llena.

La visualización se actualiza automáticamente con: cada mensaje enviado, cada mensaje eliminado, cada cambio de modelo.

### Visualización de tarjeta de archivo

Cuando se carga un archivo o se adjunta texto del portapapeles, el mensaje del usuario muestra una **tarjeta de archivo** — un elemento visual compacto similar al de Claude o ChatGPT:

```
┌─────────────────────────────────────┐
│  [PDF]  │  nombre_archivo.pdf       │
│  icono  │  Documento PDF            │
└─────────────────────────────────────┘
```

- Muestra la insignia del tipo de archivo (PDF, TXT, XLSX, etc.) derivada de la extensión del archivo
- Muestra el nombre de archivo truncado (máximo 30 caracteres con `...`)
- Se aplica a: cargas de archivos reales mediante el botón de carga, texto del portapapeles adjunto como archivo (`clipboard.txt`), todos los demás formatos aceptados y grabaciones de audio
- Las grabaciones de audio muestran la insignia `AUDIO` con la etiqueta localizada (p.ej. "Grabación de audio")

### Carga de múltiples archivos

El botón de carga admite seleccionar **varios archivos a la vez**:

- Todos los archivos seleccionados se validan individualmente (verificación de formato, inspección de magic bytes, verificación de capacidad de imágenes).
- Los archivos procesables (`.txt`, `.pdf`) se procesan en secuencia; sus contenidos se combinan con un separador `---` y una cabecera `[nombre_archivo]` por archivo.
- La barra de información de archivos muestra todos los archivos separados por ` | ` en una sola línea.
- Se genera una tarjeta de archivo por archivo en el mensaje del usuario.
- Formatos aceptados: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.csv`, `.xlsx`, `.pptx`

### Grabación de audio

El cliente incluye un **botón de grabación de micrófono** integrado que permite la entrada de voz directa a modelos con capacidad de audio:

- **Botón**: `audioButton` — estilo pastilla, posicionado en la segunda fila de botones junto al botón DeepThink.
- **Visibilidad**: El botón solo se muestra cuando el modelo actualmente seleccionado admite entrada de audio. Se oculta automáticamente cuando hay un modelo sin capacidad de audio activo. Esto es controlado por `updateAudioButtonVisibility()` que se llama en cada cambio de modelo.
- **Modelos con capacidad de audio** (constante `AUDIO_CAPABLE_MODELS`):
  - **Google Gemini**: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`, `gemini-2.0-flash`
  - **OpenAI**: `gpt-4o`, `gpt-4.1`
- **Flujo de grabación**: `getUserMedia()` → API `MediaRecorder` → grabación en trozos → `Blob` ensamblado al detener → codificado en base64.
- **Tipo MIME**: `audio/webm` (Chrome/Firefox) o `audio/mp4` (Safari) — detectado automáticamente en tiempo de ejecución.
- **Tras la grabación**: Los datos de audio se muestran en el campo `fileInfo` con una tarjeta de insignia AUDIO.
- **Envío**: `audio_data` (cadena base64) y `audio_mime_type` se incluyen en el cuerpo JSON de la solicitud junto al mensaje de texto. El indicador `hasFile` **no** se establece para audio — no se inyecta ningún prompt del sistema de procesamiento de archivos.
- **Exclusión mutua**: La carga de archivos y la grabación de audio son mutuamente excluyentes. Iniciar una grabación borra cualquier archivo adjunto pendiente y viceversa.
- **Backend — Google (`google-api.py`)**: El audio se adjunta al último mensaje del usuario como bloque `inline_data` en el formato nativo de Gemini. El modelo recibe y procesa el audio directamente.
- **Backend — OpenAI (`openai-api.py`)**: El audio se adjunta al último mensaje del usuario como bloque `input_audio` en el formato de OpenAI (`format: webm` o `mp4`).
- **Regla de mantenimiento** (documentada en el manifiesto): Cada vez que un proveedor LLM integrado añade o elimina soporte de audio para un modelo, `AUDIO_CAPABLE_MODELS` en `index.html` **debe** actualizarse inmediatamente.

### Kompressor — Compresión inteligente de contexto

Cada modelo de lenguaje tiene una ventana de contexto finita. En sesiones largas — especialmente con cargas de archivos grandes, flujos de trabajo de análisis extensos o conversaciones de varias horas — el contexto se llena y provoca errores de API (400/413), obligando al usuario a iniciar un nuevo chat y perder todo el hilo de la conversación.

El **Kompressor** resuelve este problema de forma automática y transparente.

#### Concepto central

En lugar de truncar ciegamente los mensajes antiguos o forzar un reinicio manual, el Kompressor **resume** la mitad más antigua de la conversación mediante una segunda llamada LLM dedicada. Este resumen se inyecta en el prompt del sistema de las solicitudes posteriores. El modelo activo "recuerda" el pasado a través del resumen — la conversación puede continuar indefinidamente sin pérdida de contexto.

#### Umbrales de activación

| Umbral | Acción |
|--------|--------|
| **70%** de utilización del contexto | Primera ronda de compresión |
| **85%** de utilización del contexto | Segunda ronda de compresión |
| **95%** de utilización del contexto | Tercera ronda de compresión |

Cada umbral se activa como máximo una vez por sesión. Tras cada compresión, el contador se reinicia para que los umbrales puedan activarse de nuevo cuando el contexto vuelva a llenarse.

#### Proceso de compresión

1. El cliente estima la utilización del contexto tras cada mensaje enviado.
2. Si se supera un umbral, se llama a `compress-context.py` **antes** de la llamada principal a la API.
3. Se extrae el 50% más antiguo de los mensajes. El punto de corte avanza al siguiente mensaje del usuario para garantizar la compatibilidad con la API (el contexto siempre comienza con un turno del usuario).
4. Los datos base64, imágenes y contenido multimedia se filtran — solo se envía texto plano al LLM de compresión.
5. El LLM de compresión devuelve un resumen estructurado.
6. Los mensajes antiguos se reemplazan por una única entrada de resumen (indicador `compressed: true`).
7. El resumen se añade al prompt del sistema efectivo para todas las llamadas posteriores — nunca se envía como mensaje independiente (lo que causaría errores 400 en la mayoría de las APIs).
8. El contexto actualizado se guarda. La llamada principal a la API continúa con el contexto comprimido.

#### Descarte inteligente del resumen al eliminar manualmente

Cuando el usuario elimina mensajes manualmente, el Kompressor verifica si el porcentaje de contexto cae por debajo del **último umbral activado** (no solo por debajo del 70%). Si es así, el resumen de compresión se elimina automáticamente y todo el seguimiento de umbrales se reinicia — garantizando que el estado de compresión siempre corresponda al contenido real de la conversación.

#### Restricción de proveedor (solo de pago)

El Kompressor requiere una llamada LLM separada que puede implicar grandes cantidades de tokens. Los límites de tasa del nivel gratuito de Groq (6.000–12.000 TPM) y Hugging Face son insuficientes para una compresión fiable de conversaciones reales. Solo se ofrecen proveedores de pago:

| Proveedor | Modelos de compresión |
|-----------|----------------------|
| DeepSeek | `deepseek-chat`, `deepseek-reasoner` |
| OpenAI | `gpt-4o-mini`, `gpt-4o`, `gpt-4.1` |
| Google | `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro` |

**Predeterminado recomendado**: DeepSeek + `deepseek-chat` — sin límites de tasa, menor costo, resultados más fiables.

#### Archivos de resultados

Cada ronda de compresión se guarda en:
```
/var/www/deepseek-chat/kompressor/kompressor_AAAAMMDD_HHMMSS.txt
```

### Banners de crédito y límite diario

El cliente proporciona retroalimentación visual clara y persistente cuando las cuotas de la API se agotan:

**Banner rojo — "¡El crédito debe renovarse !"** (proveedores de pago):
- Se muestra cuando una API de pago informa crédito agotado
- **DeepSeek**: activado por HTTP 402
- **OpenAI**: activado por HTTP 429 + `insufficient_quota` en el cuerpo de respuesta JSON
- Permanece visible hasta que se cierra manualmente con el botón ×

**Banner azul — "¡Límite diario alcanzado !"** (proveedores de nivel gratuito):
- Se muestra cuando una API de nivel gratuito informa cuota diaria agotada
- **Google Gemini**: activado por HTTP 429 + palabras clave diarias en el cuerpo de respuesta
- **GroqCloud**: activado por HTTP 429
- **Hugging Face**: activado por HTTP 429
- Permanece visible hasta que se cierra manualmente con el botón ×

Ambos banners se implementan como elementos de posición fija en la parte superior de la ventana del navegador con un botón de cierre (×) siguiendo la convención estándar de estilo pastilla.

### Gestión de ventana de contexto excedida

Cuando la ventana de contexto del modelo activo está completamente llena y la API devuelve un error (HTTP 400 con palabras clave relacionadas con el contexto), el cliente no muestra un mensaje de error genérico. En su lugar, aparece directamente en el chat un **cuadro interactivo**:

- **Cuadro con borde azul** con el mensaje: *"Se ha alcanzado el tamaño máximo del chat del LLM actual."*
- **Botón verde**: "Iniciar nuevo chat con contexto actual" — implementa la **Opción C**:
  1. La sesión actual se guarda automáticamente
  2. El último resumen de compresión (si está disponible) se combina con todos los mensajes posteriores como texto plano
  3. Un nuevo chat comienza con este contexto combinado precargado como archivo adjunto — la conversación continúa sin interrupciones
- **Botón azul**: "Iniciar nuevo chat sin contexto" — reinicio limpio:
  1. La sesión actual se guarda automáticamente
  2. Un nuevo chat comienza con contexto vacío

Este enfoque permite **conversaciones encadenadas** a través de múltiples sesiones — teóricamente de longitud ilimitada.

Los cinco scripts proxy CGI detectan el desbordamiento de contexto mediante análisis del código de estado HTTP y coincidencia de palabras clave en el cuerpo de respuesta, devolviendo `error_type: 'context_exceeded'` al cliente.

---

### Bloque de información del proxy API (a partir del 08.03.2026)

Cada uno de los cinco scripts proxy CGI (`openai-api.py`, `deepseek-api.py`, `google-api.py`, `hugging-api.py`, `groq-api.py`) contiene un encabezado de documentación estructurado directamente después de la declaración de codificación:

- **Fecha de importación** — cuándo se actualizó el archivo por última vez
- **Versión del modelo** — versión de cada modelo/submodelo admitido
- **Ventana de contexto** — límites de tokens de entrada y salida por modelo
- **Capacidades** — Solo texto / Texto + Imágenes + Audio + Vídeo
- **Asignación gratuito/de pago** — para proveedores con distinción de nivel
- **Enlace de fuente** — documentación oficial de la API

Esto garantiza que la información del modelo sea siempre rastreable directamente en el código fuente sin consultar documentación externa.

## El script auxiliar `repo2text.sh`

Este script Bash fue desarrollado específicamente para **exportar todo el código fuente de un repositorio de GitHub como un único archivo de texto** — ideal para proporcionar el contexto completo del proyecto a un asistente de IA.

**Cómo funciona**:
- Clona el repositorio con `git clone --depth 1`.
- Analiza todos los archivos de texto (tipo MIME + `grep -Iq .`) y los escribe con separadores en un archivo de salida.
- Utiliza `sort -z -u` para deduplicar rutas de archivo antes del procesamiento — evita entradas de archivo duplicadas.
- Utiliza un delimitador único (`############ FILE: ... ############`) que no puede aparecer en el código fuente, evitando divisiones incorrectas.
- Respeta explícitamente `.gitignore` y `.gitattributes`.
- Admite los formatos de salida TXT, JSON y Markdown.
- Crea un archivo ZIP del archivo de exportación.
- Incluye metadatos: hash de commit, rama, marca de tiempo.

**Opciones especiales**:
- `--flat`: Usar solo nombres de archivo sin rutas.
- `-o, --only RUTA`: Exportar solo un subdirectorio específico.
- `-md5, --md5`: Calcular e incluir la suma de comprobación MD5 para cada archivo.
- Detección inteligente de la URL remota cuando se ejecuta dentro de un repositorio Git.
- Se admiten tanto `md5sum` (Linux) como `md5` (macOS).

**Ejemplos**:

```bash
# Exportación simple (solicitud interactiva de URL)
./repo2text.sh

# Exportación con URL como Markdown
./repo2text.sh -f md https://github.com/debian-professional/multi-llm-chat.git

# Exportar solo el directorio 'shell-scripts' con estructura plana
./repo2text.sh --flat -o shell-scripts https://github.com/debian-professional/multi-llm-chat.git

# Exportación con sumas de comprobación MD5
./repo2text.sh -md5 https://github.com/debian-professional/multi-llm-chat.git
```

**¿Por qué es útil?**
- Permite la documentación completa del proyecto en un único archivo.
- Perfecto para insertar bases de código completas en chats de IA.
- La opción MD5 ayuda a verificar la integridad de los archivos tras la exportación.

> `repo2text` también está disponible como proyecto independiente: [github.com/debian-professional/repo2text](https://github.com/debian-professional/repo2text)

---

## Arquitectura de seguridad en detalle

La seguridad fue la máxima prioridad durante todo el proyecto. Aquí están todas las medidas clave:

### 1. Clave API — Nunca expuesta al cliente
- Todas las claves API se mantienen **exclusivamente** en variables de entorno de Apache (configuradas en `/etc/apache2/envvars`).
- Cada script CGI recupera su clave mediante `os.environ.get('..._API_KEY')`.
- El cliente solo se comunica con proxies CGI locales — nunca directamente con APIs externas.
- Incluso en caso de un ataque XSS completo, las claves no podrían leerse desde la página.

### 2. Inspección de magic bytes contra archivos ejecutables
- Antes de leer cualquier archivo cargado, los primeros 20 bytes se verifican contra una base de datos de firmas completa (ver [Carga de archivos con verificación de seguridad](#carga-de-archivos-con-verificación-de-seguridad)).
- Si una firma coincide, la carga se bloquea con un mensaje de error detallado que muestra la plataforma y el formato detectados.
- Esta protección funciona incluso si los archivos maliciosos son renombrados (p.ej. `virus.exe` → `factura.pdf`).

### 3. Almacenamiento seguro de sesiones
- Directorio de sesiones: `/var/www/deepseek-chat/sessions/` — `chmod 700`
- Cada archivo de sesión: `chmod 600`
- El formato del ID de sesión se valida en el servidor — no es posible la travesía de rutas.

### 4. Registro sin datos sensibles
- El registro contiene: marcas de tiempo, direcciones IP, métodos HTTP, rutas, códigos de estado, mensajes de error.
- **Nunca registrado**: Claves API, contenido de sesiones, texto de mensajes (más allá de las vistas previas de feedback de 60 caracteres).
- Las solicitudes OPTIONS se filtran para evitar la saturación del registro.

### 5. Sin comunicación directa cliente-API
- Todas las operaciones críticas de seguridad ocurren en el servidor mediante Python CGI.
- El cliente no tiene conocimiento de credenciales de API, rutas del servidor ni ubicaciones de almacenamiento de sesiones.

### 6. Validación de entradas
- Los formatos de archivo se validan tanto por extensión como por magic bytes.
- Los IDs de sesión se validan en el servidor contra la expresión regular de formato esperada.
- El pegado del portapapeles se filtra para bloquear rutas de archivo antes de que lleguen a la API.

### 7. Seguridad en el transporte
- HTTPS se aplica mediante la configuración SSL de Apache (`deepseek-chat-ssl.conf`).
- La configuración HTTP (`deepseek-chat.conf`) está deshabilitada mediante `a2dissite`.

---

## Despliegue y uso

### Requisitos previos

- Sistema basado en Debian (o cualquier Linux con Apache, Python 3, Bash)
- Apache con módulo CGI (`a2enmod cgi`) y SSL (`a2enmod ssl`)
- Python 3 con paquetes: `reportlab`
- Para `repo2text.sh`: `jq`, `pv`, `zip`, `git`
- Una clave API válida para al menos uno de los proveedores admitidos

### Instalación

**1. Clonar el repositorio** (como usuario `source`):
```bash
git clone https://github.com/debian-professional/multi-llm-chat.git /home/source/multi-llm-chat
```

**2. Configurar las claves API**:
```bash
# Añadir a /etc/apache2/envvars:
export DEEPSEEK_API_KEY="tu-clave-api-deepseek-aquí"
export OPENAI_API_KEY="tu-clave-api-openai-aquí"
export GOOGLE_API_KEY="tu-clave-api-google-aquí"
export HF_API_KEY="tu-token-huggingface-aquí"
export GRQ_API_KEY="tu-clave-api-groqcloud-aquí"
```

**3. Activar la configuración de Apache**:
```bash
a2ensite deepseek-chat-ssl.conf
a2dissite deepseek-chat.conf   # desactivar la configuración HTTP simple
systemctl restart apache2
```

**4. Crear los directorios necesarios**:
```bash
mkdir -p /var/www/deepseek-chat/sessions
chown www-data:www-data /var/www/deepseek-chat/sessions
chmod 700 /var/www/deepseek-chat/sessions
```

**5. Ejecutar el script de despliegue** (como root):
```bash
./deploy.sh source
```

**6. Instalar los scripts auxiliares**:
```bash
./install.sh   # como root — copia deploy.sh y sync-back.sh al directorio de producción
```

### Configuración

**Configuración de modelos** (`MODEL_CONFIG` en `index.html`):
```javascript
const MODEL_CONFIG = {
    // OpenAI
    'gpt-5.4':              { maxContextTokens: 1050000, maxOutputTokens: 16384, maxContextMessages: 100 },
    'gpt-5.2-chat-latest':  { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-4o':               { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-4.1':              { maxContextTokens: 1048576, maxOutputTokens: 32768, maxContextMessages: 100 },
    'gpt-4o-mini':          { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-5-mini':           { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    // DeepSeek
    'deepseek-chat':     { maxContextTokens: 100000,  maxOutputTokens: 8192,  maxContextMessages: 50  },
    'deepseek-reasoner': { maxContextTokens: 65000,   maxOutputTokens: 32768, maxContextMessages: 30  },
    // Google Gemini
    'gemini-2.5-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.5-pro':    { maxContextTokens: 1048576, maxOutputTokens: 65536, maxContextMessages: 100 },
    'gemini-1.5-pro':    { maxContextTokens: 2097152, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.0-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    // Hugging Face
    'Qwen/Qwen2.5-72B-Instruct':               { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mistral-7B-Instruct-v0.3':      { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    'microsoft/Phi-3.5-mini-instruct':         { maxContextTokens: 128000, maxOutputTokens: 4096, maxContextMessages: 60 },
    'meta-llama/Meta-Llama-3.1-70B-Instruct':  { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'meta-llama/Meta-Llama-3.1-405B-Instruct': { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mixtral-8x7B-Instruct-v0.1':    { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    // GroqCloud
    'llama-3.3-70b-versatile':                   { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'llama-3.1-8b-instant':                      { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 },
    'meta-llama/llama-4-scout-17b-16e-instruct': { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 },
    'qwen/qwen3-32b':                            { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 },
    'moonshotai/kimi-k2-instruct-0905':          { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 }
};
const OPENAI_MODELS_FREE = ['gpt-4o-mini', 'gpt-5-mini'];
const OPENAI_MODELS_PAID = ['gpt-5.4', 'gpt-5.2-chat-latest', 'gpt-4o', 'gpt-4.1', 'gpt-4o-mini'];
const DEEPSEEK_MODELS    = ['deepseek-chat', 'deepseek-reasoner'];
const GOOGLE_MODELS_FREE = ['gemini-2.5-flash'];
const GOOGLE_MODELS_PAID = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-pro', 'gemini-2.0-flash'];
const HF_MODELS_FREE     = ['Qwen/Qwen2.5-72B-Instruct', 'mistralai/Mistral-7B-Instruct-v0.3', 'microsoft/Phi-3.5-mini-instruct'];
const HF_MODELS_PAID     = ['meta-llama/Meta-Llama-3.1-70B-Instruct', 'meta-llama/Meta-Llama-3.1-405B-Instruct', 'Qwen/Qwen2.5-72B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1'];
const GROQ_MODELS_FREE   = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'meta-llama/llama-4-scout-17b-16e-instruct', 'qwen/qwen3-32b'];
const GROQ_MODELS_PAID   = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'meta-llama/llama-4-scout-17b-16e-instruct', 'qwen/qwen3-32b', 'moonshotai/kimi-k2-instruct-0905'];
// Modelos con soporte de entrada de audio nativo (botón de grabación de micrófono)
const AUDIO_CAPABLE_MODELS = ['gemini-2.5-flash','gemini-2.5-pro','gemini-1.5-pro','gemini-2.0-flash','gpt-4o','gpt-4.1'];
```

**Configuración de claves API** (`/etc/apache2/envvars`):
```bash
export OPENAI_API_KEY="sk-proj-..."
export DEEPSEEK_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export HF_API_KEY="hf_..."
export GRQ_API_KEY="gsk_..."
```

**Configuración de idioma** (`language.xml`):
- Añadir un nuevo bloque `<language id="custom" name="..." visible="true">` para activar la ranura de idioma personalizado.
- Establecer `has_address_form="true"` para idiomas con distinción formal/informal.

### Scripts de despliegue

| Script | Función |
|--------|---------|
| `deploy.sh <usuario>` | Copia archivos de `/home/<usuario>/multi-llm-chat/var/www/deepseek-chat/` a `/var/www/deepseek-chat/`, establece permisos, recarga Apache |
| `sync-back.sh <usuario>` | Copia los archivos modificados de producción de vuelta al repositorio fuente |
| `install.sh` | Instala `deploy.sh` y `sync-back.sh` en el directorio de producción |
| `tag-release.sh` | Crea una nueva etiqueta Git con número de versión auto-incrementado (p.ej. v0.93 → v0.94) y la envía. Ejecuta `git fetch --tags` automáticamente para evitar conflictos con etiquetas remotas existentes. |

---

## Estructura del proyecto

```
/
├── etc/apache2/sites-available/
│   ├── deepseek-chat.conf              (deshabilitado — solo HTTP, redirige a HTTPS)
│   └── deepseek-chat-ssl.conf          (activo — SSL, CGI, clave API mediante envvars)
├── shell-scripts/
│   ├── repo2text.sh                    Exportar repositorio completo como archivo de texto
│   ├── deploy.sh                       Copia repositorio fuente → producción
│   ├── sync-back.sh                    Copia producción → repositorio fuente
│   ├── install.sh                      Instala scripts deploy/sync-back
│   └── tag-release.sh                  Crea y envía etiquetas de versión Git
├── var/www/deepseek-chat/
│   ├── index.html                      Aplicación principal (todo JS/CSS/HTML)
│   ├── language.xml                    Todos los textos de la interfaz en todos los idiomas (EN, DE, ES, Custom)
│   ├── manifest                        Manifiesto de diseño (todas las convenciones)
│   ├── changelog                       Historial completo de desarrollo
│   ├── files-directorys                Resumen de archivos / listado de directorios
│   ├── cgi-bin/
│   │   ├── openai-api.py              Proxy de streaming hacia la API de OpenAI
│   │   ├── deepseek-api.py            Proxy de streaming hacia la API de DeepSeek
│   │   ├── google-api.py              Proxy de streaming hacia la API de Google Gemini
│   │   ├── hugging-api.py             Proxy de streaming hacia la API de Hugging Face Inference
│   │   ├── groq-api.py                Proxy de streaming hacia la API de GroqCloud (acelerado por LPU)
│   │   ├── compress-context.py        Compresión de contexto mediante segunda llamada LLM
│   │   ├── deepseek-models.py         Consulta el endpoint /v1/models
│   │   ├── save-session.py            Guarda sesiones de chat (POST)
│   │   ├── load-session.py            Carga lista de sesiones (GET) o sesión (GET ?id=)
│   │   ├── delete-session.py          Elimina sesión (DELETE)
│   │   ├── export-pdf.py              Exportación PDF con ReportLab
│   │   ├── export-markdown.py         Exportación Markdown
│   │   ├── export-txt.py              Exportación TXT
│   │   ├── export-rtf.py              Exportación RTF (sin biblioteca externa)
│   │   ├── feedback-log.py            Registro de Me gusta/No me gusta
│   │   └── get-log.py                 Lee y devuelve el archivo de registro
│   ├── logs/                          Archivos de registro del servidor (creados automáticamente)
│   ├── kompressor/                    Archivos de resultados de compresión (creados automáticamente)
│   └── sessions/                      Archivos JSON de sesiones de chat (creados automáticamente)
```

---

## Configuración de modelos

El objeto `MODEL_CONFIG` en `index.html` es la única fuente de verdad para todos los límites específicos de cada modelo. Cubre los cinco proveedores (objeto completo en la sección Configuración).

Fuentes: [OpenAI API Docs](https://platform.openai.com/docs), [DeepSeek API Docs](https://api-docs.deepseek.com), [Google Gemini Docs](https://ai.google.dev/gemini-api/docs), [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers), [GroqCloud Docs](https://console.groq.com/docs/models) (a fecha de 19.03.2026).

---

## Manifiesto de diseño

El proyecto incluye un archivo **`manifest`** que documenta todas las decisiones de diseño y convenciones. Cada cambio en el proyecto se documenta allí. Reglas clave:

- **Todos los botones**: Solo estilo pastilla (border-radius: 20px, height: 36px) — los botones cuadrados están prohibidos.
- **Colores de botones**: Azul (`#0056b3`) para acciones, toggle oscuro/azul para modos, rojo (`#dc3545`) para destructivos, verde (`#28a745`) para constructivos.
- **Configuración**: Solo interruptores toggle — sin botones de radio, sin casillas de verificación.
- **Sin emojis** en botones ni etiquetas (excepción: el icono DeepThink ✦).
- **Sin PHP** — exclusivamente JavaScript y Python.
- **Sin frameworks JS externos** — sin Node, sin React, sin Vue.
- **Preservación del formato**: La indentación y el formato existentes en `index.html` nunca deben cambiarse.
- **`AUDIO_CAPABLE_MODELS` debe actualizarse**: Cuando un modelo gane o pierda soporte de audio, la constante debe actualizarse inmediatamente (Regla E.1 del manifiesto).
- **Los banners de cuota/límite deben implementarse**: Al añadir un nuevo proveedor LLM, el banner apropiado (rojo para de pago, azul para gratuito) debe implementarse en el script CGI y el cliente (Regla E.1 del manifiesto).
- El manifiesto es un **archivo separado** y nunca debe incrustarse en `index.html`.

---

## Limitaciones conocidas y notas técnicas

### "Perdido en el medio" — Una limitación conocida de la IA
Todos los modelos de lenguaje actuales tienden a recordar de forma fiable el contenido al **principio y al final** de un contexto largo, pero el contenido **en el medio** a veces se pasa por alto o se alucina. (Liu et al., 2023: "Lost in the Middle: How Language Models Use Long Contexts")

**Impacto práctico en este proyecto**:
- Una exportación del repositorio de ~686.000 caracteres ≈ ~171.500 tokens.
- Ventana de contexto de DeepSeek: 100.000 tokens → la exportación completa del repositorio **supera** la ventana de contexto de DeepSeek y no puede cargarse como un único archivo. El cliente bloqueará la carga con un mensaje de error claro.
- Google Gemini (contexto de 1–2 millones de tokens) puede manejar la exportación completa sin problemas.
- **Recomendación**: Al trabajar con DeepSeek u otros modelos con ventana de contexto más pequeña, cargar solo los archivos individuales relevantes en lugar de la exportación completa del repositorio.

### Caché de URL Raw de GitHub
Tras un `git push`, la nueva versión **no está disponible inmediatamente** mediante URLs `raw.githubusercontent.com` — GitHub las almacena en caché hasta 10 minutos. Esto es normal y no puede evitarse. Los archivos se almacenan correctamente en GitHub tan pronto como `git push` tiene éxito.

### Nano y Unicode — Advertencia crítica
**Nunca** edites archivos que contengan secuencias de escape Unicode (como las funciones de diéresis) usando `nano` o copiando y pegando en un terminal. Nano corrompe `\u00e4` a `M-CM-$`, que es basura binaria para JavaScript.

**El único flujo de trabajo seguro**:
1. Editar archivos localmente (VS Code, gedit, kate o cualquier editor adecuado).
2. `git add` / `git commit` / `git push` desde la máquina local.
3. En el servidor: `git pull` (en el repositorio fuente como usuario `source`).
4. Como root: `./deploy.sh source`.

### Comportamiento de pegado en Linux/X11/Firefox
En Linux con X11 y Firefox, `e.preventDefault()` en los manejadores de eventos de pegado no bloquea de forma fiable el comportamiento de pegado nativo del navegador para contenido proveniente de gestores de archivos. La solución implementada aquí (permitir el pegado, verificar el contenido en `setTimeout(0)`, limpiar si se detectan rutas de archivo) es el workaround fiable para esta limitación específica de la plataforma.

### Detección de ventana de contexto excedida
La detección del desbordamiento de contexto en los cinco scripts CGI utiliza análisis del código de estado HTTP combinado con coincidencia de palabras clave en el cuerpo de respuesta de la API. Aunque las palabras clave son lo suficientemente amplias para capturar la mayoría de las respuestas de la API, los casos extremos con mensajes de error inusuales debidos a cambios en la infraestructura del proveedor pueden no detectarse inmediatamente y recurrirían a un mensaje de error genérico.

---

## Dependencias

| Componente | Propósito | Instalación |
|------------|-----------|------------|
| Apache2 | Servidor web, soporte CGI | `apt install apache2` |
| Python 3 | Scripts CGI del servidor | `apt install python3` |
| reportlab | Exportación PDF | `pip3 install reportlab` |
| pdf.js 3.11.174 | Extracción PDF en el cliente | Cargado desde CDN (respaldo automático) |
| jq | Procesamiento JSON en `repo2text.sh` | `apt install jq` |
| pv | Visualización de progreso en `repo2text.sh` | `apt install pv` |
| git | Gestión de versiones | `apt install git` |
| zip | Creación de archivos en `repo2text.sh` | `apt install zip` |

**Sin frameworks exóticos** — todas las dependencias son paquetes estándar en un entorno Debian o se cargan desde CDNs bien establecidas.

---

## Conclusión / Por qué destaca este proyecto

Este proyecto demuestra desarrollo web de nivel profesional con un enfoque minimalista y centrado en la seguridad:

**Arquitectura**:
- Separación limpia entre cliente (HTML/JS puro) y servidor (Python CGI) sin confusión de responsabilidades.
- Clave API nunca expuesta — incluso un compromiso XSS completo no puede filtrarla.
- Cliente de archivo único (`index.html`), completamente autónomo e internamente muy modular.

**Experiencia de usuario**:
- Respuestas en streaming con latencia de primer token inferior a un segundo.
- Gestión de contexto flexible única (eliminar cualquier mensaje + todos los posteriores).
- Manejo inteligente del portapapeles para texto, imágenes y protección de rutas de archivo.
- **Grabación de audio** directamente en el navegador — entrada de micrófono para Google Gemini (todos los modelos) y OpenAI gpt-4o / gpt-4.1.
- **Kompressor** — la compresión automática de contexto permite conversaciones indefinidamente largas, independientemente del tamaño de la ventana de contexto del modelo.
- **Gestión de ventana de contexto excedida** — cuadro interactivo en el chat con transferencia inteligente de contexto entre sesiones (Opción C).
- **Banners de crédito/límite diario** — retroalimentación visual clara y persistente para crédito agotado o límite diario.
- **Copiar al portapapeles** — el chat completo exportado directamente al portapapeles del sistema con un solo clic.
- Soporte multilingüe con distinción de forma de tratamiento, cargado desde XML externo.

**Ingeniería**:
- Inspección de magic bytes que detecta malware independientemente de la extensión del nombre de archivo.
- Sistema de marcadores de posición para diéresis que resuelve una limitación fundamental de la API de DeepSeek.
- Mapa de capacidades de modelos compatible hacia adelante, listo para modelos con soporte de imágenes.
- Descarte preciso del resumen del Kompressor: el resumen se invalida cuando el contexto cae por debajo del último umbral activado tras la eliminación manual.
- Trazabilidad completa mediante Git y registro de cambios detallado.

**Herramientas**:
- `repo2text.sh` como herramienta práctica para el desarrollo asistido por IA, con delimitador único y deduplicación mediante `sort -z -u`.
- Scripts de despliegue que garantizan despliegues consistentes y con permisos correctos.
- Etiquetado de versiones para una gestión de lanzamientos limpia, con sincronización automática de etiquetas remotas.

**Para un desarrollador profesional**, este proyecto demuestra:
- **Conciencia de seguridad** — protección de claves API, detección de malware, almacenamiento seguro de sesiones.
- **Disciplina estructurada** — manifiesto, etiquetas de versión, convenciones de diseño estrictas, registro de cambios documentado.
- **Profundidad en la resolución de problemas** — comportamiento de pegado en X11, corrupción de diéresis, salida binaria PDF, "Perdido en el medio", gestión del desbordamiento de contexto.
- **Documentación completa** — tanto en línea como en archivos dedicados.

Multi-LLM Chat Client es un **ejemplo de desarrollo web profesional** — sin sobrecarga innecesaria, pero con los más altos estándares de seguridad, corrección y facilidad de uso.

---

*Última actualización: 19.03.2026*
