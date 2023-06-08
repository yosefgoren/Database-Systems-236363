ID1=$(shell cat id1.txt)
ID2=$(shell cat id2.txt)

IDS=$(ID1)_$(ID2)
IDS_MINUS=$(ID1)-$(ID2)


$(IDS_MINUS).zip: $(IDS).pdf Solution.py $(IDS).txt
	zip $@ $^
	cp $@ /mnt/c/Users/pc/Desktop/

$(IDS).txt:
	touch $@

Solution.py: code/Solution.py
	cp $^ .

$(IDS).pdf: Report/main.pdf
	cp $^ $@

clean:
	rm -rf $(IDS).pdf Solution.py $(IDS).txt $(IDS_MINUS).zip
