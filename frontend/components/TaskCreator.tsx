'use client';

import { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import AgentSelector from './AgentSelector';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface TaskCreatorProps {
  onTaskCreated: () => void;
}

export default function TaskCreator({ onTaskCreated }: TaskCreatorProps) {
  const [description, setDescription] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const exampleTasks = [
    { text: 'Crée 5 posts Instagram pour ma startup tech', agent: 'soshie' },
    { text: 'Rédige une réponse à une réclamation client', agent: 'cassie' },
    { text: 'Optimise ma page produit pour le SEO', agent: 'seomi' },
    { text: 'Analyse mes données de ventes du mois', agent: 'dexter' },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;

    setLoading(true);
    setError('');

    try {
      await axios.post(`${API_BASE}/tasks`, {
        description: description.trim(),
        autonomous: true,
        agent_id: selectedAgent,
      });

      setDescription('');
      setSelectedAgent(null);
      onTaskCreated();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur lors de la création de la tâche');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-slate-700"
    >
      <h2 className="text-xl font-bold text-white mb-4">Nouvelle tâche</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <AgentSelector selectedAgent={selectedAgent} onSelect={setSelectedAgent} />
        
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Décrivez votre tâche
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Exemple: Crée un post Instagram pour promouvoir mon produit..."
            className="w-full px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={4}
            disabled={loading}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !description.trim()}
          className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Création en cours...
            </span>
          ) : (
            '🚀 Lancer la tâche'
          )}
        </button>
      </form>

      {/* Exemples */}
      <div className="mt-6 pt-6 border-t border-slate-700">
        <p className="text-xs font-medium text-slate-400 mb-3">EXEMPLES DE TÂCHES</p>
        <div className="space-y-2">
          {exampleTasks.map((task, index) => (
            <button
              key={index}
              onClick={() => {
                setDescription(task.text);
                setSelectedAgent(task.agent);
              }}
              className="w-full text-left px-3 py-2 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 rounded-lg transition-colors"
            >
              {task.text}
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

