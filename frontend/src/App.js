import "./App.css";
import { DropzoneArea } from "material-ui-dropzone";
import { useState, React } from "react";

function App() {
	const [fileList, setFileList] = useState([]);
	const [Volume, setvolume] = useState(100);
	const [Reverb, setReverb] = useState(0);
	const [Delay, setDelay] = useState(0);
	const [Chorus, setChorus] = useState(false);
	const [Distortion, setDistortion] = useState(0);

	const handleFileChange = (files) => {
		setFileList(files);
	};

	const handleUploadClick = () => {
		if (!fileList) {
			return;
		}

		files.forEach((file) => {
			const data = new FormData();
			const controls = [{
				Gain: [{isOn: true},{gain_db:Volume*0.01}]}, //0-200
				{ Reverb: [{isOn: true},{room_size : Reverb*0.01}]}, //0-100
				{ Delay:[{isOn: true}, {mix : Delay}]}, //0-100
				{ Chorus:[{isOn:Chorus}, {}  ]}, //boolean
				{ Distortion:[{isOn: true}, {drive_db : Distortion}]}, //0-100
			]
			console.log(JSON.stringify(controls))
			data.append(`file`, file, file.name);
			data.append(`controls`,JSON.stringify(controls) );

			fetch("http://localhost:4000", {
				method: "POST",
				body: data,
				// mode: 'cors',
				// headers: {
				//   'Access-Control-Allow-Origin':'*'
				// }
			})
				.then((res) => {
					if (res.status === 404) return;
					return res.blob();
				})
				.then((blob) => {
					console.log(blob);
					const url = window.URL.createObjectURL(blob);
					const a = document.createElement("a");
					a.style.display = "none";
					a.href = url;
					a.download = file.name;
					document.body.appendChild(a);
					a.click();
					window.URL.revokeObjectURL(url);
					alert("your file has downloaded!"); // or you know, something with better UX...
				})
				.catch(() => alert("oh no!"));
		});
	};

	function Editor() {
		return (
			<div className="Edit">
				<div className="row">
					<input
						type="range"
						id="volume"
						name="volume"
						onChange={(e) => setvolume(e.target.value)}
						value={Volume}
						step={5}
						min={0}
						max={100}
					/>
					<label htmlFor="volume">Volume {Volume}%</label>
				</div>
				<div className="row">
					<input
						type="range"
						id="Reverb"
						name="Reverb"
						step={5}
						value={Reverb}
						onChange={(e) => setReverb(e.target.value)}
						min={0}
						max={100}
					/>
					<label htmlFor="Reverb">Reverb {Reverb}%</label>
				</div>
				<div className="row">
					<input
						type="range"
						id="Delay"
						name="Delay"
						onChange={(e) => setDelay(e.target.value)}
						value={Delay}
						step={5}
						min={0}
						max={100}
					/>
					<label htmlFor="Delay">Delay {Delay}%</label>
				</div>
				<div className="row">
					<input
						type="range"
						id="Distortion"
						name="Distortion"
						onChange={(e) => setDistortion(e.target.value)}
						value={Distortion}
						step={5}
						min={0}
						max={100}
					/>
					<label htmlFor="Distortion">Distortion {Distortion}%</label>
				</div>
				<div className="row">
					<input
						type="checkbox"
						id="Chorus"
						name="Chorus"
						onChange={(e) => setChorus(e.target.checked)}
						checked={Chorus}
					/>
					<label htmlFor="Chorus">Chorus</label>
				</div>
				<input
					className="submit"
					type="submit"
					value={"上傳"}
					onClick={handleUploadClick}
				/>
			</div>
		);
	}

	// 👇 files is not an array, but it's iterable, spread to get an array of files
	const files = fileList ? [...fileList] : [];

	return (
		<div className="App">
			<h1 className="webname">Online Pedalboard</h1>
			<DropzoneArea
				acceptedFiles={["audio/*"]}
				dropzoneText={"Drag and drop audios here or click"}
				onChange={(files) => handleFileChange(files)}
				maxFileSize={9000000}
				className="Upload"
			/>
			<Editor />
		</div>
	);
}

export default App;
