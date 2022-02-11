from hse_hw_moad_vik_f import ast_vis, fib
import ast 
import inspect
import os
import shutil
from pdflatex import PDFLaTeX 
# info how to create package: https://packaging.python.org/en/latest/tutorials/packaging-projects/


def gen_pic(img_file, S=None, with_table=False):
    path = 'artifacts'
    os.makedirs(path, exist_ok=True)
    
    begin = '\\documentclass{article}\n\\usepackage{graphicx}\n\\graphicspath{ {./' + path + \
            '/} }\n\\begin{document}\n\\begin{center}\n'
    pic = '\\includegraphics[width = 15cm]{' + img_file + '}'
    
    if with_table is True and S is not None:
        pic += '\n\\begin{tabular}\n{ |' + ' c |' * len(S[0]) + ' }' + '\n\hline \n'
        pic += ' \\\ \n\\hline\n'.join(map(lambda s: ' & '.join(s), S)) + '\\\ \n\hline\n\\end{tabular}'

    end = '\n\\end{center}\n\\end{document}\n'
    
    with open(f'{path}/two.tex', 'w') as out:
               out.write(begin + pic + end)
    

if __name__ == '__main__':
    folder = 'artifacts'
    
    decor = ast_vis.AST2IMG()
    decor.visit(ast.parse(inspect.getsource(fib)))
    decor.draw(f"{folder}/ast_fib.png")
    
    S = [['Hey', 'you!', 'out there', 'in the cold'], 
        ['Getting', 'lonely,', 'getting', 'old'], 
        ['Can', 'you', 'feel', 'me'],
        ['Hey', 'you!', 'standing in', 'the aisles,'],
        ['With itchy', 'feet and', 'fading', 'smiles,'],
        ['Can', 'you', 'feel', 'me'],
        ['-', 'star', '-', 'wars'],
        ['(German)', 'Donaudampschif', 'fahrtkapitänswitwen', 'undwaisenversicherungsgesellschaft']]
        
    gen_pic('ast_fib.png', S, with_table=True)
    pdfl = PDFLaTeX.from_texfile(f'{folder}/two.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    shutil.move('two.pdf', f'{folder}/two.pdf')
    os.remove(f'{folder}/two.tex')
    os.remove(f'{folder}/ast_fib.png')
    
    with open(f'{folder}/two_package_link.txt', 'w') as out:
        out.write('https://test.pypi.org/project/hse-hw-moad-vik-f/0.0.1/\n')
        
    print('-_-_- Done -_-_-')
