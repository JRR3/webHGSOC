import re
rx = re.compile("</body>")
i_path = "interactive_gene_COL1A2.html"
o_path = "m_interactive_gene_COL1A2.html"
js_line = "<script src='add_menu_title.js'> </script>"
with open(i_path, "r") as f:
    with open(o_path, "w") as out:
        for line in f:
            if rx.match(line):
                out.write(js_line)
            out.write(line)