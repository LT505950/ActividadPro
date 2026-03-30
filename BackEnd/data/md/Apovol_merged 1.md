<!-- Source: Actividad PRO Manual 1_P31_consulta_y_registro_apovol_actividad_pro.md -->

# Guía para Consulta y Registro de Apovol

Este documento describe el flujo para consultar, registrar o modificar el Ahorro Voluntario (Apovol) de un cliente a través de la aplicación Actividad Pro.

## Descripción de la Pantalla

La pantalla inicial es la lista de "Clientes". Es una tabla que muestra información clave de cada cliente, incluyendo las columnas CURP, EDR, NRP y una columna específica llamada "Apovol". En esta última columna, un indicador de estatus circular y de color (ej. azul, naranja) señala si el cliente tiene Apovol activo o si se puede registrar uno nuevo. Este indicador es el punto de partida del flujo.

## Pasos a Seguir

Este procedimiento se realiza después de haber localizado al cliente en la lista principal.

1.  **Iniciar Consulta:** En la fila del cliente deseado, presiona sobre el indicador circular de color ubicado en la columna "Apovol".
2.  **Autenticar Cliente:** Se abrirá una ventana emergente para la "Autenticación Cliente". El sistema te pedirá validar la identidad del cliente.
3.  **Seleccionar Medio de Contacto:** Escoge el medio de autenticación a utilizar: **EMAIL** o **SMS**, según los datos previamente registrados del cliente.
4.  **Ingresar Datos y Validar Token:** Proporciona el dato de contacto (email o teléfono) y sigue los pasos para enviar y validar el token de seguridad que el cliente recibirá.
5.  **Completar Formulario de Detalle:** Una vez autenticado, se mostrará el formulario "Detalle Apovol". Debes completar o verificar los siguientes campos:
    *   **Fondo:** Selecciona el fondo de inversión correspondiente.
    *   **Origen:** Indica el origen de los recursos.
    *   **Periodicidad:** Define la frecuencia de la aportación voluntaria.
    *   **Monto:** Ingresa el importe numérico de la aportación.
6.  **Guardar Registro:** Presiona el botón **GUARDAR** para registrar la información en el sistema.
7.  **Visualizar Estatus:** La aplicación te redirigirá a la pantalla "Historial Apovol", donde podrás ver un resumen del registro, su estatus (ej. "REGISTRADO") y la fecha de la operación. Desde esta pantalla también tienes la opción de **MODIFICAR** el registro si es necesario.

## Errores Comunes y Soluciones

*   **El indicador Apovol no se sincroniza o está deshabilitado:** Asegúrate de tener una conexión a internet estable. Si el problema persiste, puede ser un fallo de sincronización temporal con los servidores. Intenta reiniciar la aplicación o inténtalo de nuevo más tarde.
*   **Fallo en la autenticación:** Verifica que el correo o teléfono ingresado sea exactamente el que el cliente tiene registrado. Si el cliente no recibe el token, pídele que revise su carpeta de spam (correo no deseado) o que verifique tener señal en su dispositivo móvil.
*   **Error al guardar el formulario:** Revisa que todos los campos obligatorios estén completos y que el formato del monto sea correcto (sin símbolos ni comas). Un error persistente puede deberse a una intermitencia en la red.

<!-- Source: Actividad PRO Manual 1_P32_guia_estatus_apovol.md -->

# Guía de Estatus de Apovol en Actividad Pro

Esta guía te ayuda a comprender y gestionar los diferentes estatus del proceso de Apovol (Aportación Voluntaria) para tus clientes dentro de la aplicación Actividad Pro.

## Descripción de la Pantalla

La pantalla informativa muestra el flujo de captura de un cliente, destacando la etapa de **APOVOL**. Presenta un sistema de semáforo con códigos de color para identificar rápidamente el estado del registro de Apovol de un cliente. Además, incluye ejemplos visuales de los escenarios más comunes: aplicado, rechazado y no identificado.

**Flujo de Proceso:**
`Modulo Cliente` > `Registra Clientes` > `Notas` > **`APOVOL`** > `Gerente`

## Pasos para Interpretar el Estatus

Después de haber registrado los datos iniciales de un nuevo cliente, el sistema procesará su solicitud de Apovol. Sigue estos pasos para verificar y entender el resultado:

1.  **Ubica al cliente:** Busca al cliente dentro de tu módulo de gestión en Actividad Pro.
2.  **Identifica el ícono de estatus:** Localiza el ícono de color (semáforo) asociado al registro de Apovol del cliente.
3.  **Interpreta el color:** Utiliza la siguiente leyenda para entender qué significa cada estatus:

    *   ⚪️ **Sin registro de Apovol:** Aún no se ha iniciado el proceso para este cliente.
    *   🔵 **Apovol Registrado o Aceptado:** La solicitud se envió correctamente y está en proceso de validación.
    *   🔷 **Apovol Aplicado:** ¡Éxito! La aportación voluntaria fue procesada y aplicada correctamente. Este es el estado final deseado.
    *   🔴 **Apovol Rechazado:** La solicitud fue rechazada. Es necesario revisar la información o contactar al cliente.
    *   🟡 **Apovol No Identificado:** El sistema no puede determinar el estatus. Generalmente es un problema de sincronización.

4.  **Actúa según el estatus:**
    *   Si el estatus es **Aplicado**, el proceso para esta etapa concluyó exitosamente.
    *   Si es **Rechazado** o **No Identificado**, consulta la sección de "Posibles Errores" a continuación.

## Posibles Errores y Soluciones

*   **Error: Estatus `Apovol Rechazado` (Rojo)**
    *   **Causa:** Puede deberse a datos incorrectos en el registro, inconsistencias en la información del cliente o incumplimiento de algún requisito.
    *   **Solución:** Verifica toda la información que registraste. Si no encuentras errores, podría ser necesario contactar al cliente para validar sus datos. Si el problema persiste, escala el caso al área de soporte correspondiente.

*   **Error: Estatus `Apovol No Identificado` (Amarillo)**
    *   **Causa:** La causa más común es que la aplicación no se ha sincronizado con los servidores después de registrar al cliente. Sin la sincronización, la app no puede obtener el estatus actualizado.
    *   **Solución:** Asegúrate de tener una conexión a internet estable (Wi-Fi o datos móviles) y ejecuta el proceso de sincronización de la aplicación. El estatus debería actualizarse a "Aplicado" o "Rechazado" después de una sincronización exitosa.

*   **Problema: El estatus permanece en `Registrado/Aceptado` por mucho tiempo.**
    *   **Causa:** Puede existir un retraso en el procesamiento del lado del servidor.
    *   **Solución:** Espera un tiempo prudente (consulta los SLAs definidos). Si el estatus no cambia después de un periodo extendido, reporta el caso a soporte técnico para su revisión.

<!-- Source: Actividad PRO Manual 1_P33_reglas_captura_apovol.md -->

# Guía de Captura APOVOL: Consideraciones Importantes

Este documento describe las reglas y consideraciones clave al llegar a la sección de APOVOL dentro del flujo de captura de clientes en la aplicación Actividad Pro.

## Descripción de la Pantalla

La pantalla es una diapositiva informativa titulada "Flujo de captura – Consideraciones de importantes". En la parte superior, se muestra un diagrama de flujo del proceso: `Módulo Cliente` > `Registra Clientes` > `Notas` > `APOVOL` > `Gerente`, con la etapa "APOVOL" resaltada en color amarillo.

El cuerpo de la pantalla contiene una sección principal llamada "Reglas", que enumera con viñetas una serie de puntos cruciales a tener en cuenta durante este paso del proceso.

## Pasos y Consideraciones

Contexto: Has completado los pasos de 'Módulo Cliente', 'Registra Clientes' y 'Notas'. Ahora te encuentras en la etapa de registro de APOVOL. Sigue estas indicaciones para asegurar un proceso exitoso.

1.  **Verifica la Información**: Antes de enviar, revisa cuidadosamente todos los datos ingresados en el formulario Apovol. Es fundamental que toda la información sea **correcta** para evitar rechazos.

2.  **Consulta el Estatus del Trámite**: Si la cuenta bancaria del cliente está en proceso de certificación, el estatus del registro Apovol aparecerá como **'Registrado'**. Para conocer el estado actualizado y real del trámite, debes usar la función **Actualizar (Sincronizar)** en la aplicación.

3.  **Registro de EDR**: Ten en cuenta que el registro de EDR (Expediente de Rendimiento) para clientes ahora se realiza **exclusivamente** a través de este módulo en Actividad Pro, sustituyendo a las antiguas Power Apps.

4.  **Exclusividad del Módulo**: Es importante saber que ningún servicio registrado a través de este módulo (EDR, NRP, registro de Apovol) será considerado para esquemas o rankings de productividad.

## Errores Posibles y Puntos Clave

*   **Error de Datos**: Ingresar información incorrecta en el formulario puede causar el rechazo del trámite y generar retrasos significativos para el cliente y el asesor.
*   **Estatus Desactualizado**: No usar la función "Actualizar (Sincronizar)" puede llevar a una mala interpretación del estado del trámite, creyendo que sigue 'Registrado' cuando ya pudo haber sido procesado o rechazado.
*   **Uso de Canales Incorrectos**: Intentar registrar el EDR de clientes en las Power Apps anteriores resultará en un fallo, ya que ese canal ha sido descontinuado para esta función.
*   **Confusión sobre Incentivos**: Asumir que los registros en este módulo contarán para rankings o esquemas de comisiones, lo cual es incorrecto según las reglas establecidas.