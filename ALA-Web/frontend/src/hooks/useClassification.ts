import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// ============================================================================
// Types
// ============================================================================

export interface Experiment {
    experiment_id: string;
    name: string;
    created_at: string;
    support_set_id: string;
    query_set_id: string;
    status: 'created' | 'running' | 'completed' | 'failed';
    results_ref: string;
    parent_experiment?: string;
    metadata?: {
        method?: string;
        threshold?: number;
        notes?: string;
    };
}

export interface SupportSet {
    support_set_id: string;
    name: string;
    version: string;
    images_count: number;
    created_at: string;
    parent_version?: string;
}

export interface QuerySet {
    query_set_id: string;
    name: string;
    images_count: number;
    created_at: string;
}

export interface ExperimentResults {
    experiment_id: string;
    completed_at: string;
    classifications: Record<string, {
        predicted_class: string;
        confidence: number;
        annotation_ref: string;
    }>;
    statistics: {
        total_classified: number;
        class_distribution: Record<string, number>;
        avg_confidence: number;
    };
}

// ============================================================================
// Experiments Hook
// ============================================================================

export const useExperiments = () => {
    const [experiments, setExperiments] = useState<Experiment[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchExperiments = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${API_URL}/api/classification/experiment/list`);
            setExperiments(response.data.experiments);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch experiments');
            console.error('Error fetching experiments:', err);
        } finally {
            setLoading(false);
        }
    };

    const createExperiment = async (data: {
        name: string;
        support_set_id: string;
        query_set_id: string;
        method?: string;
        threshold?: number;
        parent_experiment?: string;
        notes?: string;
    }) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_URL}/api/classification/experiment/create`, data);
            await fetchExperiments();
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to create experiment');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const deleteExperiment = async (experimentId: string) => {
        setLoading(true);
        setError(null);
        try {
            await axios.delete(`${API_URL}/api/classification/experiment/${experimentId}`);
            await fetchExperiments();
        } catch (err: any) {
            setError(err.message || 'Failed to delete experiment');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const getExperimentDetails = async (experimentId: string) => {
        try {
            const response = await axios.get(`${API_URL}/api/classification/experiment/${experimentId}`);
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to get experiment details');
            throw err;
        }
    };

    const runExperiment = async (experimentId: string) => {
        try {
            const response = await axios.post(`${API_URL}/api/classification/experiment/${experimentId}/run`);
            await fetchExperiments();
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to run experiment');
            throw err;
        }
    };

    const compareExperiments = async (experimentIds: string[]) => {
        try {
            const response = await axios.get(
                `${API_URL}/api/classification/experiment/compare?exp_ids=${experimentIds.join(',')}`
            );
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to compare experiments');
            throw err;
        }
    };

    useEffect(() => {
        fetchExperiments();
    }, []);

    return {
        experiments,
        loading,
        error,
        fetchExperiments,
        createExperiment,
        deleteExperiment,
        getExperimentDetails,
        runExperiment,
        compareExperiments,
    };
};

// ============================================================================
// Support Sets Hook
// ============================================================================

export const useSupportSets = () => {
    const [supportSets, setSupportSets] = useState<SupportSet[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchSupportSets = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${API_URL}/api/classification/support-set/list`);
            setSupportSets(response.data.support_sets);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch support sets');
            console.error('Error fetching support sets:', err);
        } finally {
            setLoading(false);
        }
    };

    const createSupportSet = async (data: {
        name: string;
        classes: Record<string, string[]>;
        parent_version?: string;
    }) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_URL}/api/classification/support-set/create`, data);
            await fetchSupportSets();
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to create support set');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const cloneSupportSet = async (supportSetId: string) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_URL}/api/classification/support-set/${supportSetId}/clone`);
            await fetchSupportSets();
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to clone support set');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const getSupportSetDetails = async (supportSetId: string) => {
        try {
            const response = await axios.get(`${API_URL}/api/classification/support-set/${supportSetId}`);
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to get support set details');
            throw err;
        }
    };

    useEffect(() => {
        fetchSupportSets();
    }, []);

    return {
        supportSets,
        loading,
        error,
        fetchSupportSets,
        createSupportSet,
        cloneSupportSet,
        getSupportSetDetails,
    };
};

// ============================================================================
// Query Sets Hook
// ============================================================================

export const useQuerySets = () => {
    const [querySets, setQuerySets] = useState<QuerySet[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchQuerySets = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${API_URL}/api/classification/query-set/list`);
            setQuerySets(response.data.query_sets);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch query sets');
            console.error('Error fetching query sets:', err);
        } finally {
            setLoading(false);
        }
    };

    const createQuerySet = async (data: {
        name: string;
        image_ids: string[];
    }) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_URL}/api/classification/query-set/create`, data);
            await fetchQuerySets();
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to create query set');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const getQuerySetDetails = async (querySetId: string) => {
        try {
            const response = await axios.get(`${API_URL}/api/classification/query-set/${querySetId}`);
            return response.data;
        } catch (err: any) {
            setError(err.message || 'Failed to get query set details');
            throw err;
        }
    };

    useEffect(() => {
        fetchQuerySets();
    }, []);

    return {
        querySets,
        loading,
        error,
        fetchQuerySets,
        createQuerySet,
        getQuerySetDetails,
    };
};
