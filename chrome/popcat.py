#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import sys
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    NoSuchWindowException,
)


class PopCat:
    def __init__(self, driver_name: str, head: bool = True):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument("--mute-audio")
        driver_options.add_argument("--window-size=400,600")
        driver_options.headless = not head
        self.cwd = os.getcwd()
        self.button = None
        try:
            self.driver = webdriver.Chrome(
                executable_path=os.path.join(self.cwd, driver_name),
                options=driver_options,
            )
            self.driver.get("https://popcat.click/")
        except TimeoutException:
            print("init connection timed out!")

    def screen(self) -> None:
        """Takes a screenshot of the headless chrome to check its status"""
        self.driver.get_screenshot_as_file(os.path.join(self.cwd, "screenshots.png"))

    def fetch(self) -> None:
        """Fetches button element from website"""
        try:
            self.button = self.driver.find_element_by_id("app")
        except NoSuchElementException:
            print("Button element not found!")

    def pop(self) -> None:
        """starts clicking popcat"""
        self.button.click()

    def count(self) -> str:
        """returns the current count of clicks"""
        return self.button.find_element_by_class_name("counter").text

    def pop_loop(self) -> None:
        """Starts auto clicking for popcat"""
        if self.button == None:
            self.fetch()
        try:
            while True:
                self.pop()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    try:
        PopCat("chromedriver.exe").pop_loop()
    except Exception as err:
        print(err)
    sys.exit()