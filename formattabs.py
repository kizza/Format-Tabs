import sublime
import sublime_plugin
import sys
import pprint
from datetime import date


class format_tabs_command(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        syntax = view.settings().get('syntax').lower()
        if 'python' in syntax:
            syntax = 'python'
        elif 'css' in syntax:
            syntax = 'css'

        if syntax == 'css':
            view.run_command('format_css')

        # Format tabs for left of existing lines
        offset = 0
        line_with_spaces = 0
        tab_char = '\t'

        tabs_to_spaces = view.settings().get('translate_tabs_to_spaces')
        tab_size = view.settings().get('tab_size')
        if syntax == 'python':
            tab_char = ' ' * tab_size

        while True:
            match = view.find(r'^(\t|\s)+', offset)
            if match:
                offset = match.b
                regions = view.split_by_newlines(match)
                for region in reversed(regions):
                    line = view.substr(region)
                    tabs = tab_char * line.count(tab_char)
                    spaces = ' ' * line.count(' ')
                    if line.find('\t') >= 0:
                        if syntax == 'python':
                            spaces = tab_char * line.count('\t')
                        spaces = spaces.replace('\t', tab_char)
                        view.replace(edit, region, tabs + spaces)
                    if line.find(' ') >= 0:
                        spaces = spaces.replace(' ' * 3, tab_char)
                        spaces = spaces.replace(' ', '')
                        view.replace(edit, region, tabs + spaces)
                        line_with_spaces = line_with_spaces + 1
            else:
                break

        # Remove empty lines
        regions = view.find_all(r'^('+tab_char+')+?\n')
        for region in reversed(regions):
            view.replace(edit, region, '\n')

        # Highlight tabs
        highlighted = []
        regions = view.find_all(r'^('+tab_char+')+?[^'+tab_char+']')
        for region in reversed(regions):
            highlighted.append(sublime.Region(region.a, region.b-1))

        # Find and display all comment titles
        # titles = get_comment_titles(view, 'string')
        # self.disabled_packages = titles#['test1', 'test2', 'test3']
        # self.window = sublime.active_window()
        # self.window.show_quick_panel(self.disabled_packages,
        # self.on_list_selected_done)
        # sublime.error_message(__name__ + ': There are no packages to list.')
        # self.settings = sublime.load_settings('Global.sublime-settings')

        # Display how nice it is now - for a second
        # Cleanup css for css files
        # print "Formatted tabs"

        colour = 'comment'
        outline = False
        if sys.version_info < (3, 0):
            view.add_regions(
                'starting-tabs', highlighted, colour,
                sublime.DRAW_OUTLINED if outline else sublime.DRAW_EMPTY)
        else:
            view.add_regions(
                'starting-tabs', highlighted, colour, '',
                sublime.DRAW_NO_FILL if outline else sublime.DRAW_NO_OUTLINE)

        callback = lambda: clear_regions(view)
        sublime.set_timeout(callback, 1000)


def clear_regions(view):
    view.erase_regions("starting-tabs")
