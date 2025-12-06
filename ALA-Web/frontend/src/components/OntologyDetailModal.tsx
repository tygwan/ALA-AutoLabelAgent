import React, { useState, useEffect } from 'react';
import { X, ArrowRight } from 'lucide-react';
import { useOntologies } from '../hooks/useOntologies';

interface OntologyDetailModalProps {
    ontologyId: string;
    isOpen: boolean;
    onClose: () => void;
    onLoad: (classes: Record<string, string>) => void;
    onDelete: () => Promise<void>;
}

export const OntologyDetailModal: React.FC<OntologyDetailModalProps> = ({
    ontologyId,
    isOpen,
    onClose,
    onLoad,
    onDelete
}) => {
    const { getOntology } = useOntologies();
    const [ontology, setOntology] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (isOpen && ontologyId) {
            loadOntology();
        }
    }, [isOpen, ontologyId]);

    const loadOntology = async () => {
        setLoading(true);
        const data = await getOntology(ontologyId);
        setOntology(data);
        setLoading(false);
    };

    const handleLoadIntoEditor = () => {
        if (ontology) {
            onLoad(ontology.classes);
            onClose();
        }
    };

    const handleDelete = async () => {
        if (confirm(`Are you sure you want to delete "${ontology?.name}"?`)) {
            await onDelete();
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-[60]">
            <div className="bg-gray-900 rounded-lg shadow-xl w-full max-w-3xl max-h-[80vh] flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-gray-800">
                    <div>
                        <h2 className="text-lg font-semibold text-white">
                            {loading ? 'Loading...' : ontology?.name}
                        </h2>
                        {!loading && ontology?.description && (
                            <p className="text-sm text-gray-400 mt-1">{ontology.description}</p>
                        )}
                    </div>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-white transition-colors"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-4">
                    {loading ? (
                        <div className="flex items-center justify-center h-32 text-gray-500">
                            Loading details...
                        </div>
                    ) : ontology ? (
                        <div>
                            <div className="mb-4">
                                <h3 className="text-sm font-medium text-gray-400 mb-2">
                                    Classes ({ontology.class_count})
                                </h3>
                                <div className="bg-gray-800 rounded-lg p-4 space-y-2">
                                    {Object.entries(ontology.classes).map(([prompt, className]) => (
                                        <div
                                            key={prompt}
                                            className="flex items-center gap-2 text-sm py-2 border-b border-gray-700 last:border-0"
                                        >
                                            <span className="text-blue-400 font-mono">{prompt}</span>
                                            <ArrowRight size={14} className="text-gray-600" />
                                            <span className="text-green-400 font-mono">{className}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="text-xs text-gray-500">
                                Created: {new Date(ontology.created_at).toLocaleString()}
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center justify-center h-32 text-gray-500">
                            Failed to load ontology
                        </div>
                    )}
                </div>

                {/* Footer */}
                {!loading && ontology && (
                    <div className="flex items-center justify-between gap-3 p-4 border-t border-gray-800">
                        <button
                            onClick={handleDelete}
                            className="px-4 py-2 bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white rounded-lg font-medium transition-colors"
                        >
                            Delete
                        </button>
                        <button
                            onClick={handleLoadIntoEditor}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors"
                        >
                            Load into Editor
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};
