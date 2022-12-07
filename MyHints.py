'''
Terminator plugin to implement 
   Kitty Hints-like feature for Terminator

 Author: yurenchen@yeah.net
License: GPLv2
   Site: https://github.com/yurenchen000/terminator-hints-plugin
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

AVAILABLE = ['MyHints']

import terminatorlib.plugin as plugin


## disable log
print = lambda *a:None

'''
TerminalHandler to handle each terminal
   self-construct the third type plugin for Terminator
   by play tricks on a fake URLHandler
   heavy reliance on terminator internal implementation
'''
class TerminalHandler(plugin.URLHandler):
    ''' a fake URLHandler, register to each terminal for hints '''
    capabilities = ['url_handler']
    _handler_name = 'full_uri' ## HACK: use built-in name to avoid actual cost, it will not registered to matches

    @property
    def handler_name(self):    ## HACK: use getter got opportunity to call function
        """Handle init for each term"""
        term = self.get_terminal()
        self.attach_terminal(term)
        return self._handler_name

    def unload(self):
        """Handle deinit for disable"""
        self.disable()

    def __init__(self):
        """Handle init for load or enable"""
        self.terminator = plugin.Terminator()
        terminal = self.get_terminal()
        if terminal: # is load
            self.enable(terminal)
        else:
            self.enable(None)

    # hack from https://github.com/mchelem/terminator-editor-plugin
    def get_terminal(self):    # HACK: use the inspect module to climb up the stack to the Terminal object
        import inspect
        for frameinfo in inspect.stack():
            frameobj = frameinfo[0].f_locals.get('self')
            if frameobj and frameobj.__class__.__name__ == 'Terminal':
                return frameobj

    def enable(self, terminal=None):
        ''' Callback to enable plugin
        if terminal:
            do_load_things()
            return
        for terminal in self.terminator.terminals:
            print('terminal:', terminal)
            do_init_for_terminal(terminal)
        '''
        raise NotImplementedError

    def disable(self):
        ''' Callback to disable plugin
        for terminal in self.terminator.terminals:
            print('terminal:', terminal)
            de_init_for_terminal(terminal)
        '''
        raise NotImplementedError

    def attach_terminal(self, terminal):
        ''' Callback to init for each terminal
        print('terminal:', terminal)
        do_init_for_terminal(terminal)
        '''
        raise NotImplementedError


class MyHints(TerminalHandler):
    ''' a fake URLHandler, register to each terminal for hints '''
    def attach_terminal(self, terminal):    ## register for each terminal once
        print('\n==init_term:', terminal)
        MyHintsImpl.setup_for_term(terminal)

    def disable(self):
        print('\n==disable_hints..')
        for terminal in self.terminator.terminals:
            print('term:', terminal)
            MyHintsImpl.teardown_for_term(terminal)

    def enable(self, terminal=None):
        if terminal:
            print('\n==load_hints:', terminal)
            return

        print('\n==enable_hints..')
        for terminal in self.terminator.terminals:
            print('term:', terminal)
            MyHintsImpl.setup_for_term(terminal)


import re, string
hints = {}
hotkeys = 'pnhdlwiu'
selkeys = string.digits[1:]+'0'+string.ascii_letters
selkeys = re.sub(rf'[{hotkeys}P]', '', selkeys)


def gen_hints(txt, kind='p', hl=None):
    print('==gen_hints:', kind, hl)
    # print('--txt:', txt)
    ea='\xA0\xF1'
    eb='\xA0\xF2'
    ec='\xA0\xF3'
    ez='\xA0\xF4'
    ma='<span bgcolor="lightgreen" fgcolor="black" weight="bold">'
    mb='<span color="yellow">'
    mc='<span bgcolor="#006400" fgcolor="black" weight="bold">'
    mz='</span>'

    if kind == 'p':
        pat = re.compile(r'(~?[\w/\._-]+/[\w/\._-]+)')
    elif kind == 'n':
        pat = re.compile(r'([\w/\._-]+?:\d+)')
    elif kind == 'l':
        pat = re.compile(r'^[ \f\t]*(.*\S.*)[ \f\t]*$', re.MULTILINE)
    elif kind == 'w':
        # pat = re.compile(r'([\S]{4,})')
        pat = re.compile(r'([\w-]{4,})')
    elif kind == 'h':
        pat = re.compile(r'(\b[0-9a-fA-F]{6,}\b)')
    elif kind == 'd':
        pat = re.compile(r'(\d{3,})')
    elif kind == 'i':
        pat = re.compile(r'(\d+(?:\.\d+){3}(?::\d+)?)')
    elif kind == 'u':
        pat = re.compile(r'([A-Za-z0-9]+://[A-Za-z0-9%-_]+(?:/[A-Za-z0-9%-_])*(?:#|\\?)[A-Za-z0-9%-_&=]*)')
        ## url pattern from https://stackoverflow.com/a/72358332/4896468

    ## count total
    out = re.findall(pat, txt)
    idx = {}  # DENSE RANK
    for i,v in enumerate(reversed(out)):
        idx[v] = idx.get(v, len(idx))
        # print(i, idx[v], v)

    print('--count:', len(out), len(idx))

    ## generate html
    global hints
    hints = {}
    count = len(idx)
    def replace_cb(match_obj):
        nonlocal i
        s = match_obj.group(1)
        i = idx.get(s)
        # print('match:', match_obj)
        if i<0 or i>=len(selkeys): return s   ## keys depleted, giveup
        if s is not None:
            n = ea+str(selkeys[i])+ez
            hints[selkeys[i]] = s
            if hl and hl in selkeys[:count]:
                if hl!=selkeys[i]:
                    n = ec+str(selkeys[i])+ez
                    return n+s[1:] # fade item
                else:
                    return eb+s+ez # highlight item
            return eb+n+s[1:]+ez

    out = re.sub(pat, replace_cb, txt)

    ## escape & fill markup   # NOTE: it's not safe if txt has our special escapes
    out = GLib.markup_escape_text(out)
    tbl = { ea:ma, eb:mb, ec:mc, ez:mz }
    for e,m in tbl.items(): out = out.replace(e,m)
    # print(out)

    ## append hotkeys
    # return out[:-1] + '>>' # note: maybe not \n
    tip_hotkeys = '''
    <span bgcolor="#006400" fgcolor="black" weight="bold">h</span>ex
    <span bgcolor="#006400" fgcolor="black" weight="bold">d</span>ec
    <span bgcolor="#006400" fgcolor="black" weight="bold">w</span>ord
    <span bgcolor="#006400" fgcolor="black" weight="bold">l</span>i<span
          bgcolor="#006400" fgcolor="black" weight="bold">n</span>e
    <span bgcolor="#006400" fgcolor="black" weight="bold">i</span>p
    <span bgcolor="#006400" fgcolor="black" weight="bold">u</span>rl
    '''
    tip_hotkeys = re.sub(r'\s*\n\s*', ' ', tip_hotkeys)
    # print(out)
    if out[-1] != '>': out = out[:-1]
    out = out + tip_hotkeys
    return out


def hide_widget(w):
    w.hide()
    w.set_no_show_all(True)
def show_widget(w):
    w.set_no_show_all(False)
    w.show_all()



'''
 Kitty Hints-like feature for Terminator
'''
class MyHintsImpl:
    def __init__(self, term):
        if hasattr(term, 'my_hints'): # already init
            return

        self.term = term
        self.win = None
        self.tv = None
        self.tb = None
        self.scrollbar_visible = None

        self.txt = None
        self.kind = None
        self.key_old = None
        self.key_pressed = {}
        
    @staticmethod
    def setup_for_term(term):
        if hasattr(term, 'my_hints'): # already init
            return term.my_hints

        # new, init
        self = MyHintsImpl(term)
        self.setup_ctrl_shift_p()
        term.my_hints = self

    @staticmethod
    def teardown_for_term(term):
        if not hasattr(term, 'my_hints'): # already destroy
            return 

        self = term.my_hints
        self.cancel_ctrl_shift_p()
        
        # print('--del_win:', self.win)
        if self.win:
            self.win.destroy()
        if hasattr(term, 'my_hints'):
            self.done_hints()
            del term.my_hints

    ### --------- HACK: override handle of ctrl+shift+p
    def doing_ctrl_shift_p(self):
        print('==my key_go_prev pressed:', self.term)
        self.show_hints(self.term)

    def setup_ctrl_shift_p(self):
        if not hasattr(self.term, 'bak_key_go_prev'):
            self.term.bak_key_go_prev = getattr(self.term, 'key_go_prev')
        self.term.key_go_prev = self.doing_ctrl_shift_p

    def cancel_ctrl_shift_p(self):
        if hasattr(self.term, 'bak_key_go_prev'):
            self.term.key_go_prev = self.term.bak_key_go_prev


    ### --------- hints api
    def done_hints(self, sel=None):
        term = self.term
        print('--done_hints')
        # show term
        term.vte.show()
        if self.scrollbar_visible: term.scrollbar.show()
        term.vte.grab_focus()

        # result input
        if sel:
            term.vte.feed_child(sel.encode())

    def show_hints(self, term):
        if not self.win:
            self.init_ui()
            self.init_style()

        self.txt, _ = term.vte.get_text()
        self.kind = 'p'
        self.key_old = None
        self.key_last = None
        self.key_pressed = {}
        html = gen_hints(self.txt, self.kind)
        self.set_htm(html.rstrip())

        self.scrollbar_visible = term.scrollbar.props.visible
        # hide term
        hide_widget(term.vte)
        hide_widget(term.scrollbar)

        # show hints
        show_widget(self.win)
        self.tv.grab_focus()

    ### --------- hints inner
    def init_ui(self):
        tv = Gtk.TextView()
        tb = tv.get_buffer()

        win = Gtk.ScrolledWindow()
        win.add(tv)
        # print('++add_win:', win)
        tv.connect("key-press-event", self.on_key_press)
        tv.connect('key-release-event', self.on_key_release)
        # print('self term box:', self.term.terminalbox)
        self.term.terminalbox.pack_start(win, True, True, 0)

        self.win = win
        self.tv = tv
        self.tb = tb

    def init_style(self):
        self.tv.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.tv.set_property('cursor-visible', False)
        self.tv.set_property('editable', False)
        self.tv.override_font(self.term.vte.get_font().copy())

        prov = Gtk.CssProvider.new()
        prov.load_from_data('''
        text {
            color: grey;
            background-color: black;
        }
        '''.encode())

        # self.win.set_opacity(0.8)
        ctx = self.win.get_style_context()
        ctx.add_provider_for_screen(self.win.get_screen(), prov, 800)
        pass

    def set_htm(self, txt): ## NOTE: It not real HTML, just `Pango Markup`
        self.tb.set_text('')
        self.tb.insert_markup(self.tb.get_end_iter(), txt, -1)

    def on_key_press(self, elem, event):
        key = Gdk.keyval_name(event.keyval)
        self.key_pressed[key] = True
        print('key_press:', key, key == self.key_old)
        # print('==the_win:', self.win)

        if key == 'Escape':
            self.done_hints(None)
            hide_widget(self.win)
        if key in hotkeys:
            self.kind = key
            html = gen_hints(self.txt, self.kind)
            self.set_htm(html.rstrip())
        if key in selkeys and key in hints:
            if key == self.key_old: # repeat key
                return

            html = gen_hints(self.txt, self.kind, hl=key) # change highlight item
            self.set_htm(html.rstrip())

            def done(s):
                self.done_hints(hints[key])
                hide_widget(self.win)
                return False

            # GLib.timeout_add(300, done, 'bye')

        self.key_old = key

    def on_key_release(self, elem, event):
        key = Gdk.keyval_name(event.keyval)
        self.key_pressed.pop(key, False)
        self.key_pressed.pop(key.swapcase(), False)
        print('key_release:', key, list(self.key_pressed.keys()))
        # print('==the_win:', self.win)

        if len(self.key_pressed): # change highlight item
            self.key_last = list(self.key_pressed.keys())[-1] # avoid https://gitlab.gnome.org/GNOME/gtk/-/issues/1570
            if key in selkeys and self.key_last in hints:
                html = gen_hints(self.txt, self.kind, hl=self.key_last)
                self.set_htm(html.rstrip())
            if self.key_last in ['Shift_L','Shift_R']:
                self.key_last = key
        else:                     # final choice
            if key in ['Shift_L','Shift_R']:
                # print('key_last:', self.key_last)
                key = self.key_last
            if key in hints:
                self.done_hints(hints[key])
                hide_widget(self.win)
                print('==you choice:', hints[key])

        self.key_old = None

