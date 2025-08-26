import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { TrendingUp, Users, Code, Star } from "lucide-react";

interface TrendingTopic {
  id: string | number;
  keyword: string;
  platform: string;
  trend_score: number;
  posts_count: number;
  description: string;
  language?: string;
  url?: string;
  stars?: number;
  score?: number; // Reddit score
  subreddit?: string; // Reddit subreddit
  type?: string; // 'repository' or 'discussion'
}

interface PlatformStatus {
  status: string;
  last_fetch: string;
  repos_count?: number;
  posts_count?: number;
  questions_count?: number;
  stories_count?: number;
  rate_limit_remaining?: number;
  subreddits_monitored?: number;
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
  total_posts_analyzed?: number;
  last_updated?: string;
  error?: string;
  message?: string;
}

interface LiveStatsProps {
  data: TrendingData | null;
  isLoading: boolean;
}

const LiveStats: React.FC<LiveStatsProps> = ({ data, isLoading }) => {
  if (isLoading) {
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <TrendingUp className="card-icon" />
            Live Statistics
          </div>
        </div>
        <div className="card-content">
          <div className="loading">Loading statistics...</div>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <TrendingUp className="card-icon" />
            Live Statistics
          </div>
        </div>
        <div className="card-content">
          <div className="error">No data available</div>
        </div>
      </div>
    );
  }

  // Separate GitHub and Reddit data for different visualizations
  const githubRepos =
    data.trending_topics?.filter(
      (topic) => topic.platform === "GitHub" || topic.type === "repository"
    ) || [];

  const redditPosts =
    data.trending_topics?.filter(
      (topic) => topic.platform === "Reddit" || topic.type === "discussion"
    ) || [];

  // Prepare chart data from GitHub repositories (stars vs forks)
  const githubChartData = githubRepos.slice(0, 8).map((topic) => ({
    name:
      topic.keyword.length > 10
        ? topic.keyword.substring(0, 10) + "..."
        : topic.keyword,
    stars: topic.stars || 0,
    forks: topic.posts_count || 0,
    score: Math.round(topic.trend_score || 0),
  }));

  // Prepare chart data from Reddit posts (score vs comments)
  const redditChartData = redditPosts.slice(0, 6).map((topic) => ({
    name:
      topic.keyword.length > 15
        ? topic.keyword.substring(0, 15) + "..."
        : topic.keyword,
    upvotes: topic.score || 0,
    comments: topic.posts_count || 0,
    subreddit: topic.subreddit || "programming",
  }));

  // Language distribution data from GitHub
  const languageData = data.language_stats
    ? Object.entries(data.language_stats)
        .map(([lang, stats]: [string, any]) => ({
          name: lang,
          value: stats.total_stars || 0,
          repos: stats.repos_count || 0,
        }))
        .slice(0, 6)
    : [];

  // Colors for the charts
  const GITHUB_COLORS = ["#667eea", "#00ff88"];
  const REDDIT_COLORS = ["#ff6b6b", "#ffc107"];
  const PIE_COLORS = [
    "#667eea",
    "#00ff88",
    "#ff6b6b",
    "#ffc107",
    "#ff9800",
    "#9c27b0",
  ];

  // Calculate totals
  const totalStars = githubRepos.reduce(
    (sum, topic) => sum + (topic.stars || 0),
    0
  );
  const totalForks = githubRepos.reduce(
    (sum, topic) => sum + (topic.posts_count || 0),
    0
  );
  const totalUpvotes = redditPosts.reduce(
    (sum, topic) => sum + (topic.score || 0),
    0
  );
  const totalComments = redditPosts.reduce(
    (sum, topic) => sum + (topic.posts_count || 0),
    0
  );

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <TrendingUp className="card-icon" />
          Multi-Platform Statistics
        </div>
        <div className="trend-count">Real-time data</div>
      </div>
      <div className="card-content">
        {/* Key Metrics */}
        <div className="stats-grid" style={{ marginBottom: "2rem" }}>
          <div className="stat-card">
            <div className="stat-value">{data.total_repos_analyzed || 0}</div>
            <div className="stat-label">GitHub Repos</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{data.total_posts_analyzed || 0}</div>
            <div className="stat-label">Reddit Posts</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{totalStars.toLocaleString()}</div>
            <div className="stat-label">Total Stars</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{totalUpvotes.toLocaleString()}</div>
            <div className="stat-label">Total Upvotes</div>
          </div>
        </div>

        {/* GitHub: Stars vs Forks Chart */}
        {githubChartData.length > 0 && (
          <div style={{ marginBottom: "2rem" }}>
            <h4
              style={{
                color: "#ffffff",
                marginBottom: "1rem",
                fontSize: "1.1rem",
              }}
            >
              <Star
                size={16}
                style={{ marginRight: "0.5rem", color: "#667eea" }}
              />
              GitHub Repository Stats
            </h4>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={githubChartData}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(255,255,255,0.1)"
                  />
                  <XAxis
                    dataKey="name"
                    stroke="#a0a0a0"
                    fontSize={12}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis stroke="#a0a0a0" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "rgba(0,0,0,0.8)",
                      border: "1px solid rgba(255,255,255,0.2)",
                      borderRadius: "8px",
                      color: "#ffffff",
                    }}
                  />
                  <Bar dataKey="stars" fill="#667eea" name="Stars" />
                  <Bar dataKey="forks" fill="#00ff88" name="Forks" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Reddit: Upvotes vs Comments Chart */}
        {redditChartData.length > 0 && (
          <div style={{ marginBottom: "2rem" }}>
            <h4
              style={{
                color: "#ffffff",
                marginBottom: "1rem",
                fontSize: "1.1rem",
              }}
            >
              <Users
                size={16}
                style={{ marginRight: "0.5rem", color: "#ff6b6b" }}
              />
              Reddit Discussion Stats
            </h4>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={redditChartData}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(255,255,255,0.1)"
                  />
                  <XAxis
                    dataKey="name"
                    stroke="#a0a0a0"
                    fontSize={12}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis stroke="#a0a0a0" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "rgba(0,0,0,0.8)",
                      border: "1px solid rgba(255,255,255,0.2)",
                      borderRadius: "8px",
                      color: "#ffffff",
                    }}
                  />
                  <Bar dataKey="upvotes" fill="#ff6b6b" name="Upvotes" />
                  <Bar dataKey="comments" fill="#ffc107" name="Comments" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Language Distribution (GitHub only) */}
        {languageData.length > 0 && (
          <div>
            <h4
              style={{
                color: "#ffffff",
                marginBottom: "1rem",
                fontSize: "1.1rem",
              }}
            >
              <Code
                size={16}
                style={{ marginRight: "0.5rem", color: "#667eea" }}
              />
              Language Distribution by Stars
            </h4>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={languageData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                  >
                    {languageData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={PIE_COLORS[index % PIE_COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "rgba(0,0,0,0.8)",
                      border: "1px solid rgba(255,255,255,0.2)",
                      borderRadius: "8px",
                      color: "#ffffff",
                    }}
                    formatter={(value: any, name: string) => [
                      `${value.toLocaleString()} stars`,
                      name,
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Multi-Platform API Status Footer */}
        <div
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            background: "rgba(255,255,255,0.03)",
            borderRadius: "8px",
            fontSize: "0.9rem",
            color: "#a0a0a0",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "1rem",
            }}
          >
            <span>
              GitHub API: {data.platforms?.github?.status || "unknown"}
              {data.platforms?.github?.rate_limit_remaining &&
                ` (${data.platforms.github.rate_limit_remaining} calls remaining)`}
            </span>
            <span>
              Reddit API: {data.platforms?.reddit?.status || "unknown"}
              {data.platforms?.reddit?.subreddits_monitored &&
                ` (${data.platforms.reddit.subreddits_monitored} subreddits)`}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveStats;
