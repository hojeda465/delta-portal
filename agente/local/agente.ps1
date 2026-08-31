# ===================================================================
#  Con Interes - agente local
#  Se lanza desde Agente.bat (doble clic). No editar salvo la
#  seccion CONFIGURACION de abajo.
#  Todo en ASCII a proposito: la consola de Windows rompe las tildes.
# ===================================================================

# ---------------------- CONFIGURACION ------------------------------
# Argumentos extra para Claude Code. Vacio = te pide permiso en cada
# cambio (lo mas seguro). Si te cansa confirmar cada edicion en una
# corrida de redaccion, descomenta la linea de abajo:
# $ClaudeArgs = @('--permission-mode','acceptEdits')
$ClaudeArgs = @()

# Rama del sitio
$Rama = 'main'
# -------------------------------------------------------------------

# 'Continue' a proposito: git escribe avisos por stderr y con 'Stop' el script
# se cortaria solo. Los chequeos que importan los hace el script a mano.
$ErrorActionPreference = 'Continue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

# OJO: el paquete de npm se pasa SIEMPRE entre comillas simples. Sin comillas,
# PowerShell lee el arroba de @anthropic-ai como splatting y rompe la llamada.
$PaqueteNpm = '@anthropic-ai/claude-code'

# La raiz del repo son dos niveles arriba de este script (agente\local\)
$Raiz = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $Raiz

$Misiones = Join-Path $PSScriptRoot 'misiones'

function Titulo($t) {
  Write-Host ''
  Write-Host ('  ' + $t) -ForegroundColor Cyan
  Write-Host ('  ' + ('-' * $t.Length)) -ForegroundColor DarkGray
}
function Ok($t)    { Write-Host "  [OK]    $t" -ForegroundColor Green }
function Aviso($t) { Write-Host "  [AVISO] $t" -ForegroundColor Yellow }
function Error2($t){ Write-Host "  [FALTA] $t" -ForegroundColor Red }
function Info($t)  { Write-Host "  $t" -ForegroundColor Gray }

function Hay($cmd) {
  $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

# ============================ BANNER ===============================
Clear-Host
Write-Host ''
Write-Host '   %  CON INTERES' -ForegroundColor Cyan
Write-Host '      La economia, con interes.' -ForegroundColor DarkGray
Write-Host '      Agente local - coninteres.com' -ForegroundColor DarkGray
Write-Host ''
Info "Carpeta: $Raiz"

# ========================== PREFLIGHT ==============================
Titulo 'Revisando que este todo'

$falta = $false

if (Hay 'git') {
  Ok ('git ' + (git --version).Replace('git version ',''))
} else {
  Error2 'git no esta instalado.'
  Info   'Bajalo de https://git-scm.com/download/win y volve a abrir el agente.'
  $falta = $true
}

$py = $null
foreach ($c in @('python','python3','py')) { if (Hay $c) { $py = $c; break } }
if ($py) {
  Ok ((& $py --version 2>&1) -join ' ')
} else {
  Error2 'Python no esta instalado.'
  Info   'Bajalo de https://www.python.org/downloads/'
  Info   'IMPORTANTE: marca la casilla "Add Python to PATH" durante la instalacion.'
  $falta = $true
}

$claudeCmd = $null
if (Hay 'claude') {
  $claudeCmd = 'claude'
  Ok 'Claude Code instalado'
} elseif (Hay 'npx') {
  $claudeCmd = 'npx'
  Aviso 'Claude Code no esta instalado global; se va a usar npx (arranca mas lento).'
  Info  'Para instalarlo de una vez:  npm install -g @anthropic-ai/claude-code'
} else {
  Error2 'No hay Claude Code ni npx.'
  Info   'Instala Node.js desde https://nodejs.org y despues corre:'
  Info   '  npm install -g @anthropic-ai/claude-code'
  $falta = $true
}

if ($falta) {
  Write-Host ''
  Aviso 'Falta algo de lo de arriba. Instalalo y volve a abrir Agente.bat.'
  Write-Host ''
  Read-Host '  Enter para cerrar'
  exit 1
}

# ===================== ACTUALIZAR EL REPO ==========================
Titulo 'Poniendo el repo al dia'

$sucio = git status --porcelain
if ($sucio) {
  Aviso 'Hay cambios sin commitear en la carpeta. No se hace pull para no pisarlos:'
  git status --short | ForEach-Object { Info "  $_" }
  Info 'Para commitearlos: opcion 1, escribi /exit y respondele que si a subir.'
} else {
  git fetch origin $Rama --quiet
  $detras = (git rev-list --count "HEAD..origin/$Rama").Trim()
  if ($detras -eq '0') {
    Ok 'Ya estabas al dia.'
  } else {
    git pull --ff-only origin $Rama --quiet
    Ok "Bajadas $detras novedades desde GitHub."
  }
}

# ====================== FUNCIONES DEL MENU =========================

function Correr-Mision($archivo, $extra) {
  $ruta = Join-Path $Misiones $archivo
  if (-not (Test-Path $ruta)) {
    Error2 "No encuentro la mision: $ruta"
    return
  }
  $prompt = "Sos el agente local de Con Interes. Lee CLAUDE.md y agente/NEWSROOM.md, " +
            "despues lee agente/local/misiones/$archivo y ejecutalo al pie de la letra."
  if ($extra) { $prompt += " Contexto que te da Horacio para esta corrida: $extra" }

  Write-Host ''
  Info 'Arrancando el agente... (para salir de Claude Code escribi /exit)'
  Write-Host ''

  if ($claudeCmd -eq 'npx') {
    & npx -y $PaqueteNpm @ClaudeArgs $prompt
  } else {
    & claude @ClaudeArgs $prompt
  }

  Cerrar-Corrida
}

function Cerrar-Corrida {
  Write-Host ''
  Titulo 'Como quedo la carpeta'
  $cambios = git status --porcelain
  if (-not $cambios) {
    Ok 'Sin cambios para subir.'
    return
  }
  git status --short | ForEach-Object { Info "  $_" }
  Write-Host ''
  $r = Read-Host '  Subir estos cambios a GitHub? (s/n)'
  if ($r -ne 's' -and $r -ne 'S') {
    Info 'No se subio nada. Los cambios quedan en la carpeta.'
    return
  }
  $msg = Read-Host '  Mensaje del commit'
  if (-not $msg) { $msg = 'Cambios del agente local' }
  git add -A
  git commit -m $msg | Out-Null
  Ok 'Commit hecho. El trabajo ya no se puede perder.'

  # Antes de pushear hay que estar al dia, o GitHub rechaza el push.
  # Pasa siempre que las tareas en la nube hayan publicado mientras tanto.
  git fetch origin $Rama --quiet
  $detras = (git rev-list --count "HEAD..origin/$Rama").Trim()
  if ($detras -ne '0') {
    Info "Hay $detras commit(s) nuevos en GitHub. Los traigo antes de subir..."
    git pull --rebase origin $Rama
    if ($LASTEXITCODE -ne 0) {
      Aviso 'El rebase se trabo: hay un conflicto entre tu trabajo y lo de GitHub.'
      Info  'Tu commit esta a salvo. Para volver al estado anterior:  git rebase --abort'
      Info  'Despues pedile ayuda al agente con la opcion 5.'
      return
    }
    Ok 'Al dia con GitHub.'
  }

  git push origin $Rama
  if ($LASTEXITCODE -eq 0) {
    Ok 'Subido. El sitio se actualiza en un par de minutos.'
  } else {
    Aviso 'El push fallo. El commit quedo hecho localmente, no se perdio nada.'
    Info  'Si te pidio usuario y contrasena, git no tiene la credencial guardada:'
    Info  '  git config --global credential.helper manager'
    Info  'Si dijo "rejected", alguien pusheo recien: volve a elegir la opcion y reintenta.'
  }
}

function Estado-Sitio {
  Titulo 'Estado del sitio'

  $enCola = @(Get-ChildItem -Path (Join-Path $Raiz 'cola') -Filter '*.html' -ErrorAction SilentlyContinue)
  if ($enCola.Count -eq 0) {
    Info 'Cola de revision: vacia.'
  } else {
    Info "Cola de revision: $($enCola.Count) borrador(es) esperando."
    $enCola | ForEach-Object { Info "  - $($_.BaseName)" }
  }

  $pub = @(Get-ChildItem -Path (Join-Path $Raiz 'articulos') -Filter '*.html' -ErrorAction SilentlyContinue)
  Info "Notas publicadas: $($pub.Count)"

  Write-Host ''
  Info 'Ultimos movimientos:'
  git log -6 --date=format:'%d/%m %H:%M' --format='   %ad  %an: %s' | ForEach-Object { Write-Host $_ -ForegroundColor Gray }

  $pend = (git rev-list --count "origin/$Rama..HEAD").Trim()
  Write-Host ''
  if ($pend -eq '0') { Ok 'Todo lo local ya esta en GitHub.' }
  else { Aviso "Tenes $pend commit(s) local(es) sin subir." }
}

# ============================= MENU ================================
while ($true) {
  Write-Host ''
  Write-Host '  ------------------------------------------------------' -ForegroundColor DarkGray
  Write-Host '   QUE HACEMOS' -ForegroundColor Cyan
  Write-Host ''
  Write-Host '   1  Conversar con el agente   (pedile lo que necesites, en castellano)' -ForegroundColor White
  Write-Host ''
  Write-Host '      o anda directo a una tarea:' -ForegroundColor DarkGray
  Write-Host '   2  Corrida de redaccion      (deja un borrador en la cola)'
  Write-Host '   3  Revisar y publicar        (de la cola al sitio)'
  Write-Host '   4  Ficha de investigacion    (un tema o un link -> datos verificados)'
  Write-Host '   5  Cambios al sitio          (plantilla, scripts, paginas)'
  Write-Host '   6  Estado del sitio          (solo mira, no toca nada)'
  Write-Host ''
  Write-Host '   0  Salir'
  Write-Host '  ------------------------------------------------------' -ForegroundColor DarkGray
  $op = Read-Host '   Opcion'

  switch ($op) {
    '1' {
      Write-Host ''
      Info 'El agente te va a dar el estado y esperar. Hablale normal. /exit para volver aca.'
      Correr-Mision 'conversar.md' $null
    }
    '2' { Correr-Mision 'redaccion.md' $null }
    '3' { Correr-Mision 'publicar.md' $null }
    '4' {
      Write-Host ''
      $tema = Read-Host '   Tema, pregunta o link para investigar'
      if ($tema) { Correr-Mision 'ficha.md' $tema } else { Aviso 'Sin tema no puedo arrancar.' }
    }
    '5' {
      Write-Host ''
      $q = Read-Host '   Que cambio queres hacer'
      if ($q) { Correr-Mision 'cambios-sitio.md' $q } else { Aviso 'Sin consigna no puedo arrancar.' }
    }
    '6' { Estado-Sitio }
    '0' { Write-Host ''; Info 'Listo. Hasta la proxima.'; Write-Host ''; exit 0 }
    default { Aviso 'Elegi un numero del menu.' }
  }
}
