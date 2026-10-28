#!/usr/bin/env bash
# Link the zh-tw-prose skill into ~/.claude/skills and the reviewer agent into ~/.claude/agents.
# Use this when you work on baihua itself; other users should install the plugin instead.
# Output: one line per entry, tab separated: <status> <name> [detail]
set -u

case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
        echo "error	use scripts/link.ps1 on Windows (Git Bash cannot create junctions)"
        exit 1
        ;;
esac

repo="$(cd "$(dirname "$0")/.." && pwd -P)"
config="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$config/skills" "$config/agents"

link_one() {
    target="$1"
    link="$2"
    name="$(basename "$link")"
    if [ -L "$link" ]; then
        if [ "$(readlink "$link")" = "$target" ]; then
            printf 'ok\t%s\n' "$name"
            return
        fi
        printf 'skipped\t%s\tlinked elsewhere: %s\n' "$name" "$(readlink "$link")"
        return
    fi
    if [ -e "$link" ]; then
        printf 'skipped\t%s\ta real file or directory exists; move it away and re-run\n' "$name"
        return
    fi
    ln -s "$target" "$link"
    printf 'linked\t%s\n' "$name"
}

link_one "$repo/skills/zh-tw-prose" "$config/skills/zh-tw-prose"
link_one "$repo/agents/zh-tw-reviewer.md" "$config/agents/zh-tw-reviewer.md"
