import VideoPlayer from "./components/videoplayer";

export default function Dashboard() {
  const videoSrc = "/video/dummy.mp4"; // Replace with your video path

  return (
    <div className="flex flex-col justify-start items-start min-h-screen text-center">
      <div className="w-full max-w-3xl p-4 mt-[5%] ml-[10%]">
        <VideoPlayer videoSrc={videoSrc} />
      </div>
    </div>
  );
}
