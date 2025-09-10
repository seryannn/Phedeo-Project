import requests
from colorama import Fore, init
import re
import sys
import time
import threading
import os
import random
import json
import csv
from bs4 import BeautifulSoup

init(autoreset=True)
os.system("title Phedeo")

asciiArt = f"""
{Fore.LIGHTYELLOW_EX}
                    ██████╗ ██╗  ██╗███████╗██████╗ ███████╗ ██████╗
                    ██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝██╔═══██╗
                    ██████╔╝███████║█████╗  ██║  ██║█████╗  ██║   ██║
                    ██╔═══╝ ██╔══██║██╔══╝  ██║  ██║██╔══╝  ██║   ██║
                    ██║     ██║  ██║███████╗██████╔╝███████╗╚██████╔╝
                    ╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝
{Fore.LIGHTMAGENTA_EX}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Fore.LIGHTWHITE_EX}
        [%] STATUS : {Fore.LIGHTGREEN_EX}Active
{Fore.LIGHTWHITE_EX}
        [%] Developer : {Fore.LIGHTYELLOW_EX}Seryan/Kazam
{Fore.LIGHTWHITE_EX}
        [%] Platform : {Fore.LIGHTYELLOW_EX}Windows
{Fore.LIGHTMAGENTA_EX}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def center_text(text, width=80):
    return text.center(width)

def slowprint(text, delay=0.01):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loadingAnimation(stopEvent):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stopEvent.is_set():
        print(Fore.LIGHTBLACK_EX + f"\r{center_text(f'[~] Fetching data... {chars[i % len(chars)]}')}", end="")
        time.sleep(0.1)
        i += 1
    print("\r", end="")

def loadUserAgentsFromFile(filePath):
    try:
        with open(filePath, "r") as file:
            userAgents = file.readlines()
            userAgents = [ua.strip() for ua in userAgents if ua.strip()]
        if not userAgents:
            raise ValueError("The file is empty or does not contain valid User Agents.")
        return userAgents
    except Exception as e:
        print(Fore.RED + f"Error loading User Agents : {e}")
        return []

def getRandomUserAgent(userAgents):
    if not userAgents:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    return random.choice(userAgents)

userAgentsFilePath = "api/githubapi/useragents.txt"
userAgents = loadUserAgentsFromFile(userAgentsFilePath)

def loadGitHubToken():
    tokenFilePath = "extra/gitoken.txt"
    try:
        with open(tokenFilePath, "r") as file:
            token = file.read().strip()
            if token:
                return token
    except Exception as e:
        print(Fore.RED + f"Error loading GitHub token : {e}")
    return None

def getHeadersWithToken():
    token = loadGitHubToken()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": getRandomUserAgent(userAgents)
    }
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def gtbGetUserInfo(username):
    url = f"https://api.github.com/users/{username}"
    headers = getHeadersWithToken()
    response = requests.get(url, headers=headers)
    print(f"\n[/] Response Status : {Fore.YELLOW}{response.status_code}\n")
    if response.status_code == 200:
        data = response.json()
        globalName = data.get("name") or username
        displayName = data.get("login")
        avatarUrl = data.get("avatar_url")
        lastUpdate = data.get("updated_at")
        createdAt = data.get("created_at")
        userId = data.get("id")
        email = data.get("email")
        publicRepos, followers, following = gtbGetUserStats(username)
        totalStars, repos = gtbGetStarredRepos(username)
        return globalName, displayName, avatarUrl, lastUpdate, createdAt, userId, email, publicRepos, followers, following, totalStars, repos
    return username, None, None, None, None, None, None, 0, 0, 0, 0, []

def gtbGetUserStats(username):
    url = f"https://api.github.com/users/{username}"
    headers = getHeadersWithToken()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        publicRepos = data.get("public_repos", 0)
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        return publicRepos, followers, following
    return 0, 0, 0

def gtbGetStarredRepos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = getHeadersWithToken()
    response = requests.get(url, headers=headers)
    repos = []
    totalStars = 0
    if response.status_code == 200:
        reposData = response.json()
        for repo in reposData:
            stars = repo.get("stargazers_count", 0)
            totalStars += stars
            repos.append((repo.get("name"), stars))
    return totalStars, repos

def gtbGetEmailFromEvents(username):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"User-Agent": getRandomUserAgent(userAgents)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = response.json()
            for event in events:
                if event.get('type') == 'PushEvent':
                    commits = event.get('payload', {}).get('commits', [])
                    for commit in commits:
                        author = commit.get('author', {})
                        email = author.get('email')
                        if email and 'noreply' not in email:
                            return email
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching events for {username} : {e}")
    return None

def gtbGetEmailFromEmailAddressSite(username):
    try:
        url = f"https://emailaddress.github.io/?user={username}"
        response = requests.get(url)
        if "Good news!" in response.text:
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response.text)
            for email in emails:
                if "noreply" not in email:
                    return email
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching email from emailaddress.github.io for {username} : {e}")
    return None

def gtbGetEmailFromCommitSearch(username):
    url = f"https://api.github.com/search/commits?q=author:{username}"
    headers = {"Accept": "application/vnd.github.cloak-preview", "User-Agent": getRandomUserAgent(userAgents)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("items", [])
            for item in items:
                commit = item.get("commit", {})
                author = commit.get("author", {})
                email = author.get("email")
                if email and "noreply" not in email:
                    return email
    except requests.RequestException as e:
        print(Fore.RED + f"Error searching commits for {username} : {e}")
    return None

def gtbGetEmailFromRepos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"User-Agent": getRandomUserAgent(userAgents)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                commitsUrl = repo['commits_url'].replace('{/sha}', '')
                commitsHeaders = {"User-Agent": getRandomUserAgent(userAgents)}
                commitsResponse = requests.get(commitsUrl, headers=commitsHeaders)
                if commitsResponse.status_code == 200:
                    commits = commitsResponse.json()
                    for commit in commits:
                        author = commit.get("commit", {}).get("author", {})
                        email = author.get("email")
                        if email and "noreply" not in email:
                            return email
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching repos for {username} : {e}")
    return None

def gtbGetEmailsFromPatchCommits(username):
    patchEmails = set()
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"User-Agent": getRandomUserAgent(userAgents)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                commitsUrl = repo['commits_url'].replace('{/sha}', '')
                commitsHeaders = {"User-Agent": getRandomUserAgent(userAgents)}
                commitsResponse = requests.get(commitsUrl, headers=commitsHeaders)
                if commitsResponse.status_code == 200:
                    commits = commitsResponse.json()
                    for commit in commits:
                        if 'files' in commit:
                            for file in commit['files']:
                                if file['filename'].endswith('.patch'):
                                    patchUrl = file['patch_url']
                                    patchResponse = requests.get(patchUrl, headers=commitsHeaders)
                                    if patchResponse.status_code == 200:
                                        patchContent = patchResponse.text
                                        matches = re.findall(r'<([^>]+)>', patchContent)
                                        emailMatches = [match for match in matches if '@' in match]
                                        patchEmails.update(emailMatches)
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching patch commits for {username} : {e}")
    return list(patchEmails)

def gtbAdvancedSearch(username, repos):
    phoneNumbers = set()
    proEmails = set()
    phonePattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    emailPattern = re.compile(r'[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z]{2,4})+', re.IGNORECASE)
    for repo in repos:
        readmeUrl = f"https://raw.githubusercontent.com/{username}/{repo}/master/README.md"
        try:
            response = requests.get(readmeUrl)
            if response.status_code == 200:
                readmeContent = response.text
                phoneNumbers.update(phonePattern.findall(readmeContent))
                emails = emailPattern.findall(readmeContent)
                filteredEmails = [email for email in emails if 'example' not in email.lower() and 'exemple' not in email.lower()]
                proEmails.update(filteredEmails)
        except requests.RequestException as e:
            print(Fore.RED + f"Error fetching README for {repo} : {e}")
    return list(phoneNumbers), list(proEmails)

def obfuscateEmail(email):
    if not email:
        return "N/A"
    local, domain = email.split('@')
    localObf = local[0] + '*' * (len(local) - 1)
    domainParts = domain.split('.')
    if len(domainParts) > 1:
        domainName = domainParts[0]
        domainExtension = '.'.join(domainParts[1:])
        domainObf = domainName[0] + '*' * (len(domainName) - 1) + '.' + domainExtension
    else:
        domainObf = domainParts[0]
    return localObf + '@' + domainObf

def gtbGetOrganizations(username):
    url = f"https://api.github.com/users/{username}/orgs"
    headers = {"User-Agent": getRandomUserAgent(userAgents)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orgs = response.json()
            return [org['login'] for org in orgs]
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching organizations for {username} : {e}")
    return []

def gtbGetOrganizationMembers(orgName):
    url = f"https://api.github.com/orgs/{orgName}/members"
    headers = {"User-Agent": getRandomUserAgent(userAgents)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            members = response.json()
            return [member['login'] for member in members]
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching members for organization {orgName} : {e}")
    return []

def exportResults(username, result, exportFormat):
    if exportFormat.lower() == "json":
        os.makedirs("output", exist_ok=True)
        filePath = f"output/{username}.json"
        with open(filePath, "w") as file:
            json.dump(result, file, indent=4)
        print(Fore.GREEN + f"\nResults exported to {filePath}\n")
    elif exportFormat.lower() == "csv":
        filePath = f"{username}.csv"
        with open(filePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Field", "Value"])
            for key, value in result["profileInfo"].items():
                writer.writerow([key, value])
            writer.writerow(["emails", ", ".join(result["emails"])])
            writer.writerow(["phoneNumbers", ", ".join(result["advancedSearch"]["phoneNumbers"])])
            writer.writerow(["proEmails", ", ".join(result["advancedSearch"]["proEmails"])])
            writer.writerow(["patchEmails", ", ".join(result["advancedSearch"]["patchEmails"])])
            writer.writerow(["organizations", ", ".join(result["organizations"])])
        print(Fore.GREEN + f"\nResults exported to {filePath}\n")

def handleApiLimit(response):
    if response.status_code == 403 and "API rate limit exceeded" in response.text:
        print(Fore.RED + "API rate limit exceeded.")
        useToken = input(Fore.LIGHTBLACK_EX + "Use a GitHub token? (yes/no) : ").strip().lower()
        if useToken == "yes":
            token = input(Fore.LIGHTBLACK_EX + "Enter your GitHub token : ").strip()
            tokenFilePath = "extra/gitoken.txt"
            with open(tokenFilePath, "w") as file:
                file.write(token)
            print(Fore.GREEN + "Token saved. Retrying...")
            return True
        else:
            print(Fore.RED + "Please wait and try again later.")
            return False
    return True

def display_results(username, result):
    print("\n" + " " * 20 + Fore.LIGHTMAGENTA_EX + "━" * 60)
    print(" " * 30 + Fore.LIGHTCYAN_EX + "[+] GITHUB PROFILE INFORMATION" + Fore.RESET)
    print(" " * 20 + Fore.LIGHTMAGENTA_EX + "─" * 60 + "\n")
    profile = result["profileInfo"]
    fields = [
        ("Name", profile.get("name", "N/A")),
        ("Username", profile.get("username", "N/A")),
        ("Avatar URL", profile.get("avatarUrl", "N/A")),
        ("Last Update", profile.get("lastUpdate", "N/A")),
        ("Created At", profile.get("createdAt", "N/A")),
        ("User ID", profile.get("userId", "N/A")),
        ("Public Repos", profile.get("publicRepos", 0)),
        ("Followers", profile.get("followers", 0)),
        ("Following", profile.get("following", 0)),
        ("Total Stars", profile.get("totalStars", 0))
    ]
    max_field_length = max(len(field[0]) for field in fields) + 4
    for field, value in fields:
        print(" " * 25 + Fore.LIGHTWHITE_EX + f"{field.ljust(max_field_length)}: " + Fore.LIGHTYELLOW_EX + f"{value}")
    print("\n" + " " * 25 + Fore.LIGHTWHITE_EX + "Repos:")
    repos = profile.get("repos", [])
    if repos:
        for repo in repos:
            if isinstance(repo, tuple) and len(repo) == 2:
                repo_name, stars = repo
                print(" " * 27 + Fore.LIGHTGREEN_EX + f"• {repo_name}" + Fore.LIGHTBLACK_EX + f" ({stars} stars)")
            else:
                print(" " * 27 + Fore.RED + f"• {repo} (invalid format)")
    else:
        print(" " * 27 + Fore.RED + "No repositories found.")
    print("\n" + " " * 20 + Fore.LIGHTMAGENTA_EX + "━" * 60)
    print(" " * 30 + Fore.LIGHTCYAN_EX + "[+] SENSITIVE INFORMATION" + Fore.RESET)
    print(" " * 20 + Fore.LIGHTMAGENTA_EX + "─" * 60 + "\n")
    foundEmails = result.get("emails", [])
    if foundEmails:
        print(" " * 25 + Fore.LIGHTWHITE_EX + f"Leaked Emails: " + Fore.LIGHTGREEN_EX + f"{len(foundEmails)}" + "\n")
        for idx, email in enumerate(foundEmails, 1):
            print(" " * 25 + Fore.LIGHTGREEN_EX + f"[{idx}] " + Fore.GREEN + f"{email}")
        print("\n" + " " * 25 + Fore.LIGHTWHITE_EX + "Obfuscated Emails:")
        for idx, email in enumerate(foundEmails, 1):
            obfuscated = obfuscateEmail(email)
            print(" " * 25 + Fore.LIGHTGREEN_EX + f"[{idx}] " + Fore.GREEN + f"{obfuscated}")
    else:
        print(" " * 25 + Fore.RED + "Leaked Emails: None")
    userId = profile.get("userId", "None")
    noreplyEmail = f"{userId}+{username}@users.noreply.github.com"
    print("\n" + " " * 25 + Fore.LIGHTWHITE_EX + "Noreply Email: " + Fore.LIGHTBLUE_EX + f"{noreplyEmail}")
    print(" " * 25 + Fore.LIGHTWHITE_EX + "Obfuscated Noreply: " + Fore.LIGHTBLUE_EX + f"{obfuscateEmail(noreplyEmail)}")
    print("\n" + " " * 20 + Fore.LIGHTMAGENTA_EX + "━" * 60)
    print(" " * 30 + Fore.LIGHTCYAN_EX + "[+] ADVANCED SEARCH RESULTS" + Fore.RESET)
    print(" " * 20 + Fore.LIGHTMAGENTA_EX + "─" * 60 + "\n")
    advanced = result.get("advancedSearch", {})
    phoneNumbers = advanced.get("phoneNumbers", [])
    proEmails = advanced.get("proEmails", [])
    patchEmails = advanced.get("patchEmails", [])
    organizations = result.get("organizations", [])
    def display_list(title, items, color):
        print(" " * 25 + Fore.LIGHTWHITE_EX + f"{title}: " + color + f"{len(items) if items else 'None'}")
        if items:
            for idx, item in enumerate(items, 1):
                print(" " * 25 + color + f"[{idx}] " + Fore.GREEN + f"{item}")
        print()
    display_list("Phone Numbers", phoneNumbers, Fore.LIGHTBLUE_EX)
    display_list("Other Emails", proEmails, Fore.LIGHTBLUE_EX)
    display_list("Patch Emails", patchEmails, Fore.LIGHTBLUE_EX)
    print(" " * 25 + Fore.LIGHTWHITE_EX + "Organizations: " + (Fore.LIGHTGREEN_EX if organizations else Fore.RED) + f"{len(organizations) if organizations else 'None'}")
    if organizations:
        for idx, org in enumerate(organizations, 1):
            print(" " * 25 + Fore.LIGHTGREEN_EX + f"[{idx}] " + Fore.GREEN + f"{org}")
            members = gtbGetOrganizationMembers(org)
            if members:
                print(" " * 27 + Fore.LIGHTBLACK_EX + "└ Members: " + Fore.LIGHTGREEN_EX + f"{len(members)}")
                for m_idx, member in enumerate(members, 1):
                    print(" " * 29 + Fore.LIGHTGREEN_EX + f"[{m_idx}] " + Fore.GREEN + f"{member}")
    print("\n" + " " * 20 + Fore.LIGHTMAGENTA_EX + "━" * 60 + "\n")

def gtbMailFinder(username):
    globalName, displayName, avatarUrl, lastUpdate, createdAt, userId, profileEmail, publicRepos, followers, following, totalStars, repos = gtbGetUserInfo(username)
    stopEvent = threading.Event()
    loadingThread = threading.Thread(target=loadingAnimation, args=(stopEvent,))
    loadingThread.start()
    methods = [
        gtbGetEmailFromEvents,
        gtbGetEmailFromEmailAddressSite,
        gtbGetEmailFromCommitSearch,
        gtbGetEmailFromRepos
    ]
    foundEmails = set()
    for method in methods:
        email = method(username)
        if email:
            foundEmails.add(email)
    if profileEmail:
        foundEmails.add(profileEmail)
    reposUrl = f"https://api.github.com/users/{username}/repos"
    headers = getHeadersWithToken()
    response = requests.get(reposUrl, headers=headers)
    repos_list = [repo['name'] for repo in response.json()] if response.status_code == 200 else []
    phoneNumbers, proEmails = gtbAdvancedSearch(username, repos_list)
    patchEmails = gtbGetEmailsFromPatchCommits(username)
    organizations = gtbGetOrganizations(username)
    stopEvent.set()
    loadingThread.join()
    result = {
        "profileInfo": {
            "name": globalName,
            "username": displayName,
            "avatarUrl": avatarUrl,
            "lastUpdate": lastUpdate,
            "createdAt": createdAt,
            "userId": userId,
            "publicRepos": publicRepos,
            "followers": followers,
            "following": following,
            "totalStars": totalStars,
            "repos": repos
        },
        "emails": list(foundEmails),
        "advancedSearch": {
            "phoneNumbers": phoneNumbers,
            "proEmails": proEmails,
            "patchEmails": patchEmails
        },
        "organizations": organizations
    }
    logDirectory = "logs"
    os.makedirs(logDirectory, exist_ok=True)
    logFilePath = os.path.join(logDirectory, f"{username}.json")
    with open(logFilePath, "w") as logFile:
        json.dump(result, logFile, indent=4)
    dbDirectory = os.path.join("output", "logsbase")
    os.makedirs(dbDirectory, exist_ok=True)
    dbFilePath = os.path.join(dbDirectory, "logs.txt")
    with open(dbFilePath, "a") as dbFile:
        for email in foundEmails:
            dbFile.write(f"{username} | {email}\n")
    display_results(username, result)
    exportFormat = input(Fore.LIGHTBLACK_EX + "\nExport results? (json/csv/no) : ").strip().lower()
    if exportFormat in ["json", "csv"]:
        exportResults(username, result, exportFormat)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print(Fore.YELLOW + asciiArt)
        gtbMailFinder(username)
    else:
        print(Fore.RED + "Usage : python phedeo.py {github_username}")
