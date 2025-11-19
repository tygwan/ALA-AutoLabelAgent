import React, { useState, useEffect } from 'react';
import { Stage, Layer, Image as KonvaImage } from 'react-konva';
import useImage from 'use-image';

interface ImageViewerProps {
    imageUrl: string;
}

const URLImage: React.FC<{ src: string }> = ({ src }) => {
    const [image] = useImage(src);
    return <KonvaImage image={image} />;
};

export const ImageViewer: React.FC<ImageViewerProps> = ({ imageUrl }) => {
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

    useEffect(() => {
        const updateDimensions = () => {
            const container = document.getElementById('canvas-container');
            if (container) {
                setDimensions({
                    width: container.offsetWidth,
                    height: container.offsetHeight
                });
            }
        };

        window.addEventListener('resize', updateDimensions);
        updateDimensions();

        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    return (
        <div id="canvas-container" className="w-full h-full bg-gray-900 overflow-hidden">
            <Stage width={dimensions.width} height={dimensions.height} draggable>
                <Layer>
                    <URLImage src={imageUrl} />
                </Layer>
            </Stage>
        </div>
    );
};
