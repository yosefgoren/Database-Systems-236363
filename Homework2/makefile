IDS=211515606_205797095
IDS_MIN=211515606-205797095

$(IDS_MIN).zip: $(IDS).pdf Solution.py $(IDS).txt
	zip $@ $^
	cp $@ /mnt/c/Users/pc/Desktop/

$(IDS).txt:
	touch $@

Solution.py: code/Solution.py
	cp $^ .

$(IDS).pdf: Report/main.pdf
	cp $^ $@

clean:
	rm -rf $(IDS).pdf Solution.py $(IDS).txt $(IDS_MIN).zip
