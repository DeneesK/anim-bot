import threading
import time

import gradio as gr
from PIL import Image

from src.settings.logger import logger

close_js = """
       function closeL() {
        console.log("Close");
        let tg = window.Telegram.WebApp;
        tg.close();
        }
"""

close_after = """
       function closeAfter(image, path) {
        console.log("Close");
        let tg = window.Telegram.WebApp;
        tg.close();
        return [image, path];
        }
"""

reload_js = """
       function reloadPage() {
           location.reload();
        }
"""

onStart = """
async () => {
    // set testFn() function on globalThis, so you html onlclick can access it
    // const d3 = await import("https://cdn.jsdelivr.net/npm/d3@7/+esm");
    // globalThis.d3 = d3;
    // or
    const script = document.createElement("script");
    script.onload = () =>  console.log("script loaded") ;
    script.src = "https://telegram.org/js/telegram-web-app.js";
    document.head.appendChild(script)

    let tg = window.Telegram.WebApp;
    tg.expand();
}
"""


def read_content(file_path: str) -> str:
    """read the content of target file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def save_content(file_path: str, image: Image.Image):
    image.save(file_path)


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
    with image_blocks as demo:
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
                                 scale=1)
        with gr.Row(elem_id='run_b'):
            btn = gr.Button("Раздеть!", elem_id="run_button")
        with gr.Row():
            btn2 = gr.Button("Очистить", elem_id="but_2")
            btn3 = gr.Button("Загрузить другое фото!", elem_id="but_3")
        path = gr.Text(value=path, visible=False)
        btn.click(fn=create_mask, inputs=[image, path], api_name='run')
        btn2.click(None, None, None, _js=reload_js)  # noqa
        btn3.click(None, None, None, _js=close_js)  # noqa

        gr.HTML(
            """
                <div class="footer" style="margin-bottom: 40px,
                margin-top: 30px">
                    <p></p>
                </div>
            """
        )
        demo.load(None, None, None, _js=onStart)

    return image_blocks


def close_server(server: gr.Blocks):
    time.sleep(300)
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
