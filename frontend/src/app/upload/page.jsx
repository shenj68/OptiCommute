"use client";

import { Button } from "@/app/ui/button";
import { useState } from "react";

export default function UploadPage() {
  const [video, setVideo] = useState(null);

  const handleVideoChange = (event) => {
    setVideo(event.target.files[0]);
  };

  const handleUpload = async (event) => {
    event.preventDefault();

    // check if a file was uploaded
    if (!video) {
      alert("Please upload a video file");
      return;
    }

    const formData = new FormData();
    formData.append("file", video);

    // calls api to wrtie file into public/videos
    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!!response.ok) {
        alert("File uploaded successfully.");
      } else {
        alert("Error uploading file.");
      }
    } catch (error) {
      console.log("Error occured ", error);
      alert("Error uploading file.");
    }
  };

  // do an api call or something
  return (
    <div>
      <h1>Upload File</h1>
      <form onSubmit={handleUpload}>
        <input type="file" accept="video/*" onChange={handleVideoChange} />
        <Button type="submit">Upload</Button>
      </form>
    </div>
  );
}
