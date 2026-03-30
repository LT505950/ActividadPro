<!-- Source: Actividad PRO Manual 1_P11_actividad_pro_validacion_curp_contacto.md -->

# Registro de Contacto: Validación de CURP

Guía para la validación de CURP al dar de alta un nuevo prospecto o referido en la aplicación Actividad Pro.

## Descripción de la Pantalla

La pantalla muestra un paso intermedio en el flujo de captura de un nuevo contacto. Específicamente, se observa una ventana emergente (modal) titulada **"Autenticación IMSS"** sobre la sección de "Contactos - Prospectos".

Esta ventana contiene:
- Un campo de texto obligatorio para ingresar la **CURP** (Clave Única de Registro de Población), con un indicador de que debe contener 18 caracteres.
- Un botón de acción principal con el texto **"VALIDAR"**.

Este paso es crucial para verificar que la persona que se intenta registrar no sea ya cliente o no exista en los registros nacionales.

## Pasos a Seguir

Contexto: Has llegado a esta pantalla después de seleccionar la opción para agregar un nuevo prospecto o referido.

1.  **Ingresar CURP**: En la ventana emergente "Autenticación IMSS", introduce la CURP de 18 caracteres de tu contacto en el campo correspondiente.
2.  **Verificar**: Asegúrate de que la CURP introducida sea correcta y no contenga errores de escritura.
3.  **Validar**: Presiona el botón azul **"VALIDAR"**.
4.  **Continuar**: Si la validación es exitosa, el sistema te permitirá continuar con el registro de los datos del contacto. Si falla, mostrará un mensaje de error.

## Posibles Errores y Soluciones

Durante el proceso de validación, podrías encontrar los siguientes errores:

- **"El CURP ya pertenece a un cliente Profuturo"**: 
  - **Causa**: La persona que intentas registrar ya es cliente.
  - **Solución**: No puedes registrarlo como nuevo prospecto. Debes buscarlo en tu cartera de clientes para gestionar su cuenta.

- **"CURP inexistente en RENAPO"**: 
  - **Causa**: La CURP ingresada no es válida o no existe en el Registro Nacional de Población.
  - **Solución**: Verifica que la CURP sea correcta con tu contacto. Si el error persiste, el contacto deberá regularizar su situación ante RENAPO.

- **"El contacto ya existe en tu cartera"**:
  - **Causa**: Ya has registrado previamente a esta persona como prospecto o referido.
  - **Solución**: Búscalo en tu lista de contactos existente para darle seguimiento. No es necesario registrarlo de nuevo.

- **Error de conexión**: 
  - **Causa**: Problemas con tu conexión a internet o con los servicios de validación.
  - **Solución**: Revisa tu conexión a internet (Wi-Fi o datos móviles) e inténtalo de nuevo.

<!-- Source: Actividad PRO Manual 1_P12_autenticacion_prospecto_envio_token.md -->

# Autenticación de Prospecto y Envío de Token

## Descripción de la Pantalla
La pantalla muestra el flujo de "Autenticación Prospecto" dentro de la aplicación Actividad Pro. Es un proceso de 5 pasos indicado por una barra de progreso superior (`Paso 1: Tipo Trabajador` a `Paso 5: Validar Token`). Las capturas detallan desde el ingreso de la CURP hasta la validación de un token de seguridad. Cada acción se presenta en una ventana modal sobre la pantalla principal, guiando al usuario a través de:

1.  **Captura de CURP:** Un campo para ingresar la CURP de 18 caracteres.
2.  **Selección de Medio:** Botones para elegir si el token se enviará por 'EMAIL' o 'SMS'.
3.  **Ingreso de Contacto:** Un campo para escribir el número de teléfono o email del prospecto.
4.  **Captura de Token:** Seis casillas para ingresar el código de verificación recibido.

## Pasos a Seguir
Esta guía asume que ya has completado el "Paso 1: Tipo Trabajador".

1.  **Ingresar CURP:** En la ventana "Autenticación IMSS", introduce la CURP de 18 caracteres del prospecto en el campo designado. Presiona **Siguiente**.
2.  **Seleccionar Medio de Envío:** Aparecerá la ventana "Seleccione Medio de Autenticación". Elige el método por el cual el prospecto prefiere recibir el código de seguridad: **EMAIL** o **SMS**.
3.  **Proporcionar Contacto:**
    *   Si seleccionaste **SMS**, ingresa el número de teléfono celular del prospecto a 10 dígitos.
    *   Si seleccionaste **EMAIL**, ingresa la dirección de correo electrónico del prospecto.
4.  **Enviar y Capturar Token:** Presiona **Siguiente**. El sistema enviará un código de 6 dígitos al medio seleccionado. Solicita el código al prospecto e ingrésalo en las casillas de la pantalla "Ingrese el código".
5.  **Validar:** Presiona **Siguiente** para validar el token y completar la autenticación del prospecto.

## Posibles Errores y Soluciones
- **Error de CURP:** Si el sistema indica que la CURP es inválida o ya está registrada, verifica que la hayas escrito correctamente. Si el problema persiste, puede que necesites escalar el caso.
- **Token no recibido:** Si el prospecto no recibe el código, puedes usar la opción **"Reenviar código"** que se activa después de un tiempo. Asegúrate también de que el número de teléfono o email sea correcto.
- **Cambiar método de envío:** Si el prospecto no tiene acceso al medio de contacto que seleccionaste inicialmente, utiliza la opción **"Cambiar Origen"** en la pantalla de captura de token para volver y elegir el otro método.
- **Token incorrecto o expirado:** El código tiene un tiempo de vida limitado (indicado por el contador). Si ingresas un código erróneo o si este expira, deberás solicitar uno nuevo.

<!-- Source: Actividad PRO Manual 1_P13_ingreso_token_contacto_actividad_pro.md -->

# Ingreso de Código (Token) de Contacto

## Descripción de la Pantalla

La pantalla muestra una ventana emergente (modal) dentro de la aplicación "Actividad Pro", específicamente en el paso "Contacto" del flujo de captura. El propósito es validar la información del prospecto mediante un código de seguridad.

Visualmente, contiene:
- **Título:** "Ingrese el código".
- **Campos de entrada:** Seis casillas para ingresar un código numérico.
- **Botón de acción:** Un botón azul con la etiqueta "CONTINUAR".
- **Opciones adicionales:**
  - **Reenviar código:** Un enlace que indica el método de envío actual (ej. EMAIL) y un contador para poder solicitar un nuevo código.
  - **Cambiar Origen:** Un enlace que permite modificar el método por el cual el prospecto recibe el código (ej. cambiar de EMAIL a SMS).

## Contexto

Esta pantalla aparece después de que has introducido los datos de contacto de un nuevo prospecto y has solicitado el envío de un token de verificación para validar dicha información. El token tiene una vigencia de 24 horas, durante las cuales puedes capturar múltiples prospectos.

## Pasos a Seguir

1.  **Solicita al prospecto** el código de 6 dígitos que recibió en el medio de contacto que registraste (ej. correo electrónico o SMS).
2.  **Ingresa el código** en las seis casillas que aparecen en la pantalla.
3.  Una vez completado el código, presiona el botón **"CONTINUAR"** para validar al prospecto.
4.  Si el prospecto no recibió el código o se demoró, utiliza la opción **"Reenviar código"** una vez que el contador llegue a cero.
5.  Si el medio de contacto registrado es incorrecto o el prospecto prefiere otro, selecciona **"Cambiar Origen"** para modificar el método de envío y mandar un nuevo token.

## Errores Comunes y Soluciones

- **Error: "Código incorrecto"**
  - **Causa:** El código introducido no coincide con el enviado.
  - **Solución:** Verifica nuevamente el código con el prospecto y vuelve a introducirlo con cuidado.

- **Problema: El prospecto no recibe el código.**
  - **Causa:** El dato de contacto (email/teléfono) puede ser incorrecto, o puede haber un retraso en la entrega por parte del proveedor de servicio (email, SMS).
  - **Solución:** Primero, confirma con el prospecto que el dato de contacto es correcto. Puedes usar "Cambiar Origen" para corregirlo. Si el dato es correcto, utiliza el enlace "Reenviar código" para intentar un nuevo envío.

- **Problema: El código ha expirado.**
  - **Causa:** El código específico para la captura puede tener una ventana de tiempo de uso más corta que la vigencia general del token del asesor.
  - **Solución:** Utiliza la opción "Reenviar código" para generar uno nuevo y válido para el prospecto.

<!-- Source: Actividad PRO Manual 1_P14_protocolo_envio_token_actividad_pro.md -->

# Guía de Envío de Token en Actividad Pro

Esta guía detalla el protocolo para enviar un token de validación al cliente a través de SMS o correo electrónico durante el flujo de captura en la aplicación Actividad Pro.

## Descripción de la Pantalla

La pantalla presenta el "Protocolo envío token" como parte del paso de "Contacto" en el flujo de captura. Ofrece dos métodos de envío paralelos: **Token SMS** y **Token MAIL**. Cada método se divide en tres fases con instrucciones específicas:
- **Antes:** Acciones de verificación previas al envío.
- **Durante:** Pasos a seguir si el token no llega inmediatamente.
- **Finalmente:** Instrucciones para la correcta validación del token recibido.

## Pasos a Seguir

Este proceso ocurre después de haber completado el paso de "Acceso" y te encuentras en la sección de "Contacto" con el cliente.

1.  **Verificación Inicial (Antes de enviar):**
    *   **Para Token SMS:** Confirma con el cliente que el número de celular registrado es correcto y que tiene acceso al dispositivo para recibir el mensaje.
    *   **Para Token MAIL:** Verifica que la dirección de correo electrónico del cliente sea correcta, no contenga espacios y que el cliente pueda acceder a su bandeja de entrada.

2.  **Manejo de Incidencias (Durante el envío):**
    *   **Si el SMS no llega:**
        *   Espera **siempre 3 minutos** antes de intentar un nuevo envío.
        *   Si el primer intento falla, solicita al cliente que **reinicie su celular** antes de que envíes el segundo SMS.
        *   **Importante:** Después del tercer intento fallido por SMS, la aplicación cambiará automáticamente al método de envío por correo electrónico.
    *   **Si el Mail no llega:**
        *   El sistema de correo es robusto y el email siempre es enviado.
        *   Indica al cliente que revise todas sus carpetas: **bandeja de entrada, correo no deseado (spam), promociones, publicidad, etc.**

3.  **Validación Final (Cuando el cliente recibe el token):**
    *   Asegúrate de que el token recibido sea de **6 posiciones**.
    *   Recuerda al cliente que debe utilizar **siempre el último token** que le haya llegado, ya que los anteriores se invalidan automáticamente.

## Posibles Errores y Soluciones

*   **Error: Token no recibido por SMS.**
    *   **Causa:** Mala señal, celular reiniciándose, problemas con la operadora telefónica del cliente.
    *   **Solución:** Seguir el protocolo: esperar 3 minutos, solicitar reinicio del celular y reintentar. Si falla 3 veces, el sistema usará el método de email.

*   **Error: Token no encontrado por Mail.**
    *   **Causa:** El correo fue filtrado a una carpeta secundaria (spam, promociones, etc.).
    *   **Solución:** Pedir al cliente que realice una búsqueda exhaustiva en todas las carpetas de su servicio de correo electrónico.

*   **Error: Token inválido.**
    *   **Causa:** El cliente está introduciendo un token anterior porque solicitó varios.
    *   **Solución:** Enfatizar que debe usar el token más reciente que recibió.

<!-- Source: Actividad PRO Manual 1_P15_captura_datos_complementarios_prospecto.md -->

# Guía: Captura de Datos Complementarios del Prospecto

## Descripción de la Pantalla

La pantalla forma parte del flujo de "Captura - Contacto". Tras validar exitosamente un código por SMS, se te presentará un formulario para completar los datos de un nuevo prospecto o referido.

1.  **Pantalla Izquierda (Validación Exitosa):** Muestra un ícono de check verde con el mensaje "Código de SMS correcto". Indica que el paso anterior de verificación se completó satisfactoriamente.
2.  **Pantalla Derecha (Datos Personales del Prospecto):** Es un formulario titulado "Nuevo registro". Contiene campos como Nombre(s), Apellidos, Correo, CURP, Celular, Nss y Nombre de la Empresa. Varios de estos campos ya vienen prellenados gracias a una consulta a RENAPO. Tu objetivo es llenar la información faltante.

## Pasos a Seguir

1.  Después de la pantalla de "Validación exitosa", la aplicación te dirigirá automáticamente al formulario "Datos personales del prospecto". Si no es automático, presiona el botón "CERRAR".
2.  Verifica que los datos autocompletados (Nombre, Apellidos) sean correctos. Estos se obtienen de la CURP que proporcionaste previamente.
3.  Procede a llenar los campos pendientes que están marcados con un asterisco (`*`), como el `Nss` (Número de Seguridad Social) y el `Nombre de la Empresa`.
4.  **Importante:** Si estás registrando un "Referido", el proceso podría requerir que captures también la CURP de la persona que lo refirió.
5.  Una vez que hayas completado toda la información requerida, presiona el botón "GUARDAR" en la parte inferior para registrar al prospecto y continuar con el flujo.

## Posibles Errores y Soluciones

*   **Datos Incorrectos o Faltantes:** Si omites un campo obligatorio o introduces información en un formato incorrecto (ej. un NSS inválido), la aplicación te mostrará un ícono de error (un círculo rojo con un guion o un triángulo amarillo de advertencia) junto a un mensaje descriptivo. Revisa los campos señalados, corrige la información y vuelve a intentar guardar.
*   **Error de Conexión:** Si no tienes una conexión a internet estable, es posible que no puedas guardar el registro. Asegúrate de tener buena señal de Wi-Fi o datos móviles.
*   **Datos de RENAPO incorrectos:** En raras ocasiones, los datos devueltos por RENAPO pueden ser incorrectos. Si el nombre o apellidos no coinciden con los del cliente, deberás verificar que la CURP introducida en el paso anterior sea la correcta.

<!-- Source: Actividad PRO Manual 1_P29_guia_flujo_captura_y_registro_cliente.md -->

# Guía: Flujo de Captura y Registro de Cliente

Esta guía detalla el proceso de registro de un nuevo cliente en la aplicación Actividad Pro, específicamente el paso de captura de datos y los posibles resultados.

## Descripción de la Pantalla

Después de seleccionar el tipo de trabajador e ingresar la CURP para autenticar, se presenta la pantalla **"Nuevo Registro"**, con el subtítulo **"Datos personales del cliente"**. 

Es un formulario que solicita la siguiente información:
- **Nombre(s)**
- **Primer Apellido**
- **Segundo Apellido**
- **Correo del Cliente**
- **CURP**: Este campo viene pre-llenado del paso anterior.
- **Celular**
- **NISP** (Número de Identificación de Servicio Personal)
- **Nombre Empresa**
- **Comentario 1, 2, 3**: Campos opcionales para notas.

## Pasos a Seguir

1.  **Verificar Datos**: Confirma que la CURP pre-llenada es la correcta.
2.  **Completar Formulario**: Rellena todos los campos obligatorios con la información del cliente. Es crucial que los datos sean exactos.
3.  **Guardar Registro**: Una vez completado el formulario, presiona el botón para guardar y finalizar el registro (ej. "Guardar", "Siguiente" o similar).

## Resultados Posibles

Al enviar el formulario, el sistema validará la información y te mostrará uno de los siguientes resultados:

### 1. Registro Correcto
- **Mensaje**: "Cliente dado de alta exitosamente", acompañado de un ícono de verificación (✔) verde.
- **Acción**: El proceso ha finalizado con éxito. Presiona **"CERRAR"** para volver a la pantalla principal.

### 2. Error: El cliente ya está registrado
- **Mensaje**: "La CURP ya se encuentra dada de alta en la base de Clientes", con un ícono de advertencia (❗).
- **Causa**: El cliente que intentas registrar ya existe en el sistema.
- **Acción**: No puedes duplicar el registro. Presiona **"CERRAR"** y busca al cliente por su CURP para realizar el trámite que necesites.

### 3. Error: La CURP no es de un cliente Profuturo
- **Mensaje**: "La CURP capturada aún no es cliente Profuturo, valida la información", con un ícono de advertencia (❗).
- **Causa**: La CURP ingresada en el paso anterior no está asociada a un cliente de Profuturo, por lo que no se puede proceder con el registro en esta modalidad.
- **Acción**: Presiona **"CERRAR"**. Debes validar con el cliente si la CURP es correcta y confirmar su estatus en la Afore.