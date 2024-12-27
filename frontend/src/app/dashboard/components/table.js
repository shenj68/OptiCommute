export default function table({ data }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr>
            <th className="px-4 py-2 border-b border-r border-black">Time</th>
            <th className="px-4 py-2 border-b border-black">Object</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className="px-4 py-2 border-r border-black">{item.time}</td>
              <td className="px-4 py-2">{item.object}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
