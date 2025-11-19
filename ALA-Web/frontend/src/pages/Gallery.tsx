import React from 'react';
import { useImages } from '../hooks/useImages';

interface GalleryProps {
    onSelectImage: (path: string) => void;
}

export const Gallery: React.FC<GalleryProps> = ({ onSelectImage }) => {
    const { images, loading, error } = useImages();

    if (loading) return <div className="p-8 text-gray-400">Loading gallery...</div>;
    if (error) return <div className="p-8 text-red-500">{error}</div>;

    return (
        <div className="p-8 h-full overflow-y-auto bg-gray-950">
            <h2 className="text-2xl font-bold text-white mb-6">Image Gallery</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {images.map((img) => (
                    <div
                        key={img.filename}
                        onClick={() => onSelectImage(`http://localhost:8000${img.path}`)}
                        className="group relative aspect-square bg-gray-800 rounded-xl overflow-hidden cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
                    >
                        <img
                            src={`http://localhost:8000${img.path}`}
                            alt={img.filename}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                        <div className="absolute bottom-0 left-0 right-0 bg-black/60 p-2 transform translate-y-full group-hover:translate-y-0 transition-transform">
                            <p className="text-xs text-white truncate">{img.filename}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
