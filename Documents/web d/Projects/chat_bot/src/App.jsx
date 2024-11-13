import React, { useState } from 'react';
import InputComponent from './components/InputComponent';
import BotComponent from './components/BotComponent';

function App() {
  const [input, setInput] = useState('');

  const handleInputChange = (value) => setInput(value);  // Set input state

  return (
    <>
      <InputComponent onChange={handleInputChange} />  {/* Pass the handler to InputComponent */}
      <BotComponent input={input} />  {/* Pass inputValue to BotComponent */}
    </>
  );
}

export default App;
