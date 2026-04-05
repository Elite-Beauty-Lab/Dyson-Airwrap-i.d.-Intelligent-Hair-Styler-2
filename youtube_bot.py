import os
import time
import random
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class YouTubeBot:
    def __init__(self):
        self.driver = None
        self.view_percentages = [60, 70, 75, 80, 90, 100]
        self.search_keywords = [
            "football with messi",
            "elon musk speech", 
            "ai networking tutorial"
        ]
        self.target_url = "https://www.youtube.com/watch?v=fAiusB0kS_g"
        
    def get_random_user_agent(self):
        """Return random user agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1"
        ]
        return random.choice(user_agents)
    
    def create_driver(self):
        """Create Chrome driver with proper version matching"""
        options = Options()
        
        # Random user agent
        options.add_argument(f'--user-agent={self.get_random_user_agent()}')
        
        # Headless mode for GitHub Actions
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Window size
        options.add_argument('--window-size=1366,768')
        
        # Disable notifications
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        
        # Create driver with automatic version management
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def random_mouse_move(self):
        """Random mouse movement simulation"""
        try:
            action = ActionChains(self.driver)
            x = random.randint(-100, 100)
            y = random.randint(-50, 50)
            action.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.1, 0.3))
            action.move_by_offset(-x, -y).perform()
        except:
            pass
    
    def scroll_page(self):
        """Natural scrolling"""
        scrolls = random.randint(2, 4)
        for _ in range(scrolls):
            scroll = random.randint(200, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll});")
            time.sleep(random.uniform(0.5, 1))
            if random.random() < 0.3:
                self.random_mouse_move()
    
    def search_youtube(self, query):
        """Search on YouTube"""
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.clear()
            
            # Human-like typing
            for char in query:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.12))
            
            time.sleep(random.uniform(0.3, 0.7))
            search_box.submit()
            time.sleep(random.uniform(2, 3))
            return True
        except Exception as e:
            logger.error(f"Search error: {e}")
            return False
    
    def watch_video(self, duration_percent):
        """Watch video for specific percentage"""
        try:
            time.sleep(2)
            
            # Try to get video duration
            total_seconds = 0
            try:
                duration_elem = self.driver.find_element(By.CSS_SELECTOR, ".ytp-time-duration")
                if duration_elem:
                    duration_text = duration_elem.text
                    parts = duration_text.split(':')
                    if len(parts) == 2:
                        total_seconds = int(parts[0]) * 60 + int(parts[1])
                    elif len(parts) == 3:
                        total_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            except:
                pass
            
            if total_seconds > 0 and total_seconds < 1800:
                watch_time = int(total_seconds * (duration_percent / 100))
                watch_time = min(watch_time, total_seconds - 5)
                logger.info(f"Watching {duration_percent}% ({watch_time}s of {total_seconds}s)")
            else:
                watch_time = random.randint(30, 60)
                logger.info(f"Watching {watch_time} seconds (fallback)")
            
            # Click play
            try:
                play_button = self.driver.find_element(By.CSS_SELECTOR, ".ytp-play-button")
                play_button.click()
                time.sleep(1)
            except:
                pass
            
            # Watch video
            time.sleep(min(watch_time, 60))
            return True
                
        except Exception as e:
            logger.error(f"Watch error: {e}")
            time.sleep(random.randint(20, 40))
            return False
    
    def run(self):
        """Main run method"""
        try:
            logger.info("🚀 Creating Chrome driver...")
            self.driver = self.create_driver()
            
            # Start on YouTube
            logger.info("📺 Opening YouTube...")
            self.driver.get("https://www.youtube.com")
            time.sleep(random.uniform(3, 5))
            
            # Random search
            keyword = random.choice(self.search_keywords)
            logger.info(f"🔍 Searching for: {keyword}")
            self.search_youtube(keyword)
            self.scroll_page()
            
            # Go to target video
            logger.info("🎯 Navigating to target video")
            self.driver.get(self.target_url)
            time.sleep(random.uniform(3, 5))
            
            # Watch video with different percentages
            for i, percent in enumerate(self.view_percentages):
                logger.info(f"📹 Cycle {i+1}/6 - Watching {percent}%")
                self.watch_video(percent)
                
                if i < len(self.view_percentages) - 1:
                    # YouTube home
                    logger.info("🏠 Going to YouTube home")
                    self.driver.get("https://www.youtube.com")
                    time.sleep(random.uniform(2, 4))
                    
                    # Search for "google"
                    logger.info("🔎 Searching for 'google'")
                    self.search_youtube("google")
                    self.scroll_page()
                    
                    # Random video for 5 seconds
                    try:
                        videos = self.driver.find_elements(By.CSS_SELECTOR, "#video-title")
                        if videos:
                            random.choice(videos[:5]).click()
                            logger.info("▶️ Watching random video for 5 seconds")
                            time.sleep(5)
                    except:
                        pass
                    
                    # Back to target
                    logger.info("🔄 Back to target video")
                    self.driver.get(self.target_url)
                    time.sleep(random.uniform(3, 5))
            
            logger.info("✅ All cycles completed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔒 Browser closed")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    YOUTUBE BOT - Simple & Stable             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    bot = YouTubeBot()
    bot.run()

if __name__ == "__main__":
    main()
