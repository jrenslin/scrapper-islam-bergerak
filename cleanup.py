# --------------------- Retrieve data from Islam Bergerak articles --------------------- #

from datetime import datetime
import os
import json

class Article ():

    def __init__(self):
        self.keywords = []
        self.authors = []
        self.link = []

        self.date = ""
        self.title = ""
        self.description = ""
        self.section = ""

        self.content = ""

    def return_dict (self):
        return {
            "title":self.title,
            "description":self.description,
            "section":self.section,
            "keywords":self.keywords,
            "authors":self.authors,
            "link":self.link,
            "date":self.date,
            "content":self.content
        }
    
counter = 0
for ffile in os.listdir('islambergerak-archive'):

    file = "islambergerak-archive/" + ffile

    handle = open(file, "r")
    content = handle.read()
    handle.close()

    article_metatags = content[content.find('<link'):content.find("</head>")]
    article_metatags = article_metatags[:article_metatags.find('<meta property="og:image:width"')]
    article_content = content[content.find("</head>"):]

    article = Article()

    start_key = 'rel="canonical" href="'
    article.link = article_metatags[(article_metatags.find(start_key) + len(start_key)):article_metatags.find('" />', article_metatags.find(start_key))]

    start_key = 'property="og:title" content="'
    article.title = article_metatags[(article_metatags.find(start_key) + len(start_key)):article_metatags.find('" />', article_metatags.find(start_key))].replace(" | islambergerak Magazine", "")

    start_key = 'property="og:description" content="'
    article.description = article_metatags[(article_metatags.find(start_key) + len(start_key)):article_metatags.find('" />', article_metatags.find(start_key))]

    start_key = 'property="article:section" content="'
    article.section = article_metatags[(article_metatags.find(start_key) + len(start_key)):article_metatags.find('" />', article_metatags.find(start_key))]

    start_key = 'property="article:published_time" content="'
    tdate = article_metatags[(article_metatags.find(start_key) + len(start_key)):article_metatags.find('" />', article_metatags.find(start_key))]
    article.date = tdate[:10]

    tag_spaces = article_metatags.split('property="article:tag"')
    tag_spaces.remove(tag_spaces[0])

    for tag_space in tag_spaces:
        start_key = ' content="'
        article.keywords.append(tag_space[(tag_space.find(start_key) + len(start_key)):tag_space.find('" />', tag_space.find(start_key))])

    article_content = article_content[article_content.find('<article'):article_content.find('</article>')]

    start_pos = article_content.find('<em>by</em>')
    authordate = article_content[start_pos:article_content.find("</a></span>", start_pos)].strip().split("</a>")
    aut = authordate[0]
    article.authors = aut.split('">')[1]
    print(aut)
    print(aut.split('">')[1])

    article_start = '<div class="pf-content">'
    article_end = '<div class="printfriendly pf-alignright">'

    article_c = article_content[article_content.find(article_start) + 24:article_content.find(article_end)]
    article.content = article_c.replace ("</p><p>", "</p>\n\n<p>")

    handle = open("islambergerak-json/" + str(counter) + ".json", "w")
    handle.write(json.dumps(article.return_dict(), sort_keys=True, indent=4))
    handle.close()

    print ("Stored article " + str(counter) + " to islambergerak-json/" + str(counter) + ".json (" + article.title + ")")
    del article

    counter = counter + 1
