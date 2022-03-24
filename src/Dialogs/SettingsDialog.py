from PyQt5 import QtWidgets, uic
from SyntaxHighlight import syntax_highlight


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, scene):
        """Construct SettingsDialog."""
        super(SettingsDialog, self).__init__()
        self.ui = uic.loadUi('settings_dialog.ui', self)
        self.scene = scene
        self.ui.buttonBox.accepted.connect(self.accept)

        self.ui.syntax_radio1.toggled.connect(self.syntax_radio1_func)
        self.ui.syntax_radio2.toggled.connect(self.syntax_radio2_func)
        if self.scene.syntax[0] == '$':
            self.ui.syntax_radio1.toggle()
        else:
            self.ui.syntax_radio2.toggle()
        self.ui.pygments_style.currentIndexChanged.connect(self.pygments_style_func)

    def syntax_radio1_func(self):
        """Set syntax highlighting to default."""
        self.scene.syntax = '$' + self.scene.syntax[1:]
        text = self.scene.project_data.tikzify(*self.scene.current_canvas_dims, *self.scene.init_canvas_dims)
        browser_text = syntax_highlight(self.scene.syntax, text)
        self.scene.ui.textBrowser.setText(browser_text)

    def syntax_radio2_func(self):
        """Set syntax highlighting to pygments."""
        self.scene.syntax = '^' + self.ui.pygments_style.currentText()
        text = self.scene.project_data.tikzify(*self.scene.current_canvas_dims, *self.scene.init_canvas_dims)
        browser_text = syntax_highlight(self.scene.syntax, text)
        self.scene.ui.textBrowser.setText(browser_text)

    def pygments_style_func(self):
        """Set pygments style."""
        self.scene.syntax = self.scene.syntax[0] + self.ui.pygments_style.currentText()
        text = self.scene.project_data.tikzify(*self.scene.current_canvas_dims, *self.scene.init_canvas_dims)
        browser_text = syntax_highlight(self.scene.syntax, text)
        self.scene.ui.textBrowser.setText(browser_text)

