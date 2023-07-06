import os
import sys
from syntactic import Syntactic
from argparse import ArgumentParser

argument = ArgumentParser()
argument.add_argument('-p', '--path', help='File to be compiled')
argument.add_argument('-f', '--folder', help='Folder with the example files')
argument.add_argument('-t', '--to-save', help='Test the compiler with a file')

args = argument.parse_args()

if __name__ == '__main__':
    if not args.path and not args.folder:
        print('Provide a file or a folder to compile')
        sys.exit(1)

    if args.path and args.folder:
        print('Pass a file or a folder, not both')
        print('File to compile only files, folder to compile all files in the folder (finishing with .txt)')
        sys.exit(1)

    if args.path:
        compiler = Syntactic()
        try:
            compiler.interpreter(args.path)
            compiler.initialize()
            if(args.to_save):
                compiler.symbol_table.saveTableToFile(args.to_save)
            print('Compilado com sucesso')
        except Exception as e:
            print(e)
            sys.exit(1)
        
    elif args.folder:
        files = os.listdir(args.folder)
        count = 0
        for file in files:
            count += 1
            if file.endswith('.txt'):
                print('\n------------------------\n')
                print('Compiling file: ', file)

                compiler = Syntactic()
                print('Compilado com sucesso!')
                try:
                    compiler.interpreter(os.path.join(args.folder, file))
                    compiler.initialize()
                    if(args.to_save):
                        compiler.symbol_table.saveTableToFile(args.to_save.replace('.txt', f'_{count}.txt'))
                except Exception as e:
                    print(e)