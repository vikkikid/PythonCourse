import os


def gen_table(S):
    path = 'artifacts'
    os.makedirs(path, exist_ok=True)
    
    begin = '\\documentclass{article}\n\\begin{document}\n\\begin{table}[h!]\n\\begin{center}\n\\begin{tabular}\n'
    lines = '{ |' + ' c |' * len(S[0]) + ' }' + '\n\hline \n'
    gen = ' \\\ \n\\hline\n'.join(map(lambda s: ' & '.join(s), S)) + '\\\ \n\hline'
    end = '\n\\end{tabular}\n\\end{center}\n\\end{table}\n\\end{document}\n'
    
    with open(f'{path}/one.tex', 'w') as out:
               out.write(begin + lines + gen + end)
            
    print('-_-_- Done -_-_-')
    

if __name__ == '__main__':
    S = [['Hey', 'you!', 'out there', 'in the cold'], 
        ['Getting', 'lonely,', 'getting', 'old'], 
        ['Can', 'you', 'feel', 'me'],
        ['Hey', 'you!', 'standing in', 'the aisles,'],
        ['With itchy', 'feet and', 'fading', 'smiles,'],
        ['Can', 'you', 'feel', 'me'],
        ['-', 'star', '-', 'wars'],
        ['(German)', 'Donaudampschif', 'fahrtkapitänswitwen', 'undwaisenversicherungsgesellschaft']]
    
    S = [[str(j) for j in i] for i in S] # all elements -> strings
    
    if all(len(i) == len(S[0]) for i in S) is True:
        gen_table(S)
    else:
        raise Exception('All lines must be the same length')
     