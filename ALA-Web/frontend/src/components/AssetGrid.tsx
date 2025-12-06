import React, { useState, useRef } from 'react';
import { Upload, FolderOpen, FileImage, CheckCircle2, Circle } from 'lucide-react';
import { useUploads } from '../hooks/useUploads';
import { ProjectModal } from './ProjectModal';

interface AssetGridProps {
    onSelectFile: (fileId: string, fileType: 'image' | 'video') => void;
    selectedProject: any;
    projects: any[];
    onSelectProject: (project: any) => void;
    onCreateProject: (name: string, description: string) => Promise<void>;
    onLinkFolder?: (path: string) => Promise<void>;
    selectedFiles: Set<string>;
    onToggleFileSelection: (fileId: string) => void;
    onClearSelection: () => void;
}

export const AssetGrid: React.FC<AssetGridProps> = ({
    onSelectFile,
    selectedProject,
    projects = [],
    onSelectProject,
    onCreateProject,
    onLinkFolder,
    selectedFiles,
    onToggleFileSelection,
    onClearSelection
}) => {
    const { files = [], loading, uploadBatch } = useUploads();
    const [uploading, setUploading] = useState(false);
    const [uploadMode, setUploadMode] = useState<'files' | 'folder'>('files');
    const [showProjectModal, setShowProjectModal] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Filter files by selected project
    const projectFiles = (files || []).filter(file => {
        if (!selectedProject) return true; // Show all if no project selected
        // Match by project_id in metadata or folder path
        return file.project_id === selectedProject.project_id ||
            file.original_path?.startsWith(`${selectedProject.name}/`);
    });

    const handleUpload = async (uploadedFiles: FileList) => {
        if (!selectedProject) {
            alert('Please select a project before uploading');
            return;
        }

        setUploading(true);
        try {
            await uploadBatch(uploadedFiles, selectedProject.project_id);
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed: ' + (error instanceof Error ? error.message : 'Unknown error'));
        } finally {
            setUploading(false);
        }
    };

    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        const droppedFiles = e.dataTransfer.files;
        if (droppedFiles.length > 0) {
            await handleUpload(droppedFiles);
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
    };

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files;
        if (selectedFiles && selectedFiles.length > 0) {
            await handleUpload(selectedFiles);
        }
        // Reset input
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const handleCreateProject = async (name: string, description: string) => {
        await onCreateProject(name, description);
    };

    return (
        <div className="flex flex-col h-full bg-gray-900 text-white">
            {/* Toolbar */}
            <div className="p-4 border-b border-gray-800 flex flex-wrap items-center gap-3">
                {/* Project Selector */}
                <div className="flex-1 max-w-xs min-w-[200px]">
                    <select
                        value={selectedProject?.project_id || ''}
                        onChange={(e) => {
                            const project = projects.find(p => p.project_id === e.target.value);
                            onSelectProject(project);
                        }}
                        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                    >
                        <option value="" disabled>Select Project</option>
                        {projects.map(p => (
                            <option key={p.project_id} value={p.project_id}>
                                {p.name} ({p.file_count} files)
                            </option>
                        ))}
                    </select>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-2">
                    <button
                        onClick={() => setShowProjectModal(true)}
                        className="px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm font-medium transition-colors"
                    >
                        New Project
                    </button>

                    <button
                        onClick={() => {
                            setUploadMode('folder');
                            fileInputRef.current?.click();
                        }}
                        className="px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                    >
                        <FolderOpen size={16} />
                        Upload Folder
                    </button>
                </div>

                {/* Upload Button */}
                <button
                    onClick={() => {
                        setUploadMode('files');
                        fileInputRef.current?.click();
                    }}
                    disabled={uploading || !selectedProject}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                    <Upload size={18} />
                    {uploading ? 'Uploading...' : 'Upload Files'}
                </button>

                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept="image/*,video/*"
                    onChange={handleFileSelect}
                    className="hidden"
                    {...(uploadMode === 'folder' ? { webkitdirectory: '', directory: '' } as any : {})}
                />
            </div>

            {/* Selection Info */}
            {selectedFiles.size > 0 && (
                <div className="px-4 py-2 bg-blue-900/30 border-b border-blue-600/30 flex justify-between items-center">
                    <span className="text-sm text-blue-200">
                        {selectedFiles.size} file{selectedFiles.size > 1 ? 's' : ''} selected
                    </span>
                    <button
                        onClick={onClearSelection}
                        className="text-sm text-blue-400 hover:text-blue-300 font-medium"
                    >
                        Clear Selection
                    </button>
                </div>
            )}

            {/* Drop Zone / File List */}
            <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                className="flex-1 overflow-y-auto p-4"
            >
                {loading ? (
                    <div className="flex items-center justify-center h-full text-gray-500">
                        Loading assets...
                    </div>
                ) : projectFiles.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-gray-500 text-center">
                        <Upload size={48} className="mb-4 opacity-50" />
                        <p className="text-lg font-medium mb-2">No files yet</p>
                        <p className="text-sm">
                            {selectedProject
                                ? 'Drag & drop files here or click Upload'
                                : 'Select a project to view assets'}
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
                        {projectFiles.map((file) => {
                            const isSelected = selectedFiles.has(file.file_id);
                            return (
                                <div
                                    key={file.file_id}
                                    onClick={() => onToggleFileSelection(file.file_id)}
                                    className={`relative group cursor-pointer rounded-lg overflow-hidden border-2 transition-all aspect-square ${isSelected
                                        ? 'border-blue-500 ring-2 ring-blue-500/50'
                                        : 'border-transparent hover:border-gray-700 bg-gray-800'
                                        }`}
                                >
                                    {/* Thumbnail */}
                                    <div className="w-full h-full relative">
                                        {file.file_type === 'image' ? (
                                            <img
                                                src={`http://localhost:8000/api/upload/file/${file.file_id}`}
                                                alt={file.filename}
                                                className="w-full h-full object-cover"
                                                loading="lazy"
                                                onError={(e) => {
                                                    e.currentTarget.style.display = 'none';
                                                }}
                                            />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center bg-gray-800">
                                                <FileImage size={32} className="text-gray-600" />
                                            </div>
                                        )}

                                        {/* Selection Indicator */}
                                        <div className="absolute top-2 right-2 z-10">
                                            {isSelected ? (
                                                <CheckCircle2 size={20} className="text-blue-500 bg-white rounded-full" />
                                            ) : (
                                                <Circle size={20} className="text-white/70 opacity-0 group-hover:opacity-100 transition-opacity drop-shadow-md" />
                                            )}
                                        </div>

                                        {/* Hover Overlay */}
                                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onSelectFile(file.file_id, file.file_type);
                                                }}
                                                className="px-3 py-1.5 bg-white/90 hover:bg-white text-gray-900 text-xs rounded font-medium transform translate-y-2 group-hover:translate-y-0 transition-transform"
                                            >
                                                View
                                            </button>
                                        </div>
                                    </div>

                                    {/* Filename */}
                                    <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/80 to-transparent">
                                        <p className="text-xs text-white truncate px-1" title={file.filename}>
                                            {file.filename}
                                        </p>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            {/* Project Modal */}
            <ProjectModal
                isOpen={showProjectModal}
                onClose={() => setShowProjectModal(false)}
                onCreate={handleCreateProject}
            />
        </div>
    );
};
