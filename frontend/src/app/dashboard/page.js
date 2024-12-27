import VideoPlayer from "./components/videoplayer";
import Table from "./components/table";
import Table2 from "./components/table2";

export default function Dashboard() {
  const videoSrc = "/video/dummy.mp4"; // Replace with your video path

  const jsonData = [
    { time: "9:03 AM", object: "car" },
    { time: "9:05 AM", object: "bicycle" },
    { time: "10:00 AM", object: "bicycle" },
    { time: "10:45 AM", object: "bicycle" },
    { time: "11:20 AM", object: "car" },
    { time: "12:33 PM", object: "car" },
    { time: "1:00 PM", object: "car" },
  ];

  return (
    <div className="flex flex-row justify-start items-start min-h-screen text-center mt-[2%] ml-[2%]">
      <div className="w-full max-w-5xl pr-4">
        <VideoPlayer videoSrc={videoSrc} />
      </div>
      <div className="flex flex-col gap-y-12">
        <div>
          <Table data={jsonData} />
        </div>
        <div>
          <Table2 data={jsonData} />
        </div>
      </div>
    </div>
  );
}
