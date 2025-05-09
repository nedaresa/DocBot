May 9th, 2025

Neda Jabbari



DocBot 

Gets image of your document (passport, EAD, or driver's license), identifies the document type and extracts key information using GPT-4.1 API. Works with image files. 

I tested it on jpg and png (3 total sample documents, 1 of each EAD, passport and driver's license were all correctly classified with requested fields correctly extracted). 

A combination of fine tuning a relevant multi modal LLM with legal datasets would improve the results. Another helpful step would be build and use of counrty-specific Pydantic models to extract correct information (given various formats of information representation across countries).

Example usage: $ python DocBot.py './data/2.jpg'



env:
openai=1.77.0=py39hecd8cb5_0
python=3.9.21=hce00570_1
pydantic=2.10.3=py39hecd8cb5_0
pip=25.1=pyhc872135_2