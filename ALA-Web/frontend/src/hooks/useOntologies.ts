import { useState, useEffect } from 'react';

interface Ontology {
    ontology_id: string;
    name: string;
    description: string;
    classes: Record<string, string>;
    created_at: string;
    class_count: number;
}

interface OntologyListItem {
    ontology_id: string;
    name: string;
    description: string;
    class_count: number;
    created_at: string;
}

export const useOntologies = () => {
    const [ontologies, setOntologies] = useState<OntologyListItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchOntologies = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await fetch('http://localhost:8000/api/ontology/list');
            const data = await response.json();
            setOntologies(data.ontologies);
        } catch (err) {
            console.error('Failed to fetch ontologies:', err);
            setError('Failed to fetch ontologies');
        } finally {
            setLoading(false);
        }
    };

    const saveOntology = async (
        name: string,
        description: string,
        classes: Record<string, string>
    ): Promise<string | null> => {
        try {
            setError(null);
            const response = await fetch('http://localhost:8000/api/ontology/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description, classes })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save ontology');
            }

            const result = await response.json();
            await fetchOntologies(); // Refresh list
            return result.ontology_id;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to save ontology';
            setError(errorMessage);
            alert(errorMessage);
            return null;
        }
    };

    const getOntology = async (ontologyId: string): Promise<Ontology | null> => {
        try {
            setError(null);
            const response = await fetch(`http://localhost:8000/api/ontology/${ontologyId}`);

            if (!response.ok) {
                throw new Error('Failed to fetch ontology details');
            }

            return await response.json();
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to fetch ontology';
            setError(errorMessage);
            return null;
        }
    };

    const deleteOntology = async (ontologyId: string): Promise<boolean> => {
        try {
            setError(null);
            const response = await fetch(`http://localhost:8000/api/ontology/${ontologyId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete ontology');
            }

            await fetchOntologies(); // Refresh list
            return true;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to delete ontology';
            setError(errorMessage);
            alert(errorMessage);
            return false;
        }
    };

    useEffect(() => {
        fetchOntologies();
    }, []);

    return {
        ontologies,
        loading,
        error,
        fetchOntologies,
        saveOntology,
        getOntology,
        deleteOntology
    };
};
