all: main.pdf

main.pdf:	main.tex
	pdflatex -interaction batchmode -shell-escape main.tex 
	pdflatex -interaction batchmode -shell-escape main.tex 

check:
	aspell -l en -t -c main.tex

show:
	evince main.pdf

clean:
	rm -f main.aux main.log main.out main.pdf main.aux main.bbl main.blg main.nav main.snm main.toc main.fdb_latexmk
