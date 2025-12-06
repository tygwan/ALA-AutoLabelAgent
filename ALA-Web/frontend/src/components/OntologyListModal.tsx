import React, { useState } from 'react';
import { X, Calendar, Hash } from 'lucide-react';
import { useOntologies } from '../hooks/useOntologies';
import { OntologyDetailModal } from './OntologyDetailModal';

interface OntologyListModalProps {
    isOpen: boolean;
    onClose: () => void;
    onLoad: (classes: Record<string, string>) => void;
}

export const OntologyListModal: React.FC<OntologyListModalProps> = ({
    isOpen,
    onClose,
    onLoad
}) => {
    const { ontologies, loading, deleteOntology, getOntology } = useOntologies();
    const [selectedOntologyId, setSelectedOntologyId] = useState<string | null>(null);
    const [showDetailModal, setShowDetailModal] = useState(false);

    if (!isOpen) return null;

    const handleOntologyClick = (ontologyId: string) => {
        setSelectedOntologyId(ontologyId);
        setShowDetailModal(true);
    };

    const handleLoadOntology = async (ontologyId: string) => {
        const ontology = await getOntology(ontologyId);
        if (ontology) {
            onLoad(ontology.classes);
            onClose();
        }
    };

    const handleDelete = async (ontologyId: string, e: React.MouseEvent) => {
        e.stopPropagation();
        if (confirm('Are you sure you want to delete this ontology?')) {
            await deleteOntology(ontologyId);
        }
    };

    const formatDate = (isoString: string) => {
        const date = new Date(isoString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    };

    return (
        <>
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                <div className="bg-gray-900 rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col">
                    {/* Header */}
                    <div className="flex items-center justify-between p-4 border-b border-gray-800">
                        <h2 className="text-lg font-semibold text-white">Saved Ontologies</h2>
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
                                Loading ontologies...
                            </div>
                        ) : ontologies.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-32 text-gray-500 text-center">
                                <p className="text-sm">No saved ontologies yet</p>
                                <p className="text-xs mt-2">Create and save an ontology to see it here</p>
                            </div>
                        ) : (
                            <div className="space-y-2">
                                {ontologies.map((ontology) => (
                                    <div
                                        key={ontology.ontology_id}
                                        onClick={() => handleOntologyClick(ontology.ontology_id)}
                                        className="bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-gray-600 rounded-lg p-4 cursor-pointer transition-all group"
                                    >
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <h3 className="font-medium text-white group-hover:text-blue-400 transition-colors">
                                                    {ontology.name}
                                                </h3>
                                                {ontology.description && (
                                                    <p className="text-sm text-gray-400 mt-1">
                                                        {ontology.description}
                                                    </p>
                                                )}
                                                <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                                                    <span className="flex items-center gap-1">
                                                        <Hash size={12} />
                                                        {ontology.class_count} classes
                                                    </span>
                                                    <span className="flex items-center gap-1">
                                                        <Calendar size={12} />
                                                        {formatDate(ontology.created_at)}
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="flex gap-2">
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleLoadOntology(ontology.ontology_id);
                                                    }}
                                                    className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded font-medium transition-colors"
                                                >
                                                    Load
                                                </button>
                                                <button
                                                    onClick={(e) => handleDelete(ontology.ontology_id, e)}
                                                    className="px-3 py-1.5 bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white text-xs rounded font-medium transition-colors"
                                                >
                                                    Delete
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Detail Modal */}
            {showDetailModal && selectedOntologyId && (
                <OntologyDetailModal
                    ontologyId={selectedOntologyId}
                    isOpen={showDetailModal}
                    onClose={() => {
                        setShowDetailModal(false);
                        setSelectedOntologyId(null);
                    }}
                    onLoad={onLoad}
                    onDelete={async () => {
                        await deleteOntology(selectedOntologyId);
                        setShowDetailModal(false);
                        setSelectedOntologyId(null);
                    }}
                />
            )}
        </>
    );
};
