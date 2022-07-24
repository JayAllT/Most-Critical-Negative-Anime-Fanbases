from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def main():
	profile_urls = []

	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get("https://myanimelist.net/topanime.php")

	# go through top 50 anime
	for anime in range(25):
		try:
			# get top anime
			top_anime = driver.find_elements(By.CLASS_NAME, "ml12")

			# page down once for each 8 anime loop has already been through
			for i in range(anime // 8):
				driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

			# click on anime
			top_anime[anime].click()
			time.sleep(0.5)

			driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[3]/td/div[7]/span/a').click()
			time.sleep(1)

			# save profile urls of users who leave > 6/10 reviews in first 10 pages of reviews or less if anime does not have more than 10 pages
			for i in range(9):
				reviews = driver.find_elements(By.CLASS_NAME, 'borderDark')
				for review in reviews:
					if int(review.find_element(By.CLASS_NAME, "mb8").find_elements(By.TAG_NAME, "div")[2].text.split(" ")[2]) < 6:
						profile = review.find_elements(By.TAG_NAME, "td")[1].text.split(" ")[0]
						profile_urls.append(f"https://myanimelist.net/profile/{profile}")

				# go to next page of reviews
				if i == 0:
					driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[2]/div[1]/div[6]/a').click()

				else:
					driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[2]/div[1]/div[6]/a[2]').click()

			# go back to top anime page
			driver.get("https://myanimelist.net/topanime.php")

		# skip anime and go to next if an error occurs
		except:
			time.sleep(30)
			driver.get("https://myanimelist.net/topanime.php")
			continue

	# remove duplicates
	profile_urls = list(dict.fromkeys(profile_urls))

	# save profile urls
	with open("profiles.dat", "w") as file:
		for url in profile_urls:
			file.write(f"{url}\n")


if __name__ == "__main__":
	main()