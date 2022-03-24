from PyQt5.QtCore import QProcess


def compile_latex(scene, auto_compile_check):
    """Run pdflatex and pdf2png."""
    if (not auto_compile_check) or (auto_compile_check and scene.auto_compile):
        print(scene.project_data.doc_surround_tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        with open('try.tex', 'w') as f:
            f.write(scene.project_data.doc_surround_tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        pdf_command = r'pdflatex -synctex=1 -interaction=batchmode --shell-escape -halt-on-error try.tex'
        jpg_command = f'pdftocairo -png -scale-to-x {scene.current_canvas_dims[0]} -scale-to-y {scene.current_canvas_dims[1]} try.pdf'
        process = QProcess()
        process.start(pdf_command)
        process.waitForFinished()
        process.start(jpg_command)
        process.waitForFinished()
