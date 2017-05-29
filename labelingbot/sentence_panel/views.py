from flask import render_template

from ..models import (
    Sentence, Paraphrase, SentenceSimilairty, SentenceBinary
)
from . import sentence_panel


@sentence_panel.route('/sentences', methods=['GET'])
def sentence_list():
    sentences = Sentence.query.all()
    return render_template('sentence/sentence_list.html', sentences=sentences)


@sentence_panel.route('/sentence/<int:id>', methods=['GET'])
def sentence_detail(id):
    sentence = Sentence.query.get_or_404(id)
    return render_template(
        'sentence/sentence_detail.html',
        sentence=sentence,
    )


@sentence_panel.route('/sentence/<int:sid>/paraphrase/<int:pid>')
def paraphrase_detail(sid, pid):
    paraphrase = Paraphrase.query.get_or_404(pid)
    return render_template(
        'sentence/paraphrase_detail.html',
        paraphrase=paraphrase,
    )
