# launch.ps1

pip install uv


$env:UV_LINK_MODE = "symlink"
Write-Output "UV_LINK_MODE est défini sur $env:UV_LINK_MODE"


uv venv

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
    Write-Output "Environnement virtuel activé."
} else {
    Write-Error "Le script d'activation de l'environnement virtuel n'a pas été trouvé."
    exit 1
}


uv --link-mode=copysync
uv pip install -e .
uv cache prune
uv run tests/test_env.py


if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
    Write-Output "Environnement virtuel réactivé pour continuer le développement."
}

Write-Output "Lancement terminé. Vous pouvez maintenant poursuivre le développement."