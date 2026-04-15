import fitz  # PyMuPDF
import os

def pdf_to_png_simples(pdf_path, output_folder="output_images"):
    """
    Converte um PDF em imagens PNG, uma por página, usando PyMuPDF.
    """
    # Criar pasta de saída se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Abrir o PDF
    doc = fitz.open(pdf_path)

    nome_base = os.path.splitext(os.path.basename(pdf_path))[0]
    caminhos_salvos = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        output_path = os.path.join(output_folder, f"{nome_base}_pagina_{i+1:03d}.png")
        pix.save(output_path)
        caminhos_salvos.append(output_path)

    return caminhos_salvos
