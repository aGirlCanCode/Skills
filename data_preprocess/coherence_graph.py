import os

from gensim import corpora, models, matutils
from gensim.models.coherencemodel import CoherenceModel

import matplotlib.pyplot as plt


def compute_coherence_values(id2word, dictionary, corpus, texts, limit, start, step):
    """Computes coherence values for different number of topics for the LDA Model in terms of c_v"""
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=id2word, passes=70)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    save_graph(coherence_values, limit, start, step)
    

def save_graph(coherence_values, limit, start, step):
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig(os.path.join(os.getcwd(), 'CoherenceGraph.png'), bbox_inches='tight')