param(
    [switch]$Once,
    [string]$SessionsRoot = "",
    [int]$PollInterval = 10,
    [int]$ActiveThreshold = 60,
    [double]$Opacity = 0.92,
    [ValidateSet("top-left", "top-right", "bottom-left", "bottom-right")]
    [string]$Position = "top-right"
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptRoot
$venvDir = Join-Path $projectRoot ".venv"
$python = Join-Path $venvDir "Scripts\python.exe"
$requirements = Join-Path $projectRoot "requirements.txt"

function New-AgentWardenVenv {
    if (Test-Path $python) {
        return
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3.13 -m venv $venvDir
    } else {
        & python -m venv $venvDir
    }

    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $python)) {
        throw "Failed to create virtual environment at $venvDir"
    }
}

function Install-AgentWardenIfNeeded {
    & $python -c "import agent_warden" *> $null
    if ($LASTEXITCODE -eq 0) {
        return
    }

    & $python -m pip install -r $requirements
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Agent Warden requirements"
    }
}

Push-Location $projectRoot
try {
    New-AgentWardenVenv
    Install-AgentWardenIfNeeded

    $agentArgs = @(
        "-m", "agent_warden",
        "--poll-interval", $PollInterval,
        "--active-threshold", $ActiveThreshold,
        "--opacity", $Opacity,
        "--position", $Position
    )

    if ($SessionsRoot) {
        $agentArgs += @("--sessions-root", $SessionsRoot)
    }

    if ($Once) {
        $agentArgs += "--once"
    }

    & $python @agentArgs
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
