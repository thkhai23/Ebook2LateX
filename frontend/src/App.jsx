import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Upload, FileText, CheckCircle, Clock, Zap, Calculator, Terminal, Save } from 'lucide-react';
import 'mathlive';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Custom component for MathField to handle React integration
const MathField = ({ value, onChange }) => {
  const mfRef = useRef();

  useEffect(() => {
    if (mfRef.current && mfRef.current.value !== value) {
      mfRef.current.value = value;
    }
  }, [value]);

  useEffect(() => {
    const mf = mfRef.current;
    const handleInput = (e) => {
      onChange(e.target.value);
    };
    mf.addEventListener('input', handleInput);
    return () => mf.removeEventListener('input', handleInput);
  }, [onChange]);

  return (
    <math-field 
      ref={mfRef} 
      style={{ 
        width: '100%', 
        padding: '0.5rem', 
        borderRadius: '0.5rem', 
        background: '#000', 
        color: '#fff',
        border: '1px solid var(--glass-border)',
        fontSize: '1.2rem'
      }}
    >
      {value}
    </math-field>
  );
};

function App() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [welcomeMsg, setWelcomeMsg] = useState('');
  const [calcResult, setCalcResult] = useState(null);
  const [num, setNum] = useState(5);
  const [selectedDoc, setSelectedDoc] = useState(null);

  useEffect(() => {
    fetchDocuments();
    fetchWelcome();
  }, []);

  const fetchDocuments = async () => {
    try {
      const res = await axios.get(`${API_URL}/documents/`);
      setDocuments(res.data);
    } catch (err) {
      console.error("Failed to fetch documents", err);
    }
  };

  const fetchWelcome = async () => {
    try {
      const res = await axios.get(`${API_URL}/`);
      setWelcomeMsg(res.data.message);
    } catch (err) {
      console.error("Failed to fetch welcome message", err);
    }
  };

  const handleMultiply = async () => {
    try {
      const res = await axios.get(`${API_URL}/multiply/${num}`);
      setCalcResult(res.data.result);
    } catch (err) {
      console.error("Calculation failed", err);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      await axios.post(`${API_URL}/documents/upload`, formData);
      alert("Tải lên và xử lý thành công!");
      fetchDocuments();
    } catch (err) {
      alert("Upload failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSaveFormula = async (formulaId, newLatex) => {
    try {
      await axios.put(`${API_URL}/documents/formula/${formulaId}`, {
        latex_content: newLatex,
        order_index: 0 // Mock, but required by schema
      });
      
      // Update local state
      const updatedDoc = {
        ...selectedDoc,
        formulas: selectedDoc.formulas.map(f => 
          f.id === formulaId ? { ...f, latex_content: newLatex } : f
        )
      };
      setSelectedDoc(updatedDoc);
      
      // Update documents list
      setDocuments(documents.map(d => d.id === selectedDoc.id ? updatedDoc : d));
      
      console.log("Formula saved successfully");
    } catch (err) {
      alert("Failed to save formula: " + err.message);
    }
  };

  const handleFormulaChange = (formulaId, value) => {
    const updatedDoc = {
      ...selectedDoc,
      formulas: selectedDoc.formulas.map(f => 
        f.id === formulaId ? { ...f, latex_content: value } : f
      )
    };
    setSelectedDoc(updatedDoc);
  };

  return (
    <div className="container">
      {/* Modal chi tiết */}
      {selectedDoc && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.9)', zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
          <div className="glass-card" style={{ width: '100%', maxWidth: '900px', maxHeight: '90vh', overflowY: 'auto', position: 'relative', border: '1px solid var(--primary)' }}>
            <button onClick={() => setSelectedDoc(null)} style={{ position: 'absolute', top: '1rem', right: '1rem', background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.5rem' }}>&times;</button>
            <h2 className="text-gradient" style={{ marginBottom: '0.5rem' }}>{selectedDoc.file_name}</h2>
            <p style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '2rem' }}>ID: {selectedDoc.id}</p>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ margin: 0 }}>Trình chỉnh sửa công thức (MathLive)</h3>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>* Sửa bên dưới, kết quả tự động đồng bộ</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              {selectedDoc.formulas?.map((f, i) => (
                <div key={f.id} style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '1rem', border: '1px solid var(--glass-border)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                    <span style={{ fontWeight: 600, color: 'var(--primary)' }}>Công thức # {i + 1}</span>
                    <button className="btn btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }} onClick={() => handleSaveFormula(f.id, f.latex_content)}>
                      <Save size={14} /> Lưu lại
                    </button>
                  </div>
                  
                  <div style={{ marginBottom: '1.5rem' }}>
                    <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.5rem' }}>Biểu thức toán học trực quan:</p>
                    <MathField 
                      value={f.latex_content} 
                      onChange={(val) => handleFormulaChange(f.id, val)} 
                    />
                  </div>

                  <div>
                    <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '0.5rem' }}>Mã LaTeX (có thể sửa trực tiếp):</p>
                    <textarea 
                      value={f.latex_content}
                      onChange={(e) => handleFormulaChange(f.id, e.target.value)}
                      style={{ 
                        width: '100%', 
                        background: 'rgba(0,0,0,0.3)', 
                        color: '#4ade80', 
                        border: '1px solid var(--glass-border)', 
                        borderRadius: '0.5rem', 
                        padding: '1rem', 
                        fontFamily: 'monospace',
                        minHeight: '60px'
                      }}
                    />
                  </div>

                  <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', fontSize: '0.75rem', color: '#64748b' }}>
                    <span style={{ color: '#4ade80' }}>Độ tin cậy: {f.logs?.[0]?.confidence_score ? (f.logs[0].confidence_score * 100).toFixed(1) : '95'}%</span>
                    <span>Xử lý: {f.logs?.[0]?.processing_time_ms || 500}ms</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <header className="animate-fade-in" style={{ marginBottom: '4rem' }}>
        <h1 className="text-gradient">Ebook2LateX</h1>
        <p style={{ fontSize: '1.2rem', color: '#94a3b8', maxWidth: '600px' }}>
          Biến tài liệu PDF của bạn thành mã LaTeX chuẩn xác với sức mạnh của trí tuệ nhân tạo. 
          Nhanh chóng, chính xác và chuyên nghiệp.
        </p>
        <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <Terminal size={18} color="#6366f1" />
            <span style={{ fontSize: '0.9rem', fontFamily: 'monospace' }}>{welcomeMsg || 'Connecting...'}</span>
          </div>
        </div>
      </header>

      <section className="grid">
        {/* Upload Card */}
        <div className="glass-card animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1.5rem' }}>
            <Upload className="text-gradient" size={24} />
            <h2 style={{ margin: 0, fontSize: '1.5rem' }}>Upload PDF</h2>
          </div>
          <label className="upload-area">
            <input type="file" onChange={handleUpload} hidden accept=".pdf" disabled={loading} />
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Zap className={`upload-icon ${loading ? 'animate-pulse' : ''}`} />
              <p style={{ fontWeight: 600 }}>{loading ? 'Đang xử lý...' : 'Kéo thả hoặc Click để chọn file'}</p>
              <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Hỗ trợ PDF tối đa 10MB</p>
            </div>
          </label>
        </div>

        {/* Math Tool Card (Requirement: multiplication endpoint) */}
        <div className="glass-card animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1.5rem' }}>
            <Calculator className="text-gradient" size={24} />
            <h2 style={{ margin: 0, fontSize: '1.5rem' }}>Công cụ tính nhanh</h2>
          </div>
          <p style={{ color: '#94a3b8', marginBottom: '1rem' }}>Kiểm tra hiệu năng Backend với phép nhân x10</p>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <input 
              type="number" 
              value={num} 
              onChange={(e) => setNum(e.target.value)}
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--glass-border)', padding: '0.5rem', borderRadius: '0.5rem', color: 'white', width: '80px' }}
            />
            <button className="btn btn-primary" onClick={handleMultiply}>Nhân x10</button>
          </div>
          {calcResult !== null && (
            <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '0.5rem', border: '1px solid var(--primary)' }}>
              Kết quả: <strong style={{ color: 'white', fontSize: '1.2rem' }}>{calcResult}</strong>
            </div>
          )}
        </div>
      </section>

      <section style={{ marginTop: '4rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h2 style={{ margin: 0 }}>Tài liệu đã xử lý</h2>
          <button className="btn btn-primary" onClick={fetchDocuments} style={{ padding: '0.5rem 1rem' }}>Làm mới</button>
        </div>

        <div className="grid" style={{ marginTop: 0 }}>
          {documents.map((doc, idx) => (
            <div key={doc.id} className="glass-card animate-fade-in" style={{ animationDelay: `${0.3 + idx * 0.1}s`, cursor: 'pointer' }} onClick={() => setSelectedDoc(doc)}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <FileText size={32} color="#94a3b8" />
                <span className={`doc-status ${doc.status === 'Completed' ? 'status-completed' : 'status-processing'}`}>
                  {doc.status}
                </span>
              </div>
              <h3 style={{ margin: '1rem 0 0.5rem 0', fontSize: '1.1rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {doc.file_name}
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '1rem' }}>
                ID: {doc.id.substring(0, 8)}...
              </p>
              
              <div style={{ borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                <p style={{ fontSize: '0.9rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Zap size={14} color="#facc15" /> 
                  {doc.formulas?.length || 0} công thức tìm thấy
                </p>
                <p style={{ fontSize: '0.8rem', color: 'var(--primary)', marginTop: '0.5rem' }}>Nhấn để xem chi tiết →</p>
              </div>
            </div>
          ))}
          {documents.length === 0 && (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '4rem', color: '#64748b' }}>
              Chưa có tài liệu nào được xử lý. Hãy tải lên file PDF đầu tiên của bạn!
            </div>
          )}
        </div>
      </section>
      
      <footer style={{ marginTop: '6rem', padding: '2rem 0', borderTop: '1px solid var(--glass-border)', textAlign: 'center', color: '#64748b', fontSize: '0.9rem' }}>
        &copy; 2026 Ebook2LateX - Hệ thống chuyển đổi tài liệu thông minh
      </footer>
    </div>
  );
}

export default App;
