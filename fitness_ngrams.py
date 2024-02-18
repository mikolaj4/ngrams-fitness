import re
import itertools
import string
import matplotlib.pyplot as plt
import random

ALPHABET = string.ascii_lowercase

def lclear(text):
    return re.sub(r'[^a-z]', '', text.lower())

def read_file(filename):
    counter = 0
    longtxt = ''
    with open(filename, encoding='utf8') as f:
        for line in f:
            longtxt += lclear(line.strip())
            counter += 1
    f.close()
    return lclear(longtxt)


def write_to_file(filename, content):
    with open(filename, 'w') as f:
        current_line_length = 0
        for word in content:
            word_length = len(word)
            while word_length > 0:
                if current_line_length + word_length > 200:
                    f.write('\n')
                    current_line_length = 0
                chars_to_write = min(word_length, 200 - current_line_length)
                f.write(word[:chars_to_write] + '')
                current_line_length += chars_to_write
                word = word[chars_to_write:]
                word_length -= chars_to_write


def generate_n_grams(n, alphabet):  # it creates all possible grams of len n from given alphabet and puts it in a dict with each value 0
    combinations = itertools.product(alphabet, repeat=n)
    n_grams_dict_0 = {''.join(combination): 0 for combination in combinations}
    return n_grams_dict_0


def calculate_n_grams_freq(n: int, inputFile, alphabet: str):
    grams = generate_n_grams(n, alphabet)
    # file_content = read_file(inputFile)
    file_content = inputFile
    total_n_grams = len(file_content) - n + 1

    for i in range(total_n_grams):  # after this loop the dict grams contains the NUMBER of how many times particular ngram occurs in text
        ngram = file_content[i:i+n]
        # print('gram: ',ngram)
        grams[ngram] += 1

    for key in list(grams.keys()):
        grams[key] /= total_n_grams

    # print('total ngrams freq:', total_n_grams)

    grams = {key: value for key, value in grams.items() if value != 0}

    return dict(sorted(grams.items(), key=lambda x: x[1], reverse=True))  # sorts by number of particular ngram


def compute_fitness(n, filename, frequencies):
    text = read_file(filename)
    total_n_grams = len(text) - n + 1
    score = 0.0
    for i in range(total_n_grams):
        current_gram = text[i:i+n]
        # print('cuttenr gram', current_gram)
        score += frequencies.get(current_gram, 0)
    # print('total ngrams sample:', total_n_grams)
    return round(((score / total_n_grams) * 100), 8)


def create_bar_diagram(values):
    x_positions = range(len(values))
    labels = ['plaintxt', 'random', 'cesar', 'substitution', 'vinegere', 'hill']  # Labels for each bar

    plt.bar(x_positions, values)

    # Add labels to the x-axis and y-axis
    plt.xlabel('sample text')
    plt.ylabel('fitness rating')

    # Add a title to the bar diagram
    plt.title('Fitness using quadgrams')

    # Set the x-axis tick positions and labels
    plt.xticks(x_positions, labels)

    plt.show()




n=2  # n-grams

eng_freq = calculate_n_grams_freq(n, read_file('data/Ulysses.txt'), ALPHABET)

fit_plain = compute_fitness(n, 'data/Ulysses.txt', eng_freq)
fit_random = compute_fitness(n, 'data/input_random.txt', eng_freq)
fit_cesar = compute_fitness(n, 'data/input_cesar.txt', eng_freq)
fit_subs = compute_fitness(n, 'data/input_subs.txt', eng_freq)
fit_ving = compute_fitness(n, 'data/input_vinegere.txt', eng_freq)
fit_hill = compute_fitness(n, 'data/input_hill.txt', eng_freq)

print(fit_plain)
print(fit_random)
print(fit_cesar)
print(fit_subs)
print(fit_ving)
values = [fit_plain, fit_random, fit_cesar, fit_subs, fit_ving, fit_hill]

write_to_file('data/text.txt', lclear(read_file('data/input_plaintext.txt')))

create_bar_diagram(values)










