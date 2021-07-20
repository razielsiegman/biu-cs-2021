DIRECTIVE_DEFAULTS = {
    'updates': 'sync',
    'length': '20',
    'uniqueness': 'interactions',
    'limit': '0',
    'regulation': 'noThresholds'
}

'''
model.net:
directive updates sync;
directive length 20;
directive uniqueness interactions;
directive limit 0;
directive regulation noThresholds;

model.rein:
// DTC is constitutively active

// Synchronous dynamics
directive updates sync;

// Default regulation conditions
directive regulation default;
'''
def remove_comments(text):
    new_text = ''
    for line in text.splitlines():
        if not line.startswith('//'):
            new_text += line+'\n'
    return new_text.rstrip()

def add_extra_directives(text):
    unfound_directives = list(DIRECTIVE_DEFAULTS.keys()).copy()
    for line in text.splitlines():
        if 'directive' in line:
            unfound_directives.remove(line.split()[1])
    if len(unfound_directives) == 0: return
    fill_defaults = input('Would you like to use default directives [y/n]? ').lower() in ('y','yes')
    if fill_defaults:
        for directive in unfound_directives:
            text = 'directive {} {};\n'.format(directive,DIRECTIVE_DEFAULTS[directive]) + text
    else:
        for directive in unfound_directives:
            val = input('Enter value for {}: '.format(directive))
            text = 'directive {} {};\n'.format(directive, val) + text
    return text


def main():
    rein_filename = input('Enter rein filename: ')
    text = ''
    with open(rein_filename, 'r') as f:
        #text_split = f.read().split('$', 1)
        text = f.read()
    text = add_extra_directives(text)
    text = remove_comments(text)
    split_index = text.find('$')
    with open('model.net', 'w') as f:
        #f.write(text_split[0])
        f.write(text[:split_index])

    with open('observation.spec', 'w') as f:
        # If you know that the keyword only appears once
        # you can changes this to fh.write(text_split[1])
        f.write(text[split_index:])

main()
