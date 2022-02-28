from os import system

def compile_latex(scene, auto_compile_check):
    if (not auto_compile_check) or (auto_compile_check and scene.auto_compile):
        print(scene.project_data.doc_surround_tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        with open('try.tex', 'w') as f:
            f.write(scene.project_data.doc_surround_tikzify(*scene.current_canvas_dims, *scene.init_canvas_dims))
        system(f'pdflatex -synctex=1 -interaction=batchmode --shell-escape -halt-on-error try.tex')
        system(f'pdftocairo -png -scale-to-x {scene.current_canvas_dims[0]} -scale-to-y {scene.current_canvas_dims[1]} try.pdf')
