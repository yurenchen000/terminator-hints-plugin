# Terminator Hints Plugin

A Terminator Plugin implement  
[Kitty Hints][kitty]-like feature for [gnome-terminator][terminator]


[kitty]:https://sw.kovidgoyal.net/kitty/kittens/hints/
[terminator]:https://github.com/gnome-terminator/terminator/issues/669

Repo: https://github.com/yurenchen000/terminator-hints-plugin

## requirements

only tested with terminator 2.1.1+, on ubuntu 22 lts

## Install

1. Copy MyHints.py to ~/.config/terminator/plugins/
2. Terminator Preferences > Plugins: enable MyHints


## Usage

by default, press `Ctrl+Shift+P` (override `go_prev` shortcut action), then press
- `p`: match path (default)
- `n`: match file:line
- `l`: match whole line
- `h`: match hex
- `d`: match dec
- `i`: match ip[:port]
- `w`: match word

then press the key to input highlight strings.
or `ESC` to giveup

note: behavor not exactly the same as kitty-hints

## screenshot

[terminator_hints3.webm](https://user-images.githubusercontent.com/8458213/201852859-2e9f5a76-40b3-4859-bc52-33b75099be17.webm)


