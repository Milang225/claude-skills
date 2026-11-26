# Installation de la façon de travailler MDC sur un PC Windows
# Usage (PowerShell) :
#   powershell -ExecutionPolicy Bypass -File H:\claudeskill\_harness\install.ps1 -Base "H:\MDC"
#
# -Base : dossier où vous ouvrirez vos projets (un sous-dossier par projet : SUPERVISEUR-GENERAL, CRM, LMDC...).
#         Les mémoires de chaque projet sont installées pour <Base>\<NOM DU PROJET>.

param(
  [string]$Base = "$env:USERPROFILE"
)

$ErrorActionPreference = "Stop"
$H = Split-Path -Parent $MyInvocation.MyCommand.Path      # ...\claudeskill\_harness
$Depot = Split-Path -Parent $H                            # ...\claudeskill
$C = Join-Path $env:USERPROFILE ".claude"
New-Item -ItemType Directory -Force -Path $C | Out-Null

# 1. Skills : ~/.claude/skills doit pointer vers le dépôt
$S = Join-Path $C "skills"
if (-not (Test-Path $S)) {
  New-Item -ItemType Junction -Path $S -Target $Depot | Out-Null
  Write-Host "Skills : lien $S -> $Depot"
} else {
  Write-Host "Skills : $S existe déjà (laissé tel quel). Renommez-le puis relancez pour le relier au dépôt."
}

# 2. Agents et tâches planifiées
foreach ($d in "agents","scheduled-tasks") {
  $dst = Join-Path $C $d
  New-Item -ItemType Directory -Force -Path $dst | Out-Null
  Copy-Item -Recurse -Force (Join-Path $H "$d\*") $dst
  Write-Host "$d : copiés dans $dst"
}

# 3. Mémoires : une par projet, pour <Base>\<NOM>
$P = Join-Path $C "projects"
Get-ChildItem (Join-Path $H "memory") -Directory | ForEach-Object {
  $dossier = Join-Path $Base $_.Name
  $cle = ($dossier -replace '[^A-Za-z0-9]', '-')
  $dst = Join-Path $P "$cle\memory"
  New-Item -ItemType Directory -Force -Path $dst | Out-Null
  Copy-Item -Force (Join-Path $_.FullName "*") $dst
  Write-Host "Mémoire $($_.Name) -> projet $dossier"
}

Write-Host ""
Write-Host "Terminé. Ouvrez Claude Code dans un dossier de $Base (ex. $Base\SUPERVISEUR-GENERAL) pour retrouver sa mémoire."
Write-Host "Plateforme MDC : voir _harness\README.md (étape manuelle)."
