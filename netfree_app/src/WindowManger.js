// WindowManager.js
import React, { useState } from 'react';
import WindowA from './WindowA';
import WindowB from './WindowB';

const WindowManager = () => {
    const [windowAVisible, setWindowAVisible] = useState(false);
    const [windowBVisible, setWindowBVisible] = useState(false);

    const offWindowB = () => {
        setWindowBVisible(false);
    }
    const offWindowA = () => {
        setWindowAVisible(false);
    }

    const toggleWindowA = () => {
        setWindowAVisible(true);
        offWindowB();
    };

    const toggleWindowB = () => {
        setWindowBVisible(true);
        offWindowA();
    };

    return (
        <div>
            {windowAVisible && <WindowA />}
            {windowBVisible && <WindowB />}
            <button onClick={toggleWindowA}>Toggle Window A</button>
            <br></br>
            <button onClick={toggleWindowB}>Toggle Window B</button>
        </div>
    );
}
export default WindowManager;
