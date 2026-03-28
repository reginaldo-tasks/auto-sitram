import React, { useState } from 'react';
import { searchSITRAMData, type SearchParams, type SITRAMResponse } from '../services/sitramService';
import './SITRAMPage.css';

interface FormData {
  start_date: string;
  end_date: string;
  cnpj: string;
}

export default function SITRAMPage() {
  const [formData, setFormData] = useState<FormData>({
    start_date: '',
    end_date: '',
    cnpj: '',
  });

  const [response, setResponse] = useState<SITRAMResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [csvData, setCSVData] = useState<string[] | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setCSVData(null);

    const searchParams: SearchParams = {
      start_date: formData.start_date,
      end_date: formData.end_date,
      cnpj: formData.cnpj,
    };

    const result = await searchSITRAMData(searchParams);
    setResponse(result);

    if (result.success && result.data) {
      // Parse CSV data
      const lines = result.data.split('\n').filter(line => line.trim());
      setCSVData(lines);
    }

    setLoading(false);
  };

  const downloadCSV = () => {
    if (response?.data) {
      const element = document.createElement('a');
      const file = new Blob([response.data], { type: 'text/csv' });
      element.href = URL.createObjectURL(file);
      element.download = `sitram_${new Date().toISOString()}.csv`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
  };

  return (
    <div className="sitram-container">
      <h1>SITRAM - Extração de Dados</h1>
      <p className="subtitle">Sistema para automatizar busca de pagamentos ICMS</p>

      <form onSubmit={handleSubmit} className="sitram-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="start_date">Data Inicial (DD/MM/YYYY)</label>
            <input
              type="text"
              id="start_date"
              name="start_date"
              value={formData.start_date}
              onChange={handleInputChange}
              placeholder="01/01/2024"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="end_date">Data Final (DD/MM/YYYY)</label>
            <input
              type="text"
              id="end_date"
              name="end_date"
              value={formData.end_date}
              onChange={handleInputChange}
              placeholder="31/12/2024"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="cnpj">CNPJ (XX.XXX.XXX/XXXX-XX)</label>
          <input
            type="text"
            id="cnpj"
            name="cnpj"
            value={formData.cnpj}
            onChange={handleInputChange}
            placeholder="38.009.037/0001-53"
            required
          />
        </div>

        <button type="submit" disabled={loading} className="btn-submit">
          {loading ? 'Pesquisando...' : 'Pesquisar'}
        </button>
      </form>

      {response && (
        <div className={`response-section ${response.success ? 'success' : 'error'}`}>
          {response.success ? (
            <>
              <h2>✓ Busca realizada com sucesso!</h2>
              {csvData && csvData.length > 0 && (
                <>
                  <p>Total de registros: {csvData.length - 1}</p>
                  <button onClick={downloadCSV} className="btn-download">
                    📥 Baixar CSV
                  </button>
                  <div className="csv-preview">
                    <h3>Prévia dos dados:</h3>
                    <table>
                      <tbody>
                        {csvData.slice(0, 6).map((line, idx) => (
                          <tr key={idx}>
                            {line.split(',').map((cell, cellIdx) => (
                              <td key={cellIdx}>{cell.substring(0, 20)}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    {csvData.length > 6 && <p className="more-data">+ {csvData.length - 6} linhas...</p>}
                  </div>
                </>
              )}
            </>
          ) : (
            <>
              <h2>✗ Erro na busca</h2>
              <p className="error-message">{response.error}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
