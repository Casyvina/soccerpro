import flet as ft
import datetime
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.firefox.options import Options
import pandas as pd
import random
from settings import prev_proxies, proxies, default_proxy, global_url


driver = None
dd = None
all_matches_url_list = []
home = None
away = None
h1 = None
dX = None
w2 = None
teams = []
p1 = None
p2 = None
p3 = None
p4 = None
today = datetime.date.today()
selection = None


def auto_run_data(e):
    global driver, teams, home, away, p1, p2, p3, p4, h1, dX, w2, home_last_match, away_last_match, score1, score2
    
    data = []
    
    get_all_matches_url(e)
    open_new_tab(e)
    for index, url in enumerate(all_matches_url_list):
        open_url(url)
        get_odds(e)
        sleep(3)
        get_last_match(e)
        sleep(3)
        try:
            gltH = get_last_team_home()
            gltW = get_last_team_away()
        except Exception as e:
            print(f"Error fro getting last team") 
            pass 
        try:
            teams = [home, away, gltH[0], gltW[0]]
        except:
            print("Error getting teams")
            pass
        sleep(3)
        details_from_table(e)

        my_Hypo = my_hypothesis()
        
        try:
            data.append({
                "index": index + 1,
                "url": url,
                "home": home,
                "away": away,
                "1": h1,
                "x": dX,
                "2": w2,
                "HLM": home_last_match,
                "gltH": gltH,
                "Hscore": score1,
                "Hsign": symbol1,
                "ALM": away_last_match,
                "Ascore": score2,
                "Wsign": symbol2,
                "gltW": gltW,
                "p1": p1,
                "p2": p2,
                "p3": p3,
                "p4": p4,
                "Hypothesis": my_Hypo,
            })
        except:
            print("Error fixing table")
            
        # Reset
        reset_values = [ p1, p2, p3, p4, h1, dX, w2, home, away, score1, score2 ]
        try:
            reset(reset_values)
        except:
            print("Error resting values")
            
    save_file(data=data)
    
    sleep(2)
    
    firefox_close(e)
    
    sleep(2)
    
    auto_open()

def auto_open():
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_data")  
    
    try:
        files = os.listdir(directory_path)
        
        file_info = [(file, os.path.getmtime(os.path.join(directory_path, file))) for file in files]

        file_info.sort(key=lambda x: x[1], reverse=True)


        sorted_files = [file_info[0][0]] 
        for file, _ in file_info[1:]:  
            sorted_files.append(file)
        
        if sorted_files:
            latest_file = sorted_files[0]
            file_path = os.path.join(directory_path, latest_file)
            print(file_path)    
            os.startfile(file_path)
            
        
        else:
            print("No files found in 'output_data' directory.")
            
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found. Creating it.")
        os.makedirs(directory_path, exist_ok=True)
        files = []
        
def save_file(data):
    
    today = datetime.date.today()
    filename = f"{selection}_{today.strftime('%Y-%m-%d')}.xlsx"
    try:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_data")
    except FileNotFoundError:
         print(f"Directory '{directory}' not found. Creating it.")
         os.makedirs(directory, exist_ok=True)

    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    df = pd.DataFrame(data=data)
    df.to_excel(file_path, index=False)
    
def my_hypothesis():
    global p4, p1, symbol2
    try:
        if (p4, p1, symbol2 ):
            if(p4 < p1) and ((symbol2 == "D" or symbol2 == "L")):
                return True
            else:
                return False
    except Exception as e:
        print(f"Error getting hypo")
        return None

def reset(values):
    for value in values:
        if value is not None:
            value = None

def details_from_table(e):
    global driver, p1, p2, p3, p4
    try:
        standing = driver.find_element(By.XPATH, "//button[normalize-space()='Standings']")
        standing.click()
        
        
        driver.implicitly_wait(5)
        total_matches = driver.find_elements(By.CLASS_NAME, "tableCellParticipant__name")
        
        print(len(total_matches))
        
        for index, matches in enumerate(total_matches):
            name = matches.get_attribute("innerText")
            # print(f"team {index + 1}: {name}")
            # if name in list
            if name in teams[0]:
                print(f"Team founds position {index + 1} : {name}")
                p1 = index + 1
            elif name in teams[1]:
                print(f"Team founds position {index + 1} : {name}")
                p2 = index + 1
            elif name in teams[2]:
                print(f"Team founds position {index + 1} : {name}")
                p3 = index + 1
            elif name in teams[3]:
                print(f"Team founds position {index + 1} : {name}")
                p4 = index + 1
                
        
        # and find the names of teams on table
        
        
    except Exception as e:
        print(f"Error clicking on standing table")
        pass

def get_last_team_home():

    print("print the last team name..")
            
    if home_last_match[0] == home:
        # print("Team is Home")
        return (home_last_match[1], "1TIH")
    else:
        # print("Team is away")
        return (home_last_match[0], "1TIW")

def get_last_team_away():

    # print("print the last team name..")
    if away_last_match[0] == away:
        # print("Team is Home")
        return (away_last_match[1], "2TIH")
    else:
        # print("Team is away")
        return (away_last_match[0], "2TIW")

def rotate_proxy():
    global prev_proxies
    total_no = len(proxies)
    
    if not prev_proxies:
        rand = random.choice(proxies)
        return rand
    
    else: 
        for i, proxy in enumerate(proxies): 
            if not proxy in prev_proxies and len(prev_proxies) < total_no:
                prev_proxies.append(proxy)
                print(f"next proxy no: {i}")
                return proxy
            
            if len(prev_proxies) == total_no:
                print("clear proxy_list")
                prev_proxies.clear()
                prev_proxies.append(default_proxy)
                return default_proxy

def get_last_match(e):
    global driver, home_last_match, away_last_match, score1, symbol1, score2, symbol2
    
    try:
        driver.implicitly_wait(4)
        
        h2h = driver.find_element(By.XPATH, "//button[normalize-space()='H2H']")
        h2h.click()
        
        #logic...
        home_last_game_tag = driver.find_element(By.XPATH, "//body/div[@class='container__detail']/div[@id='detail']/div[@class='h2hSection']/div[@class='h2h']/div[1]/div[2]/div[1]")
        
        home_last_game = home_last_game_tag.get_attribute("innerText")
        home_last = home_last_game.splitlines()
        
        away_last_game_tag = driver.find_element(By.XPATH, "//body/div[@class='container__detail']/div[@id='detail']/div[@class='h2hSection']/div[@class='h2h']/div[2]/div[2]/div[1]")
        
        away_last_game =away_last_game_tag.get_attribute("innerText")
        away_last = away_last_game.splitlines()
        
        teamA = home_last[2]
        teamB = home_last[3]
        score1 = f"{home_last[4]} - {home_last[5]}"
        symbol1 = home_last[6]
        teamC = away_last[2]
        teamD = away_last[3]
        score2 = f"{away_last[4]} - {away_last[5]}"
        symbol2 = away_last[6]
        
        home_last_match = [teamA, teamB]
        away_last_match = [teamC, teamD]
    except:
        print("Error getting last_match")
        pass
    
def get_odds(e):
    global driver, h1, dX, w2
    
    driver.implicitly_wait(4)
    odds_tag = driver.find_element(By.CSS_SELECTOR, "div[class='oddsRowContent']:first-of-type")
    odds_text = odds_tag.get_attribute("innerText")
    odds_list = odds_text.splitlines()

    h1 = odds_list[1]
    dX = odds_list[3]
    w2 = odds_list[5]
     
def open_url(url):
    global home, away, driver
    
    try:
        if url:
            driver.get(url)
            
            driver.implicitly_wait(4)
            
            home_tag = driver.find_element(By.CSS_SELECTOR, "div[class='duelParticipant__home '] a[class='participant__participantName participant__overflow ']")
            home = home_tag.get_attribute("innerText")
            print(f"home: {home}")
            
            away_tag = driver.find_element(By.CSS_SELECTOR, "div[class='duelParticipant__away '] a[class='participant__participantName participant__overflow ']")
            away = away_tag.get_attribute("innerText")
            print(f"away: {away}")
            
            driver.implicitly_wait(4)
    except Exception as e:
        print("Url Error")
        pass

def open_new_tab(e):
    global driver
    
    driver.switch_to.new_window(WindowTypes.TAB)
    
    driver.switch_to.window(driver.window_handles[1])
    
    # open_url()
        
def get_all_matches_url(e):
    global driver
    
    elements = driver.find_elements(By.CLASS_NAME, "eventRowLink")
    
    for element in elements:
        href = element.get_attribute("href")
        all_matches_url_list.append(href)
    print(all_matches_url_list)

def firefox_launch(e):
    global driver
    firefox_options = Options()
    firefox_options.add_argument("--disable-infobars")
    firefox_options.add_argument("--disable-extensions")
    firefox_options.add_argument("--disable-popup-blocking")
    
    
    options = webdriver.FirefoxOptions()
    proxy = rotate_proxy()
    print(proxy)
    firefox_options.add_argument(f"proxy-server={proxy}")
    # options.profile = webdriver.FirefoxProfile(pf)
    
    driver = webdriver.Firefox(options=firefox_options,)
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
    global driver, selection
    
    if awaydd.value == "Away 2.0 - 2.5":
        print(awaydd.value)
        selection = awaydd.value + " Finish"
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
        selection = awaydd.value + " Finish"
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
        selection = awaydd.value + " Finish"
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
    global driver, selection
        
    if homedd.value == "Home 2.0 - 2.5":
        print(homedd.value)
        selection = homedd.value + " Finish"
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.5 - 2.0":
        print(homedd.value)
        selection = homedd.value + " Finish"
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.3 - 1.5":
        print(homedd.value)
        selection = homedd.value + " Finish"
        driver.execute_script("""""")
        
def home_filter_live(e):
    global driver, selection
        
    if homedd.value == "Home 2.0 - 2.5":
        print(homedd.value)
        selection = homedd.value + " Live"
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.5 - 2.0":
        print(homedd.value)
        selection = homedd.value +" Live"
        driver.execute_script("""""")
        
    elif homedd.value == "Home 1.3 - 1.5":
        print(homedd.value)
        selection = homedd.value +" Live"
        driver.execute_script("""""")
        
def away_filter_live(e):
    global driver, selection
        
    if awaydd.value == "Away 2.0 - 2.5":
        print(awaydd.value)
        selection = awaydd.value + " Live"
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
        selection = awaydd.value +" Live"
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
        selection = awaydd.value +" Live"
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
    auto_run_btn = ft.ElevatedButton("Run data", icon="AUTO_FIX_HIGH_OUTLINED", on_click=auto_run_data)
    
    page.add(
        ft.Column([
            ft.Row([open, close], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([odds, refresh], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([removeHeaders, removeTitles], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([awaydd, finishAway, liveAway], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([homedd, finishHome, liveHome], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([all_matches_url_btn, open_new_tab_btn], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([odds_btn, last_event_btn, ], alignment=ft.MainAxisAlignment.CENTER,),
            ft.Row([table_btn, auto_run_btn], alignment=ft.MainAxisAlignment.CENTER,),
        ], alignment=ft.MainAxisAlignment.CENTER,)
        )
    
ft.app(main)
