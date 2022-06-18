from PyQt5 import QtWidgets, uic
from SyntaxHighlight import syntax_highlight
from CanvasRendering import clear, add_all_items


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, scene):
        """Construct SettingsDialog."""
        super(SettingsDialog, self).__init__()
        self.ui = uic.loadUi('settings_dialog.ui', self)
        self.scene = scene
        self.ui.buttonBox.accepted.connect(self.accept)

        self.ui.pygments_style.currentIndexChanged.connect(self.pygments_style_func)
        self.ui.pygments_style.setCurrentIndex(self.ui.pygments_style.findText(self.scene.syntax[1:]))

        self.ui.syntax_radio1.toggled.connect(self.syntax_radio1_func)
        self.ui.syntax_radio2.toggled.connect(self.syntax_radio2_func)
        if self.scene.syntax[0] == '$':
            self.ui.syntax_radio1.toggle()
        else:
            self.ui.syntax_radio2.toggle()

        self.ui.pdflatex.setText(self.scene.pdflatex_command)
        self.ui.pdf2png.setText(self.scene.pdf2png_command)
        self.ui.pdflatex.textEdited.connect(self.pdflatex_command_func)
        self.ui.pdf2png.textEdited.connect(self.pdf2png_command_func)

        self.ui.aspect_ratio_over.currentIndexChanged.connect(self.aspect_ratio_over_func)
        self.ui.aspect_ratio_under.currentIndexChanged.connect(self.aspect_ratio_under_func)
        self.ui.aspect_ratio_over.setCurrentIndex(self.scene.aspect_ratio[0] - 1)
        self.ui.aspect_ratio_under.setCurrentIndex(self.scene.aspect_ratio[1] - 1)

        # TODO show aspect setting button messes with the same button in the mainWindow
        # TODO amend scene to mainWindow or delete aspect ratio checkButton from settings
        self.ui.aspect_ratio_show.toggled.connect(self.aspect_ratio_func)
        self.ui.aspect_ratio_show.setChecked(self.scene.is_aspect_ratio)

    def syntax_radio1_func(self):
        """Set syntax highlighting to default."""
        self.scene.syntax = '$' + self.scene.syntax[1:]
        text = self.scene.project_data.tikzify(*self.scene.current_canvas_dims,
                                               *self.scene.init_canvas_dims)
        browser_text = syntax_highlight(self.scene.syntax, text)
        self.scene.ui.textBrowser.setText(browser_text)

    def syntax_radio2_func(self):
        """Set syntax highlighting to pygments."""
        self.scene.syntax = '^' + self.ui.pygments_style.currentText()
        text = self.scene.project_data.tikzify(*self.scene.current_canvas_dims,
                                               *self.scene.init_canvas_dims)
        browser_text = syntax_highlight(self.scene.syntax, text)
        self.scene.ui.textBrowser.setText(browser_text)

    def pygments_style_func(self, index):
        """Set pygments style."""
        self.scene.syntax = self.scene.syntax[0] + self.ui.pygments_style.currentText()
        text = self.scene.project_data.tikzify(*self.scene.current_canvas_dims,
                                               *self.scene.init_canvas_dims)
        browser_text = syntax_highlight(self.scene.syntax, text)
        self.scene.ui.textBrowser.setText(browser_text)

    def pdflatex_command_func(self, text):
        self.scene.pdflatex_command = text

    def pdf2png_command_func(self, text):
        self.scene.pdf2png_command = text

    def aspect_ratio_over_func(self, index):
        self.scene.aspect_ratio[0] = index + 1
        clear(self.scene)
        add_all_items(self.scene)

    def aspect_ratio_under_func(self, index):
        self.scene.aspect_ratio[1] = index + 1
        clear(self.scene)
        add_all_items(self.scene)

    def aspect_ratio_func(self, state):
        """Set aspect ratio boolean."""
        self.scene.is_aspect_ratio = bool(state)
        clear(self.scene)
        add_all_items(self.scene)
