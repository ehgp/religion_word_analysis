"""Main."""
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PyPDF2 import PdfReader
import os
from os import listdir
from os.path import isfile, join
import re
from nltk.corpus import stopwords

cachedStopWords = set(stopwords.words("english"), "page")

cwd = os.getcwd()
religious_sources = os.path.join(cwd, "religious_sources")
onlyfiles = [
    f
    for f in os.listdir(religious_sources)
    if os.path.isfile(os.path.join(religious_sources, f))
]

os.chdir(religious_sources)
for file in onlyfiles:
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    file = file.replace(".pdf", "")
    if file == "ChristianBible":
        file = "ChristianBibleOldTestament"
        for pageNum in range(20, 579):
            page = reader.pages[pageNum]
            text = page.extract_text().lower().replace("www.holybooks.com", "")
            text = re.sub(r"\{.*:.*\}", "", text)
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
        file = "ChristianBibleNewTestament"
        for pageNum in range(579, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower().replace("www.holybooks.com", "")
            text = re.sub(r"\{.*:.*\}", "", text)
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    if file == "Dhammapada":
        for pageNum in range(25, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    if file == "FourVedas":
        for pageNum in range(50, number_of_pages):
            page = reader.pages[pageNum]
            text = (
                page.extract_text()
                .lower()
                .replace("rig veda – english translation", "")
                .replace("yajur veda english translation", "")
                .replace("sama veda english translation", "")
                .replace("atharva veda english translation", "")
            )
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    if file == "Quran":
        for pageNum in range(17, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    if file == "SiriGuruGranthSahib":
        for pageNum in range(17, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower().replace("ó", "")
            text = re.sub(r"\|\| .* \|\|", "", text)
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    # if file == "SrimadBhagavadGita":
    #     for pageNum in range(17, number_of_pages):
    #         page = reader.pages[pageNum]
    #         text = page.extract_text().lower()
    #         with
    if file == "Tanakh":
        for pageNum in range(15, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    if file == "TheUpanishads":
        for pageNum in range(14, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^\w]", "", text)
            text = " ".join(
                [word for word in text.split() if word not in cachedStopWords]
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)

    for pageNum in range(number_of_pages):
        page = reader.pages[pageNum]
        text = page.extract_text().lower()
        text = " ".join([word for word in text.split() if word not in cachedStopWords])
        with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
            myfile.write(text)


# comment_words = " "
# stopwords = set(STOPWORDS)
# for file in onlyfiles:
#     file = file.replace(".pdf", "")
#     with open("%s.txt" % (file), "r") as myfile:
#         data = myfile.read()
#         tokens = data.split()
#         for words in tokens:
#             comment_words = comment_words + words + " "
#             wordcloud = WordCloud(
#                 width=1400,
#                 height=800,
#                 background_color="gray",
#                 stopwords=stopwords,
#                 min_font_size=10,
#             ).generate(comment_words)
#             # plot the WordCloud image
#             plt.figure(figsize=(8, 8), facecolor=None)
#             plt.imshow(wordcloud)
#             plt.axis("off")
#             plt.tight_layout(pad=0)

#             plt.savefig(os.path.join(cwd,"wordclouds/%s.png"% (file)), bbox_inches="tight")

#             plt.show()
