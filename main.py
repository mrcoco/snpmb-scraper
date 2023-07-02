import sys
import time

import psycopg2.extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

op = Options()
prefs = {'download.default_directory': "excel"}
op.add_experimental_option('prefs', prefs)
service = Service("/Users/dwiagus/.wdm/drivers/chromedriver/mac64/112.0.5615.49/chromedriver")
chromedriver = webdriver.Chrome(service=service, options=op)

chromedriver.get("https://manajemen-pusat-utbk-snpmb.bppp.kemdikbud.go.id/login/")
username = chromedriver.find_element(By.CSS_SELECTOR, "#username")
password = chromedriver.find_element(By.CSS_SELECTOR, "#password")
username.click()
username.send_keys("username")
password.click()
password.send_keys("password")
login = chromedriver.find_element(By.CSS_SELECTOR, "#__next > div > main > section > form > button")
login.click()

# link_peserta = chromedriver.find_element(By.CSS_SELECTOR,"#__next > aside > ul > div:nth-child(2) > li > a:nth-child(3)")
# link_peserta.click()


username = "postgres"
password = "postgres"
hostname = "localhost"
port = "5432"
database = "reglokal"

DB_CONNECTION_STRING = "host=%s port=%s dbname=%s user=%s password=%s" % (
    hostname, port, database, username, password)
dbConn = psycopg2.connect(DB_CONNECTION_STRING)
cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
Select = """SELECT id,nama_peserta,no_peserta_utbk FROM snpmb WHERE  nisn IS NULL ORDER BY id DESC"""
try:
    cursor.execute(Select)
    results = cursor.fetchall()
    for row in results:
        chromedriver.get("https://manajemen-pusat-utbk-snpmb.bppp.kemdikbud.go.id/fasilitas/pencarian-peserta/")
        search_nama = row['no_peserta_utbk']
        input_peserta = chromedriver.find_element(By.XPATH, "//input[@id='small']")
        input_peserta.send_keys(search_nama)
        button = chromedriver.find_element(By.CSS_SELECTOR,
                                           "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.border.flex.justify-between.rounded-md.border-gray-300.bg-white.text-lg.text-slate-700.shadow-md.outline-none > button")
        button.click()
        time.sleep(2)
        try:
            nisn = chromedriver.find_element(By.CSS_SELECTOR,
                                             "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.my-3.grid.w-full.grid-cols-2.justify-between.gap-6 > div > div.flex.grow.flex-col > p:nth-child(6)")
            nik = chromedriver.find_element(By.CSS_SELECTOR,
                                            "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.my-3.grid.w-full.grid-cols-2.justify-between.gap-6 > div > div.flex.grow.flex-col > p:nth-child(8)")
            lahir = chromedriver.find_element(By.CSS_SELECTOR,
                                              "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.my-3.grid.w-full.grid-cols-2.justify-between.gap-6 > div > div.flex.grow.flex-col > p:nth-child(10)")
            tel = chromedriver.find_element(By.CSS_SELECTOR,
                                            "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.my-3.grid.w-full.grid-cols-2.justify-between.gap-6 > div > div.flex.grow.flex-col > p:nth-child(12)")
            email = chromedriver.find_element(By.CSS_SELECTOR,
                                              "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.my-3.grid.w-full.grid-cols-2.justify-between.gap-6 > div > div.flex.grow.flex-col > p:nth-child(14)")
            alamat = chromedriver.find_element(By.CSS_SELECTOR,
                                               "#__next > div > div.mx-auto.mt-6.flex.h-full.w-full.flex-col.overflow-y-scroll.pb-16.pr-10.pl-72 > div.my-3.grid.w-full.grid-cols-2.justify-between.gap-6 > div > div.flex.grow.flex-col > p:nth-child(16)")
            ucur = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            update = """ UPDATE snpmb SET nik=%s,tgl_lahir=%s,no_telepon=%s,email=%s,alamat=%s,nisn=%s WHERE id=%s"""
            record = (nik.text, lahir.text, tel.text, email.text, alamat.text,nisn.text, row['id'])
            try:
                ucur.execute(update,record)
                dbConn.commit()
            except psycopg2.Error as err:
                print(err)
            print("insert", nik.text,lahir.text)
        except:
            print("failed load")
except psycopg2.Error as e:
    print(e)
