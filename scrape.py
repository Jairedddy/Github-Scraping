from github import Github
import csv
import os

# Authenticate using your GitHub token
token = "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"  # Replace with your token
g = Github(token)

# Clean company names
def clean_company(company):
    if company:
        company = company.strip().lstrip('@').upper()
    return company

# Fetch users from Basel with more than 10 followers
def get_users_from_basel():
    query = 'location:Basel followers:>10'
    return g.search_users(query)

# Save users to users.csv
def save_users_to_csv(users):
    with open('users.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        
        for user in users:
            try:
                writer.writerow([
                    user.login,
                    user.name or '',
                    clean_company(user.company or ''),
                    user.location or '',
                    user.email or '',
                    user.hireable,
                    user.bio or '',
                    user.public_repos,
                    user.followers,
                    user.following,
                    user.created_at
                ])
            except Exception as e:
                print(f"Error writing user data: {e}")

# Save repositories to repositories.csv
def save_repos_to_csv(users):
    with open('repositories.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
        
        for user in users:
            try:
                repos = user.get_repos()  # Get up to 500 repositories
                for repo in repos:
                    writer.writerow([
                        user.login,
                        repo.full_name,
                        repo.created_at,
                        repo.stargazers_count,
                        repo.watchers_count,
                        repo.language or '',
                        repo.has_projects,
                        repo.has_wiki,
                        repo.license.name if repo.license else ''
                    ])
            except Exception as e:
                print(f"Error writing repository data for {user.login}: {e}")

def main():
    users = get_users_from_basel()

    # Ensure both files are created
    if users.totalCount == 0:
        print("No users found in Basel with over 10 followers.")
        return

    # Save users to users.csv
    save_users_to_csv(users)
    
    # Save repositories to repositories.csv
    save_repos_to_csv(users)

if __name__ == '__main__':
    main()
