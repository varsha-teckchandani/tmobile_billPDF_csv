# tmobile_billPDF_csv
Quick python script to read multiple pdf files of format tmobile bills and generate a csv with line wise and billing period wise data for easy splitting between lines

# To run
python3 tmobile_bill_pdftocsv.py NovBill.pdf Decbill.pdf

Note that the bill files here should be direct bill pdf exports from tmobile portals only then it will work as expected.

# Example output generated 

Line,Bill Period,Base charge,"Extra charges (Equipment, Services etc)",Bill Amount
(469) 325-xxxx,Nov 12 - Dec 12,$23.33,$0.00,$23.33
(469) 438-xxxx,Nov 12 - Dec 12,$23.33,$15.00,$38.33
(972) 799-xxxx,Nov 12 - Dec 12,$23.33,$45.20,$68.53
(469) 929-xxxx,Nov 12 - Dec 12,$23.33,$0.00,$23.33
(469) 325-xxxx,Dec 12 - Jan 11,$23.33,$0.00,$23.33
(469) 438-xxxx,Dec 12 - Jan 11,$23.33,$15.00,$38.33
(972) 799-xxxx,Dec 12 - Jan 11,$23.33,$45.20,$68.53
(469) 929-xxxx,Dec 12 - Jan 11,$23.33,$0.00,$23.33
