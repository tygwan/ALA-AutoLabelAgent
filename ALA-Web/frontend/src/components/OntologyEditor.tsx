import React, { useState } from 'react';
import { X, Plus, Save, FileJson } from 'lucide-react';

interface OntologyEditorProps {
    ontology: Record<string, string>;
    onChange: (ontology: Record<string, string>) => void;
    onClose: () => void;
}

export const OntologyEditor: React.FC<OntologyEditorProps> = ({ ontology, onChange, onClose }) => {
    const [localOntology, setLocalOntology] = useState(ontology);
    const [newClassName, setNewClassName] = useState('');
    const [newDescription, setNewDescription] = useState('');
    const [error, setError] = useState('');

    const handleAddClass = () => {
        if (!newClassName.trim()) {
            setError('Class name is required');
            return;
        }
        if (localOntology[newClassName]) {
            setError('Class name already exists');
            return;
        }

        setLocalOntology({
            ...localOntology,
            [newClassName]: newDescription.trim() || newClassName
        });
        setNewClassName('');
        setNewDescription('');
        setError('');
    };

    const handleDeleteClass = (className: string) => {
        const updated = { ...localOntology };
        delete updated[className];
        setLocalOntology(updated);
    };

    const handleSave = () => {
        onChange(localOntology);
        onClose();
    };

    const handleExport = () => {
        const blob = new Blob([JSON.stringify(localOntology, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ontology.json';
        a.click();
        URL.revokeObjectURL(url);
    };

    const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    const imported = JSON.parse(event.target?.result as string);
                    setLocalOntology(imported);
                } catch (err) {
                    setError('Invalid JSON file');
                }
            };
            reader.readAsText(file);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-gray-900 rounded-xl border border-gray-700 w-full max-w-2xl max-h-[80vh] flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-gray-700">
                    <h2 className="text-xl font-semibold text-white">Caption Ontology Editor</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-white">
                        <X size={24} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {/* Add New Class */}
                    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                        <h3 className="text-sm font-semibold text-gray-300 mb-3">Add New Class</h3>
                        <div className="space-y-3">
                            <div>
                                <label className="block text-xs text-gray-400 mb-1">Class Name *</label>
                                <input
                                    type="text"
                                    value={newClassName}
                                    onChange={(e) => setNewClassName(e.target.value)}
                                    placeholder="e.g., cat, dog, person"
                                    className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
                                />
                            </div>
                            <div>
                                <label className="block text-xs text-gray-400 mb-1">Description</label>
                                <textarea
                                    value={newDescription}
                                    onChange={(e) => setNewDescription(e.target.value)}
                                    placeholder="e.g., a small feline animal"
                                    className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm h-20 resize-none focus:outline-none focus:border-blue-500"
                                />
                            </div>
                            {error && <p className="text-red-400 text-xs">{error}</p>}
                            <button
                                onClick={handleAddClass}
                                className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white py-2 rounded-lg text-sm font-medium"
                            >
                                <Plus size={16} />
                                Add Class
                            </button>
                        </div>
                    </div>

                    {/* Existing Classes */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-semibold text-gray-300">
                            Defined Classes ({Object.keys(localOntology).length})
                        </h3>
                        {Object.entries(localOntology).map(([className, description]) => (
                            <div
                                key={className}
                                className="flex items-start justify-between bg-gray-800 p-3 rounded-lg border border-gray-700"
                            >
                                <div className="flex-1">
                                    <p className="font-medium text-white">{className}</p>
                                    <p className="text-sm text-gray-400 mt-1">{description}</p>
                                </div>
                                <button
                                    onClick={() => handleDeleteClass(className)}
                                    className="text-red-400 hover:text-red-300 ml-3"
                                >
                                    <X size={18} />
                                </button>
                            </div>
                        ))}
                        {Object.keys(localOntology).length === 0 && (
                            <p className="text-gray-500 text-sm text-center py-4">
                                No classes defined yet. Add one above.
                            </p>
                        )}
                    </div>
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-gray-700 flex items-center justify-between">
                    <div className="flex gap-2">
                        <label className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-2 rounded-lg text-sm cursor-pointer">
                            <FileJson size={16} />
                            Import JSON
                            <input
                                type="file"
                                accept=".json"
                                onChange={handleImport}
                                className="hidden"
                            />
                        </label>
                        <button
                            onClick={handleExport}
                            className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-2 rounded-lg text-sm"
                        >
                            <FileJson size={16} />
                            Export JSON
                        </button>
                    </div>
                    <button
                        onClick={handleSave}
                        className="flex items-center gap-2 bg-green-600 hover:bg-green-500 text-white px-4 py-2 rounded-lg font-medium"
                    >
                        <Save size={18} />
                        Save Changes
                    </button>
                </div>
            </div>
        </div>
    );
};
