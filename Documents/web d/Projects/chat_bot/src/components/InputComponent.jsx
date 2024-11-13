import React, { useState } from 'react'; // Add useState to the import statement
import arrow_up from "../assets/arrow_up.png";
import "./InputComponent.css";

function InputComponent({ onChange }) {
  const [inputValue, setInputValue] = useState(''); // Initialize state

  const handleClick = () => {
    setInputValue('');  // Clear the input field on button click
  };

  const handleChange = (event) => {
    setInputValue(event.target.value); 
    console.log(event.target.value) // Update state when input changes
    onChange(event.target.value);  // Notify parent component of input change
  };

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={handleChange}
        placeholder="Write something"
      />
      <button onClick={handleClick} className='submit-btn'>
        <img src={arrow_up} alt="Submit" />
      </button>
    </div>
  );
}

export default InputComponent;
