import "./App.css";
import { DropzoneArea } from "material-ui-dropzone";
import { useState, React } from "react";

function App() {
	const [fileList, setFileList] = useState([]);
	const [volume, setvolume] = useState(100);
	const [Phaser, setPhaser] = useState(false);
	const [Chorus, setChorus] = useState(false);
	const [Reverb, setReverb] = useState(0);
	const [PitchShift, setPitchShift] = useState(0);
	const [LadderFilter, setLadderFilter] = useState(0);
	const [Distortion, setDistortion] = useState(false);

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
				// Volume: volume, //0-200
				Reverb: {room_size : Reverb}, //0-100
				// PitchShift: PitchShift, //-15-15
				// LadderFilter: LadderFilter, //0-1600
				// Distortion: Distortion, //boolean
				// Phaser: Phaser, //boolean
				// Chorus: Chorus, //boolean
			}]

			data.append(`file`, file, file.name);
			data.append(`controls`,JSON.stringify(controls) );

			fetch("http://localhost:4000", {
				method: "POST",
				body: data,
				mode: 'cors',
				headers: {
				  'Access-Control-Allow-Origin':'*'
				}
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
						value={volume}
						step={0.1}
						min={0}
						max={1}
					/>
					<label htmlFor="volume">Volume {volume}%</label>
				</div>
				<div className="row">
					<input
						type="range"
						id="Reverb"
						name="Reverb"
						step={0.05}
						value={Reverb}
						onChange={(e) => setReverb(e.target.value)}
						min={0}
						max={1}
					/>
					<label htmlFor="volume">Reverb {Reverb}%</label>
				</div>
				<div className="row">
					<input
						type="range"
						id="PitchShift"
						name="PitchShift"
						step={1}
						value={PitchShift}
						onChange={(e) => setPitchShift(e.target.value)}
						min={-15}
						max={15}
					/>
					<label htmlFor="PitchShift">
						PitchShift {PitchShift} semitones
					</label>
				</div>
				<div className="row">
					<input
						type="range"
						id="LadderFilter"
						name="LadderFilter"
						step={1}
						value={LadderFilter}
						onChange={(e) => setLadderFilter(e.target.value)}
						min={0}
						max={1600}
					/>
					<label htmlFor="LadderFilter">
						LadderFilter cutoff {LadderFilter}hz
					</label>
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
				<div className="row">
					<input
						type="checkbox"
						id="Phaser"
						name="Phaser"
						onChange={(e) => setPhaser(e.target.checked)}
						checked={Phaser}
					/>
					<label htmlFor="Phaser">Phaser</label>
				</div>
				<div className="row">
					<input
						type="checkbox"
						id="Distortion"
						name="Distortion"
						onChange={(e) => setDistortion(e.target.checked)}
						checked={Distortion}
					/>
					<label htmlFor="Distortion">Distortion</label>
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
