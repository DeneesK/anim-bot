css = '''
.gradio-container{max-width: 1100px !important}
#image_upload{min-height:400px}
#image_upload [data-testid="image"], #image_upload [data-testid="image"] > div{min-height: 400px}
#mask_radio .gr-form{background:transparent; border: none}
#word_mask{margin-top: .75em !important}
#word_mask textarea:disabled{opacity: 0.3}
.footer {margin-bottom: 45px;margin-top: 35px;text-align: center;border-bottom: 1px solid #e5e5e5}
.footer>p {font-size: .8rem; display: inline-block; padding: 0 10px;transform: translateY(10px);background: white}
.dark .footer {border-color: #303030}
.dark .footer>p {background: #0b0f19}
.acknowledgments h4{margin: 1.25em 0 .25em 0;font-weight: bold;font-size: 115%}
#image_upload .touch-none{display: flex}
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
#share-btn-container {padding-left: 0.5rem !important; padding-right: 0.5rem !important; background-color: #000000; justify-content: center; align-items: center; border-radius: 9999px !important; max-width: 13rem; margin-left: auto;}
div#share-btn-container > div {flex-direction: row;background: black;align-items: center}
#share-btn-container:hover {background-color: #060606}
#share-btn {all: initial; color: #ffffff;font-weight: 600; cursor:pointer; font-family: 'IBM Plex Sans', sans-serif; margin-left: 0.5rem !important; padding-top: 0.5rem !important; padding-bottom: 0.5rem !important;right:0;}
#share-btn * {all: unset}
#share-btn-container div:nth-child(-n+2){width: auto !important;min-height: 0px !important;}
#share-btn-container .wrap {display: none !important}
#share-btn-container.hidden {display: none!important}
#prompt input{width: calc(100% - 160px);border-top-right-radius: 0px;border-bottom-right-radius: 0px;}
#run_button{position:absolute;margin-top: 11px;right: 0;margin-right: 0.8em;border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;}
#prompt-container{margin-top:-18px;}
#prompt-container .form{border-top-left-radius: 0;border-top-right-radius: 0}
#image_upload{border-bottom-left-radius: 0px;border-bottom-right-radius: 0px}
'''

btn = '''<div style="text-align: center; max-width: 650px; margin: 0 auto;">
    <div style="
          display: inline-flex;
          gap: 0.8rem;
          font-size: 1.75rem;
          justify-content: center;
          margin-bottom: 10px;
        ">
      <h1 style="font-weight: 900; align-items: center; margin-bottom: 7px; margin-top: 20px;">
        Inpainting 🎨
      </h1>
    </div>
    <div>
      <p style="align-items: center; margin-bottom: 7px;">
        Inpainting <a href="https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1" target="_blank">Naked Bytes</a>, add a mask and text prompt for what you want to replace
    </div>
  </div>'''
