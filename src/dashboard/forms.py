from flask_wtf.file import FileField, FileRequired
from flask_wtf import FlaskForm
from flask import Blueprint, flash, redirect, render_template, request, url_for

class FilesUpload(FlaskForm):
    products_file = FileField("Products", validators=[FileRequired()])
    transactions_file = FileField("Transactions", validators=[FileRequired()])
    households_file = FileField("Households", validators=[FileRequired()])
