import React, { useState, useEffect } from "react";
import "./App.css";
import Dashboard from "./components/Dashboard";
import { RefreshCw, Clock, Zap } from "lucide-react";

function App() {
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [nextUpdate, setNextUpdate] = useState(3600); // 1 hour = 3600 seconds

  // Update timestamp when dashboard refreshes
  const handleDataUpdate = () => {
    setLastUpdated(new Date());
    setIsRefreshing(false);
  };

  const handleRefreshStart = () => {
    setIsRefreshing(true);
  };

  // Countdown timer for next update
  useEffect(() => {
    const timer = setInterval(() => {
      setNextUpdate((prev) => {
        if (prev <= 1) {
          handleRefreshStart();
          return 3600; // Reset to 1 hour (3600 seconds)
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("en-US", {
      hour12: true,
      hour: "numeric",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const formatCountdown = (seconds: number) => {
    if (seconds >= 3600) {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return `${hours}h ${minutes}m`;
    } else if (seconds >= 60) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}m ${remainingSeconds}s`;
    } else {
      return `${seconds}s`;
    }
  };

  return (
    <div className="App">
      {/* Header with better spacing */}
      <header className="header">
        <h1>⚡ CS Student Hub</h1>
        <p>Real-Time Tech Ecosystem Dashboard</p>

        {/* Status Bar */}
        <div className="status-bar">
          <div className="status-item">
            <Clock size={16} />
            <span>Last updated: {formatTime(lastUpdated)}</span>
          </div>

          <div className="status-item">
            <RefreshCw size={16} className={isRefreshing ? "spinning" : ""} />
            <span>
              {isRefreshing
                ? "Updating..."
                : `Next update in ${formatCountdown(nextUpdate)}`}
            </span>
          </div>

          <div className="status-item">
            <Zap size={16} />
            <span>Auto-refresh enabled</span>
          </div>
        </div>

        {/* User Notice */}
        <div className="user-notice">
          <div className="notice-content">
            <span className="notice-icon">ℹ️</span>
            <div className="notice-text">
              <strong>Live Data:</strong> This dashboard automatically fetches
              fresh GitHub and Reddit data every hour. Click refresh on any card
              to get immediate updates.
            </div>
          </div>
        </div>
      </header>

      {/* Dashboard Component */}
      <Dashboard
        onDataUpdate={handleDataUpdate}
        onRefreshStart={handleRefreshStart}
      />
    </div>
  );
}

export default App;
