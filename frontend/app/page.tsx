'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import Link from 'next/link';
import AgentStatus from '@/components/AgentStatus';
import TaskCreator from '@/components/TaskCreator';
import TaskList from '@/components/TaskList';
import MemoryViewer from '@/components/MemoryViewer';
import AgentsGallery from '@/components/AgentsGallery';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'tasks' | 'memory' | 'about'>('tasks');
  const [agentStatus, setAgentStatus] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // Actualiser toutes les 5 secondes
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [statusRes, tasksRes] = await Promise.all([
        axios.get(`${API_BASE}/agent/status`),
        axios.get(`${API_BASE}/tasks`),
      ]);
      setAgentStatus(statusRes.data);
      setTasks(tasksRes.data.tasks || []);
      setLoading(false);
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
      setLoading(false);
    }
  };

  const handleTaskCreated = () => {
    loadData();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-4"
            >
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <span className="text-2xl">🤖</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Sintra AI</h1>
                <p className="text-sm text-slate-400">Agent IA Autonome</p>
              </div>
            </motion.div>

            <AgentStatus status={agentStatus} />
          </div>
        </div>
      </header>

      {/* Navigation */}
      <div className="border-b border-slate-700 bg-slate-900/30">
        <div className="container mx-auto px-6">
          <nav className="flex space-x-8">
            {[
              { id: 'tasks', label: 'Tâches', icon: '📋' },
              { id: 'agents', label: 'Agents', icon: '👥', href: '/agents' },
              { id: 'memory', label: 'Mémoire', icon: '🧠' },
              { id: 'about', label: 'À propos', icon: 'ℹ️' },
            ].map((tab) => 
              tab.href ? (
                <Link
                  key={tab.id}
                  href={tab.href}
                  className="py-4 px-2 border-b-2 border-transparent text-slate-400 hover:text-white hover:border-slate-600 transition-colors"
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </Link>
              ) : (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-4 px-2 border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-white'
                      : 'border-transparent text-slate-400 hover:text-white'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              )
            )}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : (
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === 'tasks' && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1">
                  <TaskCreator onTaskCreated={handleTaskCreated} />
                </div>
                <div className="lg:col-span-2">
                  <TaskList tasks={tasks} onRefresh={loadData} />
                </div>
              </div>
            )}

            {activeTab === 'memory' && <MemoryViewer />}

            {activeTab === 'about' && (
              <div className="max-w-6xl mx-auto">
                <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-700 mb-8">
                  <h2 className="text-3xl font-bold text-white mb-6">Nos Agents Spécialisés</h2>
                  <p className="text-slate-300 mb-6">
                    Chaque agent possède ses propres compétences, personnalité et outils pour vous aider dans vos tâches quotidiennes.
                  </p>
                  
                  <AgentsGallery />
                </div>

                <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-8 border border-slate-700">
                  <h2 className="text-3xl font-bold text-white mb-6">À propos de Sintra AI</h2>
                  
                  <div className="space-y-6 text-slate-300">
                    <div>
                      <h3 className="text-xl font-semibold text-white mb-3">🎯 Qu'est-ce que Sintra AI ?</h3>
                      <p>
                        Sintra AI est un système d'agents IA autonomes et spécialisés, capables de comprendre, planifier et exécuter
                        des tâches complexes de manière indépendante. Chaque agent possède son expertise unique pour vous assister
                        dans différents domaines professionnels.
                      </p>
                    </div>

                    <div>
                      <h3 className="text-xl font-semibold text-white mb-3">✨ Caractéristiques principales</h3>
                      <ul className="list-disc list-inside space-y-2">
                        <li>Planification hiérarchique et décomposition de tâches</li>
                        <li>Système de mémoire multi-niveaux (court et long terme)</li>
                        <li>Exécution autonome avec gestion d'erreurs</li>
                        <li>Outils multiples (recherche web, calcul, fichiers, code)</li>
                        <li>Apprentissage et adaptation continue</li>
                        <li>API REST complète pour l'intégration</li>
                      </ul>
                    </div>

                    <div>
                      <h3 className="text-xl font-semibold text-white mb-3">🛠️ Technologies utilisées</h3>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-slate-700/50 rounded-lg p-4">
                          <p className="font-semibold">Backend</p>
                          <p className="text-sm text-slate-400">Python, FastAPI, AsyncIO</p>
                        </div>
                        <div className="bg-slate-700/50 rounded-lg p-4">
                          <p className="font-semibold">Frontend</p>
                          <p className="text-sm text-slate-400">Next.js, React, TailwindCSS</p>
                        </div>
                        <div className="bg-slate-700/50 rounded-lg p-4">
                          <p className="font-semibold">IA</p>
                          <p className="text-sm text-slate-400">OpenAI, Anthropic, LangChain</p>
                        </div>
                        <div className="bg-slate-700/50 rounded-lg p-4">
                          <p className="font-semibold">Données</p>
                          <p className="text-sm text-slate-400">ChromaDB, SQLite, Redis</p>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-xl font-semibold text-white mb-3">🚀 Utilisation</h3>
                      <ol className="list-decimal list-inside space-y-2">
                        <li>Décrivez votre tâche dans le champ prévu à cet effet</li>
                        <li>L'agent analyse et crée un plan d'exécution</li>
                        <li>Il exécute le plan de manière autonome</li>
                        <li>Vous recevez les résultats et recommandations</li>
                      </ol>
                    </div>

                    <div className="border-t border-slate-600 pt-6 mt-6">
                      <p className="text-sm text-slate-400">
                        Version 1.0.0 • Créé avec ❤️ • Open Source
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </main>
    </div>
  );
}

