import { useState } from "react";

export default function VideoUpload() {
  const [file, setFile] = useState(null);

  // Handle file selection
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a video to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("Video uploaded successfully!");
      } else {
        alert("Failed to upload video.");
      }
    } catch (error) {
      console.error("Error uploading video:", error);
      alert("Error uploading video.");
    }
  };

  return (
    <div>
      <h1>Upload Video</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}
