import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';


interface Instance {
  id: string;
  sopInstanceUid: string;
  pngUrl: string; // The URL to the static PNG file from your backend
}

interface Series {
  id: string;
  seriesDescription: string;
  instances: Instance[];
}

interface Study {
  id: string;
  series: Series[];
}

const PngDicomViewer: React.FC = () => {
  const [studyId, setStudyId] = useState('');
  const [studyData, setStudyData] = useState<Study | null>(null);
  const [selectedSeries, setSelectedSeries] = useState<Series | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [fps, setFps] = useState(15); // Adjustable speed for Cine
  
  const cineInterval = useRef<NodeJS.Timeout | null>(null);

  // --- 1. Fetch Study Metadata ---
  const fetchStudy = async () => {
    try {
      const response = await fetch(`/api/studies/${studyId}`);
      const data: Study = await response.json();
      setStudyData(data);
      if (data.series.length > 0) {
        setSelectedSeries(data.series[0]);
        setCurrentIndex(0);
      }
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  // --- 2. Performance: Pre-loading Images ---
  // This prevents the "flicker" during Cine playback
  useEffect(() => {
    if (selectedSeries) {
      selectedSeries.instances.forEach((inst) => {
        const img = new Image();
        img.src = inst.pngUrl;
      });
    }
  }, [selectedSeries]);

  // --- 3. Navigation Controls ---
  const nextImage = useCallback(() => {
    if (!selectedSeries) return;
    setCurrentIndex((prev) => (prev + 1) % selectedSeries.instances.length);
  }, [selectedSeries]);

  const prevImage = useCallback(() => {
    if (!selectedSeries) return;
    setCurrentIndex((prev) => 
      (prev - 1 + selectedSeries.instances.length) % selectedSeries.instances.length
    );
  }, [selectedSeries]);

  // Keyboard navigation
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') nextImage();
      if (e.key === 'ArrowLeft') prevImage();
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [nextImage, prevImage]);

  // --- 4. Cine Mode (Movie) ---
  useEffect(() => {
    if (isPlaying) {
      cineInterval.current = setInterval(nextImage, 1000 / fps);
    } else {
      if (cineInterval.current) clearInterval(cineInterval.current);
    }
    return () => { if (cineInterval.current) clearInterval(cineInterval.current); };
  }, [isPlaying, nextImage, fps]);

  return (
    <div style={containerStyle}>
      <header style={headerStyle}>
        <input 
          value={studyId} 
          onChange={(e) => setStudyId(e.target.value)} 
          placeholder="Enter Study UID"
          style={inputStyle}
        />
        <button onClick={fetchStudy} style={buttonStyle}>Load Study</button>
      </header>

      {studyData && (
        <div style={layoutStyle}>
          {/* Sidebar: Series Selection & Instance List */}
          <aside style={sidebarStyle}>
            <label>Series:</label>
            <select 
              style={selectStyle}
              onChange={(e) => {
                const s = studyData.series.find(ser => ser.id === e.target.value);
                setSelectedSeries(s || null);
                setCurrentIndex(0);
              }}
            >
              {studyData.series.map(s => (
                <option key={s.id} value={s.id}>{s.seriesDescription}</option>
              ))}
            </select>

            <div style={instanceListStyle}>
              {selectedSeries?.instances.map((inst, idx) => (
                <div 
                  key={inst.id}
                  onClick={() => setCurrentIndex(idx)}
                  style={{ 
                    ...instanceItemStyle, 
                    backgroundColor: currentIndex === idx ? '#333' : 'transparent' 
                  }}
                >
                  Frame {idx + 1}
                </div>
              ))}
            </div>
          </aside>

          {/* Main Viewer Area */}
          <main style={viewerAreaStyle}>
            <div style={toolbarStyle}>
              <button onClick={() => setIsPlaying(!isPlaying)} style={cineButtonStyle}>
                {isPlaying ? '⏹ STOP CINE' : '▶ PLAY CINE'}
              </button>
              <input 
                type="range" min="1" max="60" value={fps} 
                onChange={(e) => setFps(parseInt(e.target.value))}
              />
              <span>{fps} FPS</span>
            </div>

            <div style={viewportStyle}>
              {selectedSeries ? (
                <img 
                  src={selectedSeries.instances[currentIndex].pngUrl} 
                  alt="DICOM Frame" 
                  style={imgStyle}
                />
              ) : (
                <p>Select a series to begin</p>
              )}
              <div style={overlayStyle}>
                Frame: {currentIndex + 1} / {selectedSeries?.instances.length}
              </div>
            </div>
          </main>
        </div>
      )}
    </div>
  );
};

// --- Styles (CSS-in-JS for clarity) ---
const containerStyle: React.CSSProperties = { backgroundColor: '#000', color: '#ccc', height: '100vh', display: 'flex', flexDirection: 'column' };
const headerStyle: React.CSSProperties = { padding: '15px', borderBottom: '1px solid #333', display: 'flex', gap: '10px' };
const layoutStyle: React.CSSProperties = { display: 'flex', flex: 1, overflow: 'hidden' };
const sidebarStyle: React.CSSProperties = { width: '250px', borderRight: '1px solid #333', padding: '10px', display: 'flex', flexDirection: 'column' };
const viewerAreaStyle: React.CSSProperties = { flex: 1, display: 'flex', flexDirection: 'column', padding: '20px', alignItems: 'center' };
const viewportStyle: React.CSSProperties = { position: 'relative', border: '1px solid #444', width: '512px', height: '512px', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#050505' };
const imgStyle: React.CSSProperties = { maxWidth: '100%', maxHeight: '100%', imageRendering: 'pixelated' };
const overlayStyle: React.CSSProperties = { position: 'absolute', bottom: '10px', left: '10px', fontSize: '12px', color: '#0f0' };
const instanceListStyle: React.CSSProperties = { overflowY: 'auto', flex: 1, marginTop: '10px' };
const instanceItemStyle: React.CSSProperties = { padding: '8px', cursor: 'pointer', fontSize: '13px', borderBottom: '1px solid #222' };
const inputStyle: React.CSSProperties = { background: '#222', color: '#fff', border: '1px solid #444', padding: '5px' };
const buttonStyle: React.CSSProperties = { cursor: 'pointer', padding: '5px 15px' };
const cineButtonStyle: React.CSSProperties = { padding: '8px 20px', fontWeight: 'bold', cursor: 'pointer' };
const selectStyle: React.CSSProperties = { background: '#222', color: '#fff', padding: '5px' };
const toolbarStyle: React.CSSProperties = { marginBottom: '15px', display: 'flex', gap: '20px', alignItems: 'center' };

export default PngDicomViewer;