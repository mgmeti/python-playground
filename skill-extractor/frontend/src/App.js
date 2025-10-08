import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleExtract = async () => {
    const formData = new FormData();
    if (file) formData.append("file", file);
    if (text) formData.append("text", text);

    try {
      const response = await axios.post("http://localhost:8000/extract", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResult(response.data);
    } catch (error) {
      console.error("Extraction error:", error);
      setResult(null);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Job Skill Extractor</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
        cols={60}
        placeholder="Paste job description here..."
      />
      <br /><br />

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />

      <button onClick={handleExtract}>Extract</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Skills</h2>
          <ul>{result.skills.map((s, i) => <li key={i}>{s}</li>)}</ul>

          <h2>Experience</h2>
          <p>{result.experience}</p> {/* updated: now plain string */}
        </div>
      )}
    </div>
  );
}

export default App;
