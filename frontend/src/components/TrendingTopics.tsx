import React from "react";
import {
  Star,
  GitFork,
  ExternalLink,
  MessageCircle,
  ArrowUp,
  Github,
  MessageSquare,
} from "lucide-react";

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
      <>
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Github className="card-icon" />
              Trending GitHub Repositories
            </div>
            <div className="trend-count">Loading...</div>
          </div>
          <div className="card-content">
            <div className="loading">Loading GitHub repositories...</div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <MessageSquare className="card-icon" />
              Trending Reddit Discussions
            </div>
            <div className="trend-count">Loading...</div>
          </div>
          <div className="card-content">
            <div className="loading">Loading Reddit discussions...</div>
          </div>
        </div>
      </>
    );
  }

  // Separate GitHub and Reddit content
  const githubRepos = trendingData.filter(
    (topic) => topic.platform === "GitHub" || topic.type === "repository"
  );
  const redditPosts = trendingData.filter(
    (topic) => topic.platform === "Reddit" || topic.type === "discussion"
  );

  return (
    <>
      {/* GitHub Repositories Card */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Github className="card-icon" />
            Trending GitHub Repositories
          </div>
          <div className="trend-count">{githubRepos.length}</div>
        </div>
        <div className="card-content">
          {githubRepos.length > 0 ? (
            <div className="trending-list">
              {githubRepos.slice(0, 8).map((repo, index) => (
                <div key={repo.id} className="trending-item github-item">
                  <div className="trending-rank">#{index + 1}</div>
                  <div className="trending-info">
                    <div className="trending-header">
                      <div className="trending-name">{repo.keyword}</div>
                      <div className="trending-stats">
                        <span className="stat">
                          <Star size={12} />
                          {(repo.stars || 0).toLocaleString()}
                        </span>
                        <span className="stat">
                          <GitFork size={12} />
                          {(repo.posts_count || 0).toLocaleString()}
                        </span>
                      </div>
                    </div>

                    <div className="trending-meta">
                      <span className="trending-language">
                        {repo.language || "Unknown"}
                      </span>
                      <span className="trending-score">
                        {Math.round(repo.trend_score)}
                      </span>
                    </div>

                    <div className="trending-description">
                      {repo.description}
                    </div>

                    {repo.url && (
                      <a
                        href={repo.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="trending-link"
                      >
                        <ExternalLink size={12} />
                        View Repository
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">
              <p>No GitHub repositories available</p>
              <small>API may be loading or experiencing issues</small>
            </div>
          )}

          {/* GitHub Summary */}
          {githubRepos.length > 0 && (
            <div className="platform-summary">
              <div className="summary-row">
                <span>
                  <strong>Total Stars:</strong>{" "}
                  {githubRepos
                    .reduce((sum, repo) => sum + (repo.stars || 0), 0)
                    .toLocaleString()}
                </span>
                <span>
                  <strong>Total Forks:</strong>{" "}
                  {githubRepos
                    .reduce((sum, repo) => sum + (repo.posts_count || 0), 0)
                    .toLocaleString()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Reddit Discussions Card */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <MessageSquare className="card-icon" />
            Trending Reddit Discussions
          </div>
          <div className="trend-count reddit-count">{redditPosts.length}</div>
        </div>
        <div className="card-content">
          {redditPosts.length > 0 ? (
            <div className="trending-list">
              {redditPosts.slice(0, 8).map((post, index) => (
                <div key={post.id} className="trending-item reddit-item">
                  <div className="trending-rank reddit-rank">#{index + 1}</div>
                  <div className="trending-info">
                    <div className="trending-header">
                      <div className="trending-name">{post.keyword}</div>
                      <div className="trending-stats">
                        <span className="stat reddit-stat">
                          <ArrowUp size={12} />
                          {(post.score || 0).toLocaleString()}
                        </span>
                        <span className="stat reddit-stat">
                          <MessageCircle size={12} />
                          {(post.posts_count || 0).toLocaleString()}
                        </span>
                      </div>
                    </div>

                    <div className="trending-meta">
                      <span className="trending-subreddit">
                        r/{post.subreddit || "programming"}
                      </span>
                      <span className="trending-score">
                        {Math.round(post.trend_score)}
                      </span>
                    </div>

                    <div className="trending-description">
                      {post.description}
                    </div>

                    {post.url && (
                      <a
                        href={post.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="trending-link reddit-link"
                      >
                        <ExternalLink size={12} />
                        View Discussion
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data reddit-no-data">
              <p>No Reddit discussions available</p>
              <small>Reddit API may be experiencing issues</small>
            </div>
          )}

          {/* Reddit Summary */}
          {redditPosts.length > 0 && (
            <div className="platform-summary reddit-summary">
              <div className="summary-row">
                <span>
                  <strong>Total Upvotes:</strong>{" "}
                  {redditPosts
                    .reduce((sum, post) => sum + (post.score || 0), 0)
                    .toLocaleString()}
                </span>
                <span>
                  <strong>Total Comments:</strong>{" "}
                  {redditPosts
                    .reduce((sum, post) => sum + (post.posts_count || 0), 0)
                    .toLocaleString()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default TrendingTopics;
