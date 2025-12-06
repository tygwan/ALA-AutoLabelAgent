import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export interface ImageTracking {
    image_id: string;
    filename: string;
    stages: {
        uploaded?: { timestamp: string; status: string; metadata?: any };
        annotated?: { timestamp: string; status: string; metadata?: any };
        preprocessed?: { timestamp: string; status: string; metadata?: any };
        classified?: { timestamp: string; status: string; metadata?: any };
    };
    current_stage: string;
    errors: Array<{ stage: string; error: string; timestamp: string }>;
}

export interface PipelineStatus {
    stages: {
        uploaded: number;
        annotated: number;
        preprocessed: number;
        classified: number;
    };
    total_images: number;
}

export const useTracking = () => {
    const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus | null>(null);
    const [errors, setErrors] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchPipelineStatus = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${API_URL}/api/tracking/status`);
            setPipelineStatus(response.data);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch pipeline status');
        } finally {
            setLoading(false);
        }
    };

    const fetchErrors = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/tracking/errors`);
            setErrors(response.data.errors);
        } catch (err: any) {
            console.error('Failed to fetch errors:', err);
        }
    };

    const getImageHistory = async (imageId: string) => {
        try {
            const response = await axios.get(`${API_URL}/api/tracking/image/${imageId}`);
            return response.data as ImageTracking;
        } catch (err: any) {
            throw err;
        }
    };

    const retryFailed = async (imageId: string) => {
        try {
            const response = await axios.post(`${API_URL}/api/tracking/retry/${imageId}`);
            await fetchPipelineStatus();
            await fetchErrors();
            return response.data;
        } catch (err: any) {
            throw err;
        }
    };

    useEffect(() => {
        fetchPipelineStatus();
        fetchErrors();
    }, []);

    return {
        pipelineStatus,
        errors,
        loading,
        error,
        fetchPipelineStatus,
        fetchErrors,
        getImageHistory,
        retryFailed,
    };
};
