# ✏ Markdown2LaTeX

Lemnos is a simple program that allows one to manage a to-do list via the command-line. 

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