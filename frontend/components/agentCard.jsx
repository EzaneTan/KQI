import React from 'react';

const AgentCard = ({ name, status, profit, onClick }) => (
  <div className="border rounded-xl p-4 shadow hover:shadow-lg transition">
    <h2 className="text-xl font-semibold">{name}</h2>
    <p className="text-sm text-gray-500">Status: <span className={`font-bold ${status === 'live' ? 'text-green-600' : 'text-red-500'}`}>{status}</span></p>
    <p className="text-sm mt-2">Profit: <span className="font-medium">${profit}</span></p>
    <button onClick={onClick} className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md">View Agent</button>
  </div>
);

export default AgentCard;
