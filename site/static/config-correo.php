<?php
/**
 * Configuración OPCIONAL del correo del formulario.
 *
 * Por defecto el sitio usa mail() de Hostinger y no necesitas tocar nada.
 * Si los correos llegan a spam o no llegan, crea en Hostinger el buzón
 * no-reply@integralgymtech.com y escribe aquí su contraseña para enviar por SMTP.
 */
return [
    'remitente'        => 'no-reply@integralgymtech.com',
    'nombre_remitente' => 'Sitio web Integral Gym Tech',
    'smtp' => [
        'host' => '',                 // ej. 'smtp.hostinger.com'  (vacío = usar mail())
        'port' => 465,                // 465 (SSL) o 587 (STARTTLS)
        'user' => 'no-reply@integralgymtech.com',
        'pass' => '',
    ],
];
