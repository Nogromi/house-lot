import jinja2
import pdfkit
from datetime import datetime
import pydf

wkhtmltopdf_path = "third_side_soft/wkhtmltopdf/bin/wkhtmltopdf.exe"


def generate_image_blocks(links):
    columns = ""
    for link in links:
        columns += f"""<div class="column"><img src={link} alt="Snow" style="width:100%"></div>"""
    return columns


def generate_li(elements):
    """
    generate list for tags
    :param elements:
    :return:
    """
    li = "<ul>"
    for s in elements:
        ul = "<li>" + "<p>" + str(s) + "</p>" + "</li>"
        li += ul + ''
    li += "</ul>"
    return li


def sort_images_by_size(image_links):
    img_links_with_sizes = []
    for i in image_links:
        _, sizes = i.split('s=')
        width, height = sizes.split("x")
        img_links_with_sizes.append((i, width, height))
    sorted_links = [i[0] for i in sorted(img_links_with_sizes, key=lambda x: x[1], reverse=True)]
    return sorted_links


class Generator:
    """
    combine text  and images into pdf
    """

    def __init__(self,
                 content: dict):
        self.content = content.copy()
        self.content['properties'] = generate_li(self.content['properties'])
        sorted_links = sort_images_by_size(self.content['img_links'])
        self.content.pop('img_links', None)
        self.content['images_block'] = generate_image_blocks(sorted_links)
        print("init", self.content)

    def create_html(self):
        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template('template/basic-template.html')
        output_text = template.render(self.content)
        return output_text

    def html_to_pdf(self):
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        options = {
            # "enable-local-file-access": "",
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"}
        pdf_result = pdfkit.from_string(self.create_html(),
                                        # 'pdf_generated2.pdf',
                                        configuration=config,
                                        css='style.css',
                                        options=options)
        # pdf_result = pydf.generate_pdf(self.create_html(), **options)
        return pdf_result
