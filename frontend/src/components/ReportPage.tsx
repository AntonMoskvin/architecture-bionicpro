// frontend/src/components/ReportPage.tsx
import React, { useState } from 'react';

interface ReportPageProps {
  keycloak: any;
  authenticated: boolean;
}

const ReportPage: React.FC<ReportPageProps> = ({ keycloak, authenticated }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<any>(null);

  const handleLogout = () => {
    keycloak.logout();
  };

  const fetchReport = async () => {
    if (!keycloak.token) {
      setError('No token');
      return;
    }
    try {
      setLoading(true);
      const res = await fetch('http://localhost:8001/reports', {
        headers: { Authorization: `Bearer ${keycloak.token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setReport(data);
      } else {
        setError('Report not found');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  if (!authenticated) {
    return <div>Loading...</div>;
  }

  return (
      <div style={{ padding: '20px' }}>
        <h1>Report Portal</h1>
        <button onClick={handleLogout}>Logout</button>
        <br /><br />
        <button onClick={fetchReport} disabled={loading}>
          {loading ? 'Loading...' : 'Download Report'}
        </button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {report && <pre>{JSON.stringify(report, null, 2)}</pre>}
      </div>
  );
};

export default ReportPage;