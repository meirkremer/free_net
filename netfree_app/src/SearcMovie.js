import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

const SearchMovie = ({ setIsSubmitted, setResponse }) => {
    const [email, setEmail] = useState('');
    const [searchText, setSearchText] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleSearchTextChange = (event) => {
        setSearchText(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setSubmitted(true);
        setIsSubmitted(true);
        console.log('Email:', email);
        console.log('Search String:', searchText);
        try {
            Cookies.set('EmailAddres', email);
            const response = await axios.post('/api/search', { email, searchText });
            console.log('Response:', response.data);
            setResponse(response.data);
        } catch (error) {
            console.error('Error:', error);
        }
    };
    return (
        <div>
            <h1 style={{ textAlign: 'center' }} dir='rtl'>ברוך הבא</h1>
            <form onSubmit={handleSubmit}>
                <p>הכנס את כתובת האימייל שלך ואת שם הקובץ בו אתה מעוניין</p>
                <div style={{ marginBottom: '1rem', direction: 'rtl', textAlign: 'right' }}>
                    <label htmlFor="email" style={{ direction: 'rtl', textAlign: 'right' }}>דואר אלקטרוני:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={handleEmailChange}
                        required
                        style={{ width: '100%', borderRadius: '5px', padding: '0.5rem' }}
                    />
                </div>
                <div style={{ marginBottom: '1rem', direction: 'rtl', textAlign: 'right' }}>
                    <label htmlFor="searchString" style={{ direction: 'rtl', textAlign: 'right' }}>שם הקובץ:</label>
                    <input
                        type="text"
                        id="searchString"
                        value={searchText}
                        onChange={handleSearchTextChange}
                        required
                        style={{ width: '100%', borderRadius: '5px', padding: '0.5rem' }}
                    />
                </div>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <button type="submit">תמצא לי פליז</button>
                </div>
            </form>
        </div>
    );
};

export default SearchMovie;
