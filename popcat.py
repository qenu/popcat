#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import sys
import time
import threading
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    NoSuchWindowException,
    WebDriverException
)


class PopCat:
    def __init__(self, driver_name: str):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument("--mute-audio")
        driver_options.add_argument("disable-gpu")
        driver_options.add_argument("--window-size=400,600")
        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.cwd = os.getcwd()
        self.button = None
        self.count = 0
        try:
            self.driver = webdriver.Chrome(
                executable_path=os.path.join(self.cwd, driver_name),
                options=driver_options,
            )
            self.reload()
        except TimeoutException:
            print("init connection timed out!")

    def screen(self) -> None:
        """Takes a screenshot of the headless chrome to check its status"""
        self.driver.get_screenshot_as_file(os.path.join(self.cwd, "screenshots.png"))

    def reload(self) -> None:
        """reloads popcat click page"""
        self.driver.delete_all_cookies()
        self.driver.refresh()
        self.driver.get("https://popcat.click/")

    def fetch(self) -> None:
        """Fetches button element from website"""
        try:
            self.button = self.driver.find_element_by_id("app")
        except NoSuchElementException:
            print("Button element not found!")

    def pop(self) -> None:
        """starts clicking popcat"""
        try:
            self.button.click()
        except WebDriverException:
            raise NoSuchWindowException

    def _count(self) -> None:
        """returns the current count of clicks"""
        self.count = self.button.find_element_by_class_name("counter").text

    def stop(self) -> None:
        """loop toggle"""
        self._stop = True
        time.sleep(1)
        self.thread.join()
        self._count()

    def _loop(self) -> None:
        """inner function for threading"""
        try:
            self.num = 0
            while not self._stop:
                self.pop()
                self.num += 1
        except NoSuchWindowException:
            self.driver.quit()

    def start(self) -> None:
        """Starts auto clicking for popcat"""
        if self.button == None:
            self.fetch()
        self._stop = False
        self.thread = threading.Thread(target=self._loop)
        self.thread.start()

    def clickloop(self, *, safemode: bool=False) -> None:
        """limited pop and automatic refresh"""
        pop_limit = 750 if safemode else 800
        auto_refresh = sys.maxsize if safemode else 10
        if self.button == None:
            self.fetch()
        try:
            print("Popcat event has started!")
            while True:
                minute_time = time.time()
                pop_count = []
                for i in range(auto_refresh):
                    second_time = time.time()
                    self.start()
                    while not (time.time() - second_time > 29 or self.num > pop_limit):
                        time.sleep(0.5)
                    self.stop()
                    used = time.time() - second_time
                    print(
                        f"Cat {i} is going for a nap after {used:.2f} seconds\n"
                        f"  Pop Count : {sum(pop_count):,}(+{self.num}) | {self.count} | PPS={self.num/used:.2f}"
                    )
                    pop_count.append(self.num)
                    time.sleep(int(30 - (time.time() - second_time)))
                used = time.time() - minute_time
                print(
                    f"Time to grab a new popcat...\n"
                    f"  {used:.2f} total seconds elapsed\n"
                    f"    Total Pop Count : {sum(pop_count):,} | {self.count} | PPS={sum(pop_count)/used:.2f}"
                )
                self.reload()
        except NoSuchWindowException:
            print("Popcat event ending...")
            self.driver.quit()


if __name__ == "__main__":
    try:
        cat = PopCat("chromedriver.exe")
        cat.clickloop(safemode=True)
    except Exception as err:
        print(err)
        try:
            cat.driver.quit()
        except Exception:
            pass
    sys.exit()
