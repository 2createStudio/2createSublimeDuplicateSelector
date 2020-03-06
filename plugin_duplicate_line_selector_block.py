import sublime, sublime_plugin, re

class DuplicateLineSelectorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)

                is_css = self.view.match_selector( self.view.sel()[0].b, 'source.css' )
                is_less = self.view.match_selector( self.view.sel()[0].b, 'source.less' )
                is_scss = self.view.match_selector( self.view.sel()[0].b, 'source.scss' )

                if is_css or is_less or is_scss:
                        line_num, column = self.view.rowcol(line.begin())

                        line_contents = '\n' + self.view.substr(line)
                        selector = re.sub(r'(.*?)\s*(\{)\s*.*(\s*\}\s*)', r'\1  \2  \3', line_contents)
                        self.view.insert(edit, line.end(), selector)

                        pt = self.view.text_point(line_num + 1, len(selector))

                        self.view.sel().clear()
                        self.view.sel().add(sublime.Region(pt))
                        self.view.show(pt)

                        test = self.view.extract_scope(pt)
                else :
                        line_contents = self.view.substr(line) + '\n'
                        self.view.insert(edit, line.begin(), line_contents)
