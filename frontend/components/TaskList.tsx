'use client';

import { motion } from 'framer-motion';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface Task {
  id: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
  result?: any;
  error?: string;
  agent?: {
    name: string;
    emoji: string;
  };
}

interface TaskListProps {
  tasks: Task[];
  onRefresh: () => void;
}

export default function TaskList({ tasks, onRefresh }: TaskListProps) {
  const handleDelete = async (taskId: string) => {
    try {
      await axios.delete(`${API_BASE}/tasks/${taskId}`);
      onRefresh();
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'failed':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'running':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default:
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'failed':
        return '❌';
      case 'running':
        return '⚙️';
      default:
        return '⏳';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Terminée';
      case 'failed':
        return 'Échouée';
      case 'running':
        return 'En cours';
      default:
        return 'En attente';
    }
  };

  const sortedTasks = [...tasks].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  return (
    <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-slate-700">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">Historique des tâches</h2>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors text-sm"
        >
          🔄 Actualiser
        </button>
      </div>

      {sortedTasks.length === 0 ? (
        <div className="text-center py-12 text-slate-400">
          <p className="text-lg mb-2">Aucune tâche pour le moment</p>
          <p className="text-sm">Créez votre première tâche pour commencer</p>
        </div>
      ) : (
        <div className="space-y-4">
          {sortedTasks.map((task, index) => (
            <motion.div
              key={task.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-slate-900/50 rounded-xl p-5 border border-slate-700 hover:border-slate-600 transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    {task.agent && (
                      <span className="text-lg" title={task.agent.name}>
                        {task.agent.emoji}
                      </span>
                    )}
                    <p className="text-white font-medium">{task.description}</p>
                  </div>
                  <div className="flex items-center space-x-3 text-sm">
                    <span
                      className={`px-3 py-1 rounded-full border ${getStatusColor(task.status)}`}
                    >
                      {getStatusIcon(task.status)} {getStatusText(task.status)}
                    </span>
                    {task.agent && task.agent.name && (
                      <span className="text-slate-500 text-xs">
                        par {task.agent.name}
                      </span>
                    )}
                    <span className="text-slate-500">
                      {new Date(task.created_at).toLocaleString('fr-FR')}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => handleDelete(task.id)}
                  className="ml-4 px-3 py-1 text-sm text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
                >
                  Supprimer
                </button>
              </div>

              {task.status === 'running' && (
                <div className="mt-4">
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full animate-pulse w-1/2"></div>
                  </div>
                </div>
              )}

              {task.status === 'completed' && task.result && (
                <div className="mt-4 p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                  <p className="text-sm font-medium text-green-400 mb-2">Résultat</p>
                  {task.result.result?.summary && (
                    <p className="text-sm text-slate-300">{task.result.result.summary}</p>
                  )}
                  {task.result.duration && (
                    <p className="text-xs text-slate-500 mt-2">
                      Durée: {task.result.duration.toFixed(2)}s
                    </p>
                  )}
                </div>
              )}

              {task.status === 'failed' && task.error && (
                <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                  <p className="text-sm font-medium text-red-400 mb-2">Erreur</p>
                  <p className="text-sm text-slate-300">{task.error}</p>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}

