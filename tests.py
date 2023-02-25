from pdf import Generator
from scrapping import Scrapper

s = Scrapper()
url_test = "https://www.olx.ua/d/uk/obyavlenie/1-k-s-54-m2-sofievskaya-borschagovka-ul-bogolyubova-bez-komissii-IDPtrjH.html"
scrapped_data = s.scrap_olx(url_test)
print("len", len(scrapped_data))
print("scrapped_data", scrapped_data)
document = Generator(scrapped_data)
document.html_to_pdf()
