import backgroundImage from './images/me-background.jpg';
import React from 'react';

function BackgroundImage({ children }) {
    return (
        <div style={{ position: 'relative', height: '100vh' }}>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100vh',
                position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
                background: `url(${backgroundImage}) no-repeat center center fixed`, backgroundSize: '100% 100%', opacity: '0.5'
            }}></div>
            <div style={{ position: 'relative', zIndex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                {children}
            </div>
        </div>
    );
};
export default BackgroundImage;