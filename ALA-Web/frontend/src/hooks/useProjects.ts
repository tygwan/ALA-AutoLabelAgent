import { useState, useEffect } from 'react';

interface Project {
    project_id: string;
    name: string;
    display_name: string;
    description: string;
    created_at: string;
    file_count: number;
    last_upload: string | null;
    ontology: Record<string, string>;
}

export const useProjects = () => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [selectedProject, setSelectedProject] = useState<Project | null>(null);
    const [loading, setLoading] = useState(false);

    const fetchProjects = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/api/projects/list');
            const data = await response.json();
            // API returns a list directly, but handle object wrapper just in case
            const projectsList = Array.isArray(data) ? data : (data.projects || []);
            setProjects(projectsList);

            // Auto-select first project if none selected
            if (!selectedProject && projectsList.length > 0) {
                setSelectedProject(projectsList[0]);
            }
        } catch (error) {
            console.error('Failed to fetch projects:', error);
        } finally {
            setLoading(false);
        }
    };

    const createProject = async (
        name: string,
        description: string = '',
        ontology: Record<string, string> = {}
    ): Promise<Project | null> => {
        try {
            const response = await fetch('http://localhost:8000/api/projects/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description, ontology })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to create project');
            }

            const project = await response.json();
            setProjects(prev => [...prev, project]);
            setSelectedProject(project);
            return project;
        } catch (error) {
            console.error('Failed to create project:', error);
            alert(error instanceof Error ? error.message : 'Failed to create project');
            return null;
        }
    };

    const updateOntology = async (
        projectId: string,
        ontology: Record<string, string>
    ) => {
        try {
            const response = await fetch(
                `http://localhost:8000/api/projects/${projectId}/ontology`,
                {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(ontology)
                }
            );

            if (!response.ok) throw new Error('Failed to update ontology');

            const updated = await response.json();
            setProjects(prev =>
                prev.map(p => (p.project_id === projectId ? updated : p))
            );

            if (selectedProject?.project_id === projectId) {
                setSelectedProject(updated);
            }
        } catch (error) {
            console.error('Failed to update ontology:', error);
        }
    };

    const deleteProject = async (projectId: string, deleteFiles: boolean = false) => {
        try {
            const response = await fetch(
                `http://localhost:8000/api/projects/${projectId}?delete_files=${deleteFiles}`,
                { method: 'DELETE' }
            );

            if (!response.ok) throw new Error('Failed to delete project');

            setProjects(prev => prev.filter(p => p.project_id !== projectId));

            if (selectedProject?.project_id === projectId) {
                setSelectedProject(projects[0] || null);
            }
        } catch (error) {
            console.error('Failed to delete project:', error);
        }
    };

    useEffect(() => {
        fetchProjects();
    }, []);

    return {
        projects,
        selectedProject,
        setSelectedProject,
        loading,
        createProject,
        updateOntology,
        deleteProject,
        refreshProjects: fetchProjects
    };
};
