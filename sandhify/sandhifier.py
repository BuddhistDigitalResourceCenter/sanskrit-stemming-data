# encoding: utf-8
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'resources')))
from find_applicable_sandhis import FindApplicableSandhis
from collections import OrderedDict

find_sandhis = FindApplicableSandhis('sanskrit', True)


def find_uninflected_stem(stem, form):
    """
    Finds all the shared caracters from left to right.
    find_uninflected_stem('rAmaH', 'rAmo') => -1+aH

    :param stem: form to reach by applying the diff
    :param form: given form
    :return: a diff: '-<number of chars to delete>+<characters to add>'
    """
    i = 0
    while i <= len(stem)-1 and i <= len(form)-1 and stem[i] == form[i]:
        i += 1
    stem_ending = stem[i:]
    form_ending = form[i:]
    if stem_ending == '' and form_ending == '':
        operation = ''
    else:
        form_ending_len = len(form_ending)
        operation = '-{}+{}'.format(form_ending_len, stem_ending)
    return operation


def singled_entries(entries):
    singled = OrderedDict()
    for line in entries:
        form, value = line.split(',')
        value = adjust_new_initial_in_consonant1_sandhi(value)
        if form not in singled.keys():
            singled[form] = [value]
        else:
            if value not in singled[form]:
                singled[form].append(value)
    output = []
    for k, v in singled.items():
        output.append(k+','+'|'.join(v))
    return output


def adjust_new_initial_in_consonant1_sandhi(cmd):
    if '/=' not in cmd and '-+=' not in cmd and '- +=' not in cmd:
        initial, remainder = cmd.split('$')
        new_initial = cmd.split('/-')[1].split('+')[0].strip()
        if initial != new_initial:
            return '{}${}'.format(new_initial, remainder)
    return cmd


def sandhify(inflected_form):
    sandhied = find_sandhis.all_possible_sandhis(inflected_form)
    singled = singled_entries(sandhied)
    return singled


def sandhied_n_lemmatized_total(raw_pairs):
    """
    applies apply_all_sandhis() on every entry in raw_pairs
    creates a new diff with the lemma from which the inflected form was derived
    discarding the diff produced to find the unsandhied inflected form.

    outputformat: '<sandhied_inflected_form>,<initial>,<diffs>/<initial_diff>'
    <diffs>: '<diff_to_1st_lemma>;<diff_to_2nd_lemma>;…'
    <diff_to_nth_lemma>: '-<number_of_chars_to_delete>+<chars_to_add>'
    <initial_diff>: '-<sandhied_initial>+<initial>'

    :param raw_pairs: [(inflected_form, lemma), …] generated by raw_parse_Heritage_XML.py
    :return: ex. ['prezyate,a$-1+;-6+I/-'+', 'aprezyata,A:i:u:U:f:e:E:o:O$-1+;-6+I/', …]
    """
    def is_unknown_lemma(lemma, lemmas):
        if lemma not in lemmas.keys():
            lemmas[lemma] = True
            return True
        return False
    lemmas = {}
    
    total_sandhied = []
    for infl, non_infl, POS in raw_pairs:
        # adding the lemmas to the total output
        all_non_infl = [a for a in non_infl.split('/') if '—' not in a]
        all_non_infl_entries = ['{},$/=0#{}'.format(a, POS) for a in all_non_infl if is_unknown_lemma(a, lemmas)]
        total_sandhied.extend(all_non_infl_entries)
        
        sandhied = ['{},$/=0#{}'.format(infl, POS)] # include the inflected form.
        sandhied.extend([f+'#'+POS for f in find_sandhis.all_possible_sandhis(infl)])
        stems = non_infl.split('/')
        for entry in sandhied:
            parts = entry.split(',')
            partss = parts[1].split('$')
            partsss = partss[1].split('=')
            sandhied_form = parts[0]
            initial = partss[0]
            new_initials = partsss[0].split('/')[1]
            sandhi_type_n_POS = partsss[1]
            operations = []
            for stem in stems:
                operation = find_uninflected_stem(stem, sandhied_form)
                if operation != '':
                    operations.append(operation)
            to_add = '{},{}${}/{}={}'.format(sandhied_form, initial, ';'.join(operations), new_initials,
                                                sandhi_type_n_POS)
            total_sandhied.append(to_add)
    
    singled = singled_entries(total_sandhied) 
    return singled


def import_inflected_pairs():
    """

    :return: a list of tuples (inflected form, lemma, POS)
            POS values are from 1 to 4 for normal part of speech tags,
            -1 in case of multi-token lemmas.
    """
    folders = ['../input/custom_entries', '../input/maxmatch_workaround']

    input_files = ['{}/{}'.format(folder, f) for folder in folders for f in os.listdir(folder)]
    input_files.append('../input/preverbs.txt')
    input_files.append('../output/heritage_raw_pairs.txt')  # Sanskrit Heritage data

    total = []
    for in_file in input_files:
        with open(in_file) as f:
            for a in f.readlines():
                if '/' in a:
                    form, lemmas = a.strip().split(',')
                    for l in lemmas.split('/'):
                        if '—' not in l:
                            lemma, POS = l[:-1], l[-1]
                            total.append((form, lemma, POS))
                        else:
                            total.append((form, l, '-1'))  # default value for no-POS
                else:
                    form, l = a.strip().split(',')
                    if '—' not in l:
                        lemma, POS = l[:-1], l[-1]
                        total.append((form, lemma, POS))
                    else:
                        total.append((form, l, '-1'))
    return total


if __name__ == "__main__":
    # opening the inflected forms
    inflected = import_inflected_pairs()

    total_sandhied = sandhied_n_lemmatized_total(inflected)

    with open('../output/trie_content.txt', 'w', -1, 'utf-8-sig') as g:
        output = '\n'.join(total_sandhied)
        g.write(output)
