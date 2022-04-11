import { useState } from "react"

function MainPage() {

	const [images,setImages]=useState([]);

	return <>

		
		{images.length>0&&<DisplayImages images={images}/>}
		<GenImageForm setImages={setImages}/>
	</>;
}


function GenImageForm({setImages}){
	const [prompt,setPrompt]=useState('somePrompt');
	const [height,setHeight]=useState(256);
	const [width,setWidth]=useState(256);
	const [scale,setScale]=useState(5.0);
	const [numSamples,setNumSamples]=useState(4);
	let fetchImages=async ()=>{
		let resp=await fetch('http://localhost:5000/genimage',{
			body:JSON.stringify({
				prompt:prompt,
				height:height,
				width:width,
				scale:scale,
				numSamples:numSamples
			}),
			method:'POST',
			headers:{
				'Content-Type':'application/json'
			}
		});
		let dataobj=await resp.json();
		setImages(dataobj.files)
	}


	return <>
		<textarea onChange={(ev)=>{ setPrompt(ev.target.value) }} value={prompt}/>
		Width:<input value={width} onChange={(ev)=>{ setWidth(ev.target.value)}}/>
		Height:<input value={height} onChange={(ev)=>{ setHeight(ev.target.value)}}/>
		scale:<input value={scale} onChange={(ev)=>{ setScale(ev.target.value)}}/>
		numSamples:<input value={numSamples} onChange={(ev)=>{ setNumSamples(ev.target.value)}}/>
		<button onClick={fetchImages}>Click to make image</button>
	</>;

}



function DisplayImages({images}){
	console.log(images);
	
	let genImages=images.map((img)=>{
		let imgUrlBase=new URL('http://localhost:5000/');
		imgUrlBase.pathname=img;
		return (<li key={img}> <img src={ imgUrlBase.href} /> </li>);
	})
	return <>Images:<ol >{genImages}</ol></>;

}

export default MainPage