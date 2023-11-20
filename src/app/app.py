import asyncio
import threading
import time

import gradio as gr
from PIL import Image

from src.settings.logger import logger
from src.database import cache as cache_redis
from src.database.cache import get_redis


close_js = """
    function closeL() {
    console.log("Close");
    let tg = window.Telegram.WebApp;
    tg.close();
    }
"""

close_after = """
       function closeAfter(image) {
            alert("Теперь можете закрыть приложение и вернуться в телеграм");
            return image;
        }
"""

reload_js = """
       function reloadPage() {
           location.reload();
        }
"""

onStart = """
async () => {
    const script = document.createElement("script");
    script.onload = () =>  console.log("script loaded") ;
    script.src = "https://telegram.org/js/telegram-web-app.js";
    document.head.appendChild(script)
}
"""

onLoad = """
async () => {
    const scr = document.createElement("script");
    scr.onload = () =>  console.log("script2 loaded") ;
    scr.innerHTML = "window.Telegram.WebApp.expand();";
    document.body.appendChild(scr)
}
"""

get_window_url_params = """
    function(url_params) {
        const params = new URLSearchParams(window.location.search);
        url_params = Object.fromEntries(params);
        return url_params;
        }
    """


def read_content(file_path: str) -> str:
    """read the content of target file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def save_content(file_path: str, image: Image.Image):
    image.save(file_path)


def create_mask(dict_):
    print(dict_)
    # mask: Image.Image = dict_["mask"].convert("RGB")
    # save_content(f'img/{path}-mask.png', mask)

    # return mask


def create_blocks():
    image_blocks = gr.Blocks(css=read_content('src/app/style.css'),
                             title='Naked Bytes',
                             elem_id="total-container",
                             analytics_enabled=True)
    with image_blocks as demo:
        gr.HTML(read_content("src/app/header.html"))
        with gr.Row(elem_id="image_upload"):
            with gr.Row(elem_id="image_up"):
                image = gr.Image(tool='sketch',
                                 source='upload',
                                 type="filepath",
                                 interactive=True,
                                 elem_id="image_up",
                                 container=False,
                                 scale=1,
                                 brush_radius=80)
                path_ = gr.Text(value='', visible=False)

                demo.load(fn=lambda path_: eval(path_)['url'],
                          inputs=[path_],
                          outputs=[image],
                          _js=get_window_url_params)

        with gr.Row(elem_id='run_b'):
            btn = gr.Button("Раздеть!", elem_id="run_button")
        with gr.Row():
            btn2 = gr.Button("Очистить", elem_id="but_2")
            btn3 = gr.Button("Загрузить другое фото!", elem_id="but_3")
        btn.click(fn=create_mask, inputs=[image], api_name='run', _js=close_after)  # noqa
        btn2.click(None, None, None, _js=reload_js)  # noqa
        btn3.click(None, None, None, _js=close_js)  # noqa

        demo.load(None, None, None, _js=onStart)
        demo.load(None, None, None, _js=onLoad)
    return image_blocks


async def start() -> None:
    cache_redis.cache = await cache_redis.setup()
    server = create_blocks()
    data = server.queue(concurrency_count=64).launch(share=True,
                                                     server_name='0.0.0.0',
                                                     prevent_thread_lock=True)
    try:
        t1 = threading.Thread(target=time.sleep, args=(1000_000, ))  # noqa
    except Exception as ex:
        logger.error(ex)
    redis = get_redis()
    url = data[2]
    await redis.set('app', url)
    t1.start()
    t1.join()
    logger.info('APP SHUTDOWN...')

if __name__ == '__main__':
    asyncio.run(start())
