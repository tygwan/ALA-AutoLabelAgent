import { useState, useEffect } from 'react';
import axios from 'axios';

export interface ImageInfo {
    filename: string;
    path: string;
}

const API_URL = 'http://localhost:8000';

export const useImages = () => {
    const [images, setImages] = useState<ImageInfo[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchImages = async () => {
            setLoading(true);
            try {
                const response = await axios.get<ImageInfo[]>(`${API_URL}/api/images/`);
                setImages(response.data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch images');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchImages();
    }, []);

    return { images, loading, error };
};
