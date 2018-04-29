from flask import Flask, flash, abort, redirect, render_template, request, session, abort, url_for
import os
import random

password = ''
for n in range(0, 8):
    x = random.randint(0, 9)
    password += str(random.choice('abcdefghijklmnopqrstuvxyz'))


print(password)
