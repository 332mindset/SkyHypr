#!/usr/bin/env bash

set -e

echo "==> SkyHypr installer"

BACKUP_DIR="$HOME/.config-backup-$(date +%Y%m%d-%H%M%S)"

echo "==> Creating backup: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

for dir in hypr waybar kitty rofi fastfetch cava swaync; do
    if [ -d "$HOME/.config/$dir" ]; then
        cp -r "$HOME/.config/$dir" "$BACKUP_DIR/"
    fi
done

echo "==> Installing packages"
if command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --needed - < packages.txt
else
    echo "pacman not found. Install packages manually from packages.txt"
fi

echo "==> Copying configs"
mkdir -p "$HOME/.config"
cp -r .config/* "$HOME/.config/"

echo "==> Installing SkyHypr scripts"
mkdir -p "$HOME/.config/hypr/scripts"
cp scripts/*.py "$HOME/.config/hypr/scripts/"
chmod +x "$HOME/.config/hypr/scripts/"*.py

echo "==> Done!"
echo "Backup saved to: $BACKUP_DIR"
echo "Log out and log back into Hyprland."
