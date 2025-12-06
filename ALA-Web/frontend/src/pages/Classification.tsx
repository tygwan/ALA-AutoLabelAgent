import React, { useState } from 'react';
import { Beaker, Database, BarChart3, Plus, Trash2, Play, ArrowUpDown } from 'lucide-react';
import { useExperiments, useSupportSets, useQuerySets } from '../hooks/useClassification';

type TabType = 'experiments' | 'support-sets' | 'comparison';

export const Classification: React.FC = () => {
    const [activeTab, setActiveTab] = useState<TabType>('experiments');
    const [selectedExperiments, setSelectedExperiments] = useState<string[]>([]);

    const tabs = [
        { id: 'experiments' as TabType, label: 'Experiments', icon: Beaker },
        { id: 'support-sets' as TabType, label: 'Support Sets', icon: Database },
        { id: 'comparison' as TabType, label: 'Comparison', icon: BarChart3 },
    ];

    return (
        <div className="flex h-full bg-gray-950">
            {/* Left Sidebar - Tabs */}
            <div className="w-64 bg-gray-900 border-r border-gray-700 flex flex-col">
                <div className="p-4 border-b border-gray-700">
                    <h2 className="text-xl font-bold text-white">Classification</h2>
                    <p className="text-xs text-gray-400 mt-1">Experiment Management</p>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    {tabs.map((tab) => {
                        const Icon = tab.icon;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`flex items-center gap-3 px-3 py-2 rounded-lg w-full text-left transition-colors ${activeTab === tab.id
                                        ? 'bg-blue-600 text-white'
                                        : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                                    }`}
                            >
                                <Icon size={20} />
                                <span>{tab.label}</span>
                            </button>
                        );
                    })}
                </nav>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-hidden">
                {activeTab === 'experiments' && (
                    <ExperimentsTab
                        selectedExperiments={selectedExperiments}
                        setSelectedExperiments={setSelectedExperiments}
                    />
                )}
                {activeTab === 'support-sets' && <SupportSetsTab />}
                {activeTab === 'comparison' && (
                    <ComparisonTab selectedExperiments={selectedExperiments} />
                )}
            </div>
        </div>
    );
};

// ============================================================================
// Experiments Tab
// ============================================================================

interface ExperimentsTabProps {
    selectedExperiments: string[];
    setSelectedExperiments: (ids: string[]) => void;
}

const ExperimentsTab: React.FC<ExperimentsTabProps> = ({
    selectedExperiments,
    setSelectedExperiments
}) => {
    const { experiments, loading, error, createExperiment, deleteExperiment, runExperiment } = useExperiments();
    const { supportSets } = useSupportSets();
    const { querySets } = useQuerySets();
    const [showCreateModal, setShowCreateModal] = useState(false);

    const toggleExperimentSelection = (expId: string) => {
        if (selectedExperiments.includes(expId)) {
            setSelectedExperiments(selectedExperiments.filter(id => id !== expId));
        } else {
            setSelectedExperiments([...selectedExperiments, expId]);
        }
    };

    const handleDeleteSelected = async () => {
        if (selectedExperiments.length === 0) return;
        if (!confirm(`Delete ${selectedExperiments.length} experiment(s)?`)) return;

        for (const expId of selectedExperiments) {
            try {
                await deleteExperiment(expId);
            } catch (err) {
                console.error(`Failed to delete ${expId}:`, err);
            }
        }
        setSelectedExperiments([]);
    };

    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="bg-gray-900 border-b border-gray-700 p-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="text-2xl font-bold text-white">Experiments</h3>
                        <p className="text-sm text-gray-400 mt-1">
                            {experiments.length} total
                            {selectedExperiments.length > 0 && ` • ${selectedExperiments.length} selected`}
                        </p>
                    </div>
                    <div className="flex gap-2">
                        {selectedExperiments.length > 0 && (
                            <button
                                onClick={handleDeleteSelected}
                                className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg"
                            >
                                <Trash2 size={18} />
                                Delete Selected
                            </button>
                        )}
                        <button
                            onClick={() => setShowCreateModal(true)}
                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg"
                        >
                            <Plus size={18} />
                            New Experiment
                        </button>
                    </div>
                </div>
            </div>

            {/* Experiments List */}
            <div className="flex-1 overflow-y-auto p-6">
                {loading && (
                    <div className="text-center text-gray-400 py-20">Loading experiments...</div>
                )}

                {error && (
                    <div className="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg">
                        {error}
                    </div>
                )}

                {!loading && !error && experiments.length === 0 && (
                    <div className="text-center text-gray-500 py-20">
                        <Beaker size={64} className="mx-auto mb-4 text-gray-600" />
                        <p className="text-lg mb-2">No experiments yet</p>
                        <p className="text-sm">Create your first experiment to get started</p>
                    </div>
                )}

                <div className="space-y-4">
                    {experiments.map((exp) => (
                        <ExperimentCard
                            key={exp.experiment_id}
                            experiment={exp}
                            isSelected={selectedExperiments.includes(exp.experiment_id)}
                            onToggleSelect={() => toggleExperimentSelection(exp.experiment_id)}
                            onDelete={() => deleteExperiment(exp.experiment_id)}
                            onRun={() => runExperiment(exp.experiment_id)}
                        />
                    ))}
                </div>
            </div>

            {/* Create Experiment Modal */}
            {showCreateModal && (
                <CreateExperimentModal
                    supportSets={supportSets}
                    querySets={querySets}
                    onCreate={createExperiment}
                    onClose={() => setShowCreateModal(false)}
                />
            )}
        </div>
    );
};

// ============================================================================
// Experiment Card Component
// ============================================================================

interface ExperimentCardProps {
    experiment: any;
    isSelected: boolean;
    onToggleSelect: () => void;
    onDelete: () => void;
    onRun: () => void;
}

const ExperimentCard: React.FC<ExperimentCardProps> = ({
    experiment,
    isSelected,
    onToggleSelect,
    onDelete,
    onRun,
}) => {
    const statusColors = {
        created: 'bg-gray-700 text-gray-300',
        running: 'bg-yellow-700 text-yellow-300',
        completed: 'bg-green-700 text-green-300',
        failed: 'bg-red-700 text-red-300',
    };

    return (
        <div
            className={`bg-gray-800 border rounded-lg p-4 transition-all ${isSelected ? 'border-blue-500 ring-2 ring-blue-500/50' : 'border-gray-700'
                }`}
        >
            <div className="flex items-start gap-4">
                {/* Checkbox */}
                <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={onToggleSelect}
                    className="mt-1 w-4 h-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500"
                />

                {/* Content */}
                <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                        <div>
                            <h4 className="text-lg font-semibold text-white">{experiment.name}</h4>
                            <p className="text-sm text-gray-400">{experiment.experiment_id}</p>
                        </div>
                        <span
                            className={`px-2 py-1 rounded text-xs font-medium ${statusColors[experiment.status as keyof typeof statusColors]
                                }`}
                        >
                            {experiment.status}
                        </span>
                    </div>

                    <div className="grid grid-cols-2 gap-3 text-sm mb-3">
                        <div>
                            <span className="text-gray-500">Support Set:</span>{' '}
                            <span className="text-gray-300">{experiment.support_set_id}</span>
                        </div>
                        <div>
                            <span className="text-gray-500">Query Set:</span>{' '}
                            <span className="text-gray-300">{experiment.query_set_id}</span>
                        </div>
                    </div>

                    {experiment.parent_experiment && (
                        <div className="text-xs text-gray-500 mb-3">
                            📝 Revision of: {experiment.parent_experiment}
                        </div>
                    )}

                    <div className="text-xs text-gray-500">
                        Created: {new Date(experiment.created_at).toLocaleString()}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 mt-3">
                        {experiment.status === 'created' && (
                            <button
                                onClick={onRun}
                                className="flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-sm rounded"
                            >
                                <Play size={14} />
                                Run
                            </button>
                        )}
                        <button
                            onClick={() => {/* View details */ }}
                            className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded"
                        >
                            View Results
                        </button>
                        <button
                            onClick={onDelete}
                            className="px-3 py-1.5 bg-red-700 hover:bg-red-600 text-white text-sm rounded ml-auto"
                        >
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

// ============================================================================
// Support Sets Tab (Placeholder)
// ============================================================================

const SupportSetsTab: React.FC = () => {
    const { supportSets, loading } = useSupportSets();

    return (
        <div className="h-full flex flex-col p-6">
            <h3 className="text-2xl font-bold text-white mb-4">Support Sets</h3>
            {loading ? (
                <div className="text-gray-400">Loading support sets...</div>
            ) : (
                <div className="text-gray-400">
                    {supportSets.length} support set(s) available
                    <div className="mt-4 text-sm text-gray-500">
                        Support set management UI coming in Phase 5...
                    </div>
                </div>
            )}
        </div>
    );
};

// ============================================================================
// Comparison Tab (Placeholder)
// ============================================================================

interface ComparisonTabProps {
    selectedExperiments: string[];
}

const ComparisonTab: React.FC<ComparisonTabProps> = ({ selectedExperiments }) => {
    return (
        <div className="h-full flex flex-col p-6">
            <h3 className="text-2xl font-bold text-white mb-4">Experiment Comparison</h3>
            {selectedExperiments.length < 2 ? (
                <div className="text-gray-400">
                    Select at least 2 experiments from the Experiments tab to compare
                </div>
            ) : (
                <div className="text-gray-400">
                    Comparing {selectedExperiments.length} experiments
                    <div className="mt-4 text-sm text-gray-500">
                        Comparison UI coming in Phase 6...
                    </div>
                </div>
            )}
        </div>
    );
};

// ============================================================================
// Create Experiment Modal
// ============================================================================

interface CreateExperimentModalProps {
    supportSets: any[];
    querySets: any[];
    onCreate: (data: any) => Promise<any>;
    onClose: () => void;
}

const CreateExperimentModal: React.FC<CreateExperimentModalProps> = ({
    supportSets,
    querySets,
    onCreate,
    onClose,
}) => {
    const [formData, setFormData] = useState({
        name: '',
        support_set_id: '',
        query_set_id: '',
        method: 'cosine_similarity',
        threshold: 0.7,
        notes: '',
    });
    const [creating, setCreating] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setCreating(true);
        try {
            await onCreate(formData);
            onClose();
        } catch (err) {
            console.error('Failed to create experiment:', err);
        } finally {
            setCreating(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md border border-gray-700">
                <h3 className="text-xl font-bold text-white mb-4">Create New Experiment</h3>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm text-gray-300 mb-1">Experiment Name</label>
                        <input
                            type="text"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                            placeholder="e.g., Cat vs Dog Baseline"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm text-gray-300 mb-1">Support Set</label>
                        <select
                            value={formData.support_set_id}
                            onChange={(e) => setFormData({ ...formData, support_set_id: e.target.value })}
                            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                            required
                        >
                            <option value="">Select support set...</option>
                            {supportSets.map((set) => (
                                <option key={set.id} value={set.id}>
                                    {set.name} ({set.images_count} images)
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm text-gray-300 mb-1">Query Set</label>
                        <select
                            value={formData.query_set_id}
                            onChange={(e) => setFormData({ ...formData, query_set_id: e.target.value })}
                            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                            required
                        >
                            <option value="">Select query set...</option>
                            {querySets.map((set) => (
                                <option key={set.id} value={set.id}>
                                    {set.name} ({set.images_count} images)
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm text-gray-300 mb-1">Notes (Optional)</label>
                        <textarea
                            value={formData.notes}
                            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                            rows={2}
                            placeholder="Add any notes about this experiment..."
                        />
                    </div>

                    <div className="flex gap-2 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={creating}
                            className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg"
                        >
                            {creating ? 'Creating...' : 'Create Experiment'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
