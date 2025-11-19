import React, { useState } from 'react';
import { Play, Settings as SettingsIcon, Download } from 'lucide-react';

interface PreprocessingProps {
    // This page will display annotated images and allow preprocessing
}

export const Preprocessing: React.FC<PreprocessingProps> = () => {
    const [targetWidth, setTargetWidth] = useState(640);
    const [targetHeight, setTargetHeight] = useState(480);
    const [bgMode, setBgMode] = useState<string>('black');
    const [padding, setPadding] = useState(0);
    const [processing, setProcessing] = useState(false);

    const bgModeOptions = [
        { value: 'black', label: 'Black Background' },
        { value: 'white', label: 'White Background' },
        { value: 'gray', label: 'Gray Background' },
        { value: 'transparent', label: 'Transparent (PNG)' },
        { value: 'blur', label: 'Blur Background' },
        { value: 'mean', label: 'Mean Color Background' },
    ];

    const handleBatchProcess = async () => {
        setProcessing(true);
        // TODO: Implement batch processing
        console.log('Batch processing with:', { targetWidth, targetHeight, bgMode, padding });
        setTimeout(() => setProcessing(false), 2000);
    };

    return (
        <div className="flex h-full bg-gray-950">
            {/* Left: Options Panel */}
            <div className="w-80 bg-gray-900 border-r border-gray-700 p-6 overflow-y-auto">
                <h2 className="text-xl font-bold text-white mb-6">Preprocessing Options</h2>

                {/* Output Size */}
                <div className="space-y-4 mb-6">
                    <h3 className="text-sm font-semibold text-gray-300">Output Size</h3>
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="block text-xs text-gray-400 mb-1">Width (px)</label>
                            <input
                                type="number"
                                value={targetWidth}
                                onChange={(e) => setTargetWidth(parseInt(e.target.value) || 640)}
                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                            />
                        </div>
                        <div>
                            <label className="block text-xs text-gray-400 mb-1">Height (px)</label>
                            <input
                                type="number"
                                value={targetHeight}
                                onChange={(e) => setTargetHeight(parseInt(e.target.value) || 480)}
                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                            />
                        </div>
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={() => { setTargetWidth(640); setTargetHeight(480); }}
                            className="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg text-xs"
                        >
                            640×480
                        </button>
                        <button
                            onClick={() => { setTargetWidth(224); setTargetHeight(224); }}
                            className="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg text-xs"
                        >
                            224×224
                        </button>
                    </div>
                </div>

                {/* Background Mode */}
                <div className="space-y-4 mb-6">
                    <h3 className="text-sm font-semibold text-gray-300">Background Removal</h3>
                    <select
                        value={bgMode}
                        onChange={(e) => setBgMode(e.target.value)}
                        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                    >
                        {bgModeOptions.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                    <p className="text-xs text-gray-500">
                        Choose how to handle the background in preprocessed images
                    </p>
                </div>

                {/* Padding */}
                <div className="space-y-4 mb-6">
                    <h3 className="text-sm font-semibold text-gray-300">Box Padding</h3>
                    <input
                        type="range"
                        min="0"
                        max="50"
                        value={padding}
                        onChange={(e) => setPadding(parseInt(e.target.value))}
                        className="w-full"
                    />
                    <p className="text-xs text-gray-400">{padding} pixels</p>
                </div>

                {/* Batch Process Button */}
                <button
                    onClick={handleBatchProcess}
                    disabled={processing}
                    className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white px-4 py-3 rounded-lg font-medium"
                >
                    {processing ? (
                        <>Processing...</>
                    ) : (
                        <>
                            <Play size={18} />
                            Batch Process
                        </>
                    )}
                </button>

                <div className="mt-6 p-4 bg-gray-800 rounded-lg border border-gray-700">
                    <h4 className="text-xs font-semibold text-gray-400 mb-2">Processing Pipeline</h4>
                    <ol className="text-xs text-gray-500 space-y-1 list-decimal list-inside">
                        <li>Apply mask (if available)</li>
                        <li>Remove background ({bgMode})</li>
                        <li>Crop by bounding box</li>
                        <li>Resize to {targetWidth}×{targetHeight}</li>
                    </ol>
                </div>
            </div>

            {/* Right: Preview Area */}
            <div className="flex-1 p-8 overflow-y-auto">
                <div className="mb-6 flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-white">Annotated Images</h2>
                    <span className="text-gray-500 text-sm">0 images ready for preprocessing</span>
                </div>

                {/* Placeholder for annotated images grid */}
                <div className="text-gray-500 text-center py-20">
                    <SettingsIcon className="mx-auto mb-4 text-gray-600" size={64} />
                    <p className="text-lg mb-2">No annotated images yet</p>
                    <p className="text-sm">
                        Run annotation on your uploaded images first to see them here
                    </p>
                </div>

                {/* This will be replaced with actual annotated images grid */}
            </div>
        </div>
    );
};
