def remove_html_margins(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    with open(path, 'w') as f:
        for line in lines:
            if '<head>' in line:
                f.write(line.replace('<head>', '<head><style>body { margin: 0; }</style>'))
            else:
                f.write(line)


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
