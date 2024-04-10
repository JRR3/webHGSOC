import pandas as pd
import re
import os
from path import Path

#<g id="a_node186"><a xlink:href="./combined_interactive/
#71077c9ac93f8948cb0c27b916e18d2b"
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
gene_regexp = generate_regexp("all_genes_interactive")
# regexps = [combined_regexp, marker_regexp]

cell_ann_to_label= {"cell_annotations":"cluster",
           "original_cell_annotations":"full-auto"}

def generate_dictionary_from_svg(fname : str, regexp):
    # The hash2prop dictionary maps a hash to another
    # dictionary containing the properties of a given
    # category.
    hash2prop = {}
    # The prop2hash dictionary maps a string of properties
    # to the hash that represents them.
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

# Now we generate the dictionaries that contain the
# properties of each folder. We have two folders:
# combined_interactive and all_genes_interactive.

# The first one has html files with the
# description of the cell types and samples.

# The second one has html files where each file
# merges the gene markers into one object.
c_hash2prop, c_prop2hash = generate_dictionary_from_svg(
    svg_path, combined_regexp)
g_hash2prop, g_prop2hash = generate_dictionary_from_svg(
    svg_path, gene_regexp)

# We create an additional key in the
# c_prop dictionary to be filled with the
# hash of the corresponding gene marker file. 
for prop, g_hash in g_prop2hash.items():
    c_hash = c_prop2hash[prop]
    c_prop = c_hash2prop[c_hash]
    c_prop["Gene Selector"] = g_hash

df = pd.DataFrame.from_dict(c_hash2prop)
df = df.T
df = df.sort_values(["norm",
                     "theta",
                     "dist",
                     "n_ngb",
                     "ann_mode"])
df = df.reset_index(names="Sample Selector")
html = df.to_html()
print(df)
#./combined_interactive/d7f49252500e7b04f76b23aaa5f6984f/interactive_cell_annotation_scatter_plot.html
#<th><a href="./combined_interactive/d7f49252500e7b04f76b23aaa5f6984f/
#interactive_cell_annotation_scatter_plot.html">d7f49252500e7b04f76b23aaa5f6984f</a></th>
#"/interactive_cell_annotation_scatter_plot.html")

def generate_anchor(file_hash:str,
                    folder_path:str,
                    filename:str,
                    index:int)->str:
    txt = ("./" + folder_path + "/" +
           file_hash +
           "/" + filename + ".html")
    txt = '"' + txt + '"'
    txt = "<a target='_blank' href= " + txt + "> "
    txt += str(index)
    txt += " </a>"
    return txt

for index, row in df.iterrows():
    sample_hash = row["Sample Selector"]
    anchor = generate_anchor(
        sample_hash, 
        "combined_interactive",
        "interactive_cell_annotation_scatter_plot",
        index)
    html = html.replace(sample_hash, anchor)

    gene_hash = row["Gene Selector"]
    anchor = generate_anchor(
        gene_hash, 
        "all_genes_interactive",
        "interactive_all_genes",
        index)
    html = html.replace(gene_hash, anchor)

fname = "menu.html"
with open(fname, "w") as f:
    f.write(html)

    



