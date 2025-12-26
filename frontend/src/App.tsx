// frontend/src/App.tsx
import React from 'react';
import ReportPage from './components/ReportPage';

interface AppProps {
    keycloak: any;
    authenticated: boolean;
}

const App: React.FC<AppProps> = ({ keycloak, authenticated }) => {
    return (
        <div className="App">
            <ReportPage keycloak={keycloak} authenticated={authenticated} />
        </div>
    );
};

export default App;