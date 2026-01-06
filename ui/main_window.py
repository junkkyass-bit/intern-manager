import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from database.db_manager import DatabaseManager
from utils.exporter import export_csv

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Stagiaires")
        self.geometry("1350x750")
        self.minsize(1200, 650)

        self.db = DatabaseManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_widgets()
        self.load_majors()
        self.load_from_db()

    def create_widgets(self):
       
        self.form = ctk.CTkFrame(self, corner_radius=12)
        self.form.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        self.form.grid_columnconfigure(tuple(range(12)), weight=1)

        fields = ["Matricule", "Nom", "Prenom", "Adresse", "Tel", "Date naissance"]
        self.entries = {}
        for i, f in enumerate(fields):
            ctk.CTkLabel(self.form, text=f, anchor="w").grid(row=0, column=i, sticky="w", padx=5, pady=(0,5))
            e = ctk.CTkEntry(self.form, placeholder_text=f"Enter {f}")
            e.grid(row=1, column=i, padx=5, sticky="ew")
            self.entries[f] = e

        ctk.CTkLabel(self.form, text="Major", anchor="w").grid(row=0, column=6, sticky="w", padx=5)
        self.major_cb = ctk.CTkComboBox(self.form, values=[])
        self.major_cb.grid(row=1, column=6, padx=5, sticky="ew")
        self.major_cb.configure(command=self.load_classes)

        ctk.CTkLabel(self.form, text="Class", anchor="w").grid(row=0, column=7, sticky="w", padx=5)
        self.class_cb = ctk.CTkComboBox(self.form, values=[])
        self.class_cb.grid(row=1, column=7, padx=5, sticky="ew")

        btn_specs = [
            ("Ajouter", "#6082B6", self.ajouter),
            ("Modifier", "#6082B6", self.modifier),
            ("Rechercher", "#6082B6", self.rechercher)
        ]
        for i, (text, color, cmd) in enumerate(btn_specs):
            ctk.CTkButton(self.form, text=text, fg_color=color, hover_color="#555555", command=cmd)\
                .grid(row=1, column=8+i, padx=5, sticky="ew")

        self.table_frame = ctk.CTkFrame(self, corner_radius=12)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2C2F33",
                        foreground="white",
                        fieldbackground="#2C2F33",
                        rowheight=28,
                        font=("Helvetica", 11))
        style.map("Treeview", background=[("selected", "#1E90FF")])
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground="#05236E")

        self.tree = ttk.Treeview(self.table_frame,
                                 columns=("mat","nom","prenom","adresse","tel","date","class","major"),
                                 show="headings",
                                 selectmode="extended")
        for i, c in enumerate(self.tree["columns"]):
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=150, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.remplir_formulaire)

        bottom = ctk.CTkFrame(self, corner_radius=12)
        bottom.grid(row=2, column=0, sticky="ew", padx=20, pady=15)

        btn_specs_bottom = [
            ("Supprimer", "#6082B6", self.supprimer),
            ("Trier par nom", "#6082B6", self.trier),
            ("Filtrer par classe", "#6082B6", self.filtrer_par_classe),
            ("Changer classe", "#6082B6", self.changer_classe),
            ("Exporter CSV", "#6082B6", self.export_csv),
            ("Afficher tout", "#6082B6", self.load_from_db)
        ]
        for text, color, cmd in btn_specs_bottom:
            ctk.CTkButton(bottom, text=text, fg_color=color, hover_color="#555555", command=cmd)\
                .pack(side="left", padx=8, pady=5)

    def load_majors(self):
        self.majors = self.db.fetch_majors()
        self.major_cb.configure(values=[m[1] for m in self.majors])

    def load_classes(self, _=None):
        major = self.major_cb.get()
        if not major:
            return
        major_id = next(m[0] for m in self.majors if m[1] == major)
        self.classes = self.db.fetch_classes_by_major(major_id)
        self.class_cb.configure(values=[c[1] for c in self.classes])

    def get_class_id(self):
        return next(c[0] for c in self.classes if c[1] == self.class_cb.get())

    def load_from_db(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.db.fetch_all():
            self.tree.insert("", "end", values=row)

    def get_form_data(self):
        return {
            "matricule": int(self.entries["Matricule"].get()),
            "nom": self.entries["Nom"].get(),
            "prenom": self.entries["Prenom"].get(),
            "adresse": self.entries["Adresse"].get(),
            "tel": self.entries["Tel"].get(),
            "datenaissance": self.entries["Date naissance"].get(),
            "class_id": self.get_class_id()
        }

    def ajouter(self):
        if not self.entries["Matricule"].get().isdigit():
            messagebox.showerror("Erreur", "Matricule invalide")
            return
        s = self.get_form_data()
        self.db.insert(s)
        self.load_from_db()

    def modifier(self):
        s = self.get_form_data()
        self.db.update(s)
        self.load_from_db()

    def supprimer(self):
        sel = self.tree.selection()
        if not sel:
            return
        mats = [self.tree.item(i)["values"][0] for i in sel]
        self.db.delete_many(mats)
        self.load_from_db()

    def rechercher(self):
        try:
            mat = int(self.entries["Matricule"].get())
        except:
            return
        self.tree.delete(*self.tree.get_children())
        s = self.db.search_by_matricule(mat)
        if s:
            self.tree.insert("", "end", values=s)

    def trier(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.db.sort_by_name():
            self.tree.insert("", "end", values=row)

    def filtrer_par_classe(self):
        class_id = self.get_class_id()
        self.tree.delete(*self.tree.get_children())
        for row in self.db.fetch_by_class(class_id):
            self.tree.insert("", "end", values=row)

    def changer_classe(self):
        sel = self.tree.selection()
        if not sel:
            return
        class_id = self.get_class_id()
        mats = [self.tree.item(i)["values"][0] for i in sel]
        self.db.update_class_for_many(mats, class_id)
        self.load_from_db()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            export_csv(self.tree, path)
            messagebox.showinfo("Export", f"Data exported to {path} successfully!")

    def remplir_formulaire(self, _):
        sel = self.tree.selection()
        if not sel:
            return  
        vals = self.tree.item(sel[0])["values"]
        keys = list(self.entries.keys())
        for i in range(len(keys)):
            self.entries[keys[i]].delete(0, ctk.END)
            self.entries[keys[i]].insert(0, vals[i])
        self.major_cb.set(vals[7])
        self.load_classes()
        self.class_cb.set(vals[6])

if __name__ == "__main__":
    App().mainloop()
