import { FolderOpen, Plus, ChevronDown } from 'lucide-react';
import { useState } from 'react';

interface Project {
    project_id: string;
    name: string;
    display_name: string;
    file_count: number;
}

interface ProjectSelectorProps {
    projects: Project[];
    selectedProject: Project | null;
    onSelectProject: (project: Project) => void;
    onCreateNew: () => void;
}

export const ProjectSelector = ({
    projects,
    selectedProject,
    onSelectProject,
    onCreateNew
}: ProjectSelectorProps) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="relative">
            <label className="block text-xs text-gray-400 mb-1">Project</label>

            {/* Selector Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between px-3 py-2 bg-gray-900 border border-gray-600 rounded text-white hover:border-blue-500 transition-colors"
            >
                <div className="flex items-center gap-2">
                    <FolderOpen size={16} className="text-blue-400" />
                    <span className="text-sm">
                        {selectedProject ? selectedProject.display_name : 'Select Project'}
                    </span>
                    {selectedProject && (
                        <span className="text-xs text-gray-500">
                            ({selectedProject.file_count} files)
                        </span>
                    )}
                </div>
                <ChevronDown size={16} className={`text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown */}
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <div
                        className="fixed inset-0 z-10"
                        onClick={() => setIsOpen(false)}
                    />

                    {/* Menu */}
                    <div className="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-600 rounded shadow-lg z-20 max-h-64 overflow-y-auto">
                        {/* Create New Button */}
                        <button
                            onClick={() => {
                                onCreateNew();
                                setIsOpen(false);
                            }}
                            className="w-full flex items-center gap-2 px-3 py-2 hover:bg-gray-700 text-blue-400 border-b border-gray-700 transition-colors"
                                </button>
                    ))
                        )}
                </div>
        </>
    )
}
        </div >
    );
};
