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
- `u`: match url
- `w`: match word

then press the key to input highlight strings. or 
- `ESC` to giveup

Tips: hesitate choice: hold can highlight choice, then press another key can change choice (last key up is final choice)  

Note: behavor not exactly the same as kitty-hints

## screenshot & use case


[terminator_hints3.webm](https://user-images.githubusercontent.com/8458213/201852859-2e9f5a76-40b3-4859-bc52-33b75099be17.webm)

pick line  
[hints_1_line_3.webm](https://user-images.githubusercontent.com/8458213/205634937-eafc3fe0-ac91-4a43-a68d-4bdc2a1f30d7.webm)

pick word  
[hints_2_word.webm](https://user-images.githubusercontent.com/8458213/205635190-50ee1654-fea4-40d5-8317-c4e68099cabd.webm)

pick pid  
[hints_3_pid.webm](https://user-images.githubusercontent.com/8458213/205635298-b394c7b7-05ac-4c54-bbbf-3c1bcbfe8dff.webm)

pick ipaddr & hesitate choice  
[hints_4_ip_hesitate_choice.webm](https://user-images.githubusercontent.com/8458213/205635361-ae75161a-ee37-4680-bad7-9ad8e28706c0.webm)

kind change  
[hints_5_kind_change_2.webm](https://user-images.githubusercontent.com/8458213/205635441-9d6cba03-3f8d-43b5-87b4-7ab5cf9f27ed.webm)



