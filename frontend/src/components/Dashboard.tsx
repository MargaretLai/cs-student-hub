import React, { useState, useEffect } from "react";
import axios from "axios";
import TrendingTopics from "./TrendingTopics";
import LiveStats from "./LiveStats";
import { Activity, Globe, AlertCircle } from "lucide-react";

interface TrendingTopic {
  id: number;
  keyword: string;
  platform: string;
  trend_score: number;
  posts_count: number;
  description: string;
  language?: string;
  url?: string;
  stars?: number;
}

interface DashboardProps {
  onDataUpdate?: () => void;
  onRefreshStart?: () => void;
}

interface PlatformStatus {
  status: string;
  last_fetch: string;
  repos_count?: number;
  posts_count?: number;
  questions_count?: number;
  stories_count?: number;
  rate_limit_remaining?: number;
  error?: string;
}

interface TrendingData {
  trending_topics: TrendingTopic[];
  platforms: {
    github: PlatformStatus;
    reddit: PlatformStatus;
    stackoverflow: PlatformStatus;
    hackernews: PlatformStatus;
  };
  language_stats?: any;
  total_repos_analyzed?: number;
  last_updated?: string;
  error?: string;
  message?: string;
}

interface ApiStatus {
  status: string;
  message: string;
  version: string;
  features: string[];
  github_api?: {
    status: string;
    rate_limit: {
      limit: number;
      remaining: number;
      reset_time: number;
    };
    message: string;
  };
}

const Dashboard: React.FC<DashboardProps> = ({
  onDataUpdate,
  onRefreshStart,
}) => {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [trendingData, setTrendingData] = useState<TrendingData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      onRefreshStart?.(); // Notify parent that refresh started

      // Fetch API status
      const statusResponse = await axios.get(
        "http://127.0.0.1:8000/api/status/"
      );
      setApiStatus(statusResponse.data);

      // Fetch trending data
      const trendingResponse = await axios.get(
        "http://127.0.0.1:8000/api/trending/"
      );
      setTrendingData(trendingResponse.data);

      onDataUpdate?.(); // Notify parent that data was updated
    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to fetch data from API");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <div className="dashboard">
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <AlertCircle className="card-icon" />
              Connection Error
            </div>
          </div>
          <div className="card-content">
            <div className="error">
              {error}
              <br />
              <button
                onClick={fetchData}
                style={{
                  marginTop: "1rem",
                  padding: "0.5rem 1rem",
                  background: "#667eea",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  cursor: "pointer",
                }}
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* API Status Card */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Activity className="card-icon" />
            🔗 API Status
          </div>
          <div
            className={`status-indicator ${
              apiStatus?.status === "running"
                ? "status-connected"
                : "status-error"
            }`}
          >
            {apiStatus?.status || "unknown"}
          </div>
        </div>
        <div className="card-content">
          {isLoading ? (
            <div className="loading">Checking API status...</div>
          ) : (
            <div>
              <div className="api-info">
                <p>
                  <strong>Version:</strong> {apiStatus?.version}
                </p>
                <p>
                  <strong>Message:</strong> {apiStatus?.message}
                </p>

                {apiStatus?.github_api && (
                  <div
                    style={{
                      marginTop: "1rem",
                      padding: "1rem",
                      background: "rgba(255,255,255,0.05)",
                      borderRadius: "8px",
                    }}
                  >
                    <p>
                      <strong>GitHub API:</strong> {apiStatus.github_api.status}
                    </p>
                    <p>
                      <strong>Rate Limit:</strong>{" "}
                      {apiStatus.github_api.rate_limit.remaining}/
                      {apiStatus.github_api.rate_limit.limit}
                    </p>
                  </div>
                )}
              </div>

              <div className="features-list" style={{ marginTop: "1rem" }}>
                <strong>Features:</strong>
                <ul style={{ marginLeft: "1rem", marginTop: "0.5rem" }}>
                  {apiStatus?.features?.map((feature, index) => (
                    <li
                      key={index}
                      style={{ color: "#a0a0a0", marginBottom: "0.3rem" }}
                    >
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Live Stats */}
      <LiveStats data={trendingData} isLoading={isLoading} />

      {/* Trending Topics - Fixed the type issue here */}
      {trendingData && (
        <TrendingTopics
          trendingData={trendingData.trending_topics || []}
          isLoading={isLoading}
        />
      )}

      {/* Platform Status Cards */}
      {trendingData?.platforms && (
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Globe className="card-icon" />
              🌐 Platform Status
            </div>
          </div>
          <div className="card-content">
            <div className="platform-grid">
              {Object.entries(trendingData.platforms).map(
                ([platform, status]) => (
                  <div key={platform} className="platform-status">
                    <div className="platform-name">
                      {platform.charAt(0).toUpperCase() + platform.slice(1)}
                    </div>
                    <div
                      className={`platform-status-indicator status-${status.status}`}
                    >
                      {status.status}
                    </div>
                    <div
                      style={{
                        fontSize: "0.8rem",
                        color: "#a0a0a0",
                        marginTop: "0.5rem",
                      }}
                    >
                      {status.repos_count && `${status.repos_count} repos`}
                      {status.posts_count && `${status.posts_count} posts`}
                      {status.questions_count &&
                        `${status.questions_count} questions`}
                      {status.stories_count &&
                        `${status.stories_count} stories`}
                    </div>
                    {status.rate_limit_remaining && (
                      <div
                        style={{
                          fontSize: "0.7rem",
                          color: "#667eea",
                          marginTop: "0.3rem",
                        }}
                      >
                        {status.rate_limit_remaining} API calls left
                      </div>
                    )}
                  </div>
                )
              )}
            </div>
          </div>
        </div>
      )}

      {/* GitHub Statistics Summary */}
      {trendingData?.total_repos_analyzed && (
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Activity className="card-icon" />
              📊 GitHub Analytics
            </div>
          </div>
          <div className="card-content">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">
                  {trendingData.total_repos_analyzed}
                </div>
                <div className="stat-label">Repos Analyzed</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">
                  {trendingData.language_stats
                    ? Object.keys(trendingData.language_stats).length
                    : 0}
                </div>
                <div className="stat-label">Languages</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">
                  {trendingData.trending_topics
                    ? trendingData.trending_topics.length
                    : 0}
                </div>
                <div className="stat-label">Trending</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">Live</div>
                <div className="stat-label">Updates</div>
              </div>
            </div>

            {trendingData.last_updated && (
              <div
                style={{
                  textAlign: "center",
                  color: "#a0a0a0",
                  fontSize: "0.9rem",
                  marginTop: "1rem",
                }}
              >
                Last updated: {trendingData.last_updated}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
