# import tkinter as tk
# from tkinter import ttk, filedialog


# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self._configure_window()
#         self._configure_styles()
#         self._build_ui()

#     # ─────────────────────────────────────────
#     # SETUP
#     # ─────────────────────────────────────────
#     def _configure_window(self):
#         self.title("App")
#         self.geometry("600x400")
#         self.resizable(True, True)
#         self.configure(bg="#f5f5f5")

#     def _configure_styles(self):
#         style = ttk.Style(self)
#         style.theme_use("clam")

#         style.configure("TFrame",        background="#f5f5f5")
#         style.configure("TLabel",        background="#f5f5f5", font=("Segoe UI", 10))
#         style.configure("TButton",       font=("Segoe UI", 10), padding=6)
#         style.configure("TCombobox",     font=("Segoe UI", 10))
#         style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f5f5f5")
#         style.configure("Sub.TLabel",    font=("Segoe UI", 9),           background="#f5f5f5", foreground="#888")

#     # ─────────────────────────────────────────
#     # LAYOUT
#     # ─────────────────────────────────────────
#     def _build_ui(self):
#         header = ttk.Frame(self, padding=(16, 12))
#         header.pack(fill="x")
#         ttk.Label(header, text="Task Map Builder", style="Header.TLabel").pack(side="left")

#         ttk.Separator(self, orient="horizontal").pack(fill="x", padx=16)

#         content = ttk.Frame(self, padding=16)
#         content.pack(fill="both", expand=True)
#         self._build_content(content)

#         ttk.Separator(self, orient="horizontal").pack(fill="x", padx=16)
#         footer = ttk.Frame(self, padding=(16, 8))
#         footer.pack(fill="x")
#         self.status_var = tk.StringVar(value="Ready")
#         ttk.Label(footer, textvariable=self.status_var).pack(side="left")

#     def _build_content(self, parent):
#         parent.columnconfigure(1, weight=1)

#         # ── Data file ──────────────────────────────
#         ttk.Label(parent, text="Data shapefile").grid(row=0, column=0, sticky="w", pady=(0, 2))
#         ttk.Label(parent, text="Point data with values to interpolate", style="Sub.TLabel").grid(
#             row=1, column=0, columnspan=3, sticky="w", pady=(0, 8))

#         self.data_path_var = tk.StringVar()
#         ttk.Entry(parent, textvariable=self.data_path_var, state="readonly").grid(
#             row=0, column=1, sticky="ew", padx=(8, 4))
#         ttk.Button(parent, text="Browse", command=self._browse_data).grid(
#             row=0, column=2, sticky="w")

#         # ── Boundary file ──────────────────────────
#         ttk.Label(parent, text="Boundary shapefile").grid(row=2, column=0, sticky="w", pady=(0, 2))
#         ttk.Label(parent, text="Polygon defining the interpolation extent", style="Sub.TLabel").grid(
#             row=3, column=0, columnspan=3, sticky="w", pady=(0, 8))

#         self.boundary_path_var = tk.StringVar()
#         ttk.Entry(parent, textvariable=self.boundary_path_var, state="readonly").grid(
#             row=2, column=1, sticky="ew", padx=(8, 4))
#         ttk.Button(parent, text="Browse", command=self._browse_boundary).grid(
#             row=2, column=2, sticky="w")

#         # ── Column selector ────────────────────────
#         ttk.Label(parent, text="Value column").grid(row=4, column=0, sticky="w", pady=(0, 2))
#         ttk.Label(parent, text="Column to interpolate — load data file first", style="Sub.TLabel").grid(
#             row=5, column=0, columnspan=3, sticky="w", pady=(0, 16))

#         self.column_var = tk.StringVar()
#         self.column_dropdown = ttk.Combobox(
#             parent, textvariable=self.column_var, state="disabled", width=30)
#         self.column_dropdown.grid(row=4, column=1, sticky="ew", padx=(8, 4))

#         # ── Run ────────────────────────────────────
#         ttk.Button(parent, text="Run", command=self._on_run).grid(
#             row=6, column=1, sticky="e", padx=(8, 4))

#     # ─────────────────────────────────────────
#     # FILE BROWSING
#     # ─────────────────────────────────────────
#     def _browse_data(self):
#         path = filedialog.askopenfilename(
#             title="Select data shapefile",
#             filetypes=[("Shapefiles", "*.shp"), ("All files", "*.*")]
#         )
#         if not path:
#             return

#         self.data_path_var.set(path)
#         self._load_columns(path)

#     def _browse_boundary(self):
#         path = filedialog.askopenfilename(
#             title="Select boundary shapefile",
#             filetypes=[("Shapefiles", "*.shp"), ("All files", "*.*")]
#         )
#         if path:
#             self.boundary_path_var.set(path)

#     # ─────────────────────────────────────────
#     # COLUMN LOADING
#     # ─────────────────────────────────────────
#     def _load_columns(self, path):
#         try:
#             import geopandas as gpd
#             gdf = gpd.read_file(path)

#             # Only show numeric columns — non-numeric can't be interpolated
#             numeric_cols = gdf.select_dtypes(include="number").columns.tolist()

#             if not numeric_cols:
#                 self.set_status("No numeric columns found in data file.")
#                 return

#             self.column_dropdown.configure(state="readonly")
#             self.column_dropdown["values"] = numeric_cols
#             self.column_var.set(numeric_cols[0])
#             self.set_status(f"Loaded {len(numeric_cols)} numeric column(s).")

#         except Exception as e:
#             self.set_status(f"Error reading file: {e}")

#     # ─────────────────────────────────────────
#     # ACTIONS
#     # ─────────────────────────────────────────
#     def _on_run(self):
#         data_path     = self.data_path_var.get()
#         boundary_path = self.boundary_path_var.get()
#         column        = self.column_var.get()

#         if not data_path:
#             self.set_status("Please select a data shapefile.")
#             return
#         if not boundary_path:
#             self.set_status("Please select a boundary shapefile.")
#             return
#         if not column:
#             self.set_status("Please select a value column.")
#             return

#         self.set_status(f"Running on '{column}'...")

#         # ── Wire up to Core here ───────────────────
#         from core import Core
#         core = Core(data_path, boundary_path)
#         core.create_taskmap()

#     def set_status(self, message: str):
#         self.status_var.set(message)


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()




import tkinter as tk
from tkinter import ttk, filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._configure_window()
        self._configure_styles()
        self._build_ui()

    # ─────────────────────────────────────────
    # SETUP
    # ─────────────────────────────────────────
    def _configure_window(self):
        self.title("Task Map Builder")
        self.geometry("600x520")
        self.resizable(True, True)
        self.configure(bg="#f5f5f5")

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame",        background="#f5f5f5")
        style.configure("TLabel",        background="#f5f5f5", font=("Segoe UI", 10))
        style.configure("TButton",       font=("Segoe UI", 10), padding=6)
        style.configure("TCombobox",     font=("Segoe UI", 10))
        style.configure("TEntry",        font=("Segoe UI", 10))
        style.configure("TSpinbox",      font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f5f5f5")
        style.configure("Sub.TLabel",    font=("Segoe UI", 9), background="#f5f5f5", foreground="#888")
        style.configure("Class.TLabel",  font=("Segoe UI", 9, "bold"), background="#f5f5f5")

    # ─────────────────────────────────────────
    # LAYOUT
    # ─────────────────────────────────────────
    def _build_ui(self):
        header = ttk.Frame(self, padding=(16, 12))
        header.pack(fill="x")
        ttk.Label(header, text="Task Map Builder", style="Header.TLabel").pack(side="left")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=16)

        self.content = ttk.Frame(self, padding=16)
        self.content.pack(fill="both", expand=True)
        self._build_content(self.content)

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=16)
        footer = ttk.Frame(self, padding=(16, 8))
        footer.pack(fill="x")
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(footer, textvariable=self.status_var).pack(side="left")

    def _build_content(self, parent):
        parent.columnconfigure(1, weight=1)

        # ── Data file ──────────────────────────────
        ttk.Label(parent, text="Data shapefile").grid(row=0, column=0, sticky="w", pady=(0, 2))
        ttk.Label(parent, text="Point data with values to interpolate", style="Sub.TLabel").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self.data_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.data_path_var, state="readonly").grid(
            row=0, column=1, sticky="ew", padx=(8, 4))
        ttk.Button(parent, text="Browse", command=self._browse_data).grid(
            row=0, column=2, sticky="w")

        # ── Boundary file ──────────────────────────
        ttk.Label(parent, text="Boundary shapefile").grid(row=2, column=0, sticky="w", pady=(0, 2))
        ttk.Label(parent, text="Polygon defining the interpolation extent", style="Sub.TLabel").grid(
            row=3, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self.boundary_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.boundary_path_var, state="readonly").grid(
            row=2, column=1, sticky="ew", padx=(8, 4))
        ttk.Button(parent, text="Browse", command=self._browse_boundary).grid(
            row=2, column=2, sticky="w")

        # ── Column selector ────────────────────────
        ttk.Label(parent, text="Value column").grid(row=4, column=0, sticky="w", pady=(0, 2))
        ttk.Label(parent, text="Column to interpolate — load data file first", style="Sub.TLabel").grid(
            row=5, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self.column_var = tk.StringVar()
        self.column_dropdown = ttk.Combobox(
            parent, textvariable=self.column_var, state="disabled", width=30)
        self.column_dropdown.grid(row=4, column=1, sticky="ew", padx=(8, 4))
        self.column_dropdown.bind("<<ComboboxSelected>>", self._on_column_selected)

        ttk.Separator(parent, orient="horizontal").grid(
            row=6, column=0, columnspan=3, sticky="ew", pady=12)

        # ── Class ranges (injected here after column is picked) ────
        self.classes_frame = ttk.Frame(parent)
        self.classes_frame.grid(row=7, column=0, columnspan=3, sticky="ew")
        self.classes_frame.columnconfigure(1, weight=1)
        self.classes_frame.columnconfigure(3, weight=1)

        # ── Run ────────────────────────────────────
        self.run_button = ttk.Button(parent, text="Run", command=self._on_run)
        self.run_button.grid(row=8, column=1, sticky="e", padx=(8, 4), pady=(12, 0))

    # ─────────────────────────────────────────
    # CLASS RANGE BUILDER
    # ─────────────────────────────────────────
    def _build_class_ranges(self, min_val, max_val, n_classes=5):
        """Draw editable from/to rows for each class, pre-filled with equal intervals."""
        for widget in self.classes_frame.winfo_children():
            widget.destroy()

        self.class_entries = []  # list of (from_var, to_var) per class

        bins = [round(min_val + i * (max_val - min_val) / n_classes, 4)
                for i in range(n_classes + 1)]

        # Header row
        ttk.Label(self.classes_frame, text="Classes", style="Class.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Label(self.classes_frame, text="From", style="Sub.TLabel").grid(
            row=0, column=1, padx=(8, 4))
        ttk.Label(self.classes_frame, text="To", style="Sub.TLabel").grid(
            row=0, column=3, padx=(4, 0))

        for i in range(n_classes):
            from_var = tk.StringVar(value=str(bins[i]))
            to_var   = tk.StringVar(value=str(bins[i + 1]))

            ttk.Label(self.classes_frame, text=f"Class {i + 1}").grid(
                row=i + 1, column=0, sticky="w", pady=2)
            ttk.Entry(self.classes_frame, textvariable=from_var, width=10).grid(
                row=i + 1, column=1, padx=(8, 2), sticky="ew")
            ttk.Label(self.classes_frame, text="–").grid(
                row=i + 1, column=2)
            ttk.Entry(self.classes_frame, textvariable=to_var, width=10).grid(
                row=i + 1, column=3, padx=(2, 0), sticky="ew")

            self.class_entries.append((from_var, to_var))

        # Expand the window to fit
        self.update_idletasks()
        self.geometry(f"600x{self.winfo_reqheight() + 20}")

    def _get_bins(self):
        """Read class entries and return a sorted list of bin edges."""
        try:
            bins = [float(self.class_entries[0][0].get())]
            for _, to_var in self.class_entries:
                bins.append(float(to_var.get()))
            return bins
        except ValueError:
            self.set_status("Invalid class range values — please enter numbers only.")
            return None

    # ─────────────────────────────────────────
    # FILE BROWSING
    # ─────────────────────────────────────────
    def _browse_data(self):
        path = filedialog.askopenfilename(
            title="Select data shapefile",
            filetypes=[("Shapefiles", "*.shp"), ("All files", "*.*")]
        )
        if not path:
            return
        self.data_path_var.set(path)
        self._load_columns(path)

    def _browse_boundary(self):
        path = filedialog.askopenfilename(
            title="Select boundary shapefile",
            filetypes=[("Shapefiles", "*.shp"), ("All files", "*.*")]
        )
        if path:
            self.boundary_path_var.set(path)

    # ─────────────────────────────────────────
    # COLUMN LOADING
    # ─────────────────────────────────────────
    def _load_columns(self, path):
        try:
            import geopandas as gpd
            self._gdf = gpd.read_file(path)

            numeric_cols = self._gdf.select_dtypes(include="number").columns.tolist()
            if not numeric_cols:
                self.set_status("No numeric columns found in data file.")
                return

            self.column_dropdown.configure(state="readonly")
            self.column_dropdown["values"] = numeric_cols
            self.column_var.set(numeric_cols[0])
            self.set_status(f"Loaded {len(numeric_cols)} numeric column(s).")

            # Auto-populate ranges for the first column
            self._populate_ranges(numeric_cols[0])

        except Exception as e:
            self.set_status(f"Error reading file: {e}")

    def _on_column_selected(self, event=None):
        col = self.column_var.get()
        if col and hasattr(self, "_gdf"):
            self._populate_ranges(col)

    def _populate_ranges(self, column):
        col_data = self._gdf[column].dropna()
        self._build_class_ranges(col_data.min(), col_data.max())
        self.set_status(f"Showing ranges for '{column}' — edit freely.")

    # ─────────────────────────────────────────
    # ACTIONS
    # ─────────────────────────────────────────
    def _on_run(self):
        data_path     = self.data_path_var.get()
        boundary_path = self.boundary_path_var.get()
        column        = self.column_var.get()

        if not data_path:
            self.set_status("Please select a data shapefile.")
            return
        if not boundary_path:
            self.set_status("Please select a boundary shapefile.")
            return
        if not column:
            self.set_status("Please select a value column.")
            return

        bins = self._get_bins()
        if bins is None:
            return

        self.set_status(f"Running on '{column}' with {len(bins) - 1} classes...")

        # ── Wire up to Core here ───────────────────
        from core import Core
        core = Core(data_path, boundary_path)
        core.target_column = column
        core.custom_bins = bins
        core.create_taskmap()

    def set_status(self, message: str):
        self.status_var.set(message)


if __name__ == "__main__":
    app = App()
    app.mainloop()