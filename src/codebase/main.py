import os
import sys
from syntactic import Syntactic
from argparse import ArgumentParser

argument = ArgumentParser()
argument.add_argument('-p', '--path', help='File to be compiled')
argument.add_argument('-f', '--folder', help='Folder with the example files')

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
            print('Compilado com sucesso')
        except Exception as e:
            print(e)
            sys.exit(1)
        
    elif args.folder:
        files = os.listdir(args.folder)
        for file in files:
            if file.endswith('.txt'):
                print('\n------------------------\n')
                print('Compiling file: ', file)

                compiler = Syntactic()
                print('Compilado com sucesso!')
                try:
                    compiler.interpreter(os.path.join(args.folder, file))
                    compiler.initialize()
                except Exception as e:
                    print(e)