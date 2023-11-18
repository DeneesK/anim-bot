import gradio as gr
from PIL import Image


def read_content(file_path: str) -> str:
    """read the content of target file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def save_content(file_path: str, image: Image.Image):
    image.save(file_path)


def create_mask(dict):
    mask: Image.Image = dict["mask"].convert("RGB")
    save_content('result.png', mask)
    return mask


image_blocks = gr.Blocks(css=read_content('style.css'),
                         title='Naked Bytes',
                         elem_id="total-container",
                         analytics_enabled=True)
with image_blocks as demo:
    gr.HTML(read_content("header.html"))
    with gr.Row(elem_id="main-container",
                equal_height=False):
        with gr.Row(elem_id="image_upload"):
            image = gr.Image(tool='sketch',
                             source='upload',
                             type="pil",
                             interactive=True,
                             elem_id="image_up",
                             container=True)
    with gr.Row():
        btn = gr.Button("Раздеть!", elem_id="run_button")
    with gr.Row():
        btn_2 = gr.Button("Удалить выбранные элементы!", elem_id="but_2")
        btn_3 = gr.Button("Загрузить другое фото!", elem_id="but_3")

    btn.click(fn=create_mask, inputs=[image], api_name='run')

image_blocks.queue(max_size=50, concurrency_count=64).launch(share=True)
