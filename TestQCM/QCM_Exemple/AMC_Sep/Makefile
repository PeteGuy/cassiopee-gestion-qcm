.PHONY: all read clean mrproper
TEX = xelatex
AMCFILE = AMC_main_Sep.tex

all:	
	$(TEX) $(AMCFILE)

clean:
	rm -f $(AMCFILE:.tex=.aux)
	#rm -f $(AMCFILE:.tex=.bbl)
	#rm -f $(AMCFILE:.tex=.blg)
	rm -f $(AMCFILE:.tex=.dvi)
	rm -f $(AMCFILE:.tex=.log)
	rm -f $(AMCFILE:.tex=.snm)
	rm -f $(AMCFILE:.tex=.nav)
	rm -f $(AMCFILE:.tex=.out)
	rm -f $(AMCFILE:.tex=.toc)
	#rm -f $(AMCFILE:.tex=.lof)
	rm -f *~

mrproper:
	make clean
	rm -f $(AMCFILE:.tex=.amc)
	rm -f $(AMCFILE:.tex=.pdf)

read:
	evince $(AMCFILE:.tex=.pdf)


