import logo from './logo.svg';
import './App.css';
import BackgroundImage from './BackgroundImage';
import React, { useEffect, useState } from 'react';
import WindowManager from './WindowManger';
import SearchMovie from './SearcMovie';
import Spinner from './Spinner';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Result from './Result';

function App() {
  const [submit, setSubmit] = useState(false);
  const [responseJSON, setResponseJSON] = useState(null);
  useEffect(() => { 
    console.log(submit);
    console.log(responseJSON)
   }, [submit, responseJSON]);
  return (
    <Router>
      <BackgroundImage>
        {!submit ? 
        <SearchMovie setIsSubmitted={setSubmit} setResponse={setResponseJSON}></SearchMovie> :
        !responseJSON ? <Spinner /> : <Result data={responseJSON}/>
        }
      </BackgroundImage>
    </Router>
  );
}

export default App;
