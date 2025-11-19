import React, { useState, useRef } from 'react';
import { Upload, FileImage, FileVideo, Trash2 } from 'lucide-react';
import { useUploads } from '../hooks/useUploads';

interface AssetGridProps {
    onSelectFile: (fileId: string, fileType: 'image' | 'video') => void;
}

export const AssetGrid: React.FC<AssetGridProps> = ({ onSelectFile }) => {
    const { files, loading, uploadBatch, deleteFile } = useUploads();
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        const droppedFiles = e.dataTransfer.files;
        if (droppedFiles.length > 0) {
            setUploading(true);
            try {
                await uploadBatch(droppedFiles);
            } catch (error) {
                console.error('Upload failed:', error);
            }
            setUploading(false);
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
    };

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files;
        if (selectedFiles && selectedFiles.length > 0) {
            setUploading(true);
            try {
                await uploadBatch(selectedFiles);
            } catch (error) {
                console.error('Upload failed:', error);
            }
            setUploading(false);
        }
    };

    const formatFileSize = (bytes: number) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    };

    return (
        <div className="p-6 bg-gray-950 h-full overflow-y-auto">
            {/* Upload Zone */}
            <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-gray-700 rounded-xl p-8 mb-6 text-center cursor-pointer hover:border-blue-500 transition-colors bg-gray-900"
            >
                <Upload className="mx-auto mb-4 text-gray-400" size={48} />
                <p className="text-gray-300 mb-2">
                    {uploading ? 'Uploading...' : 'Drag & drop files here or click to browse'}
                </p>
                <p className="text-sm text-gray-500">
                    Supports images (JPG, PNG) and videos (MP4, AVI, MOV, MKV)
                </p>
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept="image/*,video/*"
                    onChange={handleFileSelect}
                    className="hidden"
                />
            </div>

            {/* Stats */}
            <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-white">
                    Uploaded Assets ({files.length})
                </h2>
            </div>

            {/* Grid */}
            {loading ? (
                <div className="text-gray-400 text-center py-12">Loading assets...</div>
            ) : files.length === 0 ? (
                <div className="text-gray-500 text-center py-12">
                    No assets uploaded yet. Drag and drop files above to get started.
                </div>
            ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                    {files.map((file) => (
                        <div
                            key={file.file_id}
                            className="group relative bg-gray-900 rounded-xl overflow-hidden border border-gray-800 hover:border-blue-500 transition-all cursor-pointer"
                            onClick={() => onSelectFile(file.file_id, file.file_type)}
                        >
                            {/* Thumbnail */}
                            <div className="aspect-square bg-gray-800 flex items-center justify-center">
                                {file.file_type === 'image' ? (
                                    <img
                                        src={`http://localhost:8000/api/upload/file/${file.file_id}`}
                                        alt={file.filename}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <FileVideo className="text-gray-600" size={48} />
                                )}
                            </div>

                            {/* Info */}
                            <div className="p-3">
                                <div className="flex items-start justify-between mb-1">
                                    {file.file_type === 'image' ? (
                                        <FileImage className="text-blue-400 flex-shrink-0" size={16} />
                                    ) : (
                                        <FileVideo className="text-purple-400 flex-shrink-0" size={16} />
                                    )}
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            deleteFile(file.file_id);
                                        }}
                                        className="opacity-0 group-hover:opacity-100 transition-opacity text-red-400 hover:text-red-300"
                                    >
                                        <Trash2 size={16} />
                                    </button>
                                </div>
                                <p className="text-xs text-gray-400 truncate" title={file.filename}>
                                    {file.filename}
                                </p>
                                <p className="text-xs text-gray-600 mt-1">
                                    {formatFileSize(file.size)}
                                </p>
                            </div>

                            {/* Hover Overlay */}
                            <div className="absolute inset-0 bg-blue-600 bg-opacity-0 group-hover:bg-opacity-10 transition-all pointer-events-none" />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
