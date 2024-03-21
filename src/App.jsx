import './App.css'
import { useState } from 'react'

function App() {

  const [filePath, setFilePath] = useState('testfile.mp4');

  async function getPredict() {
    let resp = await fetch('http://127.0.0.1:5000/predictions')
    const json = await resp.json()
    console.log(json);
  }

  async function postPredict() {
    if (filePath === '') {
      return
    }

    try {
        let resp = await fetch(`http://127.0.0.1:5000/prediction/new`, {
            method: 'POST',
            mode: 'cors', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filePath: filePath }), 
        });
        const json = await resp.json();
        console.log(json);

        // Initialize file path
        setFilePath('need to initialize the path');

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}



  return (
    <>
    {/* This is test to check API */}
      <div>
        <button onClick={getPredict}>Get</button>
        <button onClick={postPredict}>Post</button>
      </div>
    </>
  )
}

export default App
