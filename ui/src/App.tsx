import React, { useState } from 'react';

const MODELS = [
  { id: 'deepseek', label: 'DeepSeek', info: 'Great for code. ~4GB VRAM.' },
  { id: 'mistral', label: 'Mistral', info: 'Balanced model, moderate size.' },
  { id: 'phi-3', label: 'Phi-3-mini', info: 'Small and fast for CPU.' },
  { id: 'gpt4', label: 'OpenAI GPT-4', info: 'Requires API key, best quality.' }
];

export default function App() {
  const [dark, setDark] = useState(true);
  const [model, setModel] = useState(MODELS[0].id);
  const [apiKey, setApiKey] = useState('');
  const toggleTheme = () => setDark(!dark);

  return (
    <div className={dark ? 'dark h-full' : 'h-full'}>
      <div className="flex flex-col h-full bg-gray-100 dark:bg-gray-900">
        <header className="p-4 flex items-center justify-between bg-gray-200 dark:bg-gray-800">
          <h1 className="font-semibold">Danus</h1>
          <div className="flex items-center gap-2">
            <select
              value={model}
              onChange={e => setModel(e.target.value)}
              className="border rounded px-2 py-1 text-sm dark:bg-gray-700 dark:text-white"
            >
              {MODELS.map(m => (
                <option key={m.id} value={m.id}>{m.label}</option>
              ))}
            </select>
            <span className="relative inline-block group">
              <span className="cursor-help text-lg">?</span>
              <span className="absolute hidden group-hover:block text-xs bg-gray-700 text-white p-1 rounded w-40 -left-1/2 mt-1">
                {MODELS.find(m => m.id === model)?.info}
              </span>
            </span>
            <input
              type="password"
              placeholder="API key (optional)"
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
              className="border rounded px-2 py-1 text-sm dark:bg-gray-700 dark:text-white"
            />
            <button onClick={toggleTheme} className="ml-2 text-sm underline">
              {dark ? 'Light' : 'Dark'} mode
            </button>
          </div>
        </header>

        <main className="flex flex-1 overflow-hidden">
          <aside className="w-1/3 p-4 border-r border-gray-300 dark:border-gray-700 overflow-y-auto">
            {/* Chat messages would appear here */}
            <p className="text-gray-500">Chat coming soon…</p>
          </aside>
          <section className="flex-1 p-4 overflow-y-auto">
            <textarea
              className="w-full h-full border rounded p-2 dark:bg-gray-800 dark:text-white"
              placeholder="Type here… AI suggestions will appear as you type"
            />
          </section>
        </main>
      </div>
    </div>
  );
}
