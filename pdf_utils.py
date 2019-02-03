import pdfrw
from reportlab.pdfgen import canvas
import io


TEMPLATES_DIR_NAME = 'templates'
TEMPLATE_FILE_FORMAT = TEMPLATES_DIR_NAME + '/%s.pdf'


def fill_pdf(form_name, pointer_values):
    template_path = TEMPLATE_FILE_FORMAT % form_name
    canvas_data = get_overlay_canvas(template_path, pointer_values)
    form = merge(canvas_data, template_path=template_path)
    return form


def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())


def get_overlay_canvas(template_path, pointer_values) -> io.BytesIO:
    template = pdfrw.PdfReader(template_path)
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    for page in template.Root.Pages.Kids:
        if page.Annots:
            for pointer in page.Annots:
                label = pointer.T.replace('(', '').replace(')', '')
                if label in pointer_values:
                    value = pointer_values[label]
                    print('Filling pointer \'%s\' with vaue \'%s\'...' %
                          (label, value))
                    sides_positions = pointer.Rect
                    left = min(float(sides_positions[0]), float(
                        sides_positions[2]))
                    bottom = min(float(sides_positions[1]), float(
                        sides_positions[3]))
                    pdf.drawString(x=left, y=bottom, text=value)
            pdf.showPage()
    pdf.save()
    data.seek(0)
    return data
