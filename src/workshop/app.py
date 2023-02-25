from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Form, Response
from fastapi.responses import FileResponse

from workshop.models.models import User, Gender, Role, UpdateUser
from scrapping import Scrapper
from pdf import Generator
import os


app = FastAPI()


@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.post("/postdata")
def postdata(url=Form()):
    s = Scrapper()
    # url_test = "https://www.olx.ua/d/uk/obyavlenie/1-k-s-54-m2-sofievskaya-borschagovka-ul-bogolyubova-bez-komissii-IDPtrjH.html"
    scrapped_data = s.scrap_olx(url)
    document = Generator(scrapped_data)
    pdf_document = document.html_to_pdf()
    headers = {'Content-Disposition': 'inline; filename="out.pdf"'}
    return Response(pdf_document, headers=headers, media_type='application/pdf')

