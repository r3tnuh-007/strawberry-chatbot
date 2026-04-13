import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <section id="center">
        <div>
          <h1>Strawberry frontend</h1>
        </div>
        <button
          className="counter"
          onClick={() => setCount((count) => count + 1)}>
          Count is {count}
        </button>
      </section>
    </>
  )
}

export default App
