
# 🪼 Phedeo - GitHub Email & Profile Lookup Tool

**Phedeo** is a powerful command-line tool to fetch public (and sometimes sensitive) GitHub user information, including email addresses when available. It combines multiple techniques to maximize the chance of finding a valid, non-noreply email associated with a GitHub username.

---

## ⚙️ Features

- 🔍 **Fetch GitHub account details:**
  - Name
  - Bio
  - Username
  - Avatar URL
  - Account creation date
  - Last update
  - User ID

- 📧 **Email extraction using multiple methods:**
  - Public events
  - GitHub commit history
  - External email resolver (`emailaddress.github.io`)
  - Repositories and associated commits

- ✅ Estimated 88% success rate for finding emails

---

## 🖥️ Supported Platforms

- Windows (fully supported)

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/seryannn/Phedeo-Project.git
cd Phedeo-Main-6.7
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Usage

Run the script with a GitHub username:

```bash
python phedeo.py {github_username}
```

Example:

```bash
python phedeo.py google
```

Phedeo will retrieve public information and attempt to find associated emails.


## 📜 Example Output

```text
--------------------------------------------------
[+] GitHub Profile Information
--------------------------------------------------
Name............: Google
Username........: google
Avatar URL......: https://avatars.githubusercontent.com/u/1342004?v=4
Last Update.....: 2024-08-09T17:36:18Z
Created At......: 2012-01-18T01:30:18Z
User ID.........: 1342004
--------------------------------------------------
[+] Sensitive Information:
--------------------------------------------------
Leaked Mail.....: 3
[1].............: mail@example.com
[2].............: mail@example.com
[3].............: mail@example.com
Noreply Mail....: noreply@example.com
--------------------------------------------------
[+] Advanced Search:
--------------------------------------------------
Phone Number....: None
Other Mails.....: 5
[1].............: mail@example.com
[2].............: mail@example.com
[3].............: mail@example.com
[4].............: mail@example.com
[5].............: mail@example.com
```

---

## 🛑 Disclaimer

**For educational and ethical use only.**
Accessing or attempting to retrieve private information without consent is illegal. The developer is not responsible for any misuse.

---

## 👨‍💻 Developer

* Name: **Seryan**
* Tool: **Phedeo**
* Status: `Working ✅`

> ⚠️ Limited to 60 requests per hour.

---

## 📌 License

Open-source under the [MIT License](LICENSE).

