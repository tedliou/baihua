# Link the zh-tw-prose skill into ~/.claude/skills with a directory junction (no admin rights needed)
# and copy the reviewer agent into ~/.claude/agents (re-run after pulling to update the copy).
# Use this when you work on baihua itself; other users should install the plugin instead.
# Output: one line per entry, tab separated: <status> <name> [detail]
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$configDir = $env:CLAUDE_CONFIG_DIR
if (-not $configDir) { $configDir = Join-Path $HOME '.claude' }
$skills = Join-Path $configDir 'skills'
$agents = Join-Path $configDir 'agents'
foreach ($dir in @($skills, $agents)) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
}

$target = Join-Path $repo 'skills\zh-tw-prose'
$link = Join-Path $skills 'zh-tw-prose'
$item = Get-Item -LiteralPath $link -Force -ErrorAction SilentlyContinue
if (-not $item) {
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Output "linked`tzh-tw-prose"
} elseif ($item.LinkType -and (@($item.Target)[0].TrimEnd('\') -ieq $target)) {
    Write-Output "ok`tzh-tw-prose"
} else {
    Write-Output "skipped`tzh-tw-prose`ta different file or link exists; move it away and re-run"
}

$agentSource = Join-Path $repo 'agents\zh-tw-reviewer.md'
Copy-Item -LiteralPath $agentSource -Destination (Join-Path $agents 'zh-tw-reviewer.md') -Force
Write-Output "copied`tzh-tw-reviewer.md"
