import React from 'react';

const OCRResultTable = ({ result }) => (
    <table className="table-auto border-collapse border border-gray-200 mt-4">
        <thead>
            <tr>
                <th className="border border-gray-200 px-4 py-2">Field</th>
                <th className="border border-gray-200 px-4 py-2">Value</th>
            </tr>
        </thead>
        <tbody>
            {Object.keys(result).map((key) => (
                <tr key={key}>
                    <td className="border border-gray-200 px-4 py-2 font-bold">{key}</td>
                    <td className="border border-gray-200 px-4 py-2">{result[key]}</td>
                </tr>
            ))}
        </tbody>
    </table>
);

export default OCRResultTable;
