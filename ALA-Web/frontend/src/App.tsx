import { useState } from 'react';
import { Layout } from './components/Layout';
import { ImageViewer } from './components/ImageViewer';
import { AnnotationSidebar } from './components/AnnotationSidebar';
import { AssetGrid } from './components/AssetGrid';
import { Gallery } from './pages/Gallery';
import { Preprocessing } from './pages/Preprocessing';
import { Settings } from './pages/Settings';
import { Classification } from './pages/Classification';
import { DataTracking } from './pages/DataTracking';
import { useProjects } from './hooks/useProjects';

interface AnnotationParams {
  vlmModel: string;
  segModel: string;
  ontology: Record<string, string>;
}

function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [activePage, setActivePage] = useState('annotate');

  // Projects state
  const {
    projects,
    selectedProject,
    setSelectedProject,
    createProject,
    updateOntology,
    linkFolder
  } = useProjects();

  // Multi-select state
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());

  // Annotation State
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');

  const handleImageSelect = (path: string) => {
    setSelectedImage(path);
    setActivePage('annotate');
  };

  const handleToggleFileSelection = (fileId: string) => {
    setSelectedFiles(prev => {
      const newSet = new Set(prev);
      if (newSet.has(fileId)) {
        newSet.delete(fileId);
      } else {
        newSet.add(fileId);
      }
      return newSet;
    });
  };

  const handleClearSelection = () => {
    setSelectedFiles(new Set());
  };

  const handleCreateProject = async (name: string, description: string) => {
    await createProject(name, description);
  };

  const handleRunAnnotation = async (params: AnnotationParams) => {
    setIsProcessing(true);
    setProgress(0);
    setStatusMessage('Checking AI models availability...');

    // Auto-save caption ontology to project
    if (selectedProject && Object.keys(params.ontology).length > 0) {
      await updateOntology(selectedProject.project_id, params.ontology);
      console.log('Caption ontology saved to project:', selectedProject.display_name);
    }

    try {
      // Determine which files to annotate
      const filesToAnnotate = selectedFiles.size > 0
        ? Array.from(selectedFiles)
        : selectedImage ? [selectedImage.match(/\/file\/([^/]+)$/)?.[1]].filter(Boolean) : [];

      if (filesToAnnotate.length === 0) {
        throw new Error('No files selected for annotation');
      }

      console.log(`Running annotation on ${filesToAnnotate.length} file(s)...`);
      const results = [];

      for (let i = 0; i < filesToAnnotate.length; i++) {
        const fileId = filesToAnnotate[i];
        setStatusMessage(`Annotating file ${i + 1}/${filesToAnnotate.length}...`);
        setProgress(20 + (60 * i / filesToAnnotate.length));

        console.log('Running annotation with:', {
          file_id: fileId,
          ontology: params.ontology
        });

        // Call backend auto-annotate API
        const response = await fetch('http://localhost:8000/api/annotate/auto-annotate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            file_id: fileId,
            ontology: params.ontology,
            save_visualization: true
          })
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));

          if (response.status === 503) {
            throw new Error('AI models not installed. Please run: setup_ai_models.bat in backend folder');
          }

          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        results.push(result);

        console.log(`File ${i + 1} result:`, result);
      }

      setProgress(90);
      setStatusMessage('Annotation complete!');

      const totalObjects = results.reduce((sum, r) => sum + r.count, 0);
      const allClasses = [...new Set(results.flatMap(r => r.classes))];

      console.log('All annotation results:', results);
      console.log(`Total detected objects: ${totalObjects}`);

      // Show results to user
      alert(
        `Annotation Complete!\n\n` +
        `Files processed: ${results.length}\n` +
        `Total objects detected: ${totalObjects}\n` +
        `Classes: ${allClasses.join(', ')}\n\n` +
        `Check console for details.`
      );

      setProgress(100);
      setStatusMessage(`Complete: ${totalObjects} objects detected`);
      setIsProcessing(false);

      // Clear selection after annotation
      setSelectedFiles(new Set());

    } catch (error) {
      console.error('Annotation failed:', error);
      setStatusMessage(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setProgress(0);
      setIsProcessing(false);

      // Show error to user
      alert(`Annotation Failed:\n\n${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const handleCancelAnnotation = () => {
    setIsProcessing(false);
    setStatusMessage('Cancelled');
  };

  const renderAnnotateView = () => (
    <div className="flex h-full">
      {/* Left: Asset Grid with Projects */}
      <div className="w-80 bg-gray-800 border-r border-gray-700 overflow-hidden flex flex-col">
        <AssetGrid
          onSelectFile={(fileId) => {
            setSelectedImage(`http://localhost:8000/api/upload/file/${fileId}`);
          }}
          selectedProject={selectedProject}
          projects={projects}
          onSelectProject={setSelectedProject}
          onCreateProject={handleCreateProject}
          onLinkFolder={linkFolder}
          selectedFiles={selectedFiles}
          onToggleFileSelection={handleToggleFileSelection}
          onClearSelection={handleClearSelection}
        />
      </div>

      {/* Middle: Main Viewer */}
      <div className="flex-1 bg-gray-950 relative flex flex-col">
        {selectedImage ? (
          <ImageViewer imageUrl={selectedImage} />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-gray-500">
            {selectedProject
              ? 'Select an asset to view'
              : 'Create or select a project to get started'}
          </div>
        )}
      </div>

      {/* Right: Annotation Sidebar with Auto-loaded Ontology */}
      <AnnotationSidebar
        onRun={handleRunAnnotation}
        onCancel={handleCancelAnnotation}
        isProcessing={isProcessing}
        progress={progress}
        statusMessage={statusMessage}
        initialOntology={selectedProject?.ontology || {}}
      />
    </div>
  );

  const renderContent = () => {
    switch (activePage) {
      case 'gallery':
        return <Gallery onSelectImage={handleImageSelect} />;
      case 'preprocessing':
        return <Preprocessing />;
      case 'classification':
        return <Classification />;
      case 'tracking':
        return <DataTracking />;
      case 'settings':
        return <Settings />;
      case 'annotate':
      default:
        return renderAnnotateView();
    }
  };

  return (
    <Layout activePage={activePage} onNavigate={setActivePage}>
      {renderContent()}
    </Layout>
  );
}

export default App;
