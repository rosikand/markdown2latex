# 🪃 Markdown2LaTeX

Simple program that produces a LaTeX output based on markdown source as input.


## Example 

`examples/sample_input.md` 
```markdown
## This is a sample input

It is a pretty nice looking document and even has some in-line `code` as well as **bold** characters! 
```
Running `python3 markdown2latex.py examples/sample_input.md > examples/sample_output.tex` produces `examples/sample_output.tex`: 
```latex
\subsection{This is a sample input}

It is a pretty nice looking document and even has some in-line \codeword{code} as well as \textbf{bold} characters!
```

## How to use 

Clone this repo and `cd` into the directory. Then, for any input markdown file (e.g. `input.md`), run the following to produce the output tex file (e.g. `output.tex`):  
```
$ python3 markdown2latex.py input.md > output.tex 
```

## Note 

Since this is not a full parser/compiler, it will *not* work for all inputs. The goal here is to automate a lot of the busy work in the conversion process. It was also specifically designed for my use cases and thus has some conversion functionality that is tailored towards the syntax I use. 