import threading
import time

import gradio as gr
from PIL import Image

from src.settings.logger import logger

js = """
       function Previous(value1, value2) {
            alert("Вернись обратно в телеграм и отправьте новое фото");
            return value1, value2
        }
"""


def read_content(file_path: str) -> str:
    """read the content of target file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def save_content(file_path: str, image: Image.Image):
    image.save(file_path)


def create_mask_del(dict, path):
    path, _ = path.split('.')
    _, path = path.split('/')
    mask: Image.Image = dict["mask"].convert("RGB")
    save_content(f'img/del-{path}-mask.png', mask)
    return mask


def create_mask(dict, path):
    path, _ = path.split('.')
    _, path = path.split('/')
    mask: Image.Image = dict["mask"].convert("RGB")
    save_content(f'img/{path}-mask.png', mask)
    return mask


def create_blocks(path: str):
    image_blocks = gr.Blocks(css=read_content('src/app/style.css'),
                             title='Naked Bytes',
                             elem_id="total-container",
                             analytics_enabled=True)
    with image_blocks as _:
        gr.HTML(read_content("src/app/header.html"))
        with gr.Row(elem_id="image_upload"):
            with gr.Row(elem_id="image_up"):
                image = gr.Image(value=path,
                                 tool='sketch',
                                 source='upload',
                                 type="pil",
                                 interactive=True,
                                 elem_id="image_up",
                                 container=False,
                                 height=400)
        with gr.Row(elem_id='run_b'):
            btn = gr.Button("Раздеть!", elem_id="run_button")
        with gr.Row():
            btn2 = gr.Button("Удалить выбранные элементы!", elem_id="but_2")
            btn3 = gr.Button("Загрузить другое фото!", elem_id="but_3")
        path = gr.Text(value=path, visible=False)
        btn.click(fn=create_mask, inputs=[image, path], api_name='run')
        btn2.click(fn=create_mask_del, inputs=[image, path], api_name='run2')
        btn3.click(inputs=[image, path], api_name='run3', _js=js)
    return image_blocks


def close_server(server: gr.Blocks):
    time.sleep(600)
    server.close()


def start(path: str) -> str:
    server = create_blocks(path)
    data = server.launch(share=True,
                         server_name='0.0.0.0',
                         prevent_thread_lock=True)
    try:
        threading.Thread(target=close_server, args=(server,)).start()
    except Exception as ex:
        logger.error(ex)
    return data[2]
