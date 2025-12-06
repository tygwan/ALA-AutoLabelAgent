import React, { useState, useEffect } from 'react';
import { Play, Square, Edit2 } from 'lucide-react';
import { OntologyEditor } from './OntologyEditor';

interface AnnotationSidebarProps {
    onRun: (params: AnnotationParams) => void;
    onCancel: () => void;
    isProcessing: boolean;
    progress: number;
    statusMessage: string;
    initialOntology?: Record<string, string>;
}

export interface AnnotationParams {
    vlmModel: string;
    segModel: string;
    ontology: Record<string, string>;
}

export const AnnotationSidebar: React.FC<AnnotationSidebarProps> = ({
    onRun,
    onCancel,
    isProcessing,
    progress,
    statusMessage,
    initialOntology = {}
}) => {
    const [vlmModel, setVlmModel] = useState('florence-2-base');
    const [segModel, setSegModel] = useState('sam2-base');
    const [ontology, setOntology] = useState<Record<string, string>>(initialOntology);
    const [showOntologyEditor, setShowOntologyEditor] = useState(false);

    // Auto-load ontology when project changes
    useEffect(() => {
        if (initialOntology && Object.keys(initialOntology).length > 0) {
            setOntology(initialOntology);
            console.log('Loaded caption ontology from project:', initialOntology);
        }
    }, [initialOntology]);

    const handleRun = () => {
        if (Object.keys(ontology).length === 0) {
            alert('Please define at least one class in the ontology');
            return;
        }
        onRun({ vlmModel, segModel, ontology });
    };

    return (
        <>
            <div className="w-80 bg-gray-800 border-r border-gray-700 flex flex-col h-full">
                <div className="p-4 border-b border-gray-700">
                    <h2 className="text-lg font-semibold text-white">Auto-Annotation</h2>
                </div>

                <div className="p-4 space-y-6 flex-1 overflow-y-auto">
                    {/* VLM Model */}
                    <div className="space-y-2">
                        <label className="text-sm text-gray-400 font-medium">VLM Model</label>
                        <select
                            value={vlmModel}
                            onChange={(e) => setVlmModel(e.target.value)}
                            disabled={isProcessing}
                            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 disabled:opacity-50"
                        >
                            <option value="florence-2-large">Florence-2 Large</option>
                            <option value="florence-2-base">Florence-2 Base</option>
                        </select>
                    </div>

                    {/* Segmentation Model */}
                    <div className="space-y-2">
                        <label className="text-sm text-gray-400 font-medium">Segmentation Model</label>
                        <select
                            value={segModel}
                            onChange={(e) => setSegModel(e.target.value)}
                            disabled={isProcessing}
                            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 disabled:opacity-50"
                        >
                            <option value="sam2-base">SAM2 Base+</option>
                            <option value="sam2-large">SAM2 Large</option>
                            <option value="none">None (Boxes Only)</option>
                        </select>
                    </div>

                    {/* Caption Ontology */}
                    <div className="space-y-2">
                        <div className="flex items-center justify-between">
                            <label className="text-sm text-gray-400 font-medium">Caption Ontology</label>
                            <button
                                onClick={() => setShowOntologyEditor(true)}
                                disabled={isProcessing}
                                className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 disabled:opacity-50"
                            >
                                <Edit2 size={14} />
                                Edit
                            </button>
                        </div>
                        <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 min-h-[100px] max-h-[200px] overflow-y-auto">
                            {Object.keys(ontology).length === 0 ? (
                                <p className="text-gray-500 text-sm">No classes defined. Click Edit to add.</p>
                            ) : (
                                <div className="space-y-2">
                                    {Object.entries(ontology).map(([className, description]) => (
                                        <div key={className} className="text-sm">
                                            <span className="text-blue-400 font-medium">{className}</span>
                                            <span className="text-gray-600 mx-1">:</span>
                                            <span className="text-gray-400">{description}</span>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Progress */}
                    {isProcessing && (
                        <div className="space-y-2 bg-gray-900 p-3 rounded-lg border border-gray-700">
                            <div className="flex justify-between text-xs text-gray-400">
                                <span>Progress</span>
                                <span>{progress}%</span>
                            </div>
                            <div className="w-full bg-gray-800 rounded-full h-2">
                                <div
                                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                                    style={{ width: `${progress}%` }}
                                />
                            </div>
                            <p className="text-xs text-gray-500 truncate">{statusMessage}</p>
                        </div>
                    )}
                </div>

                {/* Actions */}
                <div className="p-4 border-t border-gray-700 space-y-3">
                    {!isProcessing ? (
                        <button
                            onClick={handleRun}
                            disabled={Object.keys(ontology).length === 0}
                            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white py-2.5 rounded-lg font-medium transition-colors"
                        >
                            <Play size={18} />
                            Run Annotation
                        </button>
                    ) : (
                        <button
                            onClick={onCancel}
                            className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-500 text-white py-2.5 rounded-lg font-medium transition-colors"
                        >
                            <Square size={18} />
                            Cancel
                        </button>
                    )}
                </div>
            </div>

            {/* Ontology Editor Modal */}
            {showOntologyEditor && (
                <OntologyEditor
                    ontology={ontology}
                    onChange={setOntology}
                    onClose={() => setShowOntologyEditor(false)}
                />
            )}
        </>
    );
};
