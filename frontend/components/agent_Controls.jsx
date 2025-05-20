const AgentControls = ({ onStart, onStop, onDeploy }) => (
  <div className="flex gap-2 mt-2">
    <button onClick={onStart} className="bg-green-700 text-white px-3 py-1 rounded">Start</button>
    <button onClick={onStop} className="bg-red-700 text-white px-3 py-1 rounded">Stop</button>
    <button onClick={onDeploy} className="bg-blue-700 text-white px-3 py-1 rounded">Deploy</button>
  </div>
);
