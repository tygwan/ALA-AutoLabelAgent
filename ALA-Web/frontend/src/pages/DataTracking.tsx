import React from 'react';
import { Activity, CheckCircle, Clock, XCircle, AlertCircle, ArrowRight } from 'lucide-react';
import { useTracking } from '../hooks/useTracking';

export const DataTracking: React.FC = () => {
    const { pipelineStatus, errors, loading, fetchPipelineStatus, retryFailed } = useTracking();

    const handleRetryAll = async () => {
        if (!confirm(`Retry all ${errors.length} failed images?`)) return;

        for (const error of errors) {
            try {
                await retryFailed(error.image_id);
            } catch (err) {
                console.error(`Failed to retry ${error.image_id}:`, err);
            }
        }
    };

    return (
        <div className="h-full bg-gray-950 overflow-y-auto">
            <div className="p-8">
                {/* Header */}
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-white mb-2">Data Flow Tracking</h2>
                    <p className="text-gray-400">Monitor images through the processing pipeline</p>
                </div>

                {loading && !pipelineStatus && (
                    <div className="text-center text-gray-400 py-20">Loading pipeline status...</div>
                )}

                {pipelineStatus && (
                    <>
                        {/* Pipeline Overview */}
                        <div className="bg-gray-900 rounded-lg p-6 mb-6 border border-gray-700">
                            <h3 className="text-lg font-semibold text-white mb-6">Pipeline Overview</h3>

                            <div className="flex items-center justify-between">
                                <StageCard
                                    label="Uploaded"
                                    count={pipelineStatus.stages.uploaded}
                                    icon={CheckCircle}
                                    color="blue"
                                />
                                <ArrowRight className="text-gray-600" size={24} />

                                <StageCard
                                    label="Annotated"
                                    count={pipelineStatus.stages.annotated}
                                    icon={CheckCircle}
                                    color="green"
                                />
                                <ArrowRight className="text-gray-600" size={24} />

                                <StageCard
                                    label="Preprocessed"
                                    count={pipelineStatus.stages.preprocessed}
                                    icon={Clock}
                                    color="yellow"
                                />
                                <ArrowRight className="text-gray-600" size={24} />

                                <StageCard
                                    label="Classified"
                                    count={pipelineStatus.stages.classified}
                                    icon={Activity}
                                    color="purple"
                                />
                            </div>

                            <div className="mt-6 pt-6 border-t border-gray-700">
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-gray-400">Total Images:</span>
                                    <span className="text-white font-semibold">{pipelineStatus.total_images}</span>
                                </div>
                            </div>
                        </div>

                        {/* Errors Section */}
                        {errors.length > 0 && (
                            <div className="bg-red-900/20 border border-red-700 rounded-lg p-6">
                                <div className="flex items-center justify-between mb-4">
                                    <h3 className="text-lg font-semibold text-red-400 flex items-center gap-2">
                                        <AlertCircle size={20} />
                                        Errors ({errors.length})
                                    </h3>
                                    <button
                                        onClick={handleRetryAll}
                                        className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-sm"
                                    >
                                        Retry All
                                    </button>
                                </div>

                                <div className="space-y-3">
                                    {errors.map((error, index) => (
                                        <div key={index} className="bg-gray-900 rounded p-3 border border-red-800">
                                            <div className="flex items-start justify-between">
                                                <div className="flex-1">
                                                    <div className="font-medium text-white">{error.filename}</div>
                                                    <div className="text-sm text-gray-400 mt-1">
                                                        Stage: {error.current_stage}
                                                    </div>
                                                    {error.errors && error.errors.length > 0 && (
                                                        <div className="text-xs text-red-400 mt-2">
                                                            {error.errors[0].error}
                                                        </div>
                                                    )}
                                                </div>
                                                <button
                                                    onClick={() => retryFailed(error.image_id)}
                                                    className="px-3 py-1 bg-red-700 hover:bg-red-600 text-white rounded text-sm"
                                                >
                                                    Retry
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {errors.length === 0 && (
                            <div className="bg-green-900/20 border border-green-700 rounded-lg p-6 text-center">
                                <CheckCircle className="mx-auto mb-2 text-green-500" size={48} />
                                <p className="text-green-400 font-medium">No errors detected</p>
                                <p className="text-gray-400 text-sm mt-1">All images are processing smoothly</p>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

// ============================================================================
// Stage Card Component
// ============================================================================

interface StageCardProps {
    label: string;
    count: number;
    icon: any;
    color: 'blue' | 'green' | 'yellow' | 'purple';
}

const StageCard: React.FC<StageCardProps> = ({ label, count, icon: Icon, color }) => {
    const colorClasses = {
        blue: 'bg-blue-900/30 border-blue-700 text-blue-400',
        green: 'bg-green-900/30 border-green-700 text-green-400',
        yellow: 'bg-yellow-900/30 border-yellow-700 text-yellow-400',
        purple: 'bg-purple-900/30 border-purple-700 text-purple-400',
    };

    return (
        <div className={`flex-1 border rounded-lg p-4 ${colorClasses[color]}`}>
            <div className="flex items-center gap-3 mb-2">
                <Icon size={20} />
                <span className="font-medium">{label}</span>
            </div>
            <div className="text-3xl font-bold text-white">{count}</div>
        </div>
    );
};
