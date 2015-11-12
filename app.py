# -*- coding: utf-8 -*-

from flask import Flask
from flask import url_for, jsonify, render_template

import pymongo
import json

app = Flask(__name__)

# @app.route('/')
# @app.route('/<tag>/<page>')
# def index(tag=all, page=1):
#     data = []
#     with open('item.json') as f:
#         for line in f:
#             js = json.loads(line)
#             data.append(js)

#     tags = []
#     items = []
#     for i in data:
#         print 'is in ?', '日报'
#         if u'日报' in i['tag'] and (tag in i['tag'] or tag == 'all'):
#             items.append(i)
#         if u'日报' in i['tag']:
#             for j in i['tag']:
#                 if '-' not in j and j not in tags:
#                     tags.append(j)

#     return render_template('index.html',
#                             items = items,
#                             current_page = page,
#                             tags = tags)

@app.route('/')
@app.route('/<tag>/<page>')
def index(tag='all', page=1):
    client = pymongo.MongoClient('localhost', 27017)
    collection = client.items.MemectSpiderItem
    page = int(page)
    tags = []
    items = []
    keyword = []
    for i in collection.find().sort("time", pymongo.DESCENDING):
        if tag in i['tag'] or tag == 'all' or tag in i['keyword']:
            items.append(i)
        if u'日报' in i['tag']:
            for j in i['tag']:
                if '-' not in j and j not in tags:
                    tags.append(j)
        else:
            for k in i['keyword']:
                if k not in keyword:
                    keyword.append(k)

    return render_template('index.html',
                            items = items[page-1:page*50-1],
                            current_page = page,
                            current_tag = tag,
                            max_page = len(items)/50,
                            tags = tags,
                            keyword = keyword)


if __name__ == '__main__':
    app.run(debug=True)