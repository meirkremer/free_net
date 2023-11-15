import React, { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
function Result({ data }) {
    const [jsonData, setJsonData] = useState(data);
    const [selectedBoxIds, setSelectBoxIds] = useState([]);
    const [selectedSend, setSelectedSend] = useState(false);
    const handleBoxClick = (id) => {
        if (selectedBoxIds.includes(id)) {
            setSelectBoxIds(selectedBoxIds.filter((boxId) => boxId !== id));
        } else {
            setSelectBoxIds([...selectedBoxIds, id]);
        }
    };
    const [response, setResponse] = useState(null);
    const handleSendToServer = async () => {
        if (selectedBoxIds.length === 0) {
            window.alert("אממ... נראה שלא בחרת כלום... איך נדע מה להוריד? תבחר משהו קודם");
        } else {
            // Perform the server request with the selectedBoxIds
            // For demonstration purposes, we will log the IDs to the console
            try {
                const emailAddres = Cookies.get('EmailAddres')
                const updateIDs = [emailAddres, ...selectedBoxIds]
                console.log("Sending selected box IDs to the server:", updateIDs);
                const response = await axios.post('api/download', { updateIDs });
                setSelectedSend(true);
                console.log(response.data);
                setResponse(response.data.status);
            } catch (error) {
                console.error('Error:', error);
            }
        }
    };
    const handleGoToWebsite = () => {
        window.location.href = "http://meirkremer.com/";
    };
    return (
        <div>
            {
                Object.entries(jsonData).length === 0 ?
                    (
                        <div dir="rtl" style={{ marginTop: '20px' }}>
                            <h1>אממ... לא הצלחתי למצוא שום קובץ בשם הזה</h1>
                            <h2>(או שיש תקלה בשרת)</h2>
                            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                                <button onClick={handleGoToWebsite}>בא ננסה למצוא משהו אחר</button>
                            </div>
                        </div>


                    ) :
                    (
                        Object.entries(jsonData).length === 1 && Object.keys(jsonData)[0] === 'user not exists' ?
                            (<div dir='rtl'>
                                <h1>
                                    אתה לא רשום במערכת!
                                </h1>
                                <h2>
                                    להרשמה שלח מייל לכתובת:
                                    s0528964723@gmail.com
                                </h2>
                                <h3>
                                    נא לציין שם מלא. פניות אנונימיות לא יתקבלו!
                                </h3>
                            </div>) :
                            (!selectedSend ? (
                                <div style={{ marginTop: '20px' }}>
                                    <h1 style={{ textAlign: 'center' }} dir="rtl">אוקיי אז זה מה שמצאתי</h1>
                                    <h2 style={{ textAlign: 'center' }} dir="rtl">בחר את הקובץ שבא לך</h2>
                                    <div
                                        style={{
                                            marginTop: '20px',
                                            height: '400px', // Adjust the height as per your requirements
                                            overflow: 'auto', // Enable scrolling if the content exceeds the height
                                            border: '1px solid silver',
                                            padding: '10px',
                                        }}
                                    >
                                        {Object.entries(jsonData).map(([id, field1]) => {
                                            console.log('Data from JSON:', id, field1[0], "\n", field1[1]); // Print data to console
                                            return (
                                                <div dir="rtl"
                                                    key={id}
                                                    style={{
                                                        border: '1px solid black',
                                                        padding: '10px',
                                                        margin: '10px',
                                                        cursor: 'pointer',
                                                        backgroundColor: selectedBoxIds.includes(id) ? 'lightblue' : 'white',
                                                    }}
                                                    onClick={() => handleBoxClick(id)}
                                                >
                                                    <div dir="rtl">שם: {field1[0]}</div>
                                                    <div dir="rtl">גודל: {field1[1]}</div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                                        <button onClick={handleSendToServer}>תוריד לי</button>
                                    </div>
                                </div>
                            ) : (
                                <div>{response}</div>
                            ))
                    )
            }
        </div >
    );
};

export default Result;