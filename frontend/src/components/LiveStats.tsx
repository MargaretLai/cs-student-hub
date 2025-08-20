import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { BarChart3 } from "lucide-react";

interface TrendingTopic {
  id: number;
  keyword: string;
  platform: string;
  trend_score: number;
  posts_count: number;
  description: string;
}

interface LiveStatsProps {
  trendingData: {
    trending_topics: TrendingTopic[];
  };
}

const LiveStats: React.FC<LiveStatsProps> = ({ trendingData }) => {
  // Prepare data for the chart
  const chartData = trendingData.trending_topics.map((topic) => ({
    name:
      topic.keyword.length > 15
        ? topic.keyword.substring(0, 12) + "..."
        : topic.keyword,
    score: topic.trend_score,
    posts: topic.posts_count,
    platform: topic.platform,
  }));

  // Calculate summary stats
  const totalPosts = trendingData.trending_topics.reduce(
    (sum, topic) => sum + topic.posts_count,
    0
  );
  const avgTrendScore = Math.round(
    trendingData.trending_topics.reduce(
      (sum, topic) => sum + topic.trend_score,
      0
    ) / trendingData.trending_topics.length
  );
  const activePlatforms = new Set(
    trendingData.trending_topics.map((topic) => topic.platform)
  ).size;

  return (
    <div className="dashboard-card stats-card">
      <div className="card-header">
        <BarChart3 className="w-6 h-6" />
        <h3>📊 Live Stats</h3>
      </div>

      {/* Summary metrics */}
      <div className="stats-summary">
        <div className="stat-item">
          <span className="stat-value">{totalPosts}</span>
          <span className="stat-label">Total Posts</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{avgTrendScore}</span>
          <span className="stat-label">Avg Trend Score</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{activePlatforms}</span>
          <span className="stat-label">Active Platforms</span>
        </div>
      </div>

      {/* Trend chart */}
      <div className="chart-container">
        <h4>Trend Scores by Topic</h4>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="name"
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis />
            <Tooltip
              formatter={(value, name) => [
                value,
                name === "score" ? "Trend Score" : "Posts",
              ]}
              labelFormatter={(label) => `Topic: ${label}`}
            />
            <Bar dataKey="score" fill="#3b82f6" name="score" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default LiveStats;
