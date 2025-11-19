import React from 'react';

export const Settings: React.FC = () => {
    return (
        <div className="p-8 h-full bg-gray-950 text-white">
            <h2 className="text-2xl font-bold mb-6">Settings</h2>

            <div className="space-y-6 max-w-2xl">
                <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
                    <h3 className="text-lg font-semibold mb-4">Model Configuration</h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Default VLM Model</label>
                            <select className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
                                <option>Florence-2-large</option>
                                <option>Florence-2-base</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Default Segmentation Model</label>
                            <select className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
                                <option>SAM2 Base+</option>
                                <option>SAM2 Large</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
                    <h3 className="text-lg font-semibold mb-4">Appearance</h3>
                    <div className="flex items-center justify-between">
                        <span className="text-gray-300">Dark Mode</span>
                        <div className="w-12 h-6 bg-blue-600 rounded-full relative cursor-pointer">
                            <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
