from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


def combine_frequecies(frequencies1: dict,
                       frequencies2: dict) -> dict[str, int]:
    all_word = set(frequencies1.keys()).union(frequencies2.keys())

    combined_frequencies = {}
    for word in all_word:
        freq1 = frequencies1.get(word, 0)
        freq2 = frequencies2.get(word, 0)
        combined_frequencies[word] = freq1 + freq2
    return combined_frequencies


def compute_differences(freq_text1, freq_text2):
    """
    Calcula a diferença de frequência (Texto 1 - Texto 2) para cada palavra.

    Args:
        freq_texto1 (dict): Frequências do Texto 1.
        freq_texto2 (dict): Frequências do Texto 2.

    Returns:
        dict: Dicionário com a diferença de frequência para cada palavra.
    """
    todas_palavras = set(freq_text1.keys()).union(freq_text2.keys())
    diferencas = {}
    for palavra in todas_palavras:
        diferencas[palavra] = freq_text1.get(
            palavra, 0) - freq_text2.get(palavra, 0)
    return diferencas


def color_func_factory(differences):
    """
    Retorna uma função de cor customizada para a nuvem de palavras baseada na diferença de frequência.

    Args:
        differences (dict): Dicionário com a diferença de frequência (Texto 1 - Texto 2) para cada palavra.

    Returns:
        function: Função que define a cor de cada palavra na nuvem.
    """
    def color_func(word,
                   font_size,
                   position,
                   orientation,
                   random_state=None,
                   **kwargs):
        diff = differences.get(word, 0)
        if diff > 0:
            # Vermelho para predominância no Texto 1
            return "rgb(255, 0, 0)"
        elif diff < 0:
            return "rgb(0, 0, 255)"      # Azul para predominância no Texto 2
        else:
            # Roxo para igualdade ou ausência de diferença
            return "rgb(128, 0, 128)"
    return color_func


def generate_and_show_wordcloud(frequencies,
                                color_func,
                                width=800,
                                height=400,
                                background_color='white', output_path="word_cloud.png"):
    """
    Gera e exibe uma nuvem de palavras a partir de um dicionário de frequências e função de cores.

    Args:
        frequencies (dict): Dicionário com as frequências de cada palavra.
        color_func (function): Função para determinar a cor de cada palavra.
        width (int, optional): Largura da imagem da nuvem de palavras.
        height (int, optional): Altura da imagem da nuvem de palavras.
        background_color (str, optional): Cor de fundo da nuvem.
    """
    wc = WordCloud(width=width,
                   height=height,
                   background_color=background_color)
    wc.generate_from_frequencies(frequencies)
    wc_recolored = wc.recolor(color_func=color_func)

    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wc_recolored, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def generate_frequencies(topics1: pd.DataFrame, topics2: pd.DataFrame):
    data1 = topics1.values.flatten()
    data2 = topics2.values.flatten()

    word_count1 = Counter(data1)
    word_count2 = Counter(data2)

    return dict(word_count1), dict(word_count2)


def wordcloud_create(topics1, topics2):
    frequencies_1, frequencies_2 = generate_frequencies(topics1, topics2)
    combined_frequencies = combine_frequecies(frequencies_1, frequencies_2)

    diffs = compute_differences(frequencies_1, frequencies_2)

    color_func = color_func_factory(diffs)

    generate_and_show_wordcloud(combined_frequencies, color_func)
