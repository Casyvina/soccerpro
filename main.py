import flet as ft
import subprocess
import pyautogui
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from time import sleep


driver = None
global_url = "https://www.flashscore.com.ng/"
dd = None
all_matches_url_list = []
home = None
away = None
teams = None

def auto_run_data(e):
    pass

def details_from_table(e):
    try:
        standing = driver.find_element(By.XPATH, "//button[normalize-space()='Standings']")
        standing.click()
        
        # logic...
        # and get total of teams
        
        driver.implicitly_wait(5)
        total_matches = driver.find_elements(By.CLASS_NAME, "tableCellParticipant__name")
        
        print(len(total_matches))
        
        for index, matches in enumerate(total_matches):
            name = matches.get_attribute("innerText")
            print(f"team {index + 1}: {name}")
            # if name in list
            if name in teams:
                print(f"Team founds position {index + 1} : {name}")
        
        # and find the names of teams on table
        
        
    except Exception as e:
        print(f"Error clicking standing{e}")

def get_last_match(e):
    global driver
    global teams
    # click the last match section
    
    h2h = driver.find_element(By.XPATH, "//button[normalize-space()='H2H']")
    h2h.click()
    
    #logic...
    home_last_game_tag = driver.find_element(By.XPATH, "//body/div[@class='container__detail']/div[@id='detail']/div[@class='h2hSection']/div[@class='h2h']/div[1]/div[2]/div[1]")
    
    home_last_game = home_last_game_tag.get_attribute("innerText")
    home_last = home_last_game.splitlines()
    
    home_values = [line for line in home_last]
    
    print(home_values)
    
    away_last_game_tag = driver.find_element(By.XPATH, "//body/div[@class='container__detail']/div[@id='detail']/div[@class='h2hSection']/div[@class='h2h']/div[2]/div[2]/div[1]")
    
    away_last_game =away_last_game_tag.get_attribute("innerText")
    away_last = away_last_game.splitlines()
    
    teamA = home_last[2]
    teamB = home_last[3]
    teamC = away_last[2]
    teamD = away_last[3]
    
    teams = [teamA, teamB, teamC, teamD]
    print(teams)
    # print(valuesA, valuesB, valuesC, valuesD)
    # print(away_last_game)
    
    away_values = [line for line in away_last]
    print(away_values)

def get_odds(e):
    global driver
    odds_tag = driver.find_element(By.CSS_SELECTOR, "div[class='oddsRowContent']:first-of-type")
    odds_text = odds_tag.get_attribute("innerText")
    odds_list = odds_text.splitlines()
    
    odds = [line for line in odds_list]
    print(odds)

def open_new_tab(e):
    global driver
    global home
    global away
    
    driver.switch_to.new_window(WindowTypes.TAB)
    
    driver.switch_to.window(driver.window_handles[1])
    
    driver.get("https://www.flashscore.com.ng/match/ttFZlfbP/#/match-summary")
    
    driver.implicitly_wait(4)
    
    home_tag = driver.find_element(By.CSS_SELECTOR, "div[class='duelParticipant__home '] a[class='participant__participantName participant__overflow ']")
    home = home_tag.get_attribute("innerText")
    print(home)
    
    away_tag = driver.find_element(By.CSS_SELECTOR, "div[class='duelParticipant__away '] a[class='participant__participantName participant__overflow ']")
    away = away_tag.get_attribute("innerText")
    print(away)
    
    driver.implicitly_wait(4)
        
def get_all_matches_url(e):
    global driver
    
    elements = driver.find_elements(By.CLASS_NAME, "eventRowLink")
    
    for element in elements:
        href = element.get_attribute("href")
        all_matches_url_list.append(href)
    print(all_matches_url_list)

def firefox_launch(e):
    global driver
    options = webdriver.FirefoxOptions()
    # options.profile = webdriver.FirefoxProfile(pf)
    options.headless=True
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get(global_url)

def odds_click(e):
    global driver
    
    try:
        driver.find_element(By.XPATH, "//button[@id='onetrust-reject-all-handler']").click()
    except:
        pass
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//div[contains(text(),'Odds')]").click()

def away_filter_finish(e):
    global driver
    global homedd
    
    
    if awaydd.value == "Away 2.0 - 2.5":
        print(awaydd.value)
        driver.execute_script("""matches = document.getElementsByClassName("event__match event__match--twoLine");
for(i=matches.length -1; i>=0; i--){
    match = matches[i];
    if(match.children.length > 9){
        if(match.children[9] && match.children[10] && match.children[11]){
            odd_1 = parseFloat(match.children[9].textContent);
            odd_x = parseFloat(match.children[10].textContent);
            odd_2 = parseFloat(match.children[11].textContent);

            if((odd_1 >= 2.50 && odd_1 <= 8.0) && (odd_x >= 2.5 && odd_x <= 8.0) && (odd_2 >= 2.0 && odd_2 < 2.5)){
                // keep code
            } else {
                match.parentElement.removeChild(match);
            }

        } else {
            match.parentElement.removeChild(match);
        }
    }
}""")
        
    elif awaydd.value == "Away 1.5 - 2.0":
        print(awaydd.value)
        driver.execute_script("""matches = document.getElementsByClassName("event__match event__match--twoLine");
for(i=matches.length-1; i>=0; i--){
    match = matches[i];
    if(match.children.length > 9){
        if(match.children[9] && match.children[10] && match.children[11]){
            odd_1 = parseFloat(match.children[9].textContent);
            odd_x = parseFloat(match.children[10].textContent);
            odd_2 = parseFloat(match.children[11].textContent);

            if((odd_1 >= 3.5 && odd_1 <= 8.0) && (odd_x >= 2.5 && odd_x <= 5.0) && (odd_2 >= 1.5 && odd_2 <= 2.0)){
                // keep code
            } else {
                match.parentElement.removeChild(match);
            }

        } else {
            match.parentElement.removeChild(match);
        }
    }
}""")
        
    elif awaydd.value == "Away 1.3 - 1.5":
        print(awaydd.value)
        driver.execute_script("""matches = document.getElementsByClassName("event__match event__match--twoLine");
for(i=matches.length -1; i>=0; i--){
    match = matches[i];
    if(match.children.length > 9){
        if(match.children[9] && match.children[10] && match.children[11]){
            odd_1 = parseFloat(match.children[9].textContent);
            odd_x = parseFloat(match.children[10].textContent);
            odd_2 = parseFloat(match.children[11].textContent);

            if((odd_1 >= 2.50 && odd_1 <= 50.0) && (odd_x >= 2.5 && odd_x <= 15.0) && (odd_2 >= 1.3 && odd_2 <= 1.5)){
                // keep code
            } else {
                match.parentElement.removeChild(match);
            }

        } else {
            match.parentElement.removeChild(match);
        }
    }
}""")
        
def home_filter_finish(e):
    global driver
    global homedd
        
    if homedd.value == "Home 2.0 - 2.5":
        print(homedd.value)
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.5 - 2.0":
        print(homedd.value)
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.3 - 1.5":
        print(homedd.value)
        driver.execute_script("""""")
        
def home_filter_live(e):
    global driver
    global homedd
        
    if homedd.value == "Home 2.0 - 2.5":
        print(homedd.value)
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.5 - 2.0":
        print(homedd.value)
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.3 - 1.5":
        print(homedd.value)
        driver.execute_script("""""")
        
def away_filter_live(e):
    global driver
    global homedd
        
    if awaydd.value == "Away 2.0 - 2.5":
        print(awaydd.value)
        driver.execute_script("""var matches = document.getElementsByClassName("event__match event__match--twoLine")
    for(i = matches.length-1; i>=0; i--){
    match = matches[i];
    if(match.className.includes("event__match--scheduled")){
        if((match.querySelector('div.odds__odd.event__odd--odd1').innerText) && (match.querySelector('div.odds__odd.event__odd--odd2').innerText) && (match.querySelector('div.odds__odd.event__odd--odd3').innerText)){
            //
            var odd_1 = match.querySelector('div.odds__odd.event__odd--odd1').innerText;
            var odd_x = match.querySelector('div.odds__odd.event__odd--odd2').innerText;
            var odd_2 = match.querySelector('div.odds__odd.event__odd--odd3').innerText;

            if((odd_1 >= 2.50 && odd_1 <= 8.00) &&
               (odd_x >= 2.50 && odd_x <= 5.50) && 
               (odd_2 >= 2.00 && odd_2 < 2.50)){
            } else {
                match.parentElement.removeChild(match);
            }
        } else {
            match.parentElement.removeChild(match);
        }
    } else {
        match.parentElement.removeChild(match);
    }
}""")
    elif awaydd.value == "Away 1.5 - 2.0":
        print(awaydd.value)

        driver.execute_script("""var matches = document.getElementsByClassName("event__match event__match--twoLine")

for(i = matches.length-1; i>=0; i--){
    match = matches[i];
    if(match.className.includes("event__match--scheduled")){
        if((match.querySelector('div.odds__odd.event__odd--odd1').innerText) && (match.querySelector('div.odds__odd.event__odd--odd2').innerText) && (match.querySelector('div.odds__odd.event__odd--odd3').innerText)){
            //
            var odd_1 = match.querySelector('div.odds__odd.event__odd--odd1').innerText;
            var odd_x = match.querySelector('div.odds__odd.event__odd--odd2').innerText;
            var odd_2 = match.querySelector('div.odds__odd.event__odd--odd3').innerText;

            if((odd_1 >= 2.00 && odd_1 <= 7.50) &&
               (odd_x >= 2.00 && odd_x <= 5.50) && 
               (odd_2 >= 1.50 && odd_2 < 2.00)){
            } else {
                match.parentElement.removeChild(match);
            }
        } else {
            match.parentElement.removeChild(match);
        }
    } else {
        match.parentElement.removeChild(match);
    }
}""")
        
    elif awaydd.value == "Away 1.3 - 1.5":
        print(awaydd.value)
        driver.execute_script("""var matches = document.getElementsByClassName("event__match event__match--twoLine")

for(i = matches.length-1; i>=0; i--){
    match = matches[i];
    if(match.className.includes("event__match--scheduled")){
        if((match.querySelector('div.odds__odd.event__odd--odd1').innerText) && (match.querySelector('div.odds__odd.event__odd--odd2').innerText) && (match.querySelector('div.odds__odd.event__odd--odd3').innerText)){
            //
            var odd_1 = match.querySelector('div.odds__odd.event__odd--odd1').innerText;
            var odd_x = match.querySelector('div.odds__odd.event__odd--odd2').innerText;
            var odd_2 = match.querySelector('div.odds__odd.event__odd--odd3').innerText;

            if((odd_1 >= 2.50 && odd_1 <= 50.00) &&
               (odd_x >= 2.50 && odd_x <= 10.50) && 
               (odd_2 >= 1.30 && odd_2 < 1.50)){
            } else {
                match.parentElement.removeChild(match);
            }
        } else {
            match.parentElement.removeChild(match);
        }
    } else {
        match.parentElement.removeChild(match);
    }
}""")
      
def remove_headers(e):
    global drive
    
    driver.execute_script("""const allsoccer = document.getElementsByClassName("sportName soccer")[0].children;
for (let i = allsoccer.length - 1; i >= 0; i--) {
	const current = allsoccer[i];
	const prev = allsoccer[i - 1];
	
	 if (prev) {
		const condition1 = prev.className.includes("wclLeagueHeader") && current.className.includes("wclLeagueHeader")
		// const condition2 = prev.className.includes("event__match") && current.className.includes("event__match")

		if(condition1) {
			prev.parentElement.removeChild(prev)
		}
  }
}""")
      
def remove_titles(e):
    global driver
    driver.execute_script("""bar = document.getElementsByClassName("wclLeagueHeader");
for(i=bar.length-1; i>=0 ; i--){
    bar[i].parentElement.removeChild(bar[i]);
}""")

def refresh_page(e):
    global driver
    
    driver.refresh()  
    
def firefox_close(e):
    global driver
    driver.quit()
    driver = None

def main(page: ft.Page):
    page.title = "SoccerProV1"
    page.window.left = 1000
    page.window.top = 200
    page.window.always_on_top = True
    # page.window.title_bar_hidden = True
    # page.window.frameless = True
    page.bgcolor = ft.colors.TRANSPARENT
    page.window.width = 300
    page.window.height = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    global awaydd
    global homedd
    
    open = ft.ElevatedButton("Open", icon="OPEN_IN_BROWSER", on_click=firefox_launch, width=110)
    close = ft.ElevatedButton("Close", icon="EXIT_TO_APP", on_click=firefox_close, width=110)
    odds = ft.ElevatedButton("Odds", on_click=odds_click, width=100)
    removeTitles = ft.ElevatedButton("Titles", on_click=remove_titles, width=100)
    removeHeaders = ft.ElevatedButton("Header", on_click=remove_headers, width=100)
    
    awaydd = ft.Dropdown(
        value="Away 2.0 - 2.5",
        width=150,
        options=[
            ft.dropdown.Option("Away 2.0 - 2.5"),
            ft.dropdown.Option("Away 1.5 - 2.0"),
            ft.dropdown.Option("Away 1.3 - 1.5"),
        ],
    )
    
    homedd = ft.Dropdown(
        value="Home 2.0 - 2.5",
        width=150,
        options=[
            ft.dropdown.Option("Home 2.0 - 2.5"),
            ft.dropdown.Option("Home 1.5 - 2.0"),
            ft.dropdown.Option("Home 1.3 - 1.5"),
        ],
    )
    
    finishAway = ft.IconButton(
                icon=ft.icons.SPORTS_BASEBALL,
                icon_color="red400",
                icon_size=30,
                tooltip="Finish",
                on_click=away_filter_finish,
            )
    
    finishHome = ft.IconButton(
            icon=ft.icons.SPORTS_BASEBALL,
            icon_color="red400",
            icon_size=30,
            tooltip="Finish",
            on_click=home_filter_finish,
        )
    
    liveAway = ft.IconButton(
                    icon=ft.icons.SPORTS_BASEBALL,
                    icon_color="green400",
                    icon_size=40,
                    tooltip="Live",
                    on_click=away_filter_live,
                )
    
    liveHome = ft.IconButton(
                icon=ft.icons.SPORTS_BASEBALL,
                icon_color="green400",
                icon_size=40,
                tooltip="Live",
                on_click=home_filter_live,
            )
    
    refresh = ft.IconButton(
        icon=ft.icons.REFRESH,
        icon_color="orange300",
        icon_size=30,
        tooltip="Refresh",
        on_click=refresh_page,
    )
    
    all_matches_url_btn = ft.ElevatedButton("Matches", icon="ADD_HOME_WORK", on_click=get_all_matches_url, )
    open_new_tab_btn = ft.ElevatedButton("new_tab", icon="BACKUP_TABLE", on_click=open_new_tab)
    odds_btn = ft.ElevatedButton("odds", icon="TABLE_BAR_OUTLINED", on_click=get_odds)
    last_event_btn = ft.ElevatedButton("last match", icon="PIVOT_TABLE_CHART_SHARP", on_click=get_last_match)
    table_btn = ft.ElevatedButton("table match", icon="TABLE_CHART_SHARP", on_click=details_from_table)
    auto_run_btn = ft.ElevatedButton("Run data", on_click=auto_run_data)
    
    page.add(
        ft.Column([
            ft.Row([open, close], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([odds, refresh], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([removeHeaders, removeTitles], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([awaydd, finishAway, liveAway], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([homedd, finishHome, liveHome], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([all_matches_url_btn, open_new_tab_btn], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([odds_btn, last_event_btn, ], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([table_btn], [auto_run_btn], alignment=ft.MainAxisAlignment.CENTER,),
        ], alignment=ft.MainAxisAlignment.CENTER,)
        )
    
ft.app(main)
