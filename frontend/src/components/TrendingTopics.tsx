import React from "react";
import { TrendingUp, Star, GitFork, ExternalLink } from "lucide-react";

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

interface TrendingTopicsProps {
  trendingData: TrendingTopic[];
  isLoading: boolean;
}

const TrendingTopics: React.FC<TrendingTopicsProps> = ({
  trendingData,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <TrendingUp className="card-icon" />
            🔥 Trending Now
          </div>
        </div>
        <div className="card-content">
          <div className="loading">Loading trending repositories...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <TrendingUp className="card-icon" />
          🔥 Trending GitHub Repos
        </div>
        <div className="trend-count">{trendingData.length} repos</div>
      </div>
      <div className="card-content">
        <div className="trending-list">
          {trendingData.slice(0, 8).map((topic, index) => (
            <div key={topic.id} className="trending-item">
              <div className="trending-rank">#{index + 1}</div>
              <div className="trending-info">
                <div className="trending-header">
                  <div className="trending-name">{topic.keyword}</div>
                  <div className="trending-stats">
                    <span className="stat">
                      <Star size={12} />
                      {topic.stars || 0}
                    </span>
                    <span className="stat">
                      <GitFork size={12} />
                      {topic.posts_count}
                    </span>
                  </div>
                </div>
                <div className="trending-meta">
                  <span className="trending-language">
                    {topic.language || "Unknown"}
                  </span>
                  <span className="trending-score">
                    {Math.round(topic.trend_score)}
                  </span>
                </div>
                <div className="trending-description">{topic.description}</div>
                {topic.url && (
                  <a
                    href={topic.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="trending-link"
                  >
                    <ExternalLink size={12} />
                    View on GitHub
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TrendingTopics;
