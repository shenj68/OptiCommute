export default function VideoPlayer({ videoSrc }) {
  return (
    <div className="w-full h-auto">
      <video className="w-full h-auto border-2 border-black rounded-lg" controls>
        <source src={videoSrc} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
