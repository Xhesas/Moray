import random

from flask import Blueprint, abort

from .extensions import langs, default_render_template

lang_app = Blueprint('lang', __name__)

@lang_app.route('/vocabs/<lang>/show')
def route_show_vocabs_all(lang):
    if not lang in langs.keys():
        abort(404)
    return default_render_template(
        'vocab_list.html',
        title='Vocabulary of ' + lang,
        languages={'w': lang, 't': 'English'},
        vocabs=langs[lang].get_vocab()
    )

@lang_app.route('/vocabs/<lang>/show/<group>')
def route_show_vocabs(lang, group):
    if not lang in langs.keys():
        abort(404)
    return ''

@lang_app.route('/vocabs/<lang>/learn')
def route_learn_vocabs(lang):
    if not lang in langs.keys():
        abort(404)
    vocabs = langs[lang].get_vocab(synonyms=True)
    random.shuffle(vocabs)
    return default_render_template(
        'learn_vocab.html',
        languages={'w': lang, 't': 'English'},
        vocabs=vocabs
    )

@lang_app.route('/<lang>')
def route_main(lang):
    if not lang in langs.keys():
        abort(404)
    return default_render_template('langs/' + lang + '-index.html', lang=lang)