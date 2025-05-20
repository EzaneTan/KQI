// components/Agent/AgentCard.jsx
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

// components/Agent/AgentStatusBadge.jsx
import React from 'react';

const AgentStatusBadge = ({ status }) => {
  const color = status === 'live' ? 'green' : status === 'training' ? 'yellow' : 'red';
  const label = status.charAt(0).toUpperCase() + status.slice(1);

  return (
    <span className={`inline-block px-2 py-1 text-xs rounded-full bg-${color}-100 text-${color}-800`}>
      {label}
    </span>
  );
};

export default AgentStatusBadge;

// components/Agent/AgentControls.jsx
import React from 'react';

const AgentControls = ({ onStart, onStop, onDeploy }) => (
  <div className="flex space-x-2">
    <button onClick={onStart} className="bg-green-600 text-white px-3 py-1 rounded-md">Start</button>
    <button onClick={onStop} className="bg-red-600 text-white px-3 py-1 rounded-md">Stop</button>
    <button onClick={onDeploy} className="bg-blue-600 text-white px-3 py-1 rounded-md">Deploy</button>
  </div>
);

export default AgentControls;

// components/Agent/AgentDetailModal.jsx
import React from 'react';

const AgentDetailModal = ({ isOpen, onClose, agent }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-xl shadow-lg w-96">
        <h3 className="text-lg font-bold mb-2">{agent.name} Details</h3>
        <p>Status: {agent.status}</p>
        <p>Profit: ${agent.profit}</p>
        <p>Strategy: {agent.strategy}</p>
        <div className="mt-4 flex justify-end">
          <button onClick={onClose} className="px-4 py-2 bg-gray-300 rounded-md">Close</button>
        </div>
      </div>
    </div>
  );
};

export default AgentDetailModal;

// components/Charts/PerformanceChart.jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PerformanceChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="timestamp" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="profit" stroke="#82ca9d" strokeWidth={2} />
    </LineChart>
  </ResponsiveContainer>
);

export default PerformanceChart;

// components/Strategy/StrategySelector.jsx
import React from 'react';

const StrategySelector = ({ strategies, selected, onSelect }) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-gray-700 mb-1">Select Strategy</label>
    <select
      value={selected}
      onChange={e => onSelect(e.target.value)}
      className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
    >
      {strategies.map(strategy => (
        <option key={strategy} value={strategy}>{strategy}</option>
      ))}
    </select>
  </div>
);

export default StrategySelector;
