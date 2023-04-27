import pandas
import json

my_url = u"https://docs.google.com/spreadsheets/d/e/2PACX-1vQqT-K5Hbn74oGF1Ejdkgz_eQtho-wA098XOXlWp0NjjiCVvpAQasqJPF7NFYJdCDF1CBRolhDxBxUr/pub?gid=0&single=true&output=csv"
def get_language_dict(data):
    language_code = data["language-code"]
    df = pandas.read_csv(my_url, delimiter=",", header=0, encoding="utf-8", index_col=0)
    language_dict = json.loads(df[language_code].to_json(orient="index"))
    return language_dict
