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

export default function AgentsPage() {
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
      console.error('Erreur:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-4 hover:opacity-80 transition-opacity">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <span className="text-2xl">🤖</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Sintra AI</h1>
                <p className="text-sm text-slate-400">Nos Agents Spécialisés</p>
              </div>
            </Link>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-white mb-4">
            Rencontrez Notre Équipe d'Agents
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Chaque agent possède son expertise unique pour vous aider dans vos tâches quotidiennes
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, index) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Link href={`/agents/${agent.id}`}>
                <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-700 hover:border-blue-500 transition-all hover:shadow-lg hover:shadow-blue-500/20 cursor-pointer h-full">
                  {/* Agent Header */}
                  <div className="text-center mb-6">
                    <div className="text-6xl mb-4">{agent.emoji}</div>
                    <h3 className="text-2xl font-bold text-white mb-2">{agent.name}</h3>
                    <p className="text-blue-400 font-medium">{agent.role}</p>
                  </div>

                  {/* Description */}
                  <p className="text-slate-300 text-center mb-6 line-clamp-2">
                    {agent.description}
                  </p>

                  {/* Specialties Preview */}
                  <div className="flex flex-wrap gap-2 justify-center mb-4">
                    {agent.specialties.slice(0, 3).map((specialty, idx) => (
                      <span
                        key={idx}
                        className="text-xs px-3 py-1 bg-blue-500/10 text-blue-400 rounded-full border border-blue-500/20"
                      >
                        {specialty.split(' ').slice(0, 3).join(' ')}
                      </span>
                    ))}
                  </div>

                  {/* CTA */}
                  <div className="text-center">
                    <span className="text-blue-400 hover:text-blue-300 font-semibold inline-flex items-center">
                      En savoir plus
                      <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </span>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        {/* Back to Home */}
        <div className="text-center mt-12">
          <Link
            href="/"
            className="inline-flex items-center px-6 py-3 bg-slate-700 text-white rounded-xl hover:bg-slate-600 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Retour à l'accueil
          </Link>
        </div>
      </main>
    </div>
  );
}

