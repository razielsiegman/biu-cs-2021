DIRECTIVE_DEFAULTS = {
    'updates': 'sync',
    'length': '20',
    'uniqueness': 'interactions',
    'limit': '0',
    'regulation': 'noThresholds'
}

def remove_comments(text):
    new_text = ''
    for line in text.splitlines():
        if not line.startswith('//'):
            new_text += (line+'\n')
    return new_text

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
    observations_text = ''
    model_text = ''
    with open(rein_filename, 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.lstrip().startswith('#') or line.lstrip().startswith('(#'): 
                observations_text += (line)
            elif line.lstrip().startswith('$'):
                while not line.rstrip().endswith(';') and i < len(lines)-1:
                    observations_text += (line)
                    i += 1
                    line = lines[i]
                observations_text += (line)
            else: model_text += (line)
            i += 1
    model_text = add_extra_directives(model_text)
    model_text = remove_comments(model_text)
    observations_text = remove_comments(observations_text)
    with open('model.net', 'w') as f: f.write(model_text)
    with open('observation.spec', 'w') as f: f.write(observations_text)
main()