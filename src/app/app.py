import asyncio
import threading
import time
import random

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
    function closeAfter(image, key) {
        alert("Теперь можете закрыть приложение и вернуться в телеграм");
        return [image, key];
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
    function(url_params, key) {
        const params = new URLSearchParams(window.location.search);
        url_params = Object.fromEntries(params);
        return [url_params, key];
        }
    """


def read_content(file_path: str) -> str:
    """read the content of target file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def prep(path: str, key: str):
    key = str(random.randint(0, 1000_000))
    path = eval(path)['url']
    v, _ = path.split('.')
    _, v = v.split('/')
    try:
        redis = get_redis()
        asyncio.run(redis.set(v, key))
    except Exception:
        pass
    image = Image.open(path)
    return image, key


def save_content(file_path: str, image: Image.Image):
    image.save(file_path)
    logger.info(f'saving----->{file_path}')


def create_mask(dict_, key: str):
    mask: Image.Image = dict_["mask"].convert("RGB")
    save_content(f'img/{key}-mask.png', mask)
    gr.Info("Теперь можете закрыть приложение, результат мы отправим тебе в телеграм!")  # noqa
    return mask


def create_blocks():
    image_blocks = gr.Blocks(css=read_content('src/app/style.css'),
                             title='Naked Bytes',
                             elem_id="total-container",
                             analytics_enabled=True)
    with image_blocks as demo:
        gr.HTML(read_content("src/app/header.html"))
        key = gr.Text(value='', visible=False)
        with gr.Row(elem_id="image_upload"):
            with gr.Row(elem_id="image_up"):
                image = gr.Image(tool='sketch',
                                 source='upload',
                                 type="pil",
                                 interactive=True,
                                 elem_id="image_up",
                                 container=False,
                                 scale=1,
                                 brush_radius=80)
                path_ = gr.Text(value='', visible=False)

                demo.load(fn=prep,
                          inputs=[path_, key],
                          outputs=[image, key],
                          _js=get_window_url_params)

        with gr.Row(elem_id='run_b'):
            btn = gr.Button("Раздеть!", elem_id="run_button")
        with gr.Row():
            btn2 = gr.Button("Очистить", elem_id="but_2")
            btn3 = gr.Button("Загрузить другое фото!", elem_id="but_3")

        btn.click(fn=create_mask, inputs=[image, key])  # noqa
        btn2.click(None, None, None, _js=reload_js)  # noqa
        btn3.click(None, None, None, _js=close_js)  # noqa

        demo.load(lambda: gr.Warning("После нажатия на кнопку 'Раздеть, дождись сообщения о том что приложение можно закрыть'"))
        demo.load(None, None, None, _js=onStart)
        demo.load(None, None, None, _js=onLoad)
    return image_blocks


async def start() -> None:
    cache_redis.cache = await cache_redis.setup()
    server = create_blocks()
    logger.info("APP STARTING...")
    data = server.queue(concurrency_count=3, max_size=3).launch(share=True,
                                                                server_name='0.0.0.0',  # noqa
                                                                prevent_thread_lock=True)  # noqa
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
