import csv

def export_csv(tree, path):
    if not path:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(tree["columns"])
        for i in tree.get_children():
            writer.writerow(tree.item(i)["values"])
