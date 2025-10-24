'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import Link from 'next/link';

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

export default function AgentsGallery() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

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
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {agents.map((agent, index) => (
        <Link key={agent.id} href={`/agents/${agent.id}`}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-slate-900/50 rounded-xl p-6 border border-slate-700 hover:border-blue-500 cursor-pointer transition-all hover:shadow-lg hover:shadow-blue-500/20"
          >
            {/* Header */}
            <div className="flex items-start space-x-4 mb-4">
              <div className="text-4xl">{agent.emoji}</div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-white">{agent.name}</h3>
                <p className="text-sm text-slate-400">{agent.role}</p>
              </div>
            </div>

            {/* Description */}
            <p className="text-sm text-slate-300 mb-4">{agent.description}</p>

            {/* Spécialités */}
            <div className="mb-4">
              <p className="text-xs font-semibold text-slate-400 mb-2">Spécialités:</p>
              <div className="flex flex-wrap gap-1">
                {agent.specialties.slice(0, 3).map((specialty, idx) => (
                  <span
                    key={idx}
                    className="text-xs px-2 py-1 bg-blue-500/10 text-blue-400 rounded border border-blue-500/20"
                  >
                    {specialty}
                  </span>
                ))}
                {agent.specialties.length > 3 && (
                  <span className="text-xs px-2 py-1 text-slate-500">
                    +{agent.specialties.length - 3}
                  </span>
                )}
              </div>
            </div>

            {/* Stats */}
            {agent.task_count > 0 && (
              <div className="flex items-center text-xs text-slate-500">
                <span>✓</span>
                <span className="ml-1">{agent.task_count} tâche{agent.task_count > 1 ? 's' : ''} complétée{agent.task_count > 1 ? 's' : ''}</span>
              </div>
            )}
          </motion.div>
        </Link>
      ))}
    </div>
  );
}

