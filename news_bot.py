import os
import smtplib
from datetime import date
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup


def scrape_bbc():
    """Scrapes top headlines from BBC News."""
    headlines = []
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all card tracking links containing heading text elements
        anchors = soup.find_all("a", href=True)
        for a in anchors:
            heading = a.find("h2") or a.find("h3")
            if heading and len(heading.text.strip()) > 20:
                title = heading.text.strip()
                link = (
                    a["href"]
                    if a["href"].startswith("http")
                    else f"https://www.bbc.com{a['href']}"
                )

                if {"title": title, "link": link} not in headlines:
                    headlines.append({"title": title, "link": link})
            if len(headlines) >= 3:
                break
    except Exception as e:
        print(f"Error scraping BBC: {e}")

    return headlines


def scrape_the_guardian():
    """Scrapes top headlines from The Guardian."""
    headlines = []
    url = "https://www.theguardian.com/international"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Select custom data-link-name headers
        links = soup.find_all("a", attrs={"data-link-name": "article"})
        for link in links:
            title = link.text.strip()
            href = link["href"]
            if title and len(title) > 25 and href.startswith("http"):
                if {"title": title, "link": href} not in headlines:
                    headlines.append({"title": title, "link": href})
            if len(headlines) >= 3:
                break
    except Exception as e:
        print(f"Error scraping The Guardian: {e}")

    return headlines


def scrape_reuters():
    """Scrapes top headlines from Reuters."""
    headlines = []
    url = "https://www.reuters.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for custom components containing headings
        elements = soup.find_all("a", attrs={"data-testid": "Heading"})
        for el in elements:
            title = el.text.strip()
            href = el["href"]
            link = (
                href
                if href.startswith("http")
                else f"https://www.reuters.com{href}"
            )
            if title and len(title) > 15:
                if {"title": title, "link": link} not in headlines:
                    headlines.append({"title": title, "link": link})
            if len(headlines) >= 3:
                break
    except Exception as e:
        print(f"Error scraping Reuters: {e}")

    return headlines


def build_html_template(bbc, guardian, reuters):
    """Compiles extracted news lists into a clean HTML format template."""
    today_str = date.today().strftime("%A, %d %B %Y")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; background: #ffffff; margin: 0 auto; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 3px solid #1a365d; padding-bottom: 15px; margin-bottom: 20px; }}
            .header h1 {{ color: #1a365d; margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 1px; }}
            .header p {{ color: #718096; margin: 5px 0 0 0; font-size: 14px; }}
            .source-section {{ margin-bottom: 25px; }}
            .source-title {{ font-size: 16px; color: #2b6cb0; font-weight: bold; border-left: 4px solid #2b6cb0; padding-left: 10px; margin-bottom: 12px; text-transform: uppercase; }}
            .news-item {{ margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px dashed #e2e8f0; }}
            .news-item:last-child {{ border-bottom: none; }}
            .news-title {{ font-size: 15px; font-weight: 500; color: #2d3748; text-decoration: none; display: block; line-height: 1.4; }}
            .news-title:hover {{ color: #3182ce; text-decoration: underline; }}
            .meta-time {{ font-size: 11px; color: #a0aec0; margin-top: 4px; display: block; }}
            .footer {{ text-align: center; font-size: 12px; color: #a0aec0; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Pulse Daily News Digest</h1>
                <p>{today_str} • Morning Edition</p>
            </div>
    """

    # Add Section Helper
    def add_section(source_name, items):
        section_html = f'<div class="source-section"><div class="source-title">{source_name}</div>'
        if not items:
            section_html += '<p style="font-size:13px; color:#a0aec0; italic">No headlines successfully captured today.</p>'
        for item in items:
            section_html += f"""
            <div class="news-item">
                <a class="news-title" href="{item['link']}" target="_blank">Concrete • {item['title']}</a>
                <span class="meta-time">Published: Morning Edition • Live Feed</span>
            </div>
            """
        section_html += "</div>"
        return section_html

    html_content += add_section("BBC World News", bbc)
    html_content += add_section("The Guardian", guardian)
    html_content += add_section("Reuters", reuters)

    html_content += """
            <div class="footer">
                <p>Automated briefing generated via Python & GitHub Actions.<br>You are receiving this because your portfolio automation suite is active.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def send_news_email(html_body):
    """Logs into mail gateway and broadcasts the HTML body summary bundle."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or not sender_password or not receiver_email:
        print("⚠️ Email environment configurations missing. Aborting send.")
        return

    msg = EmailMessage()
    msg["Subject"] = f"📰 Morning Briefing: Top Headlines — {date.today().strftime('%d %B')}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Specify HTML formatting subtype layout
    msg.set_content(
        "Please look at this email via an HTML-compatible client reader window."
    )
    msg.add_alternative(html_body, subtype="html")

    try:
        print("Opening routing tunnel to SMTP relay mail servers...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("🚀 HTML Briefing package safely sent to target receiver!")
    except Exception as e:
        print(f"❌ Mail system failure: {e}")


def run():
    print("Initializing active scraping procedures...")
    bbc_news = scrape_bbc()
    guardian_news = scrape_the_guardian()
    reuters_news = scrape_reuters()

    print(
        f"Scraping metrics acquired -> BBC: {len(bbc_news)}, Guardian: {len(guardian_news)}, Reuters: {len(reuters_news)}"
    )

    # Compile the layout structure
    full_html = build_html_template(bbc_news, guardian_news, reuters_news)

    # Disseminate Email Briefing
    send_news_email(full_html)


if __name__ == "__main__":
    run()
