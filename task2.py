def filter_gen(f_name, word_list):
    file = f_name
    if isinstance(f_name, str):
        file = open(f_name, 'r', encoding="utf-8")

    for line in file:
        splt_line = line.lower().split()
        if any(word.lower() in splt_line for word in word_list):
            yield line.rstrip("\n")

    if isinstance(f_name, str):
        file.close()
