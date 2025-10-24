'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface Agent {
  id: string;
  name: string;
  emoji: string;
  role: string;
  description: string;
  specialties: string[];
  personality_traits: string[];
  task_count: number;
}

interface AgentSelectorProps {
  selectedAgent: string | null;
  onSelect: (agentId: string | null) => void;
}

export default function AgentSelector({ selectedAgent, onSelect }: AgentSelectorProps) {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await axios.get(`${API_BASE}/agents`);
      setAgents(response.data.agents || []);
      setLoading(false);
    } catch (error) {
      console.error('Erreur lors du chargement des agents:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-slate-400 text-sm">Chargement des agents...</div>
    );
  }

  const displayedAgents = showAll ? agents : agents.slice(0, 4);

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-slate-300">
          Choisir un agent spécialisé
        </label>
        <button
          onClick={() => onSelect(null)}
          className={`text-xs px-2 py-1 rounded ${
            selectedAgent === null
              ? 'bg-blue-500 text-white'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          ✨ Auto
        </button>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {displayedAgents.map((agent, index) => (
          <motion.button
            key={agent.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            onClick={() => onSelect(agent.id)}
            className={`p-3 rounded-lg border text-left transition-all ${
              selectedAgent === agent.id
                ? 'border-blue-500 bg-blue-500/10'
                : 'border-slate-600 bg-slate-800/50 hover:border-slate-500'
            }`}
          >
            <div className="flex items-start space-x-2">
              <span className="text-2xl">{agent.emoji}</span>
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-white text-sm truncate">
                  {agent.name}
                </div>
                <div className="text-xs text-slate-400 truncate">
                  {agent.role}
                </div>
                {agent.task_count > 0 && (
                  <div className="text-xs text-slate-500 mt-1">
                    {agent.task_count} tâche{agent.task_count > 1 ? 's' : ''}
                  </div>
                )}
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {agents.length > 4 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="w-full text-sm text-blue-400 hover:text-blue-300 transition-colors"
        >
          {showAll ? '↑ Voir moins' : `↓ Voir ${agents.length - 4} agents de plus`}
        </button>
      )}

      {selectedAgent && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="p-3 bg-slate-800/50 rounded-lg border border-slate-700"
        >
          {(() => {
            const agent = agents.find((a) => a.id === selectedAgent);
            if (!agent) return null;
            return (
              <div>
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-xl">{agent.emoji}</span>
                  <div>
                    <div className="font-semibold text-white text-sm">{agent.name}</div>
                    <div className="text-xs text-slate-400">{agent.role}</div>
                  </div>
                </div>
                <p className="text-xs text-slate-300 mb-2">{agent.description}</p>
                <div className="flex flex-wrap gap-1">
                  {agent.specialties.slice(0, 3).map((specialty, idx) => (
                    <span
                      key={idx}
                      className="text-xs px-2 py-0.5 bg-slate-700 text-slate-300 rounded"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
              </div>
            );
          })()}
        </motion.div>
      )}
    </div>
  );
}

