<!-- Source: Actividad PRO Manual 1_P5_errores_acceso_actividad_pro.md -->

# Guía de Solución para Errores de Acceso en Actividad Pro

Este documento proporciona los pasos para resolver los incidentes más comunes al intentar acceder a la aplicación Actividad Pro, específicamente los errores de 'Usuario o contraseña incorrecto' y 'Usuario bloqueado'.

## Descripción de la Pantalla

La pantalla de la aplicación muestra una alerta que impide el inicio de sesión. Se presentan dos escenarios principales, ambos identificados por un ícono de advertencia (triángulo amarillo con signo de exclamación):

1.  **Usuario o Contraseña Incorrecto:** Muestra el código de error `SSO4005F` con el mensaje: `El usuario y/o contraseña son incorrectos. Al tercer intento fallido se bloqueará la cuenta.`
2.  **Usuario Bloqueado:** Muestra el código de error `SSO4004F` con el mensaje: `La cuenta de usuario está bloqueada. Favor de solicitar su desbloqueo.`

Ambas pantallas presentan un botón de 'CERRAR'.

## Pasos a Seguir

Identifica el código de error que se te presenta y sigue las instrucciones correspondientes.

### Caso 1: Usuario o Contraseña Incorrecto (Error SSO4005F)

Este error indica que las credenciales no son correctas. Tienes un máximo de tres intentos antes de que la cuenta se bloquee.

1.  **Realiza el cambio de contraseña:** Ingresa al portal de **OKTA** para restablecer tu contraseña.
2.  **Asegura los requisitos de la contraseña:** La nueva contraseña debe cumplir obligatoriamente con las siguientes reglas:
    *   2 letras mayúsculas
    *   2 letras minúsculas
    *   2 números
    *   2 caracteres especiales (ej. `!@#$%&`)
    *   Mínimo 12 y máximo 16 caracteres en total.
3.  **Espera 20 minutos:** Una vez cambiada la contraseña, es **fundamental esperar 20 minutos** para que el cambio se sincronice correctamente con la aplicación.
4.  **Ingresa de nuevo:** Transcurrido el tiempo de espera, intenta acceder a Actividad Pro con tu nueva contraseña.

### Caso 2: Usuario Bloqueado (Error SSO4004F)

Este error aparece cuando la cuenta ya ha sido bloqueada, usualmente por superar el número de intentos fallidos.

1.  **Solicita ayuda a tu gerente:** Deberás contactar a tu gerente para que te apoye con el proceso de desbloqueo.
2.  **Levanta un caso en Promesa:** Tu gerente debe generar un caso en el sistema **Promesa**, específicamente en la sección **'Desbloqueo CUSP'**.
3.  **Espera la confirmación:** Una vez que el caso sea resuelto y se te confirme el desbloqueo, podrás intentar acceder de nuevo.
4.  **Ingresa a la App:** Accede a Actividad Pro utilizando tu contraseña vigente de OKTA. Si no la recuerdas o no estás seguro, es recomendable que primero realices el cambio siguiendo los pasos del Caso 1 para evitar un nuevo bloqueo.

## Errores Posibles y Consideraciones

*   **Bloqueo por no esperar:** Si cambias tu contraseña en OKTA e intentas iniciar sesión antes de que pasen los 20 minutos, es muy probable que la app rechace el intento y cuente como un intento fallido, acercándote al bloqueo de cuenta.
*   **El desbloqueo no es instantáneo:** El proceso de desbloqueo a través de un caso en Promesa depende del tiempo de atención del equipo correspondiente. Mantén comunicación con tu gerente para conocer el estatus.