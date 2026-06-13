import os
import json
import requests

def fetch_my_github_projects(username):
    """Queries the GitHub REST API to capture all public repositories for the profile."""
    # Fetch up to 100 public repositories sorted by the most recent push event
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed"
    
    # Authenticate using the built-in GitHub Action runner token to bypass strict API rate limits
    token = os.getenv("PORTFOLIO_SYNC_TOKEN") or os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        print(f"Connecting to GitHub API for account: {username}...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to extract repositories from GitHub API: {e}")
        return []

def structure_portfolio_data(raw_repositories, portfolio_repo_name):
    """Filters out unwanted items and formats fields uniformly for frontend rendering."""
    compiled_projects = []
    
    for repo in raw_repositories:
        # 1. Skip private repositories or upstream source forks
        if repo.get("private") or repo.get("fork"):
            continue
            
        repo_name = repo.get("name")
        
        # 2. Skip meta profile repositories (like the special README repo or the portfolio itself)
        if repo_name == repo.get("owner", {}).get("login") or repo_name == portfolio_repo_name:
            continue
            
        # Clean up project titles (e.g., "pulse-summary-bot" -> "Pulse Summary Bot")
        formatted_name = repo_name.replace("-", " ").replace("_", " ").title()
        
        project_card = {
            "title": formatted_name,
            "raw_name": repo_name,
            "description": repo.get("description") or "No description provided yet. Check out the repository details via the link below!",
            "html_url": repo.get("html_url"),
            "homepage_live": repo.get("homepage") or None, # Captures GitHub Pages deploy links if present
            "primary_language": repo.get("language") or "Mixed",
            "stars_count": repo.get("stargazers_count", 0),
            "forks_count": repo.get("forks_count", 0),
            "last_pushed_at": repo.get("pushed_at")
        }
        
        compiled_projects.append(project_card)
        
    return compiled_projects

def main():
    # Capture environment properties directly from the automated GitHub Context container
    repo_full_path = os.getenv("GITHUB_REPOSITORY") # e.g. "username/portfolio"
    
    if repo_full_path:
        username, portfolio_repo_name = repo_full_path.split("/")
    else:
        # Fallbacks for manual local testing inside your VS Code terminal
        username = "snehasanthosh826"  # Replace with your actual GitHub username
        portfolio_repo_name = "portfolio"

    raw_repos = fetch_my_github_projects(username)
    if not raw_repos:
        print("⚠️ No repositories fetched. Aborting generation routine.")
        return
        
    refined_projects = structure_portfolio_data(raw_repos, portfolio_repo_name)
    
    # Save formatted manifest as projects.json directly in the workspace root layout
    output_filename = "projects.json"
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(refined_projects, file, indent=4, ensure_ascii=False)
        
    print(f"🚀 Success! Formatted and compiled {len(refined_projects)} repositories into {output_filename}")

if __name__ == "__main__":
    main()
