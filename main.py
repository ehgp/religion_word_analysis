"""Main."""
import datetime as dt
import logging
import logging.config
import os
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from PyPDF2 import PdfReader
from wordcloud import WordCloud

# Logging
path = Path(os.getcwd())
Path("log").mkdir(parents=True, exist_ok=True)
log_config = Path(path, "log_config.yaml")
timestamp = "{:%Y_%m_%d_%H_%M_%S}".format(dt.datetime.now())
with open(log_config, "r") as log_file:
    config_dict = yaml.safe_load(log_file.read())
    # Append date stamp to the file name
    log_filename = config_dict["handlers"]["file"]["filename"]
    base, extension = os.path.splitext(log_filename)
    base2 = "_" + os.path.splitext(os.path.basename(__file__))[0] + "_"
    log_filename = "{}{}{}{}".format(base, base2, timestamp, extension)
    config_dict["handlers"]["file"]["filename"] = log_filename
    logging.config.dictConfig(config_dict)
logger = logging.getLogger(__name__)

stopwords_list = stopwords.words("english")
# Update the stopwords list
stopwords_list.extend(
    [
        "said",
        "one",
        "like",
        "came",
        "back",
        "lord",
        "god",
        "allah",
        "indra",
        "gods",
        "agni",
        "page",
        "chapter",
        "said",
        "gutenberg",
        "could",
        "would",
        "shall",
        "unto",
        "thou",
        "thy",
        "ye",
        "thee",
        "upon",
        "hath",
        "came",
        "come",
        "things",
        "also",
        "saying",
        "say",
        "english",
        "translation",
        "commentary",
        "theupanishad",
        "us",
        "upanishad",
        "may",
        "shalt",
        "let",
        "indeed",
        "verily",
        "yea",
        "yay",
        "day",
        "among",
        "surely",
        "thus",
        "must",
        "therefore",
    ]
)

cwd = os.getcwd()
religious_sources = os.path.join(cwd, "religious_sources")
plots = os.path.join(cwd, "plots")
wordclouds = os.path.join(cwd, "wordclouds")

png_plot_files = [f for f in os.listdir(plots) if f.endswith(".png")]
png_wordcloud_files = [f for f in os.listdir(wordclouds) if f.endswith(".png")]

religious_sources_mod_text_files = [
    "New_Testament_Christian_Bible.txt",
    "Old_Testament_Christian_Bible.txt",
    "Siri_Guru_Granth_Sahib_Sikhism.txt",
    "Srimad_Bhagavad_Gita_Hinduism.txt",
    "Tanakh_Judaism.txt",
    "The_Upanishads_Hinduism.txt",
]

logger.info("Removing existing files to start fresh...")
for file in religious_sources_mod_text_files:
    os.remove(os.path.join(religious_sources, file))
for file in png_plot_files:
    os.remove(os.path.join(plots, file))
for file in png_wordcloud_files:
    os.remove(os.path.join(wordclouds, file))

os.chdir(religious_sources)
logger.info("Translating PDFs to text files...")
pdf_files = [f for f in os.listdir(religious_sources) if f.endswith(".pdf")]
for file in pdf_files:
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    file = file.replace(".pdf", "")
    if file == "Siri_Guru_Granth_Sahib_Sikhism":
        for pageNum in range(17, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower().replace("ó", "")
            text = re.sub(r"\|\| .* \|\|", "", text)
            text = re.sub(r"[^a-zA-Z0-9\s]+", "", text)
            text = " ".join(text.split())
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    elif file == "Tanakh_Judaism":
        for pageNum in range(15, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^a-zA-Z0-9\s]+", "", text)
            text = text.replace(" l ord ", " lord ")
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    elif file == "The_Upanishads_Hinduism":
        for pageNum in range(14, number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^a-zA-Z0-9\s]+", "", text)
            text = (
                " ".join(text.split())
                .replace("theupanishad", "")
                .replace("theupanishads", "")
                .replace("ofthe", "of the")
                .replace("themind", "the mind")
            )
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)
    else:
        for pageNum in range(number_of_pages):
            page = reader.pages[pageNum]
            text = page.extract_text().lower()
            text = re.sub(r"[^a-zA-Z0-9\s]+", "", text)
            text = " ".join(text.split())
            with open("%s.txt" % (file), "a+", encoding="utf-8") as myfile:
                myfile.write(text)

logger.info("Modifying Text Files...")
text_files = [f for f in os.listdir(religious_sources) if f.endswith(".txt")]
for file in text_files:
    if file == "Christian_Bible.txt":
        with open(
            os.path.join(religious_sources, file), "r", encoding="utf-8"
        ) as myfile:
            data = myfile.read()
            data = data.split("Matthew", 1)
        with open(
            os.path.join(religious_sources, "Old_Testament_Christian_Bible.txt"),
            "w",
            encoding="utf-8",
        ) as myfile:
            myfile.write(data[0])
        with open(
            os.path.join(religious_sources, "New_Testament_Christian_Bible.txt"),
            "w",
            encoding="utf-8",
        ) as myfile:
            myfile.write(data[1])
    else:
        continue

logger.info("Creating Bar Charts with 10 most common words and Word Clouds...")
os.chdir(cwd)
text_files = [f for f in os.listdir(religious_sources) if f.endswith(".txt")]
for file in text_files:
    with open("./religious_sources/%s" % (file), "r", encoding="utf-8") as myfile:
        data = myfile.read()
        data = data.lower()
        data = re.sub(r"[^a-zA-Z0-9\s]+", "", data)
        data = " ".join(data.split())
        data = "".join(i for i in data if not i.isdigit())
        words = word_tokenize(data)
        clean_words = [word for word in words if word not in stopwords_list]
        # tokenize text by words
        fdist = FreqDist(clean_words)
        tuple_list = fdist.most_common(10)
        # sort in-place from highest to lowest
        tuple_list.sort(key=lambda x: x[1], reverse=True)
        # save the names and their respective scores separately
        # reverse the tuples to go from most frequent to least frequent
        word, freq = map(list, zip(*tuple_list))
        x_pos = np.arange(len(word))
        # calculate slope and intercept for the linear trend line
        slope, intercept = np.polyfit(x_pos, freq, 1)
        trendline = intercept + (slope * x_pos)
        plt.figure(figsize=(12, 12), facecolor=None)
        plt.plot(x_pos, trendline, color="red", linestyle="--")
        plt.bar(x_pos, freq, align="center")
        plt.xticks(x_pos, word, rotation=90)
        plt.ylabel("Frequency")
        plt.title("Frequency of Words in %s" % (file))
        plt.savefig(
            os.path.join(cwd, "plots/bar_plot_%s.png" % (file.replace(".txt", "")))
        )
        # Convert word list to a single string
        clean_words_string = " ".join(clean_words)
        wordcloud = WordCloud(
            width=1400,
            height=800,
            background_color="gray",
            stopwords=stopwords_list,
            min_font_size=10,
        ).generate(clean_words_string)
        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.title("Word Cloud of %s" % (file))
        plt.savefig(
            os.path.join(
                cwd, "wordclouds/wordcloud_%s.png" % (file.replace(".txt", ""))
            ),
            bbox_inches="tight",
        )
