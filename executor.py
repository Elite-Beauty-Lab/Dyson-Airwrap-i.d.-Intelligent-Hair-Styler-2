"""
Professional Traffic Simulation - REAL Chrome Profile Integration
Version: 6.0.0 - Advanced Human Interaction Simulation
"""

import os
import time
import random
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ======================================================================
# Configuration
# ======================================================================

@dataclass
class ProfileConfig:
    """Real Chrome profile configuration"""
    folder_id: str = "1bLSRdF8_BY-egYAZ7pO0Ae9taTtewXwa"
    local_profile_path: str = "user_data"


@dataclass
class BehaviorConfig:
    """Human-like behavior parameters"""
    min_dwell_time: int = 30  # seconds
    max_dwell_time: int = 90  # seconds
    scroll_delay_min: float = 1.5
    scroll_delay_max: float = 4.0
    click_probability: float = 0.4  # 40% chance to click on links
    mouse_move_probability: float = 0.7  # 70% chance to move mouse randomly


class ChromeProfileManager:
    """Download and verify real Chrome profile"""
    
    def __init__(self, config: ProfileConfig = ProfileConfig()):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def download_profile_from_drive(self) -> bool:
        try:
            import gdown
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


# ======================================================================
# Human-like Browsing Simulator (Enhanced)
# ======================================================================

class AdvancedHumanSimulator:
    """Stealth browser using real Chrome profile with advanced human simulation"""
    
    def __init__(self, profile_path: str, behavior_config: BehaviorConfig = BehaviorConfig()):
        self.profile_path = os.path.abspath(profile_path)
        self.behavior = behavior_config
        self.logger = logging.getLogger(__name__)
        self.driver: Optional[webdriver.Chrome] = None

    def create_stealth_driver(self) -> webdriver.Chrome:
        """Create Chrome driver with stealth settings"""
        options = Options()
        options.add_argument(f"--user-data-dir={self.profile_path}")
        options.add_argument("--profile-directory=.")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set realistic viewport
        driver.set_window_size(1920, 1080)
        
        return driver

    def random_mouse_movement(self):
        """Simulate random mouse movements"""
        if random.random() < self.behavior.mouse_move_probability:
            try:
                action = ActionChains(self.driver)
                x_offset = random.randint(-200, 200)
                y_offset = random.randint(-100, 100)
                action.move_by_offset(x_offset, y_offset).perform()
                time.sleep(random.uniform(0.3, 0.8))
                # Move back to center
                action.move_by_offset(-x_offset, -y_offset).perform()
            except Exception:
                pass

    def natural_scroll_with_pauses(self):
        """Simulate natural reading behavior with scrolling pauses"""
        try:
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            current_pos = 0
            scroll_count = 0
            max_scrolls = random.randint(5, 15)
            
            while current_pos < total_height and scroll_count < max_scrolls:
                # Random scroll amount (smaller for reading simulation)
                step = random.randint(150, 400)
                current_pos += step
                
                # Smooth scroll
                self.driver.execute_script(f"""
                    window.scrollTo({{
                        top: {current_pos},
                        behavior: 'smooth'
                    }});
                """)
                
                # Random pause (simulates reading)
                pause_time = random.uniform(self.behavior.scroll_delay_min, self.behavior.scroll_delay_max)
                time.sleep(pause_time)
                
                # Random mouse movement during reading
                self.random_mouse_movement()
                
                scroll_count += 1
                
                # Sometimes scroll back up a bit (like re-reading)
                if random.random() < 0.2 and current_pos > 300:
                    back_scroll = random.randint(50, 150)
                    current_pos -= back_scroll
                    self.driver.execute_script(f"window.scrollTo(0, {current_pos});")
                    time.sleep(random.uniform(1, 2))
            
            # Scroll back to top slowly (like finishing reading)
            time.sleep(random.uniform(2, 4))
            self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
            
        except Exception as e:
            self.logger.warning(f"Scroll simulation error: {e}")

    def find_and_click_random_links(self):
        """Find and click on random internal links"""
        if random.random() > self.behavior.click_probability:
            self.logger.info("⏭️ Skipping random clicks this session")
            return
        
        try:
            # Find all anchor tags
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            # Filter for internal or relevant links
            valid_links = []
            for link in links:
                try:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    if href and href.startswith("http") and len(text) > 0:
                        valid_links.append(link)
                except:
                    continue
            
            if valid_links and len(valid_links) > 0:
                # Click 1-3 random links
                clicks_to_make = min(random.randint(1, 3), len(valid_links))
                clicked_links = random.sample(valid_links, clicks_to_make)
                
                for idx, link in enumerate(clicked_links):
                    try:
                        link_text = link.text[:50] if link.text else "No text"
                        self.logger.info(f"🖱️ Clicking link {idx+1}/{clicks_to_make}: '{link_text}'")
                        
                        # Scroll to link before clicking
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
                        time.sleep(random.uniform(0.5, 1))
                        
                        # Click with ActionChains for realism
                        ActionChains(self.driver).move_to_element(link).pause(random.uniform(0.2, 0.5)).click().perform()
                        
                        # Wait for page load
                        time.sleep(random.uniform(3, 6))
                        
                        # If not last click, go back
                        if idx < clicks_to_make - 1:
                            self.driver.back()
                            time.sleep(random.uniform(2, 4))
                            
                    except Exception as e:
                        self.logger.warning(f"Could not click link: {e}")
                        continue
                        
        except Exception as e:
            self.logger.warning(f"Link finding error: {e}")

    def interact_with_elements(self):
        """Interact with various page elements (buttons, images, etc.)"""
        try:
            # Find clickable elements
            clickable_selectors = [
                "button", ".btn", "[role='button']", 
                ".feature-card", ".product-card", ".slider-nav"
            ]
            
            for selector in clickable_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and random.random() < 0.3:
                    element = random.choice(elements)
                    try:
                        self.logger.info(f"🎯 Interacting with element: {selector}")
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        time.sleep(random.uniform(0.5, 1.5))
                        
                        # Hover first
                        ActionChains(self.driver).move_to_element(element).pause(0.5).perform()
                        time.sleep(random.uniform(0.5, 1))
                        
                        # Click if not already clicked
                        if random.random() < 0.5:
                            element.click()
                            time.sleep(random.uniform(2, 4))
                            self.driver.back()
                            time.sleep(random.uniform(1, 2))
                            
                    except Exception:
                        continue
                        
        except Exception as e:
            self.logger.warning(f"Element interaction error: {e}")

    def simulate_reading_behavior(self):
        """Simulate realistic reading with eye-tracking-like pauses"""
        paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
        if paragraphs:
            # "Read" 3-7 random paragraphs
            num_to_read = min(random.randint(3, 7), len(paragraphs))
            selected = random.sample(paragraphs, num_to_read)
            
            for para in selected:
                try:
                    # Scroll to paragraph
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", para)
                    time.sleep(random.uniform(2, 5))  # Time to "read"
                    
                    # Random mouse movement on paragraph
                    self.random_mouse_movement()
                    
                except Exception:
                    continue

    def get_random_user_agent(self) -> str:
        """Return a realistic user agent string"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(user_agents)

    def simulate_natural_browsing(self, target_url: str, use_google: bool = True) -> bool:
        """
        Complete natural browsing simulation
        
        Args:
            target_url: The URL to simulate traffic for
            use_google: Whether to come from Google search
        """
        try:
            # Load AI queries
            queries = self._load_queries()
            query = random.choice(queries) if queries else "dyson airwrap i.d. review 2025"
            
            if use_google:
                # --- Google search simulation ---
                self.logger.info(f"🔍 Searching Google for: {query}")
                self.driver.get("https://www.google.com")
                time.sleep(random.uniform(2, 4))
                
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                
                # Type like a human
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                # Random pause before submitting
                time.sleep(random.uniform(0.5, 1.5))
                search_box.submit()
                
                # Wait for results
                time.sleep(random.uniform(3, 6))
                
                # Scroll through results
                self._scroll_search_results()
            
            # --- Navigate to target page ---
            self.logger.info(f"🎯 Navigating to target: {target_url}")
            self.driver.get(target_url)
            
            # Wait for page to fully load
            time.sleep(random.uniform(2, 4))
            
            # --- Simulate human behavior on page ---
            
            # 1. Initial scan (quick scroll)
            self.logger.info("📖 Initial page scan...")
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(random.uniform(1, 2))
            
            # 2. Read content
            self.logger.info("📚 Reading content...")
            self.simulate_reading_behavior()
            
            # 3. Natural scrolling with pauses
            self.logger.info("📜 Natural scrolling simulation...")
            self.natural_scroll_with_pauses()
            
            # 4. Interact with elements
            self.logger.info("🖱️ Element interactions...")
            self.interact_with_elements()
            
            # 5. Click random links
            self.logger.info("🔗 Random link clicking...")
            self.find_and_click_random_links()
            
            # 6. Final dwell time
            dwell_time = random.randint(self.behavior.min_dwell_time, self.behavior.max_dwell_time)
            self.logger.info(f"⏱️ Final dwell time: {dwell_time} seconds")
            
            # Random micro-interactions during dwell time
            elapsed = 0
            while elapsed < dwell_time:
                sleep_chunk = min(random.randint(5, 15), dwell_time - elapsed)
                time.sleep(sleep_chunk)
                elapsed += sleep_chunk
                
                # Random scroll or mouse move during dwell
                if random.random() < 0.3:
                    scroll_amount = random.randint(-100, 200)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                self.random_mouse_movement()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Simulation error: {e}")
            return False
    
    def _load_queries(self) -> List[str]:
        """Load search queries from file or use defaults"""
        if Path("search_queries.txt").exists():
            with open("search_queries.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        
        # Default queries
        return [
            "dyson airwrap i.d. review 2025",
            "intelligent hair styler dyson",
            "dyson airwrap vs competitors",
            "best hair styling tool 2026",
            "dyson airwrap i.d. discount",
            "dyson airwrap honest review",
            "does dyson airwrap damage hair",
            "dyson airwrap i.d. attachments guide"
        ]
    
    def _scroll_search_results(self):
        """Scroll through Google search results naturally"""
        for _ in range(random.randint(2, 5)):
            scroll_amount = random.randint(200, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1, 3))


# ======================================================================
# Main Execution
# ======================================================================

def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     ADVANCED TRAFFIC SIMULATOR - Real Human Behavior        ║
    ║                    Version 6.0.0                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Download and setup Chrome profile
    manager = ChromeProfileManager()
    if not manager.download_profile_from_drive():
        print("❌ Could not load profile. Check folder ID or gdown installation.")
        return
    
    # Initialize simulator
    simulator = AdvancedHumanSimulator(manager.config.local_profile_path)
    
    # Create driver
    print("🚀 Launching Chrome with real profile...")
    simulator.driver = simulator.create_stealth_driver()
    
    try:
        target_url = "https://elite-beauty-lab.github.io/Dyson-Airwrap-i.d.-Intelligent-Hair-Styler/"
        
        print(f"📍 Target URL: {target_url}")
        print("🎭 Starting human-like behavior simulation...\n")
        
        success = simulator.simulate_natural_browsing(target_url, use_google=True)
        
        if success:
            print("\n" + "="*60)
            print("✅ MISSION ACCOMPLISHED!")
            print("="*60)
            print(f"✨ Traffic successfully simulated with:")
            print(f"   • Real Chrome profile data")
            print(f"   • Natural scrolling & reading patterns")
            print(f"   • Random link interactions")
            print(f"   • Mouse movement simulation")
            print(f"   • Dwell time: {simulator.behavior.min_dwell_time}-{simulator.behavior.max_dwell_time} seconds")
            print("="*60)
        else:
            print("❌ Simulation encountered errors")
            
    except KeyboardInterrupt:
        print("\n⚠️ Simulation interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if simulator.driver:
            print("\n🔒 Closing browser...")
            simulator.driver.quit()
            print("👋 Session ended")


if __name__ == "__main__":
    main()
