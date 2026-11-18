<?php
/**
 * Integral Gym Tech – procesa el formulario de contacto y envía el correo.
 *
 * Funciona con la función mail() de Hostinger. Si se configuran los datos SMTP
 * en config-correo.php (opcional), se usa SMTP autenticado para mejor entrega.
 */

declare(strict_types=1);

// ------------------------------------------------------------------ configuración
$DESTINATARIOS = [
    'gerencia@integralgymtech.com',
    'gerenciamkt@mediamaster.mx',
    'traffickermkt@mediamaster.mx',
    'programacionmkt@mediamaster.mx',
];
$REMITENTE        = 'no-reply@integralgymtech.com'; // debe ser un correo del dominio
$NOMBRE_REMITENTE = 'Sitio web Integral Gym Tech';
$SMTP = null; // opcional: ver config-correo.php
if (is_file(__DIR__ . '/config-correo.php')) {
    $cfg = require __DIR__ . '/config-correo.php';
    if (is_array($cfg)) {
        $REMITENTE        = $cfg['remitente'] ?? $REMITENTE;
        $NOMBRE_REMITENTE = $cfg['nombre_remitente'] ?? $NOMBRE_REMITENTE;
        $SMTP             = !empty($cfg['smtp']['host']) ? $cfg['smtp'] : null;
    }
}

// ------------------------------------------------------------------ utilidades
$esAjax = isset($_POST['ajax']) || (isset($_SERVER['HTTP_ACCEPT']) && str_contains($_SERVER['HTTP_ACCEPT'], 'application/json'));

function responder(bool $ok, array $extra = [], int $code = 200): void
{
    global $esAjax;
    if ($esAjax) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok] + $extra, JSON_UNESCAPED_UNICODE);
    } else {
        $volver = $_SERVER['HTTP_REFERER'] ?? '/';
        $volver = preg_replace('/[?#].*$/', '', $volver);
        header('Location: ' . $volver . ($ok ? '?enviado=1#contacto' : '?error=1#contacto'), true, 303);
    }
    exit;
}

function limpiar(string $k, int $max = 400): string
{
    $v = isset($_POST[$k]) ? (string) $_POST[$k] : '';
    $v = trim(str_replace(["\r", "\0"], '', $v));
    return mb_substr($v, 0, $max);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /', true, 302);
    exit;
}

// ------------------------------------------------------------------ anti-spam
if (limpiar('website') !== '') {               // honeypot
    responder(true);
}
$ts = (int) limpiar('ts', 20);
if ($ts > 0 && (time() * 1000 - $ts) < 3000) {   // enviado en menos de 3 s
    responder(true);
}
// límite simple: 5 envíos por IP cada 10 minutos
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$rateFile = sys_get_temp_dir() . '/igt_form_' . md5($ip);
$hits = array_filter(
    is_file($rateFile) ? (array) json_decode((string) file_get_contents($rateFile), true) : [],
    fn($t) => $t > time() - 600
);
if (count($hits) >= 5) {
    responder(false, ['message' => 'Has enviado varios mensajes seguidos. Intenta de nuevo en unos minutos.'], 429);
}
$hits[] = time();
@file_put_contents($rateFile, json_encode(array_values($hits)));

// ------------------------------------------------------------------ datos
$nombre   = limpiar('your-name');
$correo   = limpiar('your-email');
$telefono = limpiar('your-tel', 40);
$asunto   = limpiar('your-subject');
$proyecto = limpiar('select-100');
$mensaje  = limpiar('textarea-823', 2000);
$pagina   = trim(preg_replace('/[^a-z0-9\-\/]/', '', limpiar('pagina', 120)), '/');
$productos = limpiar('productos', 4000);

$errores = [];
if ($nombre === '')   $errores['your-name']  = 'Por favor, completa este campo.';
if (!filter_var($correo, FILTER_VALIDATE_EMAIL)) $errores['your-email'] = 'Ingresa un correo electrónico válido.';
if (strlen(preg_replace('/\D/', '', $telefono)) < 8) $errores['your-tel'] = 'Ingresa un número de teléfono válido.';
if ($proyecto === '') $errores['select-100'] = 'Por favor, completa este campo.';
if ($errores) {
    responder(false, ['errors' => $errores], 422);
}

// ------------------------------------------------------------------ correo
$h = fn(string $s): string => nl2br(htmlspecialchars($s, ENT_QUOTES, 'UTF-8'));
$urlPagina = 'https://integralgymtech.com/' . ($pagina && $pagina !== 'index' ? $pagina . '/' : '');
$fecha = (new DateTime('now', new DateTimeZone('America/Mexico_City')))->format('d/m/Y H:i');

$filas = [
    'Nombre'           => $nombre,
    'Correo'           => $correo,
    'Teléfono'         => $telefono,
    'Asunto'           => $asunto !== '' ? $asunto : '—',
    'Tipo de proyecto' => $proyecto,
    'Productos'        => $productos !== '' ? $productos : '—',
    'Mensaje'          => $mensaje !== '' ? $mensaje : '—',
    'Página'           => $urlPagina,
    'Fecha'            => $fecha . ' (hora del centro de México)',
];
$html = '<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:auto;border:1px solid #eee">'
    . '<div style="background:#000;padding:20px;text-align:center"><img src="https://integralgymtech.com/assets/uploads/2023/08/Logo.png" alt="Integral Gym Tech" style="max-width:180px"></div>'
    . '<div style="background:#ec3e20;color:#fff;padding:14px 20px;font-size:18px;font-weight:bold">Nueva solicitud de cotización</div>'
    . '<table style="width:100%;border-collapse:collapse;font-size:14px">';
foreach ($filas as $k => $v) {
    $html .= '<tr><td style="padding:10px 20px;border-bottom:1px solid #eee;width:150px;color:#555"><strong>' . $h($k) . '</strong></td>'
        . '<td style="padding:10px 20px;border-bottom:1px solid #eee;color:#111">' . $h($v) . '</td></tr>';
}
$html .= '</table><p style="padding:14px 20px;color:#888;font-size:12px">Mensaje enviado desde el formulario de integralgymtech.com. Responde a este correo para contestar directamente al cliente.</p></div>';

$texto = "Nueva solicitud de cotización\n\n";
foreach ($filas as $k => $v) {
    $texto .= "$k: $v\n";
}

$tituloCorreo = $productos !== '' ? 'Cotización de productos: ' . $nombre : 'Nueva cotización web: ' . $nombre . ($proyecto ? ' – ' . $proyecto : '');

$enviado = $SMTP
    ? enviarSmtp($SMTP, $REMITENTE, $NOMBRE_REMITENTE, $DESTINATARIOS, $correo, $nombre, $tituloCorreo, $html, $texto)
    : enviarMail($REMITENTE, $NOMBRE_REMITENTE, $DESTINATARIOS, $correo, $nombre, $tituloCorreo, $html, $texto);

if (!$enviado) {
    error_log('IGT formulario: fallo al enviar correo de ' . $correo);
    responder(false, ['message' => 'No pudimos enviar tu mensaje en este momento. Escríbenos por WhatsApp al 442 127 0018 o a gerencia@integralgymtech.com.'], 500);
}
responder(true);

// ------------------------------------------------------------------ envío
function encabezado(string $s): string
{
    return '=?UTF-8?B?' . base64_encode($s) . '?=';
}

function cuerpoMultipart(string $limite, string $texto, string $html): string
{
    return "--$limite\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($texto))
        . "--$limite\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($html))
        . "--$limite--\r\n";
}

function enviarMail(string $de, string $deNombre, array $para, string $replyTo, string $replyNombre, string $asunto, string $html, string $texto): bool
{
    $limite = 'igt_' . bin2hex(random_bytes(8));
    $headers = [
        'From: ' . encabezado($deNombre) . " <$de>",
        'Reply-To: ' . encabezado($replyNombre) . " <$replyTo>",
        'MIME-Version: 1.0',
        "Content-Type: multipart/alternative; boundary=\"$limite\"",
        'X-Mailer: IGT-Web',
    ];
    return @mail(implode(', ', $para), encabezado($asunto), cuerpoMultipart($limite, $texto, $html), implode("\r\n", $headers), '-f' . $de);
}

function enviarSmtp(array $c, string $de, string $deNombre, array $para, string $replyTo, string $replyNombre, string $asunto, string $html, string $texto): bool
{
    $host = $c['host'];
    $port = (int) ($c['port'] ?? 465);
    $prefijo = $port === 465 ? 'ssl://' : '';
    $fp = @stream_socket_client($prefijo . $host . ':' . $port, $errno, $errstr, 20);
    if (!$fp) {
        error_log("IGT SMTP: $errstr");
        return false;
    }
    $leer = function () use ($fp): string {
        $r = '';
        while (($l = fgets($fp, 515)) !== false) {
            $r .= $l;
            if (isset($l[3]) && $l[3] === ' ') break;
        }
        return $r;
    };
    $cmd = function (string $c, array $ok) use ($fp, $leer): bool {
        fwrite($fp, $c . "\r\n");
        $r = $leer();
        if (!in_array((int) substr($r, 0, 3), $ok, true)) {
            error_log('IGT SMTP: ' . trim($r));
            return false;
        }
        return true;
    };
    $leer();
    $ehlo = 'EHLO integralgymtech.com';
    if (!$cmd($ehlo, [250])) return false;
    if ($port === 587) {
        if (!$cmd('STARTTLS', [220])) return false;
        stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
        if (!$cmd($ehlo, [250])) return false;
    }
    if (!$cmd('AUTH LOGIN', [334])) return false;
    if (!$cmd(base64_encode($c['user']), [334])) return false;
    if (!$cmd(base64_encode($c['pass']), [235])) return false;
    if (!$cmd("MAIL FROM:<$de>", [250])) return false;
    foreach ($para as $d) {
        if (!$cmd("RCPT TO:<$d>", [250, 251])) return false;
    }
    if (!$cmd('DATA', [354])) return false;
    $limite = 'igt_' . bin2hex(random_bytes(8));
    $msg = 'Date: ' . date('r') . "\r\n"
        . 'From: ' . encabezado($deNombre) . " <$de>\r\n"
        . 'To: ' . implode(', ', $para) . "\r\n"
        . 'Reply-To: ' . encabezado($replyNombre) . " <$replyTo>\r\n"
        . 'Subject: ' . encabezado($asunto) . "\r\n"
        . "MIME-Version: 1.0\r\nContent-Type: multipart/alternative; boundary=\"$limite\"\r\n\r\n"
        . cuerpoMultipart($limite, $texto, $html);
    $msg = preg_replace('/^\./m', '..', $msg);
    if (!$cmd($msg . "\r\n.", [250])) return false;
    $cmd('QUIT', [221]);
    fclose($fp);
    return true;
}
