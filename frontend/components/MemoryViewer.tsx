'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export default function MemoryViewer() {
  const [memoryData, setMemoryData] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMemoryData();
  }, []);

  const loadMemoryData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/memory`);
      setMemoryData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Erreur lors du chargement de la mémoire:', error);
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    try {
      const response = await axios.get(`${API_BASE}/memory/search`, {
        params: { query: searchQuery, limit: 10 },
      });
      setSearchResults(response.data.results || []);
    } catch (error) {
      console.error('Erreur lors de la recherche:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats de mémoire */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 backdrop-blur-xl rounded-2xl p-6 border border-blue-500/30"
        >
          <div className="text-3xl mb-2">💭</div>
          <div className="text-2xl font-bold text-white">
            {memoryData?.size?.working || 0}
          </div>
          <div className="text-sm text-slate-300">Mémoire de travail</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 backdrop-blur-xl rounded-2xl p-6 border border-purple-500/30"
        >
          <div className="text-3xl mb-2">📚</div>
          <div className="text-2xl font-bold text-white">
            {memoryData?.size?.episodic || 0}
          </div>
          <div className="text-sm text-slate-300">Mémoire épisodique</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-green-500/20 to-green-600/20 backdrop-blur-xl rounded-2xl p-6 border border-green-500/30"
        >
          <div className="text-3xl mb-2">🧠</div>
          <div className="text-2xl font-bold text-white">
            {memoryData?.size?.semantic || 0}
          </div>
          <div className="text-sm text-slate-300">Mémoire sémantique</div>
        </motion.div>
      </div>

      {/* Recherche dans la mémoire */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-slate-700"
      >
        <h3 className="text-xl font-bold text-white mb-4">Rechercher dans la mémoire</h3>
        
        <div className="flex space-x-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Recherchez un souvenir..."
            className="flex-1 px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleSearch}
            className="px-6 py-3 bg-blue-500 text-white rounded-xl font-semibold hover:bg-blue-600 transition-colors"
          >
            🔍 Rechercher
          </button>
        </div>

        {searchResults.length > 0 && (
          <div className="mt-6 space-y-3">
            {searchResults.map((result, index) => (
              <div
                key={index}
                className="p-4 bg-slate-900/50 rounded-lg border border-slate-700"
              >
                <p className="text-sm text-slate-300">
                  {result.description || JSON.stringify(result).substring(0, 200)}
                </p>
                <p className="text-xs text-slate-500 mt-2">
                  Type: {result.type || 'unknown'}
                </p>
              </div>
            ))}
          </div>
        )}
      </motion.div>

      {/* Mémoires récentes */}
      {memoryData?.recent_memories && memoryData.recent_memories.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-slate-700"
        >
          <h3 className="text-xl font-bold text-white mb-4">Mémoires récentes</h3>
          
          <div className="space-y-3">
            {memoryData.recent_memories.map((memory: any, index: number) => (
              <div
                key={index}
                className="p-4 bg-slate-900/50 rounded-lg border border-slate-700"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-white font-medium mb-2">
                      {memory.description || 'Mémoire sans description'}
                    </p>
                    <div className="flex items-center space-x-3 text-xs text-slate-500">
                      <span>Type: {memory.type || 'unknown'}</span>
                      {memory.timestamp && (
                        <span>
                          {new Date(memory.timestamp).toLocaleString('fr-FR')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

