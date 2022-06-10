from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QIcon


def compile_latex(scene, auto_compile_check):
    """Run pdflatex and pdf2png."""

    if (not auto_compile_check) or (auto_compile_check and scene.auto_compile):
        scene.ui.compile_pushButton.setIcon(QIcon(":/images/compile/during_compile.png"))
        scene.ui.compile_pushButton.repaint()
        # print(scene.project_data.doc_surround_tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        with open('try.tex', 'w') as f:
            f.write(scene.project_data.doc_surround_tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        pdf_command = scene.pdflatex_command
        jpg_command = scene.pdf2png_command\
            .replace('#1', str(scene.current_canvas_dims[0]))\
            .replace('#2', str(scene.current_canvas_dims[1]))
        process = QProcess()
        process.start(pdf_command)
        process.waitForFinished()
        process.start(jpg_command)
        process.waitForFinished()

        scene.ui.compile_pushButton.setIcon(QIcon(":/images/compile/lets_compile.png"))
