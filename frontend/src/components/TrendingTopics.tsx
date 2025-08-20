import React from "react";
import { TrendingUp, MessageSquare } from "lucide-react";

interface TrendingTopic {
  id: number;
  keyword: string;
  platform: string;
  trend_score: number;
  posts_count: number;
  description: string;
}

interface TrendingTopicsProps {
  trendingData: {
    trending_topics: TrendingTopic[];
  };
}

const TrendingTopics: React.FC<TrendingTopicsProps> = ({ trendingData }) => {
  const getTrendColor = (score: number) => {
    if (score >= 90) return "#22c55e"; // Green
    if (score >= 70) return "#f59e0b"; // Yellow
    return "#ef4444"; // Red
  };

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case "github":
        return "#333";
      case "reddit":
        return "#ff4500";
      case "stackoverflow":
        return "#f48024";
      case "hackernews":
        return "#ff6600";
      default:
        return "#6b7280";
    }
  };

  return (
    <div className="dashboard-card trending-card">
      <div className="card-header">
        <TrendingUp className="w-6 h-6" />
        <h3>🔥 Trending Now</h3>
      </div>

      <div className="trending-list">
        {trendingData.trending_topics.map((topic) => (
          <div key={topic.id} className="trending-item">
            <div className="trending-main">
              <div className="trending-info">
                <h4 className="topic-keyword">{topic.keyword}</h4>
                <p className="topic-description">{topic.description}</p>
              </div>

              <div className="trending-metrics">
                <div
                  className="trend-score"
                  style={{ backgroundColor: getTrendColor(topic.trend_score) }}
                >
                  {topic.trend_score}
                </div>
              </div>
            </div>

            <div className="trending-footer">
              <span
                className="platform-badge"
                style={{ backgroundColor: getPlatformColor(topic.platform) }}
              >
                {topic.platform}
              </span>

              <div className="posts-count">
                <MessageSquare className="w-4 h-4" />
                <span>{topic.posts_count} posts</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrendingTopics;
