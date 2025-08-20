import React, { useState, useEffect } from "react";
import axios from "axios";
import { Activity, TrendingUp, Users, Code } from "lucide-react";
import TrendingTopics from "./TrendingTopics";
import LiveStats from "./LiveStats";

interface ApiStatus {
  status: string;
  message: string;
  version: string;
  features: string[];
}

interface TrendingData {
  status: string;
  last_updated: string;
  trending_topics: Array<{
    id: number;
    keyword: string;
    platform: string;
    trend_score: number;
    posts_count: number;
    description: string;
  }>;
  platforms: {
    [key: string]: {
      status: string;
      last_fetch: string;
    };
  };
}

const Dashboard: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [trendingData, setTrendingData] = useState<TrendingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // Fetch API status
      const statusResponse = await axios.get<ApiStatus>("/api/status/");
      setApiStatus(statusResponse.data);

      // Fetch trending data
      const trendingResponse = await axios.get<TrendingData>("/api/trending/");
      setTrendingData(trendingResponse.data);

      setError(null);
    } catch (err) {
      setError("Failed to fetch dashboard data");
      console.error("Dashboard fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case "github":
        return <Code className="w-5 h-5" />;
      case "reddit":
        return <Users className="w-5 h-5" />;
      case "stackoverflow":
        return <Activity className="w-5 h-5" />;
      case "hackernews":
        return <TrendingUp className="w-5 h-5" />;
      default:
        return <Activity className="w-5 h-5" />;
    }
  };

  if (loading && !trendingData) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <h3>⚠️ Error</h3>
        <p>{error}</p>
        <button onClick={fetchDashboardData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-grid">
        {/* API Status Card */}
        <div className="dashboard-card status-card">
          <div className="card-header">
            <Activity className="w-6 h-6" />
            <h3>🔌 API Status</h3>
          </div>
          {apiStatus && (
            <div>
              <p className="status-message">{apiStatus.message}</p>
              <p className="version">Version: {apiStatus.version}</p>
              <div className="features">
                <h4>Features:</h4>
                <ul>
                  {apiStatus.features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        {/* Live Stats */}
        {trendingData && <LiveStats trendingData={trendingData} />}

        {/* Trending Topics */}
        {trendingData && <TrendingTopics trendingData={trendingData} />}

        {/* Platform Status Cards */}
        {trendingData?.platforms && (
          <div className="platforms-grid">
            {Object.entries(trendingData.platforms).map(([platform, info]) => (
              <div key={platform} className="dashboard-card platform-card">
                <div className="platform-header">
                  {getPlatformIcon(platform)}
                  <h4>{platform}</h4>
                </div>
                <p className={`status ${info.status}`}>{info.status}</p>
                <p className="last-fetch">
                  Last fetch: {new Date(info.last_fetch).toLocaleTimeString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="dashboard-footer">
        <p>
          🔄 Auto-refreshing every 30 seconds | Last updated:{" "}
          {trendingData?.last_updated
            ? new Date(trendingData.last_updated).toLocaleString()
            : "Never"}
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
