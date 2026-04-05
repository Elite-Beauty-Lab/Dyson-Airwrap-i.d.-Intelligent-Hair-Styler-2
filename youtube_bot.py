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
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36"
        ]
        return random.choice(user_agents)
    
    def create_driver(self):
        """Create undetected Chrome driver with real profile and random user agent"""
        options = uc.ChromeOptions()
        
        # Use real Chrome profile if exists
        if os.path.exists(self.profile_path) and os.path.exists(os.path.join(self.profile_path, "Default")):
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--profile-directory=Default")
            logger.info(f"Using real Chrome profile from: {self.profile_path}")
        
        options.add_argument(f'--user-agent={self.get_random_user_agent()}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        # Random window size (desktop or mobile-like)
        if random.choice(['desktop', 'mobile']) == 'mobile':
            options.add_argument('--window-size=375,812')
        else:
            options.add_argument('--window-size=1920,1080')
        
        # Version-specific fix for undetected-chromedriver
        try:
            self.driver = uc.Chrome(options=options, version_main=120)
        except:
            self.driver = uc.Chrome(options=options)
        
        # Remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return self.driver
    
    def random_mouse_move(self):
        """Random mouse movement"""
        try:
            action = ActionChains(self.driver)
            x = random.randint(-300, 300)
            y = random.randint(-200, 200)
            action.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.2, 0.5))
            action.move_by_offset(-x, -y).perform()
        except:
            pass
    
    def scroll_page(self, times=None):
        """Natural scrolling"""
        if times is None:
            times = random.randint(2, 5)
        
        for _ in range(times):
            scroll = random.randint(300, 800)
            self.driver.execute_script(f"window.scrollBy(0, {scroll});")
            time.sleep(random.uniform(0.5, 1.5))
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
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(0.3, 0.8))
            search_box.submit()
            time.sleep(random.uniform(2, 4))
            return True
        except Exception as e:
            logger.error(f"Search error: {e}")
            return False
    
    def watch_video(self, duration_percent):
        """Watch video for specific percentage"""
        try:
            # Wait for video player
            time.sleep(3)
            
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
            
            if total_seconds > 0 and total_seconds < 3600:  # Less than 1 hour
                watch_time = int(total_seconds * (duration_percent / 100))
                watch_time = min(watch_time, total_seconds - 5)
                logger.info(f"Watching {duration_percent}% ({watch_time}s of {total_seconds}s)")
            else:
                # Fallback: watch random time
                watch_time = random.randint(30, 120)
                logger.info(f"Watching {watch_time} seconds (fallback)")
            
            # Click play if needed
            try:
                play_button = self.driver.find_element(By.CSS_SELECTOR, ".ytp-play-button")
                if "ytp-play-button" in play_button.get_attribute("class"):
                    play_button.click()
                    time.sleep(1)
            except:
                pass
            
            # Watch for calculated time
            elapsed = 0
            while elapsed < watch_time:
                sleep_time = min(random.randint(5, 15), watch_time - elapsed)
                time.sleep(sleep_time)
                elapsed += sleep_time
                
                # Random interactions while watching
                if random.random() < 0.15:
                    self.random_mouse_move()
                if random.random() < 0.1:
                    self.scroll_page(1)
            
            return True
                
        except Exception as e:
            logger.error(f"Watch error: {e}")
            time.sleep(random.randint(30, 90))
            return False
    
    def run_cycle(self):
        """Run one complete cycle of the bot"""
        driver = None
        try:
            # Create new driver with random user agent and real profile
            logger.info("Starting YouTube bot...")
            driver = self.create_driver()
            self.driver = driver
            driver.get("https://www.youtube.com")
            time.sleep(random.uniform(3, 5))
            
            # First random search
            keyword = random.choice(self.search_keywords)
            logger.info(f"Searching for: {keyword}")
            self.search_youtube(keyword)
            self.scroll_page()
            
            # Go to target video
            logger.info("Navigating to target video")
            driver.get(self.target_url)
            time.sleep(random.uniform(3, 5))
            
            # Watch videos with different percentages
            for i, percent in enumerate(self.view_percentages):
                logger.info(f"Cycle {i+1}/6 - Watching {percent}% of video")
                
                # Watch current video
                self.watch_video(percent)
                
                if i < len(self.view_percentages) - 1:  # Not last cycle
                    # Go to YouTube home
                    logger.info("Going to YouTube home")
                    driver.get("https://www.youtube.com")
                    time.sleep(random.uniform(2, 4))
                    
                    # Search for "google"
                    logger.info("Searching for 'google'")
                    self.search_youtube("google")
                    
                    # Random scroll and mouse movement
                    self.scroll_page(random.randint(2, 4))
                    self.random_mouse_move()
                    
                    # Click and watch random video for 5 seconds
                    try:
                        videos = driver.find_elements(By.CSS_SELECTOR, "#video-title")
                        if videos:
                            random_video = random.choice(videos[:10])
                            random_video.click()
                            time.sleep(5)
                            logger.info("Watched random video for 5 seconds")
                    except Exception as e:
                        logger.warning(f"Could not watch random video: {e}")
                    
                    # Navigate back to target video
                    logger.info("Navigating back to target video")
                    driver.get(self.target_url)
                    time.sleep(random.uniform(3, 5))
            
            logger.info("✅ All cycles completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in cycle: {e}")
            return False
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            self.driver = None
    
    def run(self):
        """Main run method"""
        success = self.run_cycle()
        if success:
            logger.info("YouTube bot finished successfully")
        else:
            logger.error("YouTube bot failed")

def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           YOUTUBE TRAFFIC BOT - Real Human Behavior         ║
    ║                    with Chrome Profile                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Download and setup Chrome profile (optional)
    manager = ChromeProfileManager()
    profile_exists = manager.download_profile_from_drive()
    
    if profile_exists:
        print("✅ Chrome profile loaded successfully!")
    else:
        print("⚠️ Could not load profile, continuing without it...")
    
    # Initialize and run bot
    bot = YouTubeBot(profile_path=manager.config.local_profile_path)
    bot.run()

if __name__ == "__main__":
    main()
