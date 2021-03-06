import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

#flask app
app = Flask(__name__)

#mongo variables
app.config["MONDO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

#PyMongo Instance
mongo = PyMongo(app)


@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template("index.html",
    words = mongo.db.words.find().sort("word_name",1))
    
@app.route('/add_word')
def add_word():
    return render_template('addword.html',
    partofspeech=mongo.db.partofspeech.find())
    
@app.route('/insert_word', methods=['POST'])
def insert_word():
    words = mongo.db.words
    words.insert_one(request.form.to_dict())
    return redirect(url_for('home_page'))
    
@app.route('/edit_word/<word_id>')
def edit_word(word_id):
    the_word = mongo.db.words.find_one({"_id": ObjectId(word_id)})
    all_partofspeech = mongo.db.partofspeech.find()
    return render_template('editword.html', word=the_word, partofspeech=all_partofspeech)
    
@app.route('/update_word/<word_id>', methods=["POST"])
def update_word(word_id):
    words = mongo.db.words
    words.update( {'_id': ObjectId(word_id)},
    {
        'word_name':request.form.get('word_name'),
        'part_of_speech':request.form.get('part_of_speech'),
        'word_definition':request.form.get('word_definition'),
        'pronunciation':request.form.get('pronunciation'),
        'sentence_use':request.form.get('sentence_use'),
        'submitter_name':request.form.get('submitter_name')
    })
    return redirect(url_for('home_page'))

@app.route('/delete_word/<word_id>')
def delete_word(word_id):
    mongo.db.words.remove({'_id': ObjectId(word_id)})
    return redirect(url_for('home_page'))

@app.route('/get_partofspeech')
def get_partofspeech():
    return render_template('partofspeech.html',
    partofspeech=mongo.db.partofspeech.find())


@app.route('/add_speechpart')
def add_speechpart():
    return render_template('addspeechpart.html')


@app.route('/insert_speechpart', methods=['POST'])
def insert_speechpart():
    partofspeech = mongo.db.partofspeech
    speechpart_doc = {'part_of_speech': request.form.get('part_of_speech')}
    partofspeech.insert_one(speechpart_doc)
    return redirect(url_for('get_partofspeech'))


@app.route('/edit_speechpart/<speechpart_id>')
def edit_speechpart(speechpart_id):
    return render_template('editspeechpart.html', 
    speechpart=mongo.db.partofspeech.find_one({'_id': ObjectId(speechpart_id)}))
    
    
@app.route('/update_speechpart/<speechpart_id>', methods=["POST"])
def update_speechpart(speechpart_id):
    mongo.db.partofspeech.update(
        {'_id': ObjectId(speechpart_id)},
        {'part_of_speech': request.form.get('part_of_speech')})
    
    return redirect(url_for('get_partofspeech'))   


@app.route('/delete_speechpart/<speechpart_id>')
def delete_speechpart(speechpart_id):
    mongo.db.partofspeech.remove({'_id': ObjectId(speechpart_id)})
    return redirect(url_for('get_partofspeech'))


@app.route('/about_page')
def about_page():
    return render_template("aboutflexicon.html")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=False)
        
      