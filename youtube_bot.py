import os
import time
import random
import logging
from pathlib import Path
from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ProfileConfig:
    """Real Chrome profile configuration"""
    folder_id: str = "1bLSRdF8_BY-egYAZ7pO0Ae9taTtewXwa"
    local_profile_path: str = "user_data"

class ChromeProfileManager:
    """Download and verify real Chrome profile"""
    
    def __init__(self, config: ProfileConfig = ProfileConfig()):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def download_profile_from_drive(self) -> bool:
        try:
            # Try to import gdown, if not available skip
            try:
                import gdown
            except ImportError:
                self.logger.warning("⚠️ gdown not installed, skipping profile download")
                return False
                
            url = f"https://drive.google.com/drive/folders/{self.config.folder_id}"
            self.logger.info("⏳ Downloading profile from Drive...")
            gdown.download_folder(url, output=self.config.local_profile_path, quiet=False, use_cookies=False)

            # Verify History exists
            history_file = Path(self.config.local_profile_path) / "History"
            if history_file.exists():
                self.logger.info(f"✅ Profile verified. History size: {history_file.stat().st_size / 1024 / 1024:.2f} MB")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Download failed: {e}")
            return False

class YouTubeBot:
    def __init__(self, profile_path: str = "user_data"):
        self.profile_path = os.path.abspath(profile_path)
        self.driver = None
        self.view_percentages = [60, 70, 75, 80, 90, 100]
        self.search_keywords = [
            "football with messi",
            "elon musk speech", 
            "ai networking tutorial"
        ]
        self.target_url = "https://www.youtube.com/watch?v=fAiusB0kS_g"
        
    def get_random_user_agent(self):
        """Return random user agent (mobile or desktop)"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36"
        ]
        return random.choice(user_agents)
    
    def create_driver(self):
        """Create undetected Chrome driver with random user agent"""
        # Create fresh options each time
        options = uc.ChromeOptions()
        
        # Add user agent
        options.add_argument(f'--user-agent={self.get_random_user_agent()}')
        
        # Basic options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Random window size
        if random.choice(['desktop', 'mobile']) == 'mobile':
            options.add_argument('--window-size=375,812')
        else:
            options.add_argument('--window-size=1366,768')
        
        # Use real profile if exists
        profile_default = os.path.join(self.profile_path, "Default")
        if os.path.exists(profile_default):
            options.add_argument(f'--user-data-dir={self.profile_path}')
            options.add_argument('--profile-directory=Default')
            logger.info(f"Using profile from: {self.profile_path}")
        
        # Create driver
        driver = uc.Chrome(options=options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def random_mouse_move(self):
        """Random mouse movement"""
        try:
            action = ActionChains(self.driver)
            x = random.randint(-200, 200)
            y = random.randint(-100, 100)
            action.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.2, 0.5))
            action.move_by_offset(-x, -y).perform()
        except:
            pass
    
    def scroll_page(self, times=None):
        """Natural scrolling"""
        if times is None:
            times = random.randint(2, 4)
        
        for _ in range(times):
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
            
            # Type like human
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
                duration_elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-time-duration"))
                )
                if duration_elem:
                    duration_text = duration_elem.text
                    parts = duration_text.split(':')
                    if len(parts) == 2:
                        total_seconds = int(parts[0]) * 60 + int(parts[1])
                    elif len(parts) == 3:
                        total_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            except:
                pass
            
            if total_seconds > 0 and total_seconds < 1800:  # Less than 30 min
                watch_time = int(total_seconds * (duration_percent / 100))
                watch_time = min(watch_time, total_seconds - 5)
                logger.info(f"Watching {duration_percent}% ({watch_time}s of {total_seconds}s)")
            else:
                watch_time = random.randint(45, 90)
                logger.info(f"Watching {watch_time} seconds (fallback)")
            
            # Click play if needed
            try:
                play_button = self.driver.find_element(By.CSS_SELECTOR, ".ytp-play-button")
                if play_button and "ytp-play-button" in play_button.get_attribute("class"):
                    play_button.click()
                    time.sleep(1)
            except:
                pass
            
            # Watch video
            elapsed = 0
            while elapsed < watch_time:
                sleep_time = min(random.randint(8, 12), watch_time - elapsed)
                time.sleep(sleep_time)
                elapsed += sleep_time
                
                # Random interactions
                if random.random() < 0.2:
                    self.random_mouse_move()
            
            return True
                
        except Exception as e:
            logger.error(f"Watch error: {e}")
            time.sleep(random.randint(30, 60))
            return False
    
    def run_cycle(self):
        """Run one complete cycle of the bot"""
        try:
            # Create new driver
            logger.info("🚀 Creating Chrome driver...")
            self.driver = self.create_driver()
            
            # Start on YouTube
            logger.info("📺 Opening YouTube...")
            self.driver.get("https://www.youtube.com")
            time.sleep(random.uniform(3, 5))
            
            # First random search
            keyword = random.choice(self.search_keywords)
            logger.info(f"🔍 Searching for: {keyword}")
            self.search_youtube(keyword)
            self.scroll_page()
            
            # Go to target video
            logger.info("🎯 Navigating to target video")
            self.driver.get(self.target_url)
            time.sleep(random.uniform(3, 5))
            
            # Watch videos with different percentages
            for i, percent in enumerate(self.view_percentages):
                logger.info(f"📹 Cycle {i+1}/6 - Watching {percent}% of video")
                
                # Watch current video
                self.watch_video(percent)
                
                if i < len(self.view_percentages) - 1:
                    # Go to YouTube home
                    logger.info("🏠 Going to YouTube home")
                    self.driver.get("https://www.youtube.com")
                    time.sleep(random.uniform(2, 4))
                    
                    # Search for "google"
                    logger.info("🔎 Searching for 'google'")
                    self.search_youtube("google")
                    
                    # Random scroll and mouse movement
                    self.scroll_page(random.randint(2, 3))
                    self.random_mouse_move()
                    
                    # Click and watch random video for 5 seconds
                    try:
                        videos = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#video-title"))
                        )
                        if videos:
                            random_video = random.choice(videos[:8])
                            random_video.click()
                            logger.info("▶️ Watching random video for 5 seconds")
                            time.sleep(5)
                    except Exception as e:
                        logger.warning(f"Could not watch random video: {e}")
                    
                    # Navigate back to target video
                    logger.info("🔄 Navigating back to target video")
                    self.driver.get(self.target_url)
                    time.sleep(random.uniform(3, 5))
            
            logger.info("✅ All cycles completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error in cycle: {e}")
            return False
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("🔒 Browser closed")
                except:
                    pass
    
    def run(self):
        """Main run method"""
        success = self.run_cycle()
        if success:
            logger.info("✅ YouTube bot finished successfully")
        else:
            logger.error("❌ YouTube bot failed")

def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           YOUTUBE TRAFFIC BOT - Real Human Behavior         ║
    ║                    with Chrome Profile                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Try to download profile (optional)
    manager = ChromeProfileManager()
    profile_exists = manager.download_profile_from_drive()
    
    if profile_exists:
        print("✅ Chrome profile ready!")
    else:
        print("⚠️ Running without Chrome profile")
    
    # Initialize and run bot
    bot = YouTubeBot(profile_path=manager.config.local_profile_path)
    bot.run()

if __name__ == "__main__":
    main()
