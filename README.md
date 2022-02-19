# simple-compiler
Simple compiler is a compiler written in Python, for a custom programming language 'NHD' that can be compiled into working C code.

The motivation behind writing this compiler is that we have begun to study compilers in university and I figured this would be the
best way to gain a deeper and more concrete understanding of how compilers work would be to write one myself, or at least a proof
of concept. By using a number of resources on the web as well as my own knowledge of compilers I have been able to create my own
functional compiler that takes my own language 'NHD' and allows it to be compiled into functional C that can be executed using
(for example) GCC.

How to use:
- Read syntax.nhd as this contains the syntax of expressions in the language.
- Create a file with .nhd extension and write your code in whatever editor you prefer.
- Once you've written your code, you can compile it into C using the command 'python3 nhd.py FILE.nhd' where FILE is the name of yours.
- This will create a C file called out.c and in this will be your code translated into C, which can then be compiled by using the command:
  gcc out.c, and then executed via ./a.out to check if it works
  
Needless to say there are a lot of features missing as this is just a side project I worked on over a weekend but I would like to
come back to it and add more features. I think the biggest one would be to maybe convert the syntax.nhd file into a help.nhd which
acts more as an executable tutorial to the language so it can be used to teach even those who are complete beginners to programming.
