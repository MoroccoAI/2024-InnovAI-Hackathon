import pdfplumber
import re

def extract_and_clean_text(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if text:
                full_text += text + "\n"

    cleaned_text = " ".join(full_text.split())
    cleaned_text = re.sub(r"-\n", "", cleaned_text)
    return cleaned_text

pdf_path = "example.pdf"
pdf_to_text = extract_and_clean_text(pdf_path)

with open("cleaned_example.txt", "w", encoding="utf-8") as file:
    file.write(pdf_to_text)

import re
def ArticlesWithHeaders(filepath): 
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    keyword = "Article"
    updated_text = text.replace(keyword, f"\n\n\n\n{keyword}")

    arr = text.split("Article")

    def th(t): 
        t = t.split(" ")
        def texthalver(t):
            return "".join([t[i] for i in range(len(t)) if i%2 == 0])
        for i in range(len(t)):
            t[i] = texthalver(t[i])
        return " ".join(t)


    def HeaderMaker(arr): 
        L,T,C,S = "LIVRE","TTIITTRREE","CHAPITRE","SECTION"
        LH,TH,CH,SH,text = "","","","",""
        Header = LH + TH + CH + SH
        for i in arr[:]:
            Cond = [False]*3
            Header = "\n" + "\n" + "\n" + LH + TH + CH + SH 

            if S in i:
                SH = S + i.split(S)[1].replace("\n","") 
                SH = re.sub(r"(\w+)\d+", r"\1", SH)
                i = i.replace(SH,"") + "\n"
                Cond[0] = True
            if C in i:
                CH = C + i.split(C)[1].replace("\n","")
                CH = re.sub(r"(\w+)\d+", r"\1", CH) 
                i = i.replace(CH,"") + "\n"
                CH = "\n" + CH
                Cond[1] = True
                if Cond[0] == False:
                    SH = ""
            if T in i:
                TH = T + i.split(T)[1].replace("\n","") 
                i = i.replace(TH,"") + "\n"
                TH = re.sub(r"(\w+)\d+", r"\1", th(TH))
                Cond[2] = True
                if Cond[1] == False:
                    CH = ""
            if L in i:
                LH = L + i.split(L)[1].replace("\n","") + "\n"
                i = i.replace(LH,"") 
                if Cond[2] == False:
                    TH = ""

            i = Header + "\n" + "Article" + i
            text += i
        return HeaderMaker(arr)

Text = ArticlesWithHeaders('example.txt') 
