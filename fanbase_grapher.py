from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from matplotlib import pyplot as plt

def main():
	profile_urls = []
	driver = webdriver.Chrome(ChromeDriverManager().install())

	favourite_anime = []

	# get profile urls
	with open("profiles.dat", "r") as file:
		profile_urls = file.read().split("\n")
		profile_urls = [url for idx, url in enumerate(profile_urls) if idx < len(profile_urls) - 1]  # removes last, empty string from list

	# remove duplicate users
	profile_urls = list(dict.fromkeys(profile_urls))

	# loop through urls
	for url in profile_urls:
		driver.get(url)
		time.sleep(1)

		# add names of all favourite anime to favourite_anime list if user has any favourite anime
		try:
			fav_anime = driver.find_element(By.ID, "anime_favorites").find_elements(By.CLASS_NAME, "btn-fav")

			for anime in fav_anime:
				favourite_anime.append(anime.get_attribute("title"))

		except NoSuchElementException:
			continue

	anime_tallies = []
	occurring_anime = list(dict.fromkeys(favourite_anime))

	# count occurrences of anime
	for anime in occurring_anime:
		anime_tallies.append(favourite_anime.count(anime))

	# sort lists
	_1 = []
	_2 = []

	for i in range(len(anime_tallies)):
		_1.append(max(anime_tallies))
		_2.append(occurring_anime[anime_tallies.index(max(anime_tallies))])

		anime_tallies[anime_tallies.index(max(anime_tallies))] = -1

	anime_tallies = _1
	occurring_anime = _2

	# concentrate to top 25
	anime_tallies = [tally for idx, tally in enumerate(anime_tallies) if idx < 20]
	occurring_anime = [tally for idx, tally in enumerate(occurring_anime) if idx < 20]

	# reverse lists
	anime_tallies.reverse()
	occurring_anime.reverse()

	# graph data
	plt.style.use("fivethirtyeight")
	plt.title("20 Most Critical Anime Fanbases")
	plt.xlabel("Negative Reviews Left by Fans under MAL Top 25 Anime")
	plt.ylabel("Anime Fanbases")

	plt.barh(occurring_anime, anime_tallies)

	plt.show()


if __name__ == "__main__":
	main()