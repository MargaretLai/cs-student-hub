import React from "react";
import "./App.css";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>⚡ CS Student Hub</h1>
        <p>Real-Time Tech Ecosystem Dashboard</p>
      </header>
      <main>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
