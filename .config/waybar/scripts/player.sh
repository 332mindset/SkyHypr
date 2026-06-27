#!/bin/bash

bars=("▁▂▄▆█▇▄▂" "▂▄▆█▇▄▂▁" "▄▆█▇▄▂▁▂" "▆█▇▄▂▁▂▄" "█▇▄▂▁▂▄▆" "▇▄▂▁▂▄▆█")
bar=${bars[$(( $(date +%s) % ${#bars[@]} ))]}

player=$(playerctl -l 2>/dev/null | head -n1)

if [ -z "$player" ]; then
  echo "{\"text\":\"$bar  Not playing\"}"
  exit
fi

status=$(playerctl -p "$player" status 2>/dev/null)

if [ "$status" = "Playing" ] || [ "$status" = "Paused" ]; then
  artist=$(playerctl -p "$player" metadata artist 2>/dev/null)
  title=$(playerctl -p "$player" metadata title 2>/dev/null)

  if [ -n "$artist" ] && [ -n "$title" ]; then
    echo "{\"text\":\"$bar  $artist - $title\"}"
  elif [ -n "$title" ]; then
    echo "{\"text\":\"$bar  $title\"}"
  else
    echo "{\"text\":\"$bar  Not playing\"}"
  fi
else
  echo "{\"text\":\"$bar  Not playing\"}"
fi