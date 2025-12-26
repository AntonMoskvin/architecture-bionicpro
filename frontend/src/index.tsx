// frontend/src/index.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import Keycloak from 'keycloak-js';
import App from './App';

const keycloak = new Keycloak({
    url: 'http://localhost:8080',
    realm: 'reports-realm',
    clientId: 'reports-frontend'
});

keycloak.init({
    onLoad: 'login-required',
    pkceMethod: 'S256'
}).then((authenticated) => {
    // Сохраняем в глобальную переменную для отладки
    (window as any).keycloak = keycloak;

    const root = createRoot(document.getElementById('root')!);
    root.render(<App keycloak={keycloak} authenticated={authenticated} />);
}).catch(error => {
    console.error('Keycloak init failed', error);
    alert('Authentication failed');
});