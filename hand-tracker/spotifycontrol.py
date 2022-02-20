from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F')

# remember to remove this information before making commit
login = ['charlesliu688@gmail.com', 'letsgospurs']

email_form = driver.find_element(By.ID, 'login-username')
email_form.send_keys(login[0])

password_form = driver.find_element(By.ID, 'login-password')
password_form.send_keys(login[1])

driver.find_element(By.ID, 'login-button').click()

while True:
    action = str(input('What would you like to do?: '))

    if action == 'exit':
        break
    elif action == 'play':
        play_button = driver.find_element(By.CLASS_NAME, 'A8NeSZBojOQuVvK4l1pS')
        if play_button.get_dom_attribute('aria-label') == 'Play':
            play_button.click()
    elif action == 'pause':
        play_button = driver.find_element(By.CLASS_NAME, 'A8NeSZBojOQuVvK4l1pS')
        if play_button.get_dom_attribute('aria-label') == 'Pause':
            play_button.click()
    elif action == 'next':
        driver.find_element(By.CLASS_NAME, 'ARtnAVxkbmzyEjniZXVO').click()
    elif action == 'previous':
        driver.find_element(By.CLASS_NAME, "FKTganvAaWqgK6MUhbkx").click()
    elif action == 'like':
        like_button = driver.find_element(By.CLASS_NAME, "Fm7C3gdh5Lsc9qSXrQwO")
        if like_button.get_dom_attribute('aria-checked') == 'false':
            like_button.click()
    elif action == 'unlike':
        like_button = driver.find_element(By.CLASS_NAME, "Fm7C3gdh5Lsc9qSXrQwO")
        if like_button.get_dom_attribute('aria-checked') == 'true':
            like_button.click()
    elif action == 'repeat':
        driver.find_element(By.CLASS_NAME, "bQY5A9SJfdFiEvBMM6J5").click()
    elif action == 'shuffle':
        driver.find_element(By.CLASS_NAME, "d4u88Fc9OM6kXh7FYYRj").click()


driver.close()