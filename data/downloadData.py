import wget, gzip, shutil

url1 = "https://datasets.imdbws.com/name.basics.tsv.gz"
url2 = "https://datasets.imdbws.com/title.akas.tsv.gz"
url3 = "https://datasets.imdbws.com/title.basics.tsv.gz"
url4 = "https://datasets.imdbws.com/title.crew.tsv.gz"
url5 = "https://datasets.imdbws.com/title.episode.tsv.gz"
url6 = "https://datasets.imdbws.com/title.principals.tsv.gz"
url7 = "https://datasets.imdbws.com/title.ratings.tsv.gz"

wget.download(url1, "nameBasics.tsv.gz")
wget.download(url2, "akas.tsv.gz")
wget.download(url3, "basics.tsv.gz")
wget.download(url4, "crew.tsv.gz")
wget.download(url5, "episode.tsv.gz")
wget.download(url6, "principals.tsv.gz")
wget.download(url7,"ratings.tsv.gz")

names = ["nameBasics.tsv.gz",
"akas.tsv.gz",
"basics.tsv.gz",
"crew.tsv.gz",
"episode.tsv.gz",
"principals.tsv.gz",
"ratings.tsv.gz"]

for name in names:
    with gzip.open(name, 'rb') as f_in:
        with open(name[:name.find('.')+4], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)