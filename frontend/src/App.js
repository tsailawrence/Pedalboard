import "./App.css";
import { DropzoneArea } from "material-ui-dropzone";
import { useState, React } from "react";

function App() {
  const [fileList, setFileList] = useState([]);
  const [echo, setecho] = useState(false);
  const [volume, setvolume] = useState(100);

  const handleFileChange = (files) => {
    setFileList(files);
  };

  const handleEchoChange = () => {
    setecho(!echo);
  };

  const handleValueChange = (e) => {
    setvolume(e.target.value);
  };

  const handleUploadClick = () => {
    if (!fileList) {
      return;
    }

    const data = new FormData();
    files.forEach((file) => {
      data.append(`file`, file, file.name);
      data.append(`echo`, echo);
      data.append(`volume`, volume);
      fetch("/api/", {
        method: "POST",
        body: data,
      })
        .then((res) => res.blob())
        .then((blob) => {
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
      console.log(data);
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
            onChange={handleValueChange}
            value={volume}
            min={0}
            max={200}
          />
          <label htmlFor="volume">音量 {volume}%</label>
        </div>
        <div className="row">
          <input
            type="checkbox"
            id="echo"
            name="echo"
            onChange={handleEchoChange}
            checked={echo}
          />
          <label htmlFor="echo">回響</label>
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
