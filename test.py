# -*- coding: utf-8 -*-

def _write_new_file(content, index):
    with open('joke-%d.json' % index, 'w', encoding='utf-8') as f:
        content = content.replace('jokeInfo', 'content')
        f.write(content)
    f.close()

with open('jokes.json', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    i = 1
    for line in lines:
        _write_new_file(line, i)
        i+=1
file.close()
