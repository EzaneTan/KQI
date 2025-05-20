const AgentStatusBadge = ({ status }) => {
  const statusColors = {
    live: 'bg-green-600',
    training: 'bg-yellow-500',
    offline: 'bg-gray-500',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-white text-xs ${statusColors[status]}`}>
      {status.toUpperCase()}
    </span>
  );
};
