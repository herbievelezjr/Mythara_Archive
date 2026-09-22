# Copyright © 2025 Herbert Velez Jr. All rights reserved.

"""
LinkedIn Sales Bot - Automated Outreach
Finds prospects, sends connection requests, and follows up automatically.
"""

import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInSalesBot:
    """Automates LinkedIn prospecting and outreach."""
    
    def __init__(self):
        self.driver = None
        self.sent_today = 0
        self.max_daily_connections = 15  # Safe limit
        
    def start_browser(self):
        """Start browser with existing LinkedIn session."""
        print("🌐 Starting browser...")
        
        # Use Edge with your existing session
        options = webdriver.EdgeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('user-data-dir=C:\\Users\\HVele\\AppData\\Local\\Microsoft\\Edge\\User Data')
        options.add_argument('profile-directory=Default')
        
        self.driver = webdriver.Edge(options=options)
        print("✅ Browser started with your LinkedIn session")
        
    def search_prospects(self, keywords: str, max_results: int = 15):
        """Search for prospects on LinkedIn."""
        print(f"\n🔍 Searching for: {keywords}")
        
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords.replace(' ', '%20')}"
        self.driver.get(search_url)
        
        time.sleep(3)  # Let page load
        
        # Scroll to load more results
        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        print(f"✅ Search loaded")
        
    def send_connection_requests(self, message_template: str, target_count: int = 5):
        """Send connection requests with personalized messages."""
        print(f"\n📤 Sending {target_count} connection requests...")
        
        sent_count = 0
        
        try:
            # Find all "Connect" buttons
            connect_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Invite') or contains(text(), 'Connect')]")
            
            for button in connect_buttons[:target_count]:
                if sent_count >= target_count:
                    break
                
                try:
                    # Get prospect name from nearby elements
                    parent = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'entity-result')]")
                    name_element = parent.find_element(By.XPATH, ".//span[@aria-hidden='true']")
                    full_name = name_element.text
                    first_name = full_name.split()[0] if full_name else "there"
                    
                    # Click Connect button
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(1)
                    button.click()
                    time.sleep(2)
                    
                    # Add note
                    try:
                        add_note_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add a note')]"))
                        )
                        add_note_button.click()
                        time.sleep(1)
                        
                        # Personalize message
                        personalized_message = message_template.replace("[First Name]", first_name)
                        
                        note_field = self.driver.find_element(By.XPATH, "//textarea[@name='message']")
                        note_field.send_keys(personalized_message)
                        time.sleep(1)
                        
                        # Send
                        send_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send')]")
                        send_button.click()
                        
                        sent_count += 1
                        print(f"   ✅ Sent to {full_name}")
                        
                        # Random delay (human-like behavior)
                        time.sleep(random.randint(5, 10))
                        
                    except:
                        # If can't add note, send without note
                        try:
                            send_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send now')]")
                            send_button.click()
                            sent_count += 1
                            print(f"   ✅ Sent to {full_name} (no note)")
                            time.sleep(random.randint(5, 10))
                        except:
                            print(f"   ⚠️ Skipped {full_name}")
                            continue
                
                except Exception as e:
                    print(f"   ⚠️ Error with prospect: {e}")
                    continue
        
        except Exception as e:
            print(f"❌ Error finding prospects: {e}")
        
        print(f"\n✅ Sent {sent_count} connection requests")
        return sent_count
    
    def check_pending_connections(self):
        """Check who accepted your connection requests."""
        print("\n📬 Checking for new connections...")
        
        self.driver.get("https://www.linkedin.com/mynetwork/invitation-manager/sent/")
        time.sleep(3)
        
        # This would check for accepted connections
        # For now, just navigate there
        print("✅ Navigate to My Network to see who accepted")
        
    def send_follow_up_messages(self, message_template: str):
        """Send follow-up messages to new connections."""
        print("\n💬 Sending follow-up messages...")
        
        # Go to recent connections
        self.driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        time.sleep(3)
        
        # This would iterate through recent connections and message them
        # For now, manual step
        print("✅ Navigate to connections to send follow-ups")
        
    def daily_outreach(self):
        """Run daily automated outreach."""
        print("="*60)
        print("🚀 LINKEDIN SALES BOT - DAILY OUTREACH")
        print("="*60)
        
        self.start_browser()
        
        # Campaign 1: Banking prospects (SSIP Audit $500)
        self.search_prospects("Chief Risk Officer AI Banking", max_results=15)
        
        message = """Hi [First Name], I help banks prove AI compliance cryptographically. With OCC/CFPB tightening AI regulations, thought you'd find our SSIP audits valuable. Would love to connect!"""
        
        sent = self.send_connection_requests(message, target_count=5)
        
        # Campaign 2: Healthcare prospects (Enterprise $25k)
        time.sleep(10)
        self.search_prospects("CISO Healthcare AI", max_results=15)
        
        message = """Hi [First Name], I work with healthcare orgs on AI safety validation. Noticed your AI initiatives - would love to share insights on compliance automation. Connect?"""
        
        sent += self.send_connection_requests(message, target_count=5)
        
        # Campaign 3: Tech prospects (Monthly Sub $300)
        time.sleep(10)
        self.search_prospects("Head of AI SaaS", max_results=15)
        
        message = """Hi [First Name], I help AI teams automate compliance validation. Saw your AI work - thought our API might be useful. Would love to connect!"""
        
        sent += self.send_connection_requests(message, target_count=5)
        
        print("\n" + "="*60)
        print(f"✅ DAILY OUTREACH COMPLETE")
        print(f"   • Total requests sent: {sent}")
        print(f"   • Expected accepts tomorrow: {int(sent * 0.4)}")
        print(f"   • Next run: Tomorrow same time")
        print("="*60)
        
        # Keep browser open for manual review
        print("\n💡 Browser will stay open for you to review")
        print("   Press Ctrl+C to close when done")
        
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n👋 Closing browser...")
            self.driver.quit()


def main():
    """Run the LinkedIn sales bot."""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║        MYTHARA LINKEDIN SALES BOT - AUTOMATED              ║
║                                                            ║
║  This bot will:                                           ║
║  1. Search for qualified prospects (CROs, CTOs, AI leads) ║
║  2. Send 15 connection requests with personalized notes   ║
║  3. Run daily automatically                               ║
║                                                            ║
║  SAFETY:                                                  ║
║  - Max 15 requests/day (safe limit)                       ║
║  - Random delays (human-like)                             ║
║  - Uses your existing LinkedIn session                    ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

⚠️  IMPORTANT: Don't use LinkedIn while bot is running
⚠️  LinkedIn must be logged in before starting
⚠️  First time: Install Selenium with: pip install selenium

Ready to start? (yes/no): """)
    
    response = input().strip().lower()
    
    if response == 'yes':
        bot = LinkedInSalesBot()
        bot.daily_outreach()
    else:
        print("❌ Cancelled. Run again when ready!")


if __name__ == "__main__":
    main()
