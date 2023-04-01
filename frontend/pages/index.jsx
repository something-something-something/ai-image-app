import {
	useContext,
	useEffect,
	useReducer,
	createContext,
	useState,
} from 'react';

function MainPage() {
	return (
		<>
			<details>
				<summary>Stable Diffusion 2.1 768</summary>
				<ImageGenForm
					endpointForFetchingFormData="http://localhost:5000/stableDiffusion2-1-768/getFormFields"
					endpointForSubmittingForm="http://localhost:5000/stableDiffusion2-1-768/genimage"
				/>
			</details>
			<details>
				<summary>Stable Diffusion</summary>
				<ImageGenForm
					endpointForFetchingFormData="http://localhost:5000/stableDiffusion/getFormFields"
					endpointForSubmittingForm="http://localhost:5000/stableDiffusion/genimage"
				/>
			</details>
			<details>
				<summary>Image To Image Stable Diffusion</summary>
				<ImageGenForm
					endpointForFetchingFormData="http://localhost:5000/stableDiffusionImgToImg/getFormFields"
					endpointForSubmittingForm="http://localhost:5000/stableDiffusionImgToImg/genimage"
				/>
			</details>
			<details>
				<summary>Latent Diffusion</summary>
				<ImageGenForm
					endpointForFetchingFormData="http://localhost:5000/latentDiffusion/getFormFields"
					endpointForSubmittingForm="http://localhost:5000/latentDiffusion/genimage"
				/>
			</details>
		</>
	);
}

const ImageGenFormDispatch = createContext(null);

//TODO figure out Names
function ImageGenFormWithTextFields({
	formFieldsData,
	formFieldValues,
	submitAction,
}) {
	console.log(formFieldsData);
	return (
		<form
			onSubmit={async (ev) => {
				ev.preventDefault();
				submitAction();
			}}
		>
			{formFieldsData.map((fieldData) => {
				return (
					<ImageGenField
						key={fieldData.name}
						name={fieldData.name}
						displayName={fieldData.displayName}
						value={formFieldValues[fieldData.name]}
						type={fieldData.type}
						possibleValues={fieldData.possibleValues}
					/>
				);
			})}

			<input type="submit" value="Generate Image" />
		</form>
	);
}

function ImageGenField({ name, value, displayName, type, possibleValues }) {
	const dispatch = useContext(ImageGenFormDispatch);
	const updateFieldValue = (value) => {
		dispatch({
			type: 'formField',
			action: 'set',
			name: name,
			value: value,
		});
	};
	const changeFunc = (ev) => {
		updateFieldValue(ev.target.value);
	};

	let FieldToUse = TextFieldInput;
	if (type === 'textbox') {
		FieldToUse = TextBoxFieldInput;
	} else if (type === 'radio') {
		FieldToUse = RadioFieldInput;
	} else if (type === 'imagewidthheight') {
		FieldToUse = FileFieldInput;
	}

	return (
		<div style={{ padding: '0.5rem' }}>
			<label>
				{displayName}
				<br />

				<FieldToUse
					value={value}
					name={name}
					onChange={changeFunc}
					possibleValues={possibleValues}
					updateFieldValue={updateFieldValue}
				/>
			</label>
			<br />
			<button
				type="button"
				onClick={(ev) => {
					if (confirm('Reset ' + displayName)) {
						dispatch({
							type: 'formField',
							action: 'reset',
							name: name,
						});
					}
				}}
			>
				reset
			</button>
		</div>
	);
}

function RadioFieldInput({ value, name, onChange, possibleValues }) {
	return (
		<>
			{possibleValues.map((pv) => {
				return (
					<label key={pv.value} style={{ display: 'block' }}>
						<input
							value={pv.value}
							name={name}
							onChange={onChange}
							type="radio"
							checked={pv.value === value}
						/>
						{pv.displayName}
					</label>
				);
			})}
		</>
	);
}

function TextFieldInput({ value, name, onChange }) {
	return <input value={value} name={name} onChange={onChange} type="text" />;
}

function fileToDataURL(file) {
	return new Promise((resolve) => {
		const fr = new FileReader();
		fr.addEventListener('load', () => {
			resolve(fr.result);
		});
		fr.readAsDataURL(file);
	});
}

//rename
//clean up
function FileFieldInput({ value, name, onChange, updateFieldValue }) {
	const [imgOriginalHeight, setImgOriginalHeight] = useState(value.height);

	const [imgOriginalWidth, setImgOriginalWidth] = useState(value.height);

	const [scale, setScale] = useState(1);

	const calcScaledDimensions = ({ scale, height, width }) => {
		return {
			width: Math.round(scale * width),
			height: Math.round(scale * height),
		};
	};

	const fileSelected = async (ev) => {
		if (ev.target.files.length > 0) {
			let originalImage = await createImageBitmap(ev.target.files[0]);
			setImgOriginalHeight(originalImage.height);

			setImgOriginalWidth(originalImage.width);

			updateFieldValue({
				...calcScaledDimensions({
					height: originalImage.height,
					width: originalImage.width,
					scale: scale,
				}),
				imgUrl: await fileToDataURL(ev.target.files[0]),
			});
		}
	};

	const getScaleToTarget = (basedimm, targetdimm) => {
		return targetdimm / basedimm;
	};

	const updateDimmAndScaleBasedOnTarget = (basedimm, targetdimm) => {
		const scaleValue = getScaleToTarget(basedimm, targetdimm);
		updateFieldValue({
			...calcScaledDimensions({
				height: imgOriginalHeight,
				width: imgOriginalWidth,
				scale: scaleValue,
			}),
			imgUrl: value.imgUrl,
		});
		setScale(scaleValue);
	};

	return (
		<>
			render height:<b>{value.height}</b>
			<button
				onClick={(ev) => {
					updateDimmAndScaleBasedOnTarget(imgOriginalHeight, 512);
				}}
				type="button"
			>
				Set to 512
			</button>
			<br />
			render width:<b>{value.width} </b>
			<button
				onClick={(ev) => {
					updateDimmAndScaleBasedOnTarget(imgOriginalWidth, 512);
				}}
				type="button"
			>
				Set to 512
			</button>
			<br />
			<label>
				Scale:
				<input
					value={scale}
					onChange={(ev) => {
						setScale(ev.target.value);
						updateFieldValue({
							...calcScaledDimensions({
								height: imgOriginalHeight,
								width: imgOriginalWidth,
								scale: ev.target.value,
							}),
							imgUrl: value.imgUrl,
						});
					}}
					type="number"
					min="0"
					step="any"
				/>
			</label>
			<br />
			Original Height:{imgOriginalHeight}
			<br /> original width: {imgOriginalWidth}
			<br />
			<input
				onChange={fileSelected}
				name={name}
				accept="image/*"
				style={{ maxWidth: '90%' }}
				type="file"
			/>
			{value?.imgUrl?.length > 0 ? (
				<img alt="input image" style={{ maxWidth: '90%' }} src={value.imgUrl} />
			) : (
				<b>You must upload an img</b>
			)}
		</>
	);
}

function TextBoxFieldInput({ value, name, onChange }) {
	return (
		<textarea
			value={value}
			name={name}
			onChange={onChange}
			style={{ minHeight: '4rem', minWidth: '30rem' }}
		/>
	);
}

function formImageReducer(state, data) {
	switch (data.type) {
		case 'formField':
			return formImageFormFieldReducer(state, data);
			break;
		case 'loadFormData':
			return formFieldsPopulateReducer(state, data);
			break;
		case 'images':
			return formImageFormImageReducer(state, data);
			break;
		default:
			return data;
			break;
	}
	return state;
}

function formImageFormImageReducer(state, data) {
	switch (data.action) {
		case 'set':
			return { ...state, images: [...data.value.files] };
			break;
		default:
			return state;
			break;
	}
}

function formFieldsPopulateReducer(state, data) {
	let valuesOfFormFields = {};
	for (let field of data.value.formFieldsData) {
		valuesOfFormFields[field.name] = field.defaultValue;
	}

	return {
		...state,
		images: [],
		formFieldsData: [...data.value.formFieldsData],
		formFieldValues: valuesOfFormFields,
	};
}

function formImageFormFieldReducer(state, data) {
	switch (data.action) {
		case 'set':
			return {
				...state,
				formFieldValues: {
					...state.formFieldValues,
					[data.name]: data.value,
				},
			};
			break;
		case 'reset':
			let matchingFields = state.formFieldsData.filter((field) => {
				return field.name === data.name;
			});
			if (matchingFields.length > 0) {
				return {
					...state,
					formFieldValues: {
						...state.formFieldValues,
						[data.name]: matchingFields[0].defaultValue,
					},
				};
			}

		default:
			return state;
			break;
	}
}

async function getFormDataFromEndpoint({
	dispatch,
	endpointForFetchingFormData,
}) {
	try {
		let resp = await fetch(endpointForFetchingFormData, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
		});
		let formData = await resp.json();

		dispatch({ type: 'loadFormData', value: formData });
	} catch (err) {
		console.log('FETCH OF INIT DATA FAILED');

		console.log(err);
		///alert('error check console +')
	}
}

async function submitPromptAndParameters({
	formFieldsData,
	formFieldValues,
	endpointForSubmittingForm,
	dispatch,
}) {
	try {
		let jsonForSubmiting = {};
		for (let field of formFieldsData) {
			jsonForSubmiting[field.name] = formFieldValues[field.name];
		}

		let resp = await fetch(endpointForSubmittingForm, {
			method: 'POST',
			body: JSON.stringify(jsonForSubmiting, null, '\t'),
			headers: {
				'Content-Type': 'application/json',
			},
		});
		let imgData = await resp.json();

		dispatch({ type: 'images', action: 'set', value: imgData });
	} catch (err) {
		console.log(err);

		alert('Error occured check console: ' + err);
	}
}

function ImageGenForm({
	endpointForFetchingFormData,
	endpointForSubmittingForm,
}) {
	const [state, dispatch] = useReducer(formImageReducer, {
		images: [],
		formFieldValues: {},
		formFieldsData: [],
	});

	useEffect(() => {
		getFormDataFromEndpoint({
			dispatch: dispatch,
			endpointForFetchingFormData: endpointForFetchingFormData,
		});
	}, [endpointForFetchingFormData]);

	return (
		<>
			<ImageGenFormDispatch.Provider value={dispatch}>
				{state.images.length > 0 && <DisplayImages images={state.images} />}
				<ImageGenFormWithTextFields
					formFieldValues={state.formFieldValues}
					formFieldsData={state.formFieldsData}
					submitAction={() => {
						submitPromptAndParameters({
							dispatch: dispatch,
							formFieldsData: state.formFieldsData,
							formFieldValues: state.formFieldValues,
							endpointForSubmittingForm,
						});
					}}
				/>
			</ImageGenFormDispatch.Provider>
		</>
	);
}

function DisplayImages({ images }) {
	let genImages = images.map((img) => {
		let imgUrlBase = new URL('http://localhost:5000/');
		imgUrlBase.pathname = img;
		return (
			<img
				alt="generated images"
				key={img}
				style={{ width: '30vw', margin: '1vw' }}
				src={imgUrlBase.href}
			/>
		);
	});
	return (
		<>
			Images:
			<div
				style={{
					display: 'grid',
					gridTemplateColumns: '1fr 1fr 1fr',
				}}
			>
				{genImages}
			</div>
		</>
	);
}

export default MainPage;
