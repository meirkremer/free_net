import React, { useEffect, useState } from 'react';
import './Spinner.css'; // Import the CSS file for styling

const Spinner = () => {
  return (
    <div>
      <div className="loader"></div>
      <p>מחפש</p>
      <div />
    </div>
  );
};
export default Spinner;
