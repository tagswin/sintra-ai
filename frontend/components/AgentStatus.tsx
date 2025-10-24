'use client';

import { motion } from 'framer-motion';

interface AgentStatusProps {
  status: any;
}

export default function AgentStatus({ status }: AgentStatusProps) {
  if (!status) {
    return (
      <div className="flex items-center space-x-2 text-slate-400">
        <div className="w-3 h-3 rounded-full bg-slate-500 animate-pulse"></div>
        <span className="text-sm">Chargement...</span>
      </div>
    );
  }

  const isRunning = status.is_running;
  const statusColor = isRunning ? 'bg-green-500' : 'bg-blue-500';
  const statusText = isRunning ? 'En cours' : 'Disponible';

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="flex items-center space-x-6"
    >
      {/* Status */}
      <div className="flex items-center space-x-2">
        <div className={`w-3 h-3 rounded-full ${statusColor} ${isRunning ? 'animate-pulse' : ''}`}></div>
        <span className="text-sm text-white">{statusText}</span>
      </div>

      {/* Stats */}
      <div className="flex items-center space-x-4 text-sm text-slate-400">
        <div>
          <span className="font-semibold text-white">{status.tasks_completed}</span> tâches
        </div>
        <div>
          <span className="font-semibold text-white">
            {status.memory_size?.episodic || 0}
          </span>{' '}
          mémoires
        </div>
      </div>

      {/* Model */}
      <div className="px-3 py-1 bg-slate-700/50 rounded-full text-xs text-slate-300">
        {status.model}
      </div>
    </motion.div>
  );
}

