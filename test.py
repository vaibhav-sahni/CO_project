import re

def tokens(assembly_text):
    for line in assembly_text.split('\n'):
        tokens = re.findall(r'\w+\[.*?\]|\w+|\(.*?\)|[^\w\s]', line)
    return tokens

print(tokens("4label::add ra, sp, gp").count(":"))
