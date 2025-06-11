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
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const toggleTheme = () => setDark(!dark);

  const askBackend = async () => {
    try {
      const resp = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await resp.json();
      setAnswer(data.summary || '');
    } catch (err) {
      console.error(err);
      setAnswer('Error contacting API');
    }
  };

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
            {answer ? (
              <div>
                <h2 className="font-semibold mb-2">Answer</h2>
                <p>{answer}</p>
              </div>
            ) : (
              <p className="text-gray-500">Ask a question to see a reply.</p>
            )}
          </aside>
          <section className="flex-1 p-4 overflow-y-auto flex flex-col">
            <textarea
              value={question}
              onChange={e => setQuestion(e.target.value)}
              className="flex-1 border rounded p-2 dark:bg-gray-800 dark:text-white"
              placeholder="Type your question here..."
            />
            <button
              onClick={askBackend}
              className="mt-2 self-start px-3 py-1 border rounded text-sm dark:border-gray-600"
            >
              Ask
            </button>
          </section>
        </main>
      </div>
    </div>
  );
}
