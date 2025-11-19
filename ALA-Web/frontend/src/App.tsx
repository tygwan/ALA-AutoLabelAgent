import { useState } from 'react';
import { Layout } from './components/Layout';
import { ImageViewer } from './components/ImageViewer';
import { AnnotationSidebar } from './components/AnnotationSidebar';
import { AssetGrid } from './components/AssetGrid';
import { Gallery } from './pages/Gallery';
import { Preprocessing } from './pages/Preprocessing';
import { Settings } from './pages/Settings';

interface AnnotationParams {
  vlmModel: string;
  segModel: string;
  ontology: Record<string, string>;
}

function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [activePage, setActivePage] = useState('annotate');

  // Annotation State
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');

  const handleImageSelect = (path: string) => {
    setSelectedImage(path);
    setActivePage('annotate');
  };

  const handleRunAnnotation = async (params: AnnotationParams) => {
    setIsProcessing(true);
    setProgress(0);
    setStatusMessage('Initializing models...');

    // TODO: Connect to backend
    console.log('Running annotation with:', params);

    // Mock progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsProcessing(false);
          setStatusMessage('Complete');
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  const handleCancelAnnotation = () => {
    setIsProcessing(false);
    setStatusMessage('Cancelled');
  };

  const renderAnnotateView = () => (
    <div className="flex h-full">
      {/* Left: Asset Grid (replaces simple image list) */}
      <div className="w-80 bg-gray-800 border-r border-gray-700 overflow-hidden flex flex-col">
        <AssetGrid onSelectFile={(fileId) => {
          setSelectedImage(`http://localhost:8000/api/upload/file/${fileId}`);
        }} />
      </div>

      {/* Middle: Main Viewer */}
      <div className="flex-1 bg-gray-950 relative flex flex-col">
        {selectedImage ? (
          <ImageViewer imageUrl={selectedImage} />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-gray-500">
            Select an asset to view
          </div>
        )}
      </div>

      {/* Right: Annotation Sidebar */}
      <AnnotationSidebar
        onRun={handleRunAnnotation}
        onCancel={handleCancelAnnotation}
        isProcessing={isProcessing}
        progress={progress}
        statusMessage={statusMessage}
      />
    </div>
  );

  const renderContent = () => {
    switch (activePage) {
      case 'gallery':
        return <Gallery onSelectImage={handleImageSelect} />;
      case 'preprocessing':
        return <Preprocessing />;
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
