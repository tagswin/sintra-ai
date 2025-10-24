'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
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
  preferred_tools: string[];
  task_count: number;
}

export default function AgentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const agentId = params?.agentId as string;
  
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (agentId) {
      loadAgent();
    }
  }, [agentId]);

  const loadAgent = async () => {
    try {
      const response = await axios.get(`${API_BASE}/agents/${agentId}`);
      setAgent(response.data);
      setLoading(false);
    } catch (error: any) {
      console.error('Erreur:', error);
      setError(error.response?.data?.detail || 'Agent non trouvé');
      setLoading(false);
    }
  };

  const handleStartTask = () => {
    router.push(`/?agent=${agentId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || !agent) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">Agent non trouvé</h1>
          <p className="text-slate-400 mb-8">{error}</p>
          <Link
            href="/agents"
            className="px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors inline-block"
          >
            Voir tous les agents
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800">
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
                <p className="text-sm text-slate-400">Agent Spécialisé</p>
              </div>
            </Link>

            <Link
              href="/agents"
              className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors text-sm"
            >
              Tous les agents
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="border-b border-slate-700 bg-gradient-to-r from-blue-500/10 to-purple-500/10">
        <div className="container mx-auto px-6 py-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-4xl mx-auto"
          >
            <div className="text-8xl mb-6">{agent.emoji}</div>
            <h1 className="text-5xl font-bold text-white mb-4">{agent.name}</h1>
            <p className="text-2xl text-blue-400 font-semibold mb-6">{agent.role}</p>
            <p className="text-xl text-slate-300 mb-8">{agent.description}</p>
            
            <button
              onClick={handleStartTask}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-all shadow-lg hover:shadow-blue-500/50"
            >
              🚀 Commencer à travailler avec {agent.name}
            </button>
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Specialties */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-700"
          >
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="text-3xl mr-3">✨</span>
              Spécialités
            </h2>
            <div className="space-y-3">
              {agent.specialties.map((specialty, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + idx * 0.05 }}
                  className="flex items-start space-x-3 p-3 bg-slate-900/50 rounded-lg"
                >
                  <span className="text-blue-400 mt-1">•</span>
                  <span className="text-slate-300">{specialty}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Personality */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-700"
          >
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="text-3xl mr-3">💫</span>
              Personnalité
            </h2>
            <div className="space-y-3">
              {agent.personality_traits.map((trait, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + idx * 0.05 }}
                  className="px-4 py-3 bg-purple-500/10 text-purple-400 rounded-lg border border-purple-500/20 font-medium"
                >
                  {trait}
                </motion.div>
              ))}
            </div>

            {/* Tools */}
            <div className="mt-8">
              <h3 className="text-lg font-semibold text-white mb-3">Outils préférés</h3>
              <div className="flex flex-wrap gap-2">
                {agent.preferred_tools.map((tool, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-slate-700 text-slate-300 rounded-full text-sm"
                  >
                    {tool}
                  </span>
                ))}
              </div>
            </div>

            {/* Stats */}
            {agent.task_count > 0 && (
              <div className="mt-8 p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                <p className="text-green-400 font-semibold">
                  ✓ {agent.task_count} tâche{agent.task_count > 1 ? 's' : ''} complétée{agent.task_count > 1 ? 's' : ''}
                </p>
              </div>
            )}
          </motion.div>
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-12 max-w-4xl mx-auto text-center bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-2xl p-12 border border-blue-500/20"
        >
          <h2 className="text-3xl font-bold text-white mb-4">
            Prêt à travailler avec {agent.name} ?
          </h2>
          <p className="text-slate-300 mb-8 text-lg">
            {agent.name} est là pour vous aider avec {agent.role.toLowerCase()}
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <button
              onClick={handleStartTask}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 transition-all"
            >
              Créer une tâche
            </button>
            <Link
              href="/agents"
              className="px-8 py-4 bg-slate-700 text-white rounded-xl font-semibold hover:bg-slate-600 transition-colors"
            >
              Voir les autres agents
            </Link>
          </div>
        </motion.div>
      </main>
    </div>
  );
}

