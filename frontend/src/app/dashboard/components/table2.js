import processData from "./conversion";

export default function table2({ data }) {
  data = processData(data);

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr>
            <th className="px-4 py-2 border-b border-r border-black">Time Period</th>
            <th className="px-4 py-2 border-b border-black">Bikes</th>
            <th className="px-4 py-2 border-b border-black">Cars</th>
            {/* <th className="px-4 py-2 border-b border-black">Trucks</th> */}
            <th className="px-4 py-2 border-b border-black">Sum</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className="px-4 py-2 border-r border-black">{item.period}</td>
              <td className="px-4 py-2">{item.bikes}</td>
              <td className="px-4 py-2">{item.cars}</td>
              {/* <td className="px-4 py-2">{item.trucks}</td> */}
              <td className="px-4 py-2">{item.sum}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
