import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from typing import Literal
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


OrientationType = Literal["vertical", "horizontal", "automatica"]


class ImageToPDFApp:
    """Aplicación GUI para convertir imágenes a PDF."""

    def __init__(self, root: tk.Tk) -> None:
        """Inicializar la aplicación."""
        self.root = root
        self.root.title("IMG-TO-PDF Converter")
        self.root.geometry("600x450")

        self._setup_dark_theme()

        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.orientation = tk.StringVar(value="automatica")
        self.document_title = tk.StringVar()

        self._create_widgets()

    def _setup_dark_theme(self) -> None:
        """Configurar tema oscuro para la aplicación."""
        bg_color = "#1e1e1e"
        fg_color = "#ffffff"
        entry_bg = "#2d2d2d"
        button_bg = "#0e639c"
        button_hover = "#1177bb"

        # Configurar colores de la ventana principal
        self.root.configure(bg=bg_color)

        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use("clam")

        # Configurar Frame
        style.configure("TFrame", background=bg_color)

        # Configurar Label
        style.configure(
            "TLabel",
            background=bg_color,
            foreground=fg_color,
            font=("Segoe UI", 10),
        )

        # Configurar Entry
        style.configure(
            "TEntry",
            fieldbackground=entry_bg,
            background=entry_bg,
            foreground=fg_color,
            insertcolor=fg_color,
            bordercolor=entry_bg,
            lightcolor=entry_bg,
            darkcolor=entry_bg,
        )

        # Configurar Button
        style.configure(
            "TButton",
            background=button_bg,
            foreground=fg_color,
            bordercolor=button_bg,
            focuscolor="none",
            font=("Segoe UI", 9),
            padding=6,
        )
        style.map(
            "TButton",
            background=[("active", button_hover), ("pressed", button_hover)],
        )

        # Configurar botón de acento (Generar PDF)
        style.configure(
            "Accent.TButton",
            background="#0e7c3a",
            foreground=fg_color,
            font=("Segoe UI", 11, "bold"),
            padding=10,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#10954a"), ("pressed", "#10954a")],
        )

        # Configurar Radiobutton
        style.configure(
            "TRadiobutton",
            background=bg_color,
            foreground=fg_color,
            font=("Segoe UI", 9),
            focuscolor=bg_color,
        )
        style.map(
            "TRadiobutton",
            background=[("active", bg_color)],
            foreground=[("active", fg_color)],
        )

        # Configurar Progressbar
        style.configure(
            "TProgressbar",
            background=button_bg,
            troughcolor=entry_bg,
            bordercolor=entry_bg,
            lightcolor=button_bg,
            darkcolor=button_bg,
        )

    def _create_widgets(self) -> None:
        """Crear los widgets de la interfaz."""
        # Configurar padding
        padding = {"padx": 20, "pady": 10}

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Carpeta de origen
        ttk.Label(main_frame, text="Carpeta de origen:").grid(
            row=0, column=0, sticky=tk.W, **padding
        )
        ttk.Entry(main_frame, textvariable=self.source_folder, width=40).grid(
            row=0, column=1, **padding
        )
        ttk.Button(
            main_frame, text="Seleccionar", command=self._select_source
        ).grid(row=0, column=2, **padding)

        # Carpeta de destino
        ttk.Label(main_frame, text="Carpeta de destino:").grid(
            row=1, column=0, sticky=tk.W, **padding
        )
        ttk.Entry(main_frame, textvariable=self.dest_folder, width=40).grid(
            row=1, column=1, **padding
        )
        ttk.Button(
            main_frame, text="Seleccionar", command=self._select_dest
        ).grid(row=1, column=2, **padding)

        # Título del documento
        ttk.Label(main_frame, text="Título del documento:").grid(
            row=2, column=0, sticky=tk.W, **padding
        )
        ttk.Entry(main_frame, textvariable=self.document_title, width=40).grid(
            row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), **padding
        )

        # Orientación
        ttk.Label(main_frame, text="Orientación:").grid(
            row=3, column=0, sticky=tk.W, **padding
        )
        orientation_frame = ttk.Frame(main_frame)
        orientation_frame.grid(
            row=3, column=1, columnspan=2, sticky=tk.W, **padding
        )

        ttk.Radiobutton(
            orientation_frame,
            text="Vertical",
            variable=self.orientation,
            value="vertical",
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            orientation_frame,
            text="Horizontal",
            variable=self.orientation,
            value="horizontal",
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            orientation_frame,
            text="Automática",
            variable=self.orientation,
            value="automatica",
        ).pack(side=tk.LEFT, padx=5)

        # Botón de generar PDF
        ttk.Button(
            main_frame,
            text="Generar PDF",
            command=self._generate_pdf,
            style="Accent.TButton",
        ).grid(row=4, column=0, columnspan=3, pady=30)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), **padding
        )

        # Configurar peso de las columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def _select_source(self) -> None:
        """Seleccionar carpeta de origen."""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de origen")
        if folder:
            self.source_folder.set(folder)

    def _select_dest(self) -> None:
        """Seleccionar carpeta de destino."""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if folder:
            self.dest_folder.set(folder)

    def _get_image_files(self, folder: Path) -> list[Path]:
        """Obtener lista de archivos de imagen ordenados alfabéticamente."""
        # Extensiones de imagen soportadas
        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".tif",
            ".webp",
            ".ico",
            ".ppm",
            ".pgm",
            ".pbm",
            ".pnm",
        }

        images = [
            f
            for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]

        return sorted(images, key=lambda x: x.name.lower())

    def _determine_orientation(
        self, img: Image.Image, orientation_setting: OrientationType
    ) -> tuple[float, float]:
        """Determinar el tamaño de página basado en la orientación."""
        if orientation_setting == "vertical":
            return A4
        elif orientation_setting == "horizontal":
            return landscape(A4)
        else:  # automática
            width, height = img.size
            if width > height:
                return landscape(A4)
            else:
                return A4

    def _generate_pdf(self) -> None:
        """Generar el PDF con las imágenes."""
        # Validar inputs
        if not self.source_folder.get():
            messagebox.showerror(
                "Error", "Por favor seleccione una carpeta de origen"
            )
            return

        if not self.dest_folder.get():
            messagebox.showerror(
                "Error", "Por favor seleccione una carpeta de destino"
            )
            return

        if not self.document_title.get():
            messagebox.showerror(
                "Error", "Por favor ingrese un título para el documento"
            )
            return

        source = Path(self.source_folder.get())
        dest = Path(self.dest_folder.get())

        # Obtener imágenes
        image_files = self._get_image_files(source)

        if not image_files:
            messagebox.showerror(
                "Error", "No se encontraron imágenes en la carpeta de origen"
            )
            return

        # Iniciar barra de progreso
        self.progress.start()

        try:
            # Crear PDF
            pdf_path = dest / f"{self.document_title.get()}.pdf"
            pdf = canvas.Canvas(str(pdf_path))

            orientation_setting: OrientationType = self.orientation.get()  # type: ignore

            for idx, image_path in enumerate(image_files):
                try:
                    # Abrir imagen
                    img = Image.open(image_path)

                    # Convertir a RGB si es necesario
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")

                    # Determinar orientación
                    page_width, page_height = self._determine_orientation(
                        img, orientation_setting
                    )
                    pdf.setPageSize((page_width, page_height))

                    # Calcular dimensiones para la imagen
                    img_width, img_height = img.size
                    aspect = img_height / img_width

                    # Dejar espacio para el título (80 puntos desde arriba)
                    available_height = page_height - 120
                    available_width = page_width - 80

                    # Ajustar imagen manteniendo aspect ratio
                    if aspect > available_height / available_width:
                        # La imagen es más alta proporcionalmente
                        draw_height = available_height
                        draw_width = draw_height / aspect
                    else:
                        # La imagen es más ancha proporcionalmente
                        draw_width = available_width
                        draw_height = draw_width * aspect

                    # Centrar imagen
                    x = (page_width - draw_width) / 2
                    y = (page_height - draw_height) / 2 - 20

                    # Dibujar títulos
                    pdf.setFont("Helvetica-Bold", 16)

                    if idx == 0:
                        # Primera página: título del documento
                        pdf.drawCentredString(
                            page_width / 2,
                            page_height - 40,
                            self.document_title.get(),
                        )
                        pdf.setFont("Helvetica", 12)
                        pdf.drawCentredString(
                            page_width / 2, page_height - 60, image_path.stem
                        )
                    else:
                        # Resto de páginas: solo nombre de imagen
                        pdf.drawCentredString(
                            page_width / 2, page_height - 40, image_path.stem
                        )

                    # Dibujar imagen
                    pdf.drawImage(
                        ImageReader(img),
                        x,
                        y,
                        width=draw_width,
                        height=draw_height,
                        preserveAspectRatio=True,
                    )

                    # Nueva página si no es la última imagen
                    if idx < len(image_files) - 1:
                        pdf.showPage()

                except Exception as e:
                    messagebox.showwarning(
                        "Advertencia",
                        f"No se pudo procesar la imagen {image_path.name}: {str(e)}",
                    )
                    continue

            # Guardar PDF
            pdf.save()

            # Detener barra de progreso
            self.progress.stop()

            messagebox.showinfo(
                "Éxito", f"PDF generado exitosamente:\n{pdf_path}"
            )

        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"Error al generar el PDF: {str(e)}")


def main() -> None:
    """Función principal."""
    root = tk.Tk()
    ImageToPDFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
