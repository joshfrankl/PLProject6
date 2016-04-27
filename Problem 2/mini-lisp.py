# -*- coding: utf-8 -*-
from yacc import yacc, lisp_str
import cmd

class MiniLisp(cmd.Cmd):     # See https://docs.python.org/2/library/cmd.html
    """
    MiniLisp evalúa expresiones sencillas con sabor a lisp, 
    más información en http://www.juanjoconti.com.ar
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "ml> "
        self.intro  = "Bienvenido a MiniLisp"

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_EOF(self, args):
        """Exit on system end of file character"""
        print "Good bye!"
        return self.do_exit(args)

    def do_help(self, args):
        print self.__doc__

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def parse(self, program):
        "Read a Scheme expression from a string."
        return self.read_from_tokens(self.tokenize(program))

    def tokenize(self, line):
        "Convert a string into a list of tokens."
        return line.replace('(',' ( ').replace(')',' ) ').split()

    def read_from_tokens(self, tokens):
        "Read an expression from a sequence of tokens."
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF while reading')
        token = tokens.pop(0)
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(self.read_from_tokens(tokens))
            tokens.pop(0) # pop off ')'
            return L
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            return str(token)

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        print self.parse(line)
        '''result = yacc.parse(line)
        s = lisp_str(result)
        if s != 'nil':
            print s'''

if __name__ == '__main__':
        ml = MiniLisp()
        ml.cmdloop()     # See https://docs.python.org/2/library/cmd.html
