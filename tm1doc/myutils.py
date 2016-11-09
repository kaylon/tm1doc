

def replace_multiple(to_replace, replace_by, text):
    for single_replace in to_replace:
        text = text.replace(single_replace, replace_by)

    return text
