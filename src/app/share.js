async () => {
	async function uploadFile(file){
		const UPLOAD_URL = 'https://huggingface.co/uploads';
		const response = await fetch(UPLOAD_URL, {
			method: 'POST',
			headers: {
				'Content-Type': file.type,
				'X-Requested-With': 'XMLHttpRequest',
			},
			body: file, /// <- File inherits from Blob
		});
		const url = await response.text();
		return url;
	}
	async function getInputImgFile(imgCanvas){
        const blob = await new Promise(resolve => imgCanvas.toBlob(resolve));
        const imgId = Date.now() % 200;
        const fileName = `sd-inpainting-${{imgId}}.png`;
        return new File([blob], fileName, { type: 'image/png' });
	}
    async function getOutoutImgFile(imgEl){
        const res = await fetch(imgEl.src);
        const blob = await res.blob();
        const imgId = Date.now() % 200;
        const fileName = `sd-inpainting-${{imgId}}.png`;
        return new File([blob], fileName, { type: 'image/png' });
    }
    const gradioEl = document.querySelector('body > gradio-app');
    // const gradioEl = document.querySelector("gradio-app").shadowRoot;
    const inputImgCanvas = gradioEl.querySelector('canvas[key="drawing"]');
    const outputImgEl = gradioEl.querySelector('#output-img img');
    const promptTxt = gradioEl.querySelector('#prompt textarea').value;
    let titleTxt = promptTxt;
    if(titleTxt.length > 100){
        titleTxt = titleTxt.slice(0, 100) + ' ...';
    }
    const shareBtnEl = gradioEl.querySelector('#share-btn');
    const shareIconEl = gradioEl.querySelector('#share-btn-share-icon');
    const loadingIconEl = gradioEl.querySelector('#share-btn-loading-icon');
    if(!outputImgEl){
        return;
    };
    shareBtnEl.style.pointerEvents = 'none';
    shareIconEl.style.display = 'none';
    loadingIconEl.style.removeProperty('display');
    const inputImgFile = await getInputImgFile(inputImgCanvas);
    const outputImgFile = await getOutoutImgFile(outputImgEl);
    const files = [inputImgFile, outputImgFile];
    const urls = await Promise.all(files.map((f) => uploadFile(f)));
	const htmlImgs = urls.map(url => `<img src='${url}' style='max-width: 450px;'>`);
    const [inputImgUrl, outputImgUrl] = htmlImgs;
	const descriptionMd = `<div style='display: flex; flex-wrap: wrap; column-gap: 0.75rem;'>
<div>
${inputImgUrl}
${promptTxt}
</div>
<div>
${outputImgUrl}
</div>
</div>`;
    const params = new URLSearchParams({
        title: titleTxt,
        description: descriptionMd,
    });
	const paramsStr = params.toString();
 
	window.open(`https://huggingface.co/spaces/diffusers/stable-diffusion-xl-inpainting/discussions/new?${paramsStr}&preview=true`, '_blank');
    shareBtnEl.style.removeProperty('pointer-events');
    shareIconEl.style.removeProperty('display');
    loadingIconEl.style.display = 'none';
}