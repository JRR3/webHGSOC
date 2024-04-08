import pandas as pd
import re
import os
from path import Path

#<g id="a_node186"><a xlink:href="./combined_interactive/71077c9ac93f8948cb0c27b916e18d2b"
# xlink:title="merge_19_samples/scRNAseq/merge_19_samples@
#scRNAseq@get_matrix@anndata@noparams/merge_19_samples@
#scRNAseq@qc_metrics@compute_qc@noparams/merge_19_samples@
#scRNAseq@norm_all@freeman_tukey@noparams/merge_19_samples@
#scRNAseq@pca_all@pca@n_pcs~300/merge_19_samples@
#scRNAseq@harmonize_all@harmony@theta~1/merge_19_samples@
#scRNAseq@embedding_umap_all@umap@dist~0.5_n_ngb~150/
#merge_19_samples@scRNAseq@combined_interactive@iumap@
#cellAnn~cell_annotations">
def generate_regexp(mode: str):
    txt = (mode + "/(?P<hash>[a-z0-9]{32})"
            ".*?"
            "norm_all@(?P<norm_method>[a-z0-9_]+)@"
            ".*?"
            "theta~(?P<theta>[0-9]+)"
            ".*?"
            "dist~(?P<dist>[0-9]+[.]?[0-9]*)_"
            "n_ngb~(?P<n_ngb>[0-9]+)"
            ".*?"
            "cellAnn~(?P<ann_mode>[a-z_]+)"
            )
    return re.compile(txt)

combined_regexp = generate_regexp("combined_interactive")
gene_regexp = generate_regexp("gene_interactive")
# regexps = [combined_regexp, marker_regexp]

cell_ann_to_label= {"cell_annotations":"cluster",
           "original_cell_annotations":"full-auto"}

def generate_dictionary_from_svg(fname : str, regexp):
    hash2prop = {}
    prop2hash = {}
    with open(fname, "r") as f:

        while line := f.readline():

            obj = regexp.search(line)
            if obj is None:
                continue

            hsh = obj.group("hash")
            norm = obj.group("norm_method")
            theta = obj.group("theta")
            dist = obj.group("dist")
            n_ngb = obj.group("n_ngb")
            ann_mode = obj.group("ann_mode")

            key = norm + theta + dist + n_ngb + ann_mode
            prop2hash[key] = hsh



            local = {"norm":norm,
                    "theta":float(theta),
                    "dist":float(dist),
                    "n_ngb":int(n_ngb),
                    "ann_mode":cell_ann_to_label[ann_mode],
                    }

            hash2prop[hsh] = local

    return (hash2prop, prop2hash)

current = os.getcwd()
fname = "navigate.svg"
svg_path = Path(current) / fname

c_hash2prop, c_prop2hash = generate_dictionary_from_svg(
    svg_path, combined_regexp)
g_hash2prop, g_prop2hash = generate_dictionary_from_svg(
    svg_path, gene_regexp)

for prop, g_hash in g_prop2hash.items():
    c_hash = c_prop2hash[prop]
    c_prop = c_hash2prop[c_hash]
    c_prop["markers"] = g_hash

df = pd.DataFrame.from_dict(c_hash2prop)
df = df.T
df = df.sort_values(["norm",
                     "theta",
                     "dist",
                     "n_ngb",
                     "ann_mode"])
html = df.to_html()
print(df)
exit()
#./combined_interactive/d7f49252500e7b04f76b23aaa5f6984f/interactive_cell_annotation_scatter_plot.html
#<th><a href="./combined_interactive/d7f49252500e7b04f76b23aaa5f6984f/
#interactive_cell_annotation_scatter_plot.html">d7f49252500e7b04f76b23aaa5f6984f</a></th>
def generate_anchor(h:str, index:int)->str:
    txt = ("./combined_interactive/" +
           h +
           "/interactive_cell_annotation_scatter_plot.html")
    txt = '"' + txt + '"'
    txt = "<a target='_blank' href= " + txt + "> "
    txt += str(index)
    txt += " </a>"
    return txt

for index, h in enumerate(df.index):
    anchor = generate_anchor(h, index)
    html = html.replace(h, anchor)

fname = "menu.html"
with open(fname, "w") as f:
    f.write(html)

    



